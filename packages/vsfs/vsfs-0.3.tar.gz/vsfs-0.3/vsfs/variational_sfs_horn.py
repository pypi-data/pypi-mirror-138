#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 16:00:54 2021

@author: mariedautume
"""
# %% Imports

import sys, os, math, glob

import numpy as np
import numpy.matlib as matlib

from scipy.sparse import eye, kron, diags, vstack, spdiags

import iio, vpv

#import image_processing_with_graphs as ipg

from scikits.umfpack import spsolve

from scipy import ndimage
from scipy.ndimage import gaussian_filter

from copy import copy

# %% With  another discretization for the gradient


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
    # associated laplacian
    Bx, By = gradient_stencil_shift(w, h)
    return - (Bx.T @ Bx + By.T @ By)

def local_mean_diagonal(A):
    h, w = A.shape 
    L = laplacian_diagonal(w, h)
    return (L @ A.flatten() / 2 + A.flatten()).reshape([h,w])

# %% SFS specific functions

def sun_direction_from_position(azel):
    az, el = azel
    azrad = float(az) * math.pi / 180
    elrad = float(el) * math.pi / 180
    α = math.cos(elrad) * math.sin(azrad)
    β = - math.cos(elrad) * math.cos(azrad) # le moins correspond au fait que python a un axe vertical vers le bas (-y au  lieu de y)
    γ = math.sin(elrad)
    return α, β, γ

# %% Functions

def Reflectance(p, q, azel):
    α, β, γ = sun_direction_from_position(azel)
    R = (γ - α * p - β * q) / np.sqrt(1 + p ** 2 + q ** 2)
    return R

def Reflectance_p(p, q, azel):
    α, β, γ = sun_direction_from_position(azel)
    den = np.sqrt(1 + p ** 2 + q ** 2)
    Rp = (- α * den ** 2 - p * (γ - α * p - β * q)) / (den ** 3)
    return Rp

def Reflectance_q(p, q, azel):
    α, β, γ = sun_direction_from_position(azel)
    den = np.sqrt(1 + p ** 2 + q ** 2)
    Rq = (- β * den ** 2 - q * (γ - α * p - β * q)) / (den ** 3)
    return Rq

# %% Iteration schemes



def iteration_pq_56(p, q, z, azel, h, w, λ1, λ2, κ=2):
    p0 = 1 * p
    q0 = 1 * q
    
    p_mean = local_mean_diagonal(p.reshape([h - 1, w - 1])).flatten()
    q_mean = local_mean_diagonal(q.reshape([h - 1, w - 1])).flatten()
    z_mean = local_mean_diagonal(z.reshape([h, w])).flatten()
    
    A = (κ * λ1 * (p_mean - p0) + μ * (Bx @ z - p0) 
         + (I.flatten() - Reflectance(p_mean, q_mean, azel)) 
         * Reflectance_p(p_mean, q_mean, azel))
    B = (κ * λ1 * (q_mean - q0) + μ * (By @ z - q0) 
         + (I.flatten() - Reflectance(p_mean, q_mean, azel)) 
         * Reflectance_q(p_mean, q_mean, azel))
    D = λ2 * (λ2 + Reflectance_p(p_mean, q_mean, azel) ** 2
              + Reflectance_q(p_mean, q_mean, azel) ** 2)
    δp = ((λ2 + Reflectance_q(p_mean, q_mean, azel) ** 2) * A 
          - Reflectance_p(p_mean, q_mean, azel) 
          * Reflectance_q(p_mean, q_mean, azel)
          * B) / D
    δq = ((λ2 + Reflectance_p(p_mean, q_mean, azel) ** 2) * B 
          - Reflectance_p(p_mean, q_mean, azel) 
          * Reflectance_q(p_mean, q_mean, azel)
          * A) / D
    
    p_new = p0 + δp
    q_new = q0 + δq
    z_new = z_mean + (ε ** 2 / κ) * (Bx.T @ p_new + By.T @ q_new)
    
    return p_new, q_new, z_new

def iteration_pq_56_2d(I, p, q, z, azel, λ, μ, ε=1, κ=2):
    p0 = 1 * p.flatten()
    q0 = 1 * q.flatten()
    
    h, w = z.shape
    Bx, By = gradient_stencil_shift(w, h)
    
    λ1 = λ / (ε ** 2)
    λ2 = κ * λ1 + μ
    
    p_mean = local_mean_diagonal(p).flatten()
    q_mean = local_mean_diagonal(q).flatten()
    z_mean = local_mean_diagonal(z).flatten()
    
    A = (κ * λ1 * (p_mean - p0) + μ * (Bx @ z.flatten() - p0) 
         + (I.flatten() - Reflectance(p_mean, q_mean, azel)) 
         * Reflectance_p(p_mean, q_mean, azel))
    B = (κ * λ1 * (q_mean - q0) + μ * (By @ z.flatten() - q0) 
         + (I.flatten() - Reflectance(p_mean, q_mean, azel)) 
         * Reflectance_q(p_mean, q_mean, azel))
    D = λ2 * (λ2 + Reflectance_p(p_mean, q_mean, azel) ** 2
              + Reflectance_q(p_mean, q_mean, azel) ** 2)
    δp = ((λ2 + Reflectance_q(p_mean, q_mean, azel) ** 2) * A 
          - Reflectance_p(p_mean, q_mean, azel) 
          * Reflectance_q(p_mean, q_mean, azel)
          * B) / D
    δq = ((λ2 + Reflectance_p(p_mean, q_mean, azel) ** 2) * B 
          - Reflectance_p(p_mean, q_mean, azel) 
          * Reflectance_q(p_mean, q_mean, azel)
          * A) / D
    
    p_new = p0 + δp
    q_new = q0 + δq
    z_new = z_mean + (ε ** 2 / κ) * (Bx.T @ p_new + By.T @ q_new)
    
    return (p_new.reshape([h - 1, w - 1]), 
            q_new.reshape([h - 1, w - 1]), 
            z_new.reshape([h, w]))


# %%

def energy_56(I, p, q, z, λ, μ, azel):
    h, w = z.shape
    Bx, By = gradient_stencil_shift(w, h)
    E1 = np.sum((I.flatten() 
                 - Reflectance(p.flatten(), q.flatten(), azel)) ** 2)
    E2 = λ * np.sum((Bx.T @ p.flatten()) ** 2 
                    + (By.T @ p.flatten()) ** 2 
                    + (Bx.T @ q.flatten()) ** 2 + (By.T @ q.flatten()) ** 2)
    E3 = μ * np.sum((Bx @ z.flatten() - p.flatten()) ** 2 
                    + (By @ z.flatten() - q.flatten()) ** 2)
    print('energy: ' + str(E1) + ' ' + str(E2) + ' ' + str(E3) + ' ' + str(E1 + E2 + E3))
    Global_Energies.append([E1, E2, E3, E1 + E2 + E3])
    return E1 + E2 + E3

def energy_56_1d(I, p, q, z, h, w, azel):
    Bx, By = gradient_stencil_shift(w, h)
    E1 = np.sum((I.flatten() 
                 - Reflectance(p.flatten(), q.flatten(), azel)) ** 2)
    E2 = λ * np.sum((Bx.T @ p.flatten()) ** 2 
                    + (By.T @ p.flatten()) ** 2 
                    + (Bx.T @ q.flatten()) ** 2 + (By.T @ q.flatten()) ** 2)
    E3 = μ * np.sum((Bx @ z.flatten() - p.flatten()) ** 2 
                    + (By @ z.flatten() - q.flatten()) ** 2)
    print('energy: ' + str(E1) + ' ' + str(E2) + ' ' + str(E3) + ' ' + str(E1 + E2 + E3))
    Global_Energies.append([E1, E2, E3, E1 + E2 + E3])
    return E1 + E2 + E3


def variational_sfs(I, p, q, z, azel, λ=0.1, μ=0.1, ε=1, κ=2, stop=0.0001, itermax=10000):
    E = 100000000
    k = 0
    h, w = z.shape
    
    while (k < itermax) & (E - energy_56(I, p, q, z, λ, μ, azel) > stop):
        k += 1
        E = 1 * energy_56(I, p, q, z, λ, μ, azel)
        p, q, z = iteration_pq_56_2d(I, p, q, z, azel, λ, μ, ε=ε, κ=κ)
        print(f'iter: {k} \t energy: {E} \t '
              f'new energy: {energy_56(I, p, q, z, λ, μ, azel)} \t'
              f'diff: {E - energy_56(I, p, q, z, λ, μ, azel) > stop}')
    return p, q, z

def zoom_out_all(I, p, q, z, H, W, Im):
    I = I[:-1:2, :-1:2]
    p = p[:-1:2, :-1:2]
    q = q[:-1:2, :-1:2]
    if (z.shape[0] % 2):
        if (z.shape[1] % 2):
            z = z[::2, ::2]
        else:
            z = z[::2, :-1:2]
    else:
        if (z.shape[1] % 2):
            z = z[:-1:2, ::2]
        else:
            z = z[:-1:2, :-1:2]
    H.append(I.shape[0] + 1)
    W.append(I.shape[1] + 1)
    Im.append(I)
    assert(z.shape[0] == I.shape[0] + 1)
    return I, p, q, z, H, W, Im

def zoom_in_all(p, q, z, H, W, Im):
    hp, wp = z.shape
    m = np.zeros((hp, wp))
    m[2:-2, 2:-2] = 1
    m1 = np.zeros((hp - 1, wp - 1))
    m1[1:-1, 1:-1] = 1
    pz = ndimage.zoom(p, 2, order=0) * ndimage.zoom(m1, 2, order=0)
    qz = ndimage.zoom(q, 2, order=0) * ndimage.zoom(m1, 2, order=0)
    zz = ndimage.zoom(z, 2, order=0) * ndimage.zoom(m, 2, order=0)
    h = H[s]
    w = W[s]
    I = Im[s]
    p = np.zeros((h - 1, w - 1))
    p[:pz.shape[0],:pz.shape[1]] = pz
    q = np.zeros((h -  1, w - 1))
    q[:pz.shape[0],:pz.shape[1]] = qz
    z = np.zeros((h, w))
    z[:,:] = zz[:z.shape[0],:z.shape[1]]
    return p, q, z


def pyramid_var_sfs(I, p, q, z, azel, nscales=8, λ=0.1, μ=0.1, ε=1, κ=4, stop=0.0001, itermax=10000):
    print('start pyramid')
    H = [z.shape[0]]
    W = [z.shape[1]]
    s = 0
    Im = [I]
    assert(I.shape == p.shape)
    while (H[s] > 10) & (W[s] > 10):
        I, p, q, z, H, W, Im = zoom_out_all(I, p, q, z, H, W, Im)
        s += 1
    print('enter pyramid')
    while (s > 0):
        #print(f's: {s} \t h: {H[s]} \t w: {W[s]} \t shape I: ({I.shape}) \t shape z: ({z.shape})')
        s -= 1
        p, q, z = variational_sfs(I, p, q, z, azel)
        p, q, z = zoom_in_all(p, q, z, H, W, Im)
    I = Im[s]
    p, q, z = variational_sfs(I, p, q, z, azel)
    vpv(I, Reflectance(p, q, azel),z,p)
    return p, q, z

# %% Simulation cône

x = np.arange(-5, 5, 0.1)
y = np.arange(-5, 5, 0.1)
xx, yy = np.meshgrid(x, y)
z = np.sqrt((xx ** 2 + yy ** 2) / (np.tan(0.18)) ** 2)
height = (20 - z)
height[height < 0] = 0
height[height > 18] = 18

m = np.zeros_like(height)
m[10:-10, 10:-10] = 1
M = diags(m.flatten())

h, w = height.shape

azel = np.array([45, 30])
α, β, γ = sun_direction_from_position(azel)

#Bx, By = gradient_stencil_shift(w, h)
Bx, By = gradient_stencil_shift(w, h)
p = Bx @ height.flatten()
q = By @ height.flatten()

I = Reflectance(p, q, azel).reshape([h - 1, w - 1]) #+ σ * np.random.normal(size=(h - 1, w - 1))

  
# %% reconstruction cône

h, w = height.shape
azel = np.array([45, 30])
α, β, γ = sun_direction_from_position(azel)
p = (Bx @ height.flatten())#.reshape([h - 1, w - 1])
q = (By @ height.flatten())#.reshape([h - 1, w - 1])
z = 1 * height.flatten()
κ = 2
ε = 1
m = np.zeros((h, w))
m[2:-2, 2:-2] = 1
m1 = np.zeros((h - 1, w - 1))
m1[1:-1, 1:-1] = 1

λ = 0.1
μ = 0.1
λ1 = λ / (ε ** 2)
λ2 = κ * λ1 + μ
k = 0
Global_Energies = []
Global_P = []
Global_Q = []
Global_Z = []
#E = energy_51_2d(I, p, q, z, μ, azel)
#energy_56(I, p, q, z, λ, μ, azel)
while (k < 100):
    k += 1
    #p, q, z = iteration_pq_56_2d(I, p, q, z, azel, μ, ε, κ)
    p, q, z = iteration_pq_56(p, q, z, azel, h, w, λ1, λ2, κ)
    energy_56_1d(I, p, q, z, h, w, azel)
    #if not (k % 10):
    # print(f'iter: {k} \t energy: {E} \t '
    #       f'new energy: {energy_56(I, p, q, z, λ, μ, azel)} \t'
    #       f'diff: {E - energy_56(I, p, q, z, λ, μ, azel)}')
        #E = energy_56(I, p, q, z, λ, μ, azel)
        #E = energy_51_2d(I, p, q, z, μ, azel)
        
    # z = z  * m
    # p = p * m1
    # q = q * m1
        




# %% reconstruction

p = Bx @ height.flatten()
q = By @ height.flatten()
z = (height + 0.1 * np.random.normal(size=(h, w))).flatten()
κ = 2
ε = 1

m1 = (abs(Bx) @ m.flatten()).reshape([h - 1, w - 1]) > 1

iterations = [100, 400, 800, 160, 320, 640, 1280, 2300, 3320, 4350,
              5380, 6660, 8700, 10760]
lambdas = [1.0, 0.5, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.001, 0.0005,
           0.0003, 0.0002, 0.0001, 0.0]
mus = [0.1, 0.1, 0.1, 0.1, 0.1, 0.08, 0.05, 0.03, 0.02, 0.01, 0.008,
       0.0007, 0.0005, 0.0002, 0.0001]

k = 0
E = energy_56_1d(I, p, q, z, h, w, azel)
for i in range(0, 1):
    λ = lambdas[i]
    μ = mus[i]
    μ = 0.1
    λ1 = λ / (ε ** 2)
    λ2 = κ * λ1 + μ
    print('λ: ' + str(λ) + '\t μ: ' + str(μ))

    while k < 100:
        p, q, z = iteration_pq_56(p, q, z, azel, h, w, λ1, λ2)
        E = energy_56_1d(I, p, q, z, h, w, azel)
        k += 1
        
