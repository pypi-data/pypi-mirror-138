#!/usr/bin/env python3
# vim: set fileencoding=utf-8
import math
from copy  import copy

#SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'
#sys.path.append(os.path.dirname(SCRIPT_DIR))

import numpy as np

from scipy import ndimage
from scipy.sparse import eye, diags
from scikits.umfpack import spsolve

#import sfs as sfs
import image_processing_with_graphs as ipg
#from . import image_processing_with_graphs as ipg


################################  io functions  ################################

import rasterio
from pyproj import CRS, Transformer


def azimuth_elevation_from_metadata(metadata, crs):
    """Compute azimuth and elevation angles from the metadata of a Capella image

    Args:
        metadata (dict): image's metadata
        crs (pyproj.CRS): image's CRS (should be UTM)
    """

    # get center pixel and corresponding time
    center_pixel = metadata['collect']['image']['center_pixel']
    # np.datetime64 does not handle time zones
    center_time = np.datetime64(center_pixel['center_time'].replace('Z', ''))

    # get state vector closest to center_pixel's acquisition time
    state_vectors = metadata['collect']['state']['state_vectors']
    center_state_vector_idx = np.argmin(
        [np.abs(np.datetime64(sv['time'].replace('Z', '')) - center_time)
         for sv in state_vectors])
    center_state_vector = state_vectors[center_state_vector_idx+1]

    # convert coordinates in source image's CRS
    # State vectors are given in CRS "ECEF", i.e. EPSG:4978
    crs_ecef = CRS.from_epsg(4978)
    transformer = Transformer.from_crs(crs_ecef, crs, always_xy=True)
    target_position = transformer.transform(*center_pixel['target_position'])
    satellite_position = transformer.transform(*center_state_vector['position'])

    # compute azimuth and elevation
    return azel_from_utm_positions(target_position, satellite_position)


############# azimuth  and elevation #####################


def azel_from_utm_positions(target, satellite):
    """Azimuth and Elevation from target and satellite position in UTM

    (Code extracted from rpcm)
    """
    p0 = np.array(target)
    p1 = np.array(satellite)

    # compute local satellite incidence direction
    satellite_direction = (p1 - p0) / np.linalg.norm(p1 - p0)

    # zenith is the angle between the satellite direction and the vertical
    # zenith = np.degrees(np.arccos(np.dot(satellite_direction, [0, 0, 1])))
    # elevation is the angle between the SAR beam and the horizontal
    elevation = np.degrees(np.arcsin(np.dot(satellite_direction, [0, 0, 1])))

    # azimuth is the clockwise angle with respect to the North
    # of the projection of the satellite direction on the horizontal plane
    # This can be computed by taking the argument of a complex number
    # in a coordinate system where northing is the x axis and easting the y axis
    easting, northing = satellite_direction[:2]
    azimuth = np.degrees(np.angle(np.complex(northing, easting)))

    return azimuth, elevation


def azel_from_cartesian_positions(ground, sat):
    # function azel_from_utm_positions() above gives the same result
    # ground and sat: cartesian coordinates in meters
    xg, yg, zg = ground
    xs, ys, zs = sat
    n = np.sqrt((xs - xg) ** 2 + (ys - yg) ** 2 + (zs - zg) ** 2)
    α = (xs - xg) / n
    β = (ys - yg) / n
    γ = (zs - zg) / n
    elrad = math.asin(γ)
    if β >= 0:
        azrad = math.pi / 2 - math.acos(α / np.sqrt(α ** 2 + β ** 2))
    else:
        azrad = math.pi / 2 + math.acos(α / np.sqrt(α ** 2 + β ** 2))
    return [180 * azrad / math.pi, 180 * elrad / math.pi]


def sun_direction_from_position(azel):
    az, el = azel
    azrad = float(az) * math.pi / 180
    elrad = float(el) * math.pi / 180
    α = math.cos(elrad) * math.sin(azrad)
    β = - math.cos(elrad) * math.cos(azrad) # le moins correspond au fait que python a un axe vertical vers le bas (-y au  lieu de y)
    γ = math.sin(elrad)
    return α, β, γ

def sun_direction_image(h, w, azel):
    α, β, γ = sun_direction_from_position(azel)
    xx, yy = np.meshgrid(np.linspace(0, w-1, w), np.linspace(0, h-1, h))
    sun_direction =  - α * xx - β * yy
    return sun_direction

#########################################################
###################### SFS Linear ###########################
#########################################################

def sfs_dirichlet(s, d, m, ε, azel, dirichlet=None, neumann=None, pixel_spacing=None):
    # s: image to interpret
    # d: image encoding the sun direction
    # m: mask, 1 in ROI, 0 outside
    # eps: coefficient for regularisation term.
    # azel: azimuth and elevation
    # neumann: 1 in occlusions, 0 outside
    # optimising permutation matrix
    s = copy(s)
    α, β, γ = sun_direction_from_position(azel)

    if (len(s.shape) == 3):
        s = np.sum(s, axis=2)
    m = (m > 0.5).astype(float)

    if dirichlet is None:
        dirichlet = np.zeros_like(m)
        
    out = dirichlet.flatten()

    if neumann is None:
        full_mask = m
    else:
        neumann = (neumann > 0) * (m > 0)
        full_mask = (m > 0) * (1-neumann)
    
 #   s = normalise_input_image(s, m, azel, dirichlet, neumann)
 #   s = s - γ

    h, w = s.shape
    if pixel_spacing is None:
        B = ipg.incidence_matrix(w, h)
    else:
        B = ipg.anisotropic_incidence_matrix(w, h, 1 / pixel_spacing[0], 
                 1 / pixel_spacing[1])
  
    # remove edges and vertices outside the dilated ROI
    mask_dilated = ndimage.binary_dilation(m, np.ones((6,6)))
    flat_dilated_mask = mask_dilated.flatten()
    s = s.flatten()[flat_dilated_mask > 0]
    d = d.flatten()[flat_dilated_mask > 0]
    m = m.flatten()[flat_dilated_mask > 0]
    full_mask = full_mask.flatten()[flat_dilated_mask > 0]
    dirichlet = dirichlet.flatten()[flat_dilated_mask > 0]

    mask_areas = abs(B) @ flat_dilated_mask # ROI 2, across 1, outside 0
    Bcsr = B.tocsr()
    Bcsr = Bcsr[mask_areas > 1, :]
    Bcsr = Bcsr[:, flat_dilated_mask > 0]
    B = Bcsr.tocoo()

    # remove edges across neumann boundaries from  B
    if neumann is not None:
        Ln = - B.T @ B
        neumann = (neumann > 0.5).astype(float)
        mask = neumann.flatten()[flat_dilated_mask > 0]
        t = ((B @ mask) != 0)               # 1 across boundary, 0 outside
        ind = np.array((np.logical_not(t)).nonzero()) # index of t nonzero
        Bcsr = B.tocsr()
        Bcsr = Bcsr[ind.flatten(), :]
        B = Bcsr.tocoo()

    C = abs(B)/2
    L = - B.T @ B

    # linear system definition
    A1 = C.T @ diags(B @ d.flatten()) @ B
    M = diags(full_mask.flatten())
    nv,_ = M.shape
    I = eye(nv)

    A = A1.T @ M @ A1 - ε * L + I - M
    b = A1.T @ M @ s.flatten() + (I - M) @ dirichlet

    # linear system resolution with umfpack
    u = spsolve(A,b)

    if neumann is not None:
        M = diags(neumann.flatten()[flat_dilated_mask > 0])
        A = I - M + M @ Ln
        b = (I - M) @ u# + M @ (B.T @ B @ dirichlet)
        u = spsolve(A,b)
    
    #out = np.zeros((h,w)).flatten()
    out[flat_dilated_mask > 0] = u
    return out.reshape(h,w)

def sfs_pentland(s, d, m, ε, azel, dirichlet=None, neumann=None, pixel_spacing=None):
    # s: image to interpret
    # d: image encoding the sun direction
    # m: mask, 1 in ROI, 0 outside
    # eps: coefficient for regularisation term.
    # azel: azimuth and elevation
    # neumann: 1 in occlusions, 0 outside
    # optimising permutation matrix
    s = copy(s)
    α, β, γ = sun_direction_from_position(azel)

    if (len(s.shape) == 3):
        s = np.sum(s, axis=2)
    m = (m > 0.5).astype(float)

    if dirichlet is None:
        dirichlet = np.zeros_like(m)
        
    out = dirichlet.flatten()

    if neumann is None:
        full_mask = m
    else:
        full_mask = (m > 0) * (1-neumann)
    
    fm = 1 * full_mask

#    s = normalise_input_image(s, m, azel, dirichlet, neumann)
#    s = s - γ

    h, w = s.shape
    if pixel_spacing is None:
        B = ipg.incidence_matrix(w, h)
    else:
        B = ipg.anisotropic_incidence_matrix(w, h, 1 / pixel_spacing[0], 
                 1 / pixel_spacing[1])
  
    # remove edges and vertices outside the dilated ROI
    mask_dilated = ndimage.binary_dilation(m, np.ones((6,6)))
    flat_dilated_mask = mask_dilated.flatten()
    s = s.flatten()[flat_dilated_mask > 0]
    d = d.flatten()[flat_dilated_mask > 0]
    m = m.flatten()[flat_dilated_mask > 0]
    full_mask = full_mask.flatten()[flat_dilated_mask > 0]
    dirichlet = dirichlet.flatten()[flat_dilated_mask > 0]

    mask_areas = abs(B) @ flat_dilated_mask # ROI 2, across 1, outside 0
    Bcsr = B.tocsr()
    Bcsr = Bcsr[mask_areas > 1, :]
    Bcsr = Bcsr[:, flat_dilated_mask > 0]
    B = Bcsr.tocoo()

    # remove edges across neumann boundaries from  B
    if neumann is not None:
        Ln = - B.T @ B
        neumann = (neumann > 0.5).astype(float)
        mask = neumann.flatten()[flat_dilated_mask > 0]
        t = ((B @ mask) != 0)               # 1 across boundary, 0 outside
        ind = np.array((np.logical_not(t)).nonzero()) # index of t nonzero
        Bcsr = B.tocsr()
        Bcsr = Bcsr[ind.flatten(), :]
        B = Bcsr.tocoo()

    C = abs(B)/2
    L = - B.T @ B

    # matrices for non flat height (here dirichlet) see pentland
    den = np.sqrt(1 + (B @ dirichlet) ** 2)
    fac = (B @ d) / den - (B @ dirichlet) * ((B @ d) * (B @ dirichlet) + γ) / (den ** 3)

    # linear system definition
    A1 = C.T @ diags(fac) @ B
    M = diags(full_mask.flatten())
    nv,_ = M.shape
    I = eye(nv)

    A = A1.T @ M @ A1 - ε * L + I - M
    b = A1.T @ M @ s.flatten() + (I - M) @ dirichlet

    # linear system resolution with umfpack
    u = spsolve(A,b)

    if neumann is not None:
        M = diags(neumann.flatten()[flat_dilated_mask > 0])
        A = I - M + M @ Ln
        b = (I - M) @ u# + M @ (B.T @ B @ dirichlet)
        u = spsolve(A,b)
    
    #out = np.zeros((h,w)).flatten()
    out[flat_dilated_mask > 0] = u
    return out.reshape(h,w)

######################################################################
########################### HORN #####################################
######################################################################

def Reflectance(p, q, azel):
    α, β, γ = sfs.sun_direction_from_position(azel)
    R = (γ - α * p - β * q) / np.sqrt(1 + p ** 2 + q ** 2)
    return R

def Reflectance_p(p, q, azel):
    α, β, γ = sfs.sun_direction_from_position(azel)
    den = np.sqrt(1 + p ** 2 + q ** 2)
    Rp = - (α / den) - p * (γ - α * p - β * q) / (den ** 3)
    return Rp

def Reflectance_q(p, q, azel):
    α, β, γ = sfs.sun_direction_from_position(azel)
    den = np.sqrt(1 + p ** 2 + q ** 2)
    Rq = - (β / den) - q * (γ - α * p - β * q) / (den ** 3)
    return Rq

def energy_53_flat(I, p, q, z, m, b, w, h, azel, μ, λ, Bx=None, By=None, A=1, B=0):
    if Bx is None or By is None:
        Bx, By = ipg.gradient_stencil_shift(w, h)
    
    mg = (abs(Bx) @ m) > 1
    
    R = Reflectance(p, q, azel)
    
    E1 = np.sum(mg * (I - A * R - B) ** 2)
    E2 = μ * np.sum(mg * ((Bx @ z - p) ** 2 + (By @ z - q) ** 2))
    E3 = λ * np.sum(m * ((Bx.T @ p) ** 2 + (By.T @ p) ** 2
                         + (Bx.T @ q) ** 2 + (By.T @ q) ** 2))
    E4 = np.sum((1 - m) * ((z - b) ** 2))
    #print(f'E1: {E1} E2: {E2} E3: {E3} E4: {E4}')
    return E1 + E2 + E3 + E4

def horn_iter_56_flat(I, p, q, z, m, b, azel, μ, λ, w, h, al=1, amb=0, Bx=None, By=None):
    if Bx is None or By is None:
        Bx, By = ipg.gradient_stencil_shift(w, h)
    
    p0 = 1 * p
    q0 = 1 * q
    p_mean = ipg.flat_local_mean_diagonal(p, w-1, h-1)
    q_mean = ipg.flat_local_mean_diagonal(q, w-1, h-1)
    z_mean = ipg.flat_local_mean_diagonal(z, w, h)
    mg = ((abs(Bx) + abs(By)) @ m) > 1
    
    R = Reflectance(p0, q0, azel) + amb
    Rp = Reflectance_p(p0, q0, azel)
    Rq = Reflectance_q(p0, q0, azel)
    
    δp_mean = p_mean - p0
    δq_mean = q_mean - q0
    δzx = (Bx @ z) - p0
    δzy = (By @ z) - q0
    
    D = (2 * λ + μ) * (2 * λ + μ + Rp ** 2 + Rq ** 2)
    A = 2 * λ * δp_mean + μ * δzx + (I - R) * Rp
    B = 2 * λ * δq_mean + μ * δzy + (I - R) * Rq
    
    δp = ((μ + 2 * λ + Rq ** 2) * A - Rp * Rq * B) / D
    δq = ((μ + 2 * λ + Rp ** 2) * B - Rp * Rq * A) / D
    
    p = p0 + mg * δp
    q = q0 + mg * δq
    #z = (m * (z_mean + (Bx.T @ p + By.T @ q) / 2) + (1 - m) * ((z - b) ** 2))
    z = (m * μ * (2 * z_mean + (Bx.T @ p + By.T @ q)) + (1 - m) * b) / (m * μ * 2 + 1 - m)
    
    return p, q, z

def variational_horn(im, m, I, azel, μ, λ, niter=2000, b=None, z=None, p=None, q=None, al=1, amb=0, energy=false):
    α, β, γ = sfs.sun_direction_from_position(azel)
    m = (m > 0).flatten()
    h, w = im.shape
    Bx, By = ipg.gradient_stencil_shift(w, h)
    I = I[:-1, :-1]
    E = []

    if b is None:
        b = 0 * im.flatten()
    if z is None:
        z = 0 * im.flatten()
    p = Bx @ z.flatten()
    q = By @ z.flatten()

    if energy:
        E.append(energy_53_flat(I, p, q, z, m, b, w, h, azel, μ, λ, Bx=Bx, By=By))

    p, q, z =  horn_iter_56_flat(I, p, q, z, m, b, azel, μ, λ, w, h, Bx=Bx, By=By)
    if energy:
        E.append(energy_53_flat(I, p, q, z, m, b, w, h, azel, μ, λ, Bx=Bx, By=By))


    #for i in range(0, niter):
    i = 0
    while (i < niter): #& (np.abs(E[-2] - E[-1]) > 0.005):
        i += 1
        p, q, z =  horn_iter_56_flat(I, p, q, z, m, b, azel, μ, λ, w, h, Bx=Bx, By=By)
        E.append(energy_53_flat(I, p, q, z, m, b, w, h, azel, μ, λ, Bx=Bx, By=By))

    I = 0 * im
    I[:-1, :-1] = Reflectance(Bx @ z, By @ z, azel).reshape([h-1, w-1])

    return z.reshape([h, w]), I, E 

######################################################################
################## Shading from shape ################################
######################################################################

def simulate(height, azel):
    h, w = height.shape
    α, β, γ = sun_direction_from_position(azel)
    d = sun_direction_image(h, w, azel)
    B = ipg.incidence_matrix(w, h)
    C = abs(B)/2
    den = np.sqrt(1 + C.T @ np.power(B@height.flatten(),2))
    A1 = C.T @ diags(B @ d.flatten()) @ B
    sim = (A1 @ height.flatten() + γ)/(den)
    return sim.reshape([h, w])

def simulate_linear(height, azel):
    h, w = height.shape
    d = sun_direction_image(h, w, azel)
    B = ipg.incidence_matrix(w, h)
    C = abs(B)/2
    elrad = float(azel[1]) * math.pi / 180
    A1 = C.T @ diags(B @ d.flatten()) @ B
    sim = (A1 @ height.flatten())
    return sim.reshape([h, w])



