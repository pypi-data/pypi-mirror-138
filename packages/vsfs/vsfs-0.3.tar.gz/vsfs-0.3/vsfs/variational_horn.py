#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 18:34:51 2021

@author: mariedautume
"""

import numpy as np

from scipy import ndimage
from scipy.sparse import kron, spdiags, eye, block_diag, hstack

import iio

import sfs as sfs
import image_processing_with_graphs as ipg

B = ipg.gradient_stencil_shift(3, 4)
print(B)

def gradient_stencil_shift(w, h):
    # gradient with staggered grids (Horn & Schunck, 1981)
    diag = np.array([0, 1])
    
    submat_x = spdiags(np.vstack([ - np.ones(w), np.ones(w)]) / 2, 
                       diag, w - 1, w)
    mat_x = spdiags(np.vstack([ np.ones(h), np.ones(h)]), diag, h - 1, h)
    
    submat_y = spdiags(np.vstack([np.ones(w), np.ones(w)]) / 2, 
                       diag, w - 1, w)
    mat_y = spdiags(np.vstack([ - np.ones(h), np.ones(h)]), diag, h - 1, h)
   
    return kron(mat_x, submat_x), kron(mat_y, submat_y)

def laplacian_diagonal(w, h):
    # associated laplacia
    Bx, By = gradient_stencil_shift(w, h)
    return - (Bx.T @ Bx + By.T @ By)

def local_mean_diagonal(A):
    h, w = A.shape 
    L = laplacian_diagonal(w, h)
    return (L @ A.flatten() / 2 + A.flatten()).reshape([h,w])

def simulate_truncated_cone_100(azel):
    x = np.arange(-5, 5, 0.1)
    y = np.arange(-5, 5, 0.1)
    xx, yy = np.meshgrid(x, y)
    z = np.sqrt((xx ** 2 + yy ** 2) / (np.tan(0.18)) ** 2)
    
    height = (20 - z)
    height[height < 0] = 0
    height[height > 18] = 18

    m = np.zeros_like(height)
    m[10:-10, 10:-10] = 1

    h, w = height.shape
    
    Bx, By = gradient_stencil_shift(w, h)
    p = (Bx @ height.flatten()).reshape([h - 1, w - 1])
    q = (By @ height.flatten()).reshape([h - 1, w - 1])

    I = Reflectance(p, q, azel) #+ σ * np.random.normal(size=(h - 1, w - 1))
    
    return height, I, m

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

def energy_53(I, p, q, z, m, b, azel, μ, λ, A=1, B=0):
    h, w = z.shape
    Bx, By = ipg.gradient_stencil_shift(w, h)
    
    I = I.flatten()
    p = p.flatten()
    q = q.flatten()
    z = z.flatten()
    b = b.flatten()
    m = m.flatten()
    mg = (abs(Bx) @ m) > 1
    
    R = Reflectance(p, q, azel)
    
    E1 = np.sum(mg * (I - A * R - B) ** 2)
    E2 = μ * np.sum(mg * ((Bx @ z - p) ** 2 + (By @ z - q) ** 2))
    E3 = λ * np.sum(m * ((Bx.T @ p) ** 2 + (By.T @ p) ** 2
                         + (Bx.T @ q) ** 2 + (By.T @ q) ** 2))
    E4 = np.sum((1 - m) * ((z - b) ** 2))
    #print(f'E1: {E1} E2: {E2} E3: {E3} E4: {E4}')
    return E1 + E2 + E3 + E4

def energy_53_flat(I, p, q, z, m, b, w, h, azel, μ, λ, A=1, B=0):
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

def energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ, A=1, B=0):
    Bx, By = ipg.gradient_stencil_shift(w, h)
    
    mg = (abs(Bx) @ m) > 1
    
    R = Reflectance(p, q, azel)
    
    E1 = np.sum(mg * (I - A * R - B) ** 2)
    E2 = μ * np.sum(mg * ((Bx @ z - p) ** 2 + (By @ z - q) ** 2))
    E4 = np.sum((1 - m) * ((z - b) ** 2))
    #print(f'E1: {E1} E2: {E2} E3: {E3} E4: {E4}')
    return E1 + E2 + E4

def energy_gradient_53(I, p, q, z, m, b, azel, μ,  λ, A=1, B=0):
    h, w = z.shape
    Bx, By = ipg.gradient_stencil_shift(w, h)
    
    I = I.flatten()
    p = p.flatten()
    q = q.flatten()
    z = z.flatten()
    b = b.flatten()
    m = m.flatten()
    mg = (abs(Bx) @ m) > 1
    
    R = Reflectance(p, q, azel)
    Rp = Reflectance_p(p, q, azel)
    Rq = Reflectance_q(p, q, azel)
    
    dp = (Rp * mg * (I - R) + μ * mg * (p - Bx @ z)
          + λ * mg * (Bx @ Bx.T @ p + By @ By.T @ p))
    dq = (Rq * mg * (I - R) + μ * mg * (q - By @ z)
          + λ * mg * (Bx @ Bx.T @ q + By @ By.T @ q))
    dz = (m * (μ * ((Bx.T @ Bx + By.T @ By) @ z )
              - Bx.T @ p - By.T @ q) 
          + (1 - m) * ((z - b) ** 2))

    return (dp.reshape([h-1, w-1]), 
            dq.reshape([h-1, w-1]), 
            dz.reshape([h, w]))

def gradient_descent_53(I, p, q, z, m, b, azel, μ, λ, τ):
    dp, dq, dz = energy_gradient_53(I, p, q, z, m, b, azel, μ, λ)
    p = p - τ * dp
    q = p - τ * dq
    z = p - τ * dz
    return p, q, z

def horn_iter_56(I, p, q, z, m, b, azel, μ, λ, al=1, amb=0):
    h, w = z.shape
    Bx, By = ipg.gradient_stencil_shift(w, h)
    
    I = I.flatten()
    p0 = p.flatten()
    q0 = q.flatten()
    p_mean = ipg.local_mean_diagonal(p).flatten()
    q_mean = ipg.local_mean_diagonal(q).flatten()
    z_mean = ipg.local_mean_diagonal(z).flatten()
    z = z.flatten()
    b = b.flatten()
    m = m.flatten()
    mg = (abs(Bx) @ m) > 1
    
    R = al * Reflectance(p0, q0, azel) + amb
    Rp = al * Reflectance_p(p0, q0, azel)
    Rq = al * Reflectance_q(p0, q0, azel)
    
    δp_mean = p_mean - p0
    δq_mean = q_mean - q0
    δzx = (Bx @ z) - p0
    δzy = (By @ z) - q0
    print()
    
    D = (2 * λ + μ) * (2 * λ + μ + Rp ** 2 + Rq ** 2)
    A = 2 * λ * δp_mean + μ * δzx + (I - R) * Rp
    B = 2 * λ * δq_mean + μ * δzy + (I - R) * Rq
    
    δp = ((μ + 2 * λ + Rq ** 2) * A - Rp * Rq * B) / D
    δq = ((μ + 2 * λ + Rp ** 2) * B - Rp * Rq * A) / D
    
    p = p0 + mg * δp
    q = q0 + mg * δq
    #z = (m * (z_mean + (Bx.T @ p + By.T @ q) / 2) + (1 - m) * ((z - b) ** 2))
    z = (m * μ * (2 * z_mean + (Bx.T @ p + By.T @ q)) + (1 - m) * b) / (m * μ * 2 + 1 - m)
    
    return (p.reshape([h-1, w-1]), 
            q.reshape([h-1, w-1]), 
            z.reshape([h, w]))


def variational_horn(imfile, mfile, azel, μ, λ, niter=2000, b=None, p=None, q=None, al=1, amb=0):
    α, β, γ = sfs.sun_direction_from_position(azel)
    height = 0.1*iio.read(imfile)[:,:,0]
    m = (iio.read(mfile)[:,:,0] > 0).flatten()
    h, w = height.shape
    Bx, By = ipg.gradient_stencil_shift(w, h)

    p = Bx @ height.flatten()
    q = By @ height.flatten()
    I = Reflectance(p, q, azel)
    b = 0 * height.flatten()
    z = 0 * height.flatten()
    p = 0 * p 
    q = 0 * q 
    E = [energy_53_flat(I, p, q, z, m, b, w, h, azel, μ, λ)]

    p, q, z =  horn_iter_56_flat(I, p, q, z, m, b, azel, μ, λ, w, h)
    E.append(energy_53_flat(I, p, q, z, m, b, w, h, azel, μ, λ))


    #for i in range(0, niter):
    i = 0
    while (i < niter) & (np.abs(E[-2] - E[-1]) > 0.005):
        i += 1
        p, q, z =  horn_iter_56_flat(I, p, q, z, m, b, azel, μ, λ, w, h)
        E.append(energy_53_flat(I, p, q, z, m, b, w, h, azel, μ, λ))

    return z.reshape([h, w]), I.reshape([h-1, w-1]), Reflectance(Bx @ z, By @ z, azel).reshape([h-1, w-1]), E 

def horn_iter_56_2d(I, p, q, z, m, b, azel, μ, λ, al=1, amb=0):
    h, w = z.shape
    I = I.flatten()
    p = p.flatten()
    q = q.flatten()
    z = z.flatten()
    m = m.flatten()
    b = b.flatten()
    p, q, z = horn_iter_56_flat(I, p, q, z, m, b, azel, μ, λ, w, h)
    return (p.reshape([h-1, w-1]), 
            q.reshape([h-1, w-1]), 
            z.reshape([h, w]))


def horn_iter_56_flat(I, p, q, z, m, b, azel, μ, λ, w, h, al=1, amb=0):
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

def horn_iter_56_bb(I, p, q, z, m, mg, b, azel, μ, λ, w, h, Bx, By, al=1, amb=0):
    p0 = 1 * p
    q0 = 1 * q
    p_mean = ipg.flat_local_mean_diagonal(p, w-1, h-1)
    q_mean = ipg.flat_local_mean_diagonal(q, w-1, h-1)
    z_mean = ipg.flat_local_mean_diagonal(z, w, h)
    
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

def horn_iter_56_inside(I, p, q, z, m, mg, b, azel, μ, λ, w, h, Bx, By, Lpq, al=1, amb=0):
    
    p0 = 1 * p
    q0 = 1 * q
    p_mean = (Lpq @ p / 2 + p)
    q_mean = (Lpq @ q / 2 + q)
    z_mean = - (Bx.T @ Bx + By.T @ By) @ z / 2 + z
    #mg = ((abs(Bx) + abs(By)) @ m) > 1
    
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

def horn_iter_neu(I, p, q, z, m, b, m_neu, w, h, azel, μ, λ, al=1, amb=0):
    Bx, By = ipg.gradient_stencil_shift(w, h)
    
    p0 = 1 * p
    q0 = 1 * q
    p_mean = ipg.flat_local_mean_diagonal(p, w-1, h-1)
    q_mean = ipg.flat_local_mean_diagonal(q, w-1, h-1)
    z_mean = ipg.flat_local_mean_diagonal(z, w, h)
    mg = (abs(Bx) @ m) > 1
    
    R = al * Reflectance(p0, q0, azel) + amb
    Rp = al * Reflectance_p(p0, q0, azel)
    Rq = al * Reflectance_q(p0, q0, azel)
    
    δp_mean = p_mean - p0
    δq_mean = q_mean - q0
    δzx = (Bx @ z) - p0
    δzy = (By @ z) - q0
    print()
    
    D = (2 * λ + μ) * (2 * λ + μ + Rp ** 2 + Rq ** 2)
    A = 2 * λ * δp_mean + μ * δzx + (I - R) * Rp
    B = 2 * λ * δq_mean + μ * δzy + (I - R) * Rq
    
    δp = ((μ + 2 * λ + Rq ** 2) * A - Rp * Rq * B) / D
    δq = ((μ + 2 * λ + Rp ** 2) * B - Rp * Rq * A) / D
    
    p = p0 + mg * δp
    q = q0 + mg * δq
    #z = (m * (z_mean + (Bx.T @ p + By.T @ q) / 2) + (1 - m) * ((z - b) ** 2))
    z = (m * μ * (2 * z_mean + (Bx.T @ p + By.T @ q)) + (1 - m) * b) / (m * μ * 2 + 1 - m)
    
    return (p.reshape([h-1, w-1]), 
            q.reshape([h-1, w-1]), 
            z.reshape([h, w]))

def zoom_matrix_even(m, n):
    # h = 2m    w = 2n
    # A   : 2m 2n ->  m  n
    # A.T :  m  n -> 2m 2n
    # 1/4 A @ A.T = Id
    A = kron(kron(eye(m), [1,1]), kron(eye(n), [1,1]))
    return A

def zoom_matrix_odd(m, n):
    # h = 2m+1 w = 2n+1
    # A   : 2m+1 2n+1 ->  m    n
    # A.T :  m    n   -> 2m+1 2n+1
    # 1/4 A @ A.T = Id
    a = kron(eye(n), [1,1])
    b = hstack([a, 0 * eye(n, 1, k=0)])
    c = kron(eye(m), [1,1])
    A = hstack([kron(c, b), 0 * eye(m*n, 2*n+1, k=0)])
    return A

def zoom_bil_even(m, n):
    a = [3, 1]
    b = [1, 3]
    cn = eye(n, n-1, k=0)
    dn = eye(n, n-1, k=-1)
    cm = eye(m, m-1, k=0)
    dm = eye(m, m-1, k=-1)
    en = 4*eye(n,1)
    fn = 4*eye(n, 1, k = -n+1)
    em = 4*eye(m,1)
    fm = 4*eye(m, 1, k = -m+1)

    gn = kron(cn, a) + kron(dn, b)
    hn = hstack([en, gn, fn])
    gm = kron(cm, a) + kron(dm, b)
    hm = hstack([em, gm, fm])
    return kron(hm, hn)

def zoom_bil_odd(m, n):
    a = [3, 1]
    b = [1, 3]
    cn = eye(n, n-1, k=0)
    dn = eye(n, n-1, k=-1)
    cm = eye(m, m-1, k=0)
    dm = eye(m, m-1, k=-1)
    en = 4*eye(n,1)
    fn = 4*eye(n, 1, k = -n+1)
    em = 4*eye(m,1)
    fm = 4*eye(m, 1, k = -m+1)

    gn = kron(cn, a) + kron(dn, b)
    hn = hstack([en, gn, fn, 0 * eye(n, 1, k=0)])
    gm = kron(cm, a) + kron(dm, b)
    hm = hstack([em, gm, fm])
    A = hstack([kron(hm, hn), 0 * eye(m*n, 2*n+1, k=0)])
    return A

def zoom_out_all(I, p, q, z, m, b, H, W, Im, M, B):
    
    I = zoom_matrix_even()
    I = I[:-1:2, :-1:2]
    p = p[:-1:2, :-1:2]
    q = q[:-1:2, :-1:2]
    if (z.shape[0] % 2):
        if (z.shape[1] % 2):
            z = z[::2, ::2]
            m = m[::2, ::2]
            b = b[::2, ::2]
        else:
            z = z[::2, :-1:2]
            m = m[::2, :-1:2]
            b = b[::2, :-1:2]
    else:
        if (z.shape[1] % 2):
            z = z[:-1:2, ::2]
            m = m[:-1:2, ::2]
            b = b[:-1:2, ::2]
        else:
            z = z[:-1:2, :-1:2]
            m = m[:-1:2, :-1:2]
            b = b[:-1:2, :-1:2]
    H.append(I.shape[0] + 1)
    W.append(I.shape[1] + 1)
    Im.append(I)
    M.append(m)
    B.append(b)
    assert(z.shape[0] == I.shape[0] + 1)
    return I, p, q, z, m, b, H, W, Im, M, B

def zoom_in_all(p, q, z, H, W, Im, M, B, s):
    hp, wp = z.shape
    m = np.zeros((hp, wp))
    m[2:-2, 2:-2] = 1
    m1 = np.zeros((hp - 1, wp - 1))
    m1[1:-1, 1:-1] = 1
    pz = ndimage.zoom(p, 2, order=0) * ndimage.zoom(m1, 2, order=0)
    qz = ndimage.zoom(q, 2, order=0) * ndimage.zoom(m1, 2, order=0)
    zz = ndimage.zoom(z, 2, order=0) * ndimage.zoom(m, 2, order=0)
    h = H[s-1]
    w = W[s-1]
    p = np.zeros((h - 1, w - 1))
    p[:pz.shape[0],:pz.shape[1]] = pz
    q = np.zeros((h -  1, w - 1))
    q[:pz.shape[0],:pz.shape[1]] = qz
    z = np.zeros((h, w))
    z = zz[:z.shape[0],:z.shape[1]]
    I = Im[s-1]
    m = M[s-1]
    b = B[s-1]
    return I, p, q, z, m, b


import sfs
I = imread(...)
z1 = sfs.variational(I, m, b, azel)
z2 = sfs.linear(I, m, b, azel)
z3 = sfs.eikonal(I, m, b, azel)



def pyramid_var_sfs(I, z, m, b, azel, nscales=8, λ=0.1, μ=0.1, ε=1, κ=4, stop=0.0001, itermax=10000):
    print('start pyramid')
    h, w = z.shape
    H = [z.shape[0]]
    W = [z.shape[1]]
    s = 0
    Im = [I]
    M = [m]
    B = [b]
    Z = []
    E = []

    # start with z even and I odd
    if h % 2 > 0:
        z = np.vstack((z, z[-1,:]))
        b = np.vstack((b, b[-1,:]))
        m = np.vstack((m, m[-1,:]))
        I = np.vstack((I, I[-1, :]))
        h = h+1
    if w % 2 > 0:
        z = np.hstack((z, z[:,-1].reshape([h, 1])))
        m = np.hstack((m, m[:,-1].reshape([h, 1])))
        b = np.hstack((b, b[:,-1].reshape([h, 1])))
        I = np.hstack((I, I[:,-1].reshape([h-1, 1])))
        w = w+1
    k = np.int(h / 2)
    l = np.int(w / 2)
    print(f'k: {k}, l:{l}')
    while (k >= 5) and (l >= 5) and (s < nscales):
        Ae = zoom_matrix_even(k, l)
        Ao = zoom_matrix_odd(k-1, l-1)
        #print(f'Ae: {Ae.shape}, Ao: {Ao.shape}, z: {z.shape}, I: {I.shape}')
        z = (Ae @ z.flatten() / 4).reshape([k,l])
        b = (Ae @ b.flatten() / 4).reshape([k,l])
        m = (Ae @ m.flatten() / 4).reshape([k,l]) > 0
        I = (Ao @ I.flatten() / 4).reshape([k-1, l-1])
        Im.append(I)
        M.append(m)
        B.append(b)
        # z must be even and I odd
        assert(I.shape[0] == z.shape[0] - 1)
        assert(I.shape[1] == z.shape[1] - 1)
        if k % 2 > 0:
            z = np.vstack((z, z[-1,:]))
            m = np.vstack((m, m[-1,:]))
            b = np.vstack((b, b[-1,:]))
            I = np.vstack((I, I[-1, :]))
            k = k+1
        if l % 2 > 0:
            z = np.hstack((z, z[:,-1].reshape([k, 1])))
            m = np.hstack((m, b[:,-1].reshape([k, 1])))
            b = np.hstack((b, b[:,-1].reshape([k, 1])))
            I = np.hstack((I, I[:,-1].reshape([k-1, 1])))
            l = l+1
        k = np.int(k / 2)
        l = np.int(l / 2)
        #print(f'k: {k}, l:{l}')
        s = s + 1
    h, w = z.shape
    while (s > 0):
        Bx, By = ipg.gradient_stencil_shift(w, h)
        p = Bx @ z.flatten()
        q = By @ z.flatten()
        z = z.flatten()
        m = m.flatten()
        b = b.flatten()
        I = I.flatten()
        i = 0
        print(f'h: {h}, w:{w}, z: {z.shape}, I: {I.shape}')
        #while (i < 100):
        #    i += 1
        #    p, q, z = horn_iter_56_flat(I, p, q, z, m, b, azel, μ, 1, w, h)
        #    E.append((100/h) * (150 / w) * energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ))
        #i = 0
        while (i < 500):
            i += 1
            p, q, z = horn_iter_56_flat(I, p, q, z, m, b, azel, μ, 0.1, w, h)
            E.append((100/h) * (150 / w) * energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ))
        i = 0
        #while (i < 100):
        #    i += 1
        #    p, q, z = horn_iter_56_flat(I, p, q, z, m, b, azel, μ, 0.01, w, h)
        #    E.append((100/h) * (150 / w) * energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ))
        #i = 0
        while (i < 500):
            i += 1
            p, q, z = horn_iter_56_flat(I, p, q, z, m, b, azel, μ, 0.001, w, h)
            E.append((100/h) * (150 / w) * energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ))
        Z.append(z.reshape([h,w]))
#        Ae = zoom_matrix_even(h, w)
        Ae = zoom_bil_even(h, w) / 8
        z = (Ae.T @ z.flatten()).reshape([2*h, 2*w])
        for i in range(len(Z)):
            Z[i] = (Ae.T @ Z[i].flatten()).reshape([2*h, 2*w])
        I = Im[s-1]
        m = M[s-1]
        b = B[s-1]
        h, w = m.shape
        print(f'h: {h}, w:{w}')
        z = z[:h, :w]
        for i in range(len(Z)):
            Z[i] = Z[i][:h, :w]
        Bx, By = ipg.gradient_stencil_shift(w, h)
        p = Bx @ z.flatten()
        q = By @ z.flatten()
        s = s - 1
    i = 0
    z = z.flatten()
    m = m.flatten()
    b = b.flatten()
    I = I.flatten()
    while (i < 2000):
        i += 1
        p, q, z = horn_iter_56_flat(I, p, q, z, m, b, azel, μ, λ, w, h)
        E.append((100/h) * (150 / w) * energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ))
    Z.append(z.reshape([h, w]))
    i = 0
    while (i < 2000):
        i += 1
        p, q, z = horn_iter_56_flat(I, p, q, z, m, b, azel, μ, 0, w, h)
        E.append((100/h) * (150 / w) * energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ))
    Z.append(z.reshape([h, w]))
    return Z, z.reshape([h, w]), E

        

def pyramid_var_sfs_bb(I, z, m, b, azel, nscales=8, λ=0.1, μ=0.1, ε=1, κ=4, stop=0.0001, itermax=10000):
    print('start pyramid')
    h, w = z.shape
    H = [z.shape[0]]
    W = [z.shape[1]]
    s = 0
    Im = [I]
    M = [m]
    B = [b]
    Z = []
    E = []

    # start with z even and I odd
    if h % 2 > 0:
        z = np.vstack((z, z[-1,:]))
        b = np.vstack((b, b[-1,:]))
        m = np.vstack((m, m[-1,:]))
        I = np.vstack((I, I[-1, :]))
        h = h+1
    if w % 2 > 0:
        z = np.hstack((z, z[:,-1].reshape([h, 1])))
        m = np.hstack((m, m[:,-1].reshape([h, 1])))
        b = np.hstack((b, b[:,-1].reshape([h, 1])))
        I = np.hstack((I, I[:,-1].reshape([h-1, 1])))
        w = w+1
    k = np.int(h / 2)
    l = np.int(w / 2)
    print(f'k: {k}, l:{l}')
    while (k >= 5) and (l >= 5) and (s < nscales):
        Ae = zoom_matrix_even(k, l)
        Ao = zoom_matrix_odd(k-1, l-1)
        #print(f'Ae: {Ae.shape}, Ao: {Ao.shape}, z: {z.shape}, I: {I.shape}')
        z = (Ae @ z.flatten() / 4).reshape([k,l])
        b = (Ae @ b.flatten() / 4).reshape([k,l])
        m = (Ae @ m.flatten() / 4).reshape([k,l]) > 0
        I = (Ao @ I.flatten() / 4).reshape([k-1, l-1])
        Im.append(I)
        M.append(m)
        B.append(b)
        # z must be even and I odd
        assert(I.shape[0] == z.shape[0] - 1)
        assert(I.shape[1] == z.shape[1] - 1)
        if k % 2 > 0:
            z = np.vstack((z, z[-1,:]))
            m = np.vstack((m, m[-1,:]))
            b = np.vstack((b, b[-1,:]))
            I = np.vstack((I, I[-1, :]))
            k = k+1
        if l % 2 > 0:
            z = np.hstack((z, z[:,-1].reshape([k, 1])))
            m = np.hstack((m, b[:,-1].reshape([k, 1])))
            b = np.hstack((b, b[:,-1].reshape([k, 1])))
            I = np.hstack((I, I[:,-1].reshape([k-1, 1])))
            l = l+1
        k = np.int(k / 2)
        l = np.int(l / 2)
        #print(f'k: {k}, l:{l}')
        s = s + 1
    h, w = z.shape
    while (s > 0):
        Bx, By = ipg.gradient_stencil_shift(w, h)
        p = Bx @ z.flatten()
        q = By @ z.flatten()
        z = z.flatten()
        m = m.flatten()
        mg = ((abs(Bx) + abs(By)) @ m) > 1
        b = b.flatten()
        I = I.flatten()
        i = 0
        print(f'h: {h}, w:{w}, z: {z.shape}, I: {I.shape}')
        #while (i < 100):
        #    i += 1
        #    p, q, z = horn_iter_56_flat(I, p, q, z, m, b, azel, μ, 1, w, h)
        #    E.append((100/h) * (150 / w) * energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ))
        #i = 0
        while (i < 500):
            i += 1
            p, q, z = horn_iter_56_bb(I, p, q, z, m, mg, b, azel, μ, 0.1, w, h, Bx, By)
            E.append((100/h) * (150 / w) * energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ))
        i = 0
        #while (i < 100):
        #    i += 1
        #    p, q, z = horn_iter_56_flat(I, p, q, z, m, b, azel, μ, 0.01, w, h)
        #    E.append((100/h) * (150 / w) * energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ))
        #i = 0
        while (i < 500):
            i += 1
            p, q, z = horn_iter_56_bb(I, p, q, z, m, mg, b, azel, μ, 0.1, w, h, Bx, By)
            E.append((100/h) * (150 / w) * energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ))
        Z.append(z.reshape([h,w]))
#        Ae = zoom_matrix_even(h, w)
        Ae = zoom_bil_even(h, w) / 8
        z = (Ae.T @ z.flatten()).reshape([2*h, 2*w])
        for i in range(len(Z)):
            Z[i] = (Ae.T @ Z[i].flatten()).reshape([2*h, 2*w])
        I = Im[s-1]
        m = M[s-1]
        b = B[s-1]
        h, w = m.shape
        print(f'h: {h}, w:{w}')
        z = z[:h, :w]
        for i in range(len(Z)):
            Z[i] = Z[i][:h, :w]
        Bx, By = ipg.gradient_stencil_shift(w, h)
        p = Bx @ z.flatten()
        q = By @ z.flatten()
        s = s - 1
    i = 0
    z = z.flatten()
    m = m.flatten()
    b = b.flatten()
    I = I.flatten()
    while (i < 2000):
        i += 1
        p, q, z = horn_iter_56_bb(I, p, q, z, m, mg, b, azel, μ, 0.1, w, h, Bx, By)
        E.append((100/h) * (150 / w) * energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ))
    Z.append(z.reshape([h, w]))
    i = 0
    while (i < 2000):
        i += 1
        p, q, z = horn_iter_56_bb(I, p, q, z, m, mg, b, azel, μ, 0.1, w, h, Bx, By)
        E.append((100/h) * (150 / w) * energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ))
    Z.append(z.reshape([h, w]))
    return Z, z.reshape([h, w]), E

        
        



#    assert(I.shape == p.shape)
#    while (H[s] > 10) & (W[s] > 10):
#        s += 1
#        I, p, q, z, m, b, H, W, Im, M, B = zoom_out_all(I, p, q, z, m, b, H, W, Im, M, B)
#    print('enter pyramid')
#    while (s > 0):
#        i = 0
#        print(f's: {s} \t h: {H[s]} \t w: {W[s]} \t shape I: ({I.shape}) \t shape z: ({z.shape})')
#        while (i < 10):# & (np.abs(E[-2] - E[-1]) > 0.005):
#            i += 1
#            p, q, z = horn_iter_56_2d(I, p, q, z, m, b, azel, μ, λ)
#        p, q, z = horn_iter_56_2d(I, p, q, z, m, b, azel, μ, λ)
#        #p, q, z = variational_sfs(I, p, q, z, azel)
#        I, p, q, z, m, b = zoom_in_all(p, q, z, H, W, Im, M, B, s)
#        s -= 1
#    #p, q, z = variational_sfs(I, p, q, z, azel)
#    while (i < 100):# & (np.abs(E[-2] - E[-1]) > 0.005):
#        i += 1
#        p, q, z = horn_iter_56_2d(I, p, q, z, m, b, azel, μ, λ)
#    #p, q, z = horn_iter_56_2d(I, p, q, z, m, b, azel, μ, λ)
#    return p, q, z
#
#

def pyramid_var_sfs_inside(I, z, m, b, azel, nscales=8, λ=0.1, μ=0.1, ε=1, κ=4, stop=0.0001, itermax=10000):
    print('start pyramid')
    h, w = z.shape
    H = [z.shape[0]]
    W = [z.shape[1]]
    s = 0
    Im = [I]
    M = [m]
    B = [b]
    Z = []
    E = []

    # start with z even and I odd
    if h % 2 > 0:
        z = np.vstack((z, z[-1,:]))
        b = np.vstack((b, b[-1,:]))
        m = np.vstack((m, m[-1,:]))
        I = np.vstack((I, I[-1, :]))
        h = h+1
    if w % 2 > 0:
        z = np.hstack((z, z[:,-1].reshape([h, 1])))
        m = np.hstack((m, m[:,-1].reshape([h, 1])))
        b = np.hstack((b, b[:,-1].reshape([h, 1])))
        I = np.hstack((I, I[:,-1].reshape([h-1, 1])))
        w = w+1
    k = np.int(h / 2)
    l = np.int(w / 2)
    print(f'k: {k}, l:{l}')
    while (k >= 5) and (l >= 5) and (s < nscales):
        Ae = zoom_matrix_even(k, l)
        Ao = zoom_matrix_odd(k-1, l-1)
        #print(f'Ae: {Ae.shape}, Ao: {Ao.shape}, z: {z.shape}, I: {I.shape}')
        z = (Ae @ z.flatten() / 4).reshape([k,l])
        b = (Ae @ b.flatten() / 4).reshape([k,l])
        m = (Ae @ m.flatten() / 4).reshape([k,l]) > 0
        I = (Ao @ I.flatten() / 4).reshape([k-1, l-1])
        Im.append(I)
        M.append(m)
        B.append(b)
        # z must be even and I odd
        assert(I.shape[0] == z.shape[0] - 1)
        assert(I.shape[1] == z.shape[1] - 1)
        if k % 2 > 0:
            z = np.vstack((z, z[-1,:]))
            m = np.vstack((m, m[-1,:]))
            b = np.vstack((b, b[-1,:]))
            I = np.vstack((I, I[-1, :]))
            k = k+1
        if l % 2 > 0:
            z = np.hstack((z, z[:,-1].reshape([k, 1])))
            m = np.hstack((m, b[:,-1].reshape([k, 1])))
            b = np.hstack((b, b[:,-1].reshape([k, 1])))
            I = np.hstack((I, I[:,-1].reshape([k-1, 1])))
            l = l+1
        k = np.int(k / 2)
        l = np.int(l / 2)
        #print(f'k: {k}, l:{l}')
        s = s + 1
    h, w = z.shape
    while (s > 0):
        Bx, By = ipg.gradient_stencil_shift(w, h)
        p = Bx @ z.flatten()
        q = By @ z.flatten()
        z = z.flatten()
        #m = m.flatten()
        #b = b.flatten()
        #I = I.flatten()
        print(f'h: {h}, w:{w}, z: {z.shape}, I: {I.shape}')
        #while (i < 100):
        #    i += 1
        #    p, q, z = horn_iter_56_flat(I, p, q, z, m, b, azel, μ, 1, w, h)
        #    E.append((100/h) * (150 / w) * energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ))
        #i = 0
        mask_dilated = (ndimage.binary_dilation(m.reshape([h, w]), np.ones((4,4)))).flatten()
        flat_dilated_mask = mask_dilated.flatten()
        flat_dilated_mask_g = ((abs(Bx) + abs(By)) @ flat_dilated_mask) > 1

        zm = z.flatten()[flat_dilated_mask > 0]
        b = b.flatten()[flat_dilated_mask > 0]
        m = m.flatten()[flat_dilated_mask > 0]
        I = I.flatten()[flat_dilated_mask_g > 0]

        Bxcsr = Bx.tocsr()
        Bxcsr = Bxcsr[flat_dilated_mask > 0, :]
        Bxcsr = Bxcsr[:, flat_dilated_mask > 0]
        Bx = Bxcsr.tocoo()
        Bycsr = By.tocsr()
        Bycsr = Bycsr[flat_dilated_mask > 0, :]
        Bycsr = Bycsr[:, flat_dilated_mask > 0]
        By = Bycsr.tocoo()
        Bpx, Bpy = ipg.gradient_stencil_shift(w-1, h-1)
        Bxcsr = Bpx.tocsr()
        Bxcsr = Bxcsr[flat_dilated_mask_g > 0, :]
        Bxcsr = Bxcsr[:, flat_dilated_mask_g > 0]
        Bpx = Bxcsr.tocoo()
        Bycsr = Bpy.tocsr()
        Bycsr = Bycsr[flat_dilated_mask_g > 0, :]
        Bycsr = Bycsr[:, flat_dilated_mask_g > 0]
        Bpy = Bycsr.tocoo()
        Lpq = - (Bpx.T @ Bpx + Bpy.T @ Bpy)

        mg = ((abs(Bx) + abs(By)) @ m) > 1

        i = 0
        while (i < 500):
            i += 1
            p, q, zm = horn_iter_56_inside(I, p, q, zm, m, mg, b, azel, μ, 0.1, w, h, Bx, By, Lpq)
            #E.append((100/h) * (150 / w) * energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ))
        i = 0
        #while (i < 100):
        #    i += 1
        #    p, q, z = horn_iter_56_flat(I, p, q, z, m, b, azel, μ, 0.01, w, h)
        #    E.append((100/h) * (150 / w) * energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ))
        #i = 0
        while (i < 500):
            i += 1
            p, q, zm = horn_iter_56_inside(I, p, q, zm, m, mg, b, azel, μ, 0.1, w, h, Bx, By, Lpq)
            #p, q, z = horn_iter_56_flat(I, p, q, z, m, b, azel, μ, 0.001, w, h)
            #E.append((100/h) * (150 / w) * energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ))

        z[flat_dilated_mask > 0] = zm
        Z.append(z.reshape([h,w]))
#        Ae = zoom_matrix_even(h, w)
        Ae = zoom_bil_even(h, w) / 8
        z = (Ae.T @ z.flatten()).reshape([2*h, 2*w])
        for i in range(len(Z)):
            Z[i] = (Ae.T @ Z[i].flatten()).reshape([2*h, 2*w])
        I = Im[s-1]
        m = M[s-1]
        b = B[s-1]
        h, w = m.shape
        print(f'h: {h}, w:{w}')
        z = z[:h, :w]
        for i in range(len(Z)):
            Z[i] = Z[i][:h, :w]
        Bx, By = ipg.gradient_stencil_shift(w, h)
        p = Bx @ z.flatten()
        q = By @ z.flatten()
        s = s - 1

    mask_dilated = (ndimage.binary_dilation(m.reshape([h, w]), np.ones((4,4)))).flatten()
    flat_dilated_mask = mask_dilated.flatten()
    flat_dilated_mask_g = ((abs(Bx) + abs(By)) @ flat_dilated_mask) > 1

    zm = z.flatten()[flat_dilated_mask > 0]
    b = b.flatten()[flat_dilated_mask > 0]
    m = m.flatten()[flat_dilated_mask > 0]
    I = I.flatten()[flat_dilated_mask_g > 0]

    Bxcsr = Bx.tocsr()
    Bxcsr = Bxcsr[flat_dilated_mask > 0, :]
    Bxcsr = Bxcsr[:, flat_dilated_mask > 0]
    Bx = Bxcsr.tocoo()
    Bycsr = By.tocsr()
    Bycsr = Bycsr[flat_dilated_mask > 0, :]
    Bycsr = Bycsr[:, flat_dilated_mask > 0]
    By = Bycsr.tocoo()
    Bpx, Bpy = ipg.gradient_stencil_shift(w-1, h-1)
    Bxcsr = Bpx.tocsr()
    Bxcsr = Bxcsr[flat_dilated_mask_g > 0, :]
    Bxcsr = Bxcsr[:, flat_dilated_mask_g > 0]
    Bpx = Bxcsr.tocoo()
    Bycsr = Bpy.tocsr()
    Bycsr = Bycsr[flat_dilated_mask_g > 0, :]
    Bycsr = Bycsr[:, flat_dilated_mask_g > 0]
    Bpy = Bycsr.tocoo()
    Lpq = - (Bpx.T @ Bpx + Bpy.T @ Bpy)

    mg = ((abs(Bx) + abs(By)) @ m) > 1
    i = 0
    while (i < 2000):
        i += 1
        p, q, z = horn_iter_56_flat(I, p, q, z, m, b, azel, μ, λ, w, h)
        E.append((100/h) * (150 / w) * energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ))
   # Z.append(z.reshape([h, w]))
    i = 0
    while (i < 2000):
        i += 1
        p, q, z = horn_iter_56_flat(I, p, q, z, m, b, azel, μ, 0, w, h)
        E.append((100/h) * (150 / w) * energy_53_scaled(I, p, q, z, m, b, w, h, azel, μ, λ))
    z[flat_dilated_mask > 0] = zm
    Z.append(z.reshape([h, w]))
    return Z, z.reshape([h, w]), E
