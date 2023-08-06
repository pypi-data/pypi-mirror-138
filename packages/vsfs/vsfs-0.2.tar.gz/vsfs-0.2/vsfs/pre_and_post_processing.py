#!/usr/bin/env python3
# vim: set fileencoding=utf-8
#%% 
import sys, os, glob, math
import numpy as np

from scipy import ndimage
from scipy.interpolate import griddata
from skimage import measure


import json
import pandas as pd
import plotly.graph_objs as go

import iio

from . import image_processing_with_graphs as ipg
from . import sfs as sfs
#import image_processing_with_graphs as ipg
#import sfs as sfs


#########################################################
############### PLANETSCOPE #############################
#########################################################

############# azimuth  and elevation #####################

def get_az_el(i, azel=np.array([360.0, 90.0])):
    from osgeo import gdal
    az, el = azel
    if (az < 360) and (el < 90) and (az >= 0) and (el >= 0):
        return np.array([az, el])

    ds = gdal.Open(i)
    meta = ds.GetMetadata()
    keys = list(k.lower() for k in meta)
    combined = '\t'.join(keys)

    if (('SUN_AZ').lower() not in combined) or (('SUN_EL').lower() not in combined):
        sys.exit("Sun azimuth and elevation not found in metadata. "
             "Provide sun informations and try again.")

    az = [value for key, value in meta.items() if 'SUN_AZ' in key.upper()]
    el = [value for key, value in meta.items() if 'SUN_EL' in key.upper()]
    return np.array([float(az[0]), float(el[0])])

def gdal_copy(source_file, dest_file):
    from osgeo import gdal
    ds = gdal.Open(source_file)
    if ds is None:
        print('Unable to open' + source_file + 'for reading')
        return

    metadata = ds.GetMetadata()
    if metadata is None:
        print('No metadata found on file' + source_file)
        return

    ds2 = gdal.Open(dest_file, gdal.GA_Update)
    if ds2 is None:
        print('Unable to open' + source_file + 'for reading')
        return

    ds2.SetMetadata(metadata)
    return

def add_json_metadata_to_geotiff_gdal(imfile, jsonfile):
    from osgeo import gdal
    f = open(jsonfile)
    json_metadata = json.load(f)['properties']
    im_data = gdal.Open(imfile)
    im_metadata = im_data.GetMetadata()
    im_metadata.update(json_metadata)
    im_data.SetMetadata(im_metadata)
    return


###########  crane detection and image normalisation ##################
def crane_mask_optical(im, m):
    im = (im - np.mean(im[m])) / np.std(im[m])
    mask = ndimage.binary_dilation(m * im > 4, np.ones((7, 7))) * m
    return mask

def normalise_input_image(s, m, azel, neumann=None):
    _, _, γ = sfs.sun_direction_from_position(azel)

    if neumann is None:
        full_mask = m
    else:
        full_mask = (m > 0) * (1 - neumann)

    # with mean put to zeros
    #s = (s - np.mean(s[full_mask > 0])) / np.std(s[full_mask > 0])
    #s[full_mask == 0] = 0
    # with mean γ
    s = (s - np.mean(s[full_mask > 0])) / np.std(s[full_mask > 0]) + γ
    s[full_mask == 0] = γ
    # with A and B
    # s = (s - B) / A
    # s[full_mask == 0] = γ
    return s

# on whole directory
def sfs_optical_directory(imdir, mfile, outdir, ε, specifier='.tif'):
    from osgeo import gdal
    ## TODO : improve comment
    os.makedirs(outdir, exist_ok=True)
    cdir = os.getcwd()
    os.chdir(imdir)

    images = sorted(glob.glob('*' + specifier))
    m = iio.read(mfile)[:,:,0] > 0
    h, w = m.shape

    for k in range(0, len(images)):
        #print('sfs: image ' + str(k) + ' / ' + str(len(images)))
        ofile = outdir + images[k]

        im = iio.read(images[k])[:,:,0]
        cmask = crane_mask_optical(im, m)

        azel = get_az_el(images[k])
        d = sfs.sun_direction_image(h, w, azel)
        u = sfs.sfs_dirichlet(im, d, m, ε, azel, neumann=cmask)

        iio.write(ofile, u)
        gdal_copy(images[k], ofile)

    os.chdir(cdir)

    
############### volume estimation #############################
def find_mode(im, m, width=2):
    counts,bins = np.histogram(im[m],bins=200)
    vals = (bins[:-1]+bins[1:])/2 # average value of bin
    where = np.logical_and.reduce([counts >= np.roll(counts,w)
                                   for w in range(-width,width+1)])
    where = np.logical_and(where,counts>=np.max(counts))

    return float(vals[where][0])

def volume_mode(im, m, scale=18):
    im = im * m
    
    mode = find_mode(im, m)
    
    xmin = np.percentile(im[im > mode].flatten(), 20)
    xmax = np.percentile(im[m].flatten(), 95)
    
    im[im < xmin] = mode
    im[im > xmax] = xmax
    im = 18 * (im - mode) / (xmax - mode)
    
    return np.sum(im[m].flatten()) - np.sum(m > 0)
        
def volume_csv(imdir, mfile, outfile, specifier='.tif'):
    os.chdir(imdir)
    cdir = os.getcwd()
    images = glob.glob('*' + specifier)
    
    m = (iio.read(mfile)[:,:,0] > 0)

    vf = open(outfile,"w")
    vf.write('date' + ',' + 'time' + ',' + 'volume' + ',' 
             + 'elevation' + ',' + 'azimuth' + '\n')
   
    for k in range(0, len(images)):
        im = iio.read(images[k])[:,:,0]
        az, el = get_az_el(images[k])
        
        vol = volume_mode(im, m)
        
        vf.write(images[k][6:8] + '/' + images[k][4:6] + '/' + images[k][0:4] + ',' 
                 + images[k][9:11] + ':' + images[k][11:13] + ':' + images[k][13:15] 
                 + ',' + str(vol) + ',' + str(el) + ',' + str(az) +  '\n')

    vf.close()
    os.chdir(cdir)

def read_volumes_csv_default_settings(csv):
    csv_data = pd.read_csv(csv, 
                       parse_dates=['date'], dayfirst=True, index_col=['date'])
    return csv_data

def plot_vs_ground_truth(ground_truth_csv=0, sfs_csv_list=[]):
    fig = go.Figure()
    traces = []

    if ground_truth_csv:
        ground_truth_data = read_volumes_csv_default_settings(ground_truth_csv)
        traces.append(go.Scatter(x=ground_truth_data.sort_values(['date']).index[1200:],
                              y=ground_truth_data.sort_values(['date'])['Stock'][1200:]
                              .values * 1000000 / 1.7,
                              mode='lines+markers',
                              name='reported data',
                              yaxis='y1'))
    sfs_data = []
    for i in range(0, len(sfs_csv_list)):
        sfs_data = read_volumes_csv_default_settings(sfs_csv_list[i])
        traces.append(go.Scatter(x=sfs_data.sort_values(['date']).index, 
                                     y=(sfs_data.sort_values(['date'])['volume']
                                        .values) * 9 * 1000,
                                     mode='markers+lines',
                                     name=sfs_csv_list[i].split('/')[-1],
                                     yaxis='y1'))
    
    layout = go.Layout(title='Coal volume', yaxis=dict(title='m^3'))
    fig = go.Figure(data=traces, layout=layout)
    fig.show()


######################################################################
######################### SAR ########################################
######################################################################

######################## masks ######################################
def crane_mask_sar(im, m, fm, threshold=50, dilation_factor=(5,5),
                   size_threshold=8000, final_dilation_factor=(10,10)):
    '''
    args:   - im                input image
            - m                 binary mask of the lanes
            - fm                binary mask of the region of interest (rails included)
            - threshold         brightness threshold (cranes are assumed very bright)
            - dilation_factor   first dilation
            - size_threshold    cranes are supposed larger than this number of pixel
            - final_dilation    
    outputs: binary mask with 1 where there is a crane
    '''
    mask = (im > threshold)
    dilation = ndimage.binary_dilation(mask * fm, np.ones(dilation_factor))

    all_labels = measure.label(dilation)
    size_components = np.zeros_like(all_labels)
    for i in range(1, np.max(all_labels)):
        size_components[all_labels == i] = np.sum(all_labels == i)
    cranes = (size_components > size_threshold) * m
    final_mask = ndimage.binary_dilation(cranes, np.ones(final_dilation_factor))
    return final_mask

def bright_edge_mask_sar(im, m, threshold=0.6, erosion_factor=(1,1),
                         dilation_factor=(4,4), min_component_size=150):
    # not really necessary for capella images but useful for cosmoskymed
    h, w = im.shape
    
    mask = (im > threshold) * m
    erosion = ndimage.binary_erosion(mask, np.ones(erosion_factor))
    dilation = ndimage.binary_dilation(erosion, np.ones(dilation_factor))
    
    all_labels = measure.label(dilation)
    size_components = np.zeros_like(all_labels)
    for i in range(1, np.max(all_labels) + 1):
        size_components[all_labels == i] = np.sum(all_labels == i)
    large_comonents = size_components > min_component_size
    
    dx, dy = ipg.grid_centered_gradient(w, h)
    edges = (1 - ((dx @ large_comonents.flatten()) >= 0)).reshape([h, w])
    return edges


################## create slant for dirichlet boundaries #################
# in the direction of the satellite, rotation of -elevation (- (90 - incidence)) of the ground

def Rx(theta):
    r = np.array([[1, 0,            0],
                  [0, math.cos(theta), -math.sin(theta)],
                  [0, math.sin(theta),  math.cos(theta)]])
    return r

def Ry(theta):
    r = np.array([[math.cos(theta),  0, math.sin(theta)],
                  [0,            1, 0         ],
                  [-math.sin(theta), 0, math.cos(theta)]])
    return r

def Rz(theta):
    r = np.array([[math.cos(theta), -math.sin(theta), 0],
                  [math.sin(theta),  math.cos(theta), 0],
                  [0,           0,            1]])
    return r

def sar_ground_slant(azel, h, w): 
# azel : azimuth and elevation of the satellite
    azrad = math.pi * azel[0] / 180
    elrad = math.pi * azel[1] / 180
    x = np.linspace(0, w-1, w)
    y = np.linspace(0, h-1, h)
    xv, yv = np.meshgrid(x,y)
    slant = - math.tan(elrad) * (math.sin(azrad) * xv - math.cos(azrad) * yv)
    return slant

def rotate(im, azel):
    h, w = im.shape
    azrad = math.pi * (90 - azel[0]) / 180
    elrad = math.pi * azel[1] / 180
    Kx = [[math.cos(elrad), 0, 0], 
          [ 0, 1, 0],
          [ 0, 0, 1]]
    R = Rz(-azrad) @ Kx @ Ry(- elrad) @ Rz(azrad)
    x = np.linspace(0, w-1, w)
    y = np.linspace(0, h-1, h)
    xv, yv = np.meshgrid(x,y)
    u = np.zeros((h,w,3))
    u[:,:,0] = xv
    u[:,:,1] = yv
    u[:,:,2] = im
    ur = u @ R.T
    return ur


def project(ur, azel, method='nearest'):
    h, w, _ = ur.shape
    elrad = azel[1] / 180 * math.pi
    x = np.linspace(0, w-1, w)
    y = np.linspace(0, h-1, h)
    xv, yv = np.meshgrid(x,y)
    points = np.zeros((h * w, 2))
    points[:,0] = ur[:,:,1].flatten()
    points[:,1] = ur[:,:,0].flatten()
    values = ur[:,:,2].flatten()
    grid = griddata(points, values, (yv, xv), method=method)
    return grid

############### stockpiles mask from sfs output #################################

def surface_mask_from_sfs_sar(im, m, threshold=5,
                              large_piles_height_min=20,
                              small_piles_size_minmax=np.array([150, 3000])):
    # default values for Newcastle_1 cosmoskymed
    eroded_mask = ndimage.binary_erosion(m, np.ones((20, 20)))

    first_thresholding = (im > threshold) * eroded_mask
    all_labels = measure.label(first_thresholding)
    height_components = 1.0 * np.zeros_like(all_labels)
    for i in range(1, np.max(all_labels) + 1):
        height_components[all_labels == i] = np.max(im[all_labels == i])

    large_piles = height_components > large_piles_height_min

    second_thresholding = ((height_components < large_piles_height_min)
                           * (height_components> 1))
    all_labels = measure.label(second_thresholding)
    size_components = np.zeros_like(all_labels)
    for i in range(1, np.max(all_labels) + 1):
        size_components[all_labels == i] = np.sum(all_labels == i)
    tmin, tmax = small_piles_size_minmax

    small_piles = (size_components < tmax) * (size_components > tmin)

    return (large_piles + small_piles) > 0

def surface_mask_from_sfs_sar_and_sar(im, h, m, threshold=5,
                              large_piles_height_min=20,
                              small_piles_size_minmax=np.array([150, 3000])):
    surface_sfs = surface_mask_from_sfs_sar(im, m)

    # default values for Newcastle_1 cosmoskymed
    eroded_mask = ndimage.binary_erosion(m, np.ones((20, 20)))
    first_thresholding = (np.sqrt(im) < 0.2) * eroded_mask
    all_labels = measure.label(first_thresholding)
    size_components = np.zeros_like(all_labels)
    for i in range(1, np.max(all_labels)):
        size_components[all_labels == i] = np.sum(all_labels == i)
    large_piles = size_components > 400
    dilation = ndimage.binary_dilation(large_piles, np.ones((5,5)))
    return (surface_sfs + dilation) > 0



