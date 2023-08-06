# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Standard
import glob, math, os, sys
from copy import copy
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.append(os.path.dirname(SCRIPT_DIR))

import numpy as np
import numpy.matlib as matlib
np.set_printoptions(threshold=sys.maxsize)

from scipy import ndimage
from scipy.sparse import eye, kron, diags, vstack, spdiags
from scikits.umfpack import spsolve, splu

from skimage import data, transform, img_as_float, measure, filters
from skimage.transform import rescale
from skimage.filters import median
from skimage.morphology import disk

from scipy.interpolate import griddata

import pandas as pd
from pandas.plotting import register_matplotlib_converters

import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.io as pio
pio.renderers.default='browser'

from tqdm import tqdm_notebook as tqdm

from osgeo import gdal
#pyo.ini_notebook_mode()

# Third parties
import vpv
import iio

# Local modules
import image_processing_with_graphs as ipg
import sfs as sfs
    
        
# %% Test sur Newcastle_1 Planetscope

rootdir = ('/Users/mariedautume/Documents/work/kayrros/from_scratch/newcastle_12_june20_april21_psscene4band_analytic_sr_udm2/')
rootdir = ('/Users/mariedautume/Documents/work/kayrros/tas-de-charbon/outputs/newcastle_1/all_inputs/itsr_tscs/')
mfile  = rootdir + 'mask.png'
imdir = rootdir + '/new1/'
hdir = rootdir + '/heights_sfs_dirichlet_14_10_21/'
hdir = rootdir + 'spyder/heights_sfs_dirichlet_17_09_21/'
csv_file_mode = hdir + 'volume_mode.csv'
csv_file_classic = hdir + 'volume_classic.csv'
ground_truth_csv = ('/Users/mariedautume/Documents/work/kayrros/tas-de-charbon/'
                    'outputs/newcastle.csv')

# run sfs on all images
#sfs.sfs_optical_directory(imdir, mfile, hdir, specifier='.tif')

# compute volume on all images
sfs.volume_csv(hdir, mfile, csv_file_mode, specifier='.tif', method='mode')
#volume_csv(hdir, mfile, csv_file_classic, specifier='*.tif', method='classic')
sfs.plot_vs_ground_truth(ground_truth_csv, sfs_csv_list=[csv_file_mode, csv_file_classic])



# %% Test sur Newcastle_1 SAR
rootdir = ('/Users/mariedautume/Documents/work/kayrros/tas-de-charbon/'
           'denoised_sar_thibaud/aoi1/')
mfile  = rootdir + 'mask_full.png'
mdir = rootdir + '/mask_handmade/'
cdir = rootdir + '/crane_mask/'
imdir = rootdir + '/denoised_inputs/'
edir = rootdir + '/spyder/edges/'
edir = '/tmp/edges_mask_2/'
hdir = rootdir + '/spyder/heights_sfs_sar_mask_hand_17_09_21/'
sdir = rootdir + '/spyder/stockpiles_mask/'
vdir = rootdir + '/spyder/stockpiles_visualisation/'

sfs.bright_edge_mask_sar_directory(imdir, mdir, edir, specifier='.tif',
                                    threshold=0.42, erosion_factor=(1,1),
                                    dilation_factor=(4,4), 
                                    min_component_size=150)

# sfs.sfs_sar_directory(imdir, mdir, hdir, edir,
#                       specifier='.tif', incidence=27.5,
#                       pixel_spacing=np.array([0.70, 0.31]))

# sfs.surface_mask_from_sfs_sar_directory(hdir, mdir, sdir, specifier='.tif',
#                                     threshold=10, large_piles_height_min=20,
#                                     small_piles_size_minmax=np.array([150, 3000]))

# sfs.surface_visualisation_sar_directory(imdir, sdir, vdir)



# hdir= rootdir + '/spyder/heights_sfs_sar_mask_auto_17_09_21/'

# sfs.crane_mask_sar_directory(imdir, mfile, cdir, specifier='.tif', threshold=0.6, 
#                          dilation_factor=(4,4), size_threshold=1000, 
#                          final_dilation_factor=(10,10))
# sfs.bright_edge_mask_sar_directory(imdir, mdir, edir, specifier='.tif',
#                                    threshold=0.6, erosion_factor=(1,1),
#                                    dilation_factor=(4,4), 
#                                    min_component_size=150)
# sfs.sfs_sar_directory(imdir, mdir, hdir, edir,
#                       specifier='.tif', incidence=27.5,
#                       pixel_spacing=np.array([0.70, 0.31]))




# %%
# os.chdir(imdir)
# images = sorted(glob.glob('*.tif'))
# for k in range(9, 10):
#     im = iio.read(images[k])[:,:,0]
#     mfile = mdir + images[k]
#     m = iio.read(mfile)[:,:,0] > 0
#     edge = bright_edge_mask_sar(im, m)
#     print(np.mean(im[m]))

u = sfs.sfs_dirichlet(z*0 + 0.8, d, m, 0.1, azel)

# %% Misc
import json

def add_json_metadata_to_geotiff_gdal(imfile, jsonfile):
    f = open(jsonfile)
    json_metadata = json.load(f)['properties']
    im_data = gdal.Open(imfile)
    im_metadata = im_data.GetMetadata()
    im_metadata.update(json_metadata)
    im_data.SetMetadata(im_metadata)
    return



# %%

d = sfs.sun_direction_image(h, w, azel)
u = sfs.sfs_dirichlet(z*0 + 0.9, d, m, 0.1, azel)
sarfile = '/Users/mariedautume/Documents/work/kayrros/tas-de-charbon/denoised_sar_thibaud/aoi1/denoised_inputs/2019-06-08_CSKS1_SCS_B_S2_05_HH_RD_SF_20190608070334_20190608070341.tif'
msarfile = '/Users/mariedautume/Documents/work/kayrros/tas-de-charbon/denoised_sar_thibaud/aoi1/mask_handmade/2019-06-08_CSKS1_SCS_B_S2_05_HH_RD_SF_20190608070334_20190608070341.tif'
sar = iio.read(sarfile)
msar = iio.read(msarfile)[:,:,0] > 0

BB = 0.01
I00 = 0.1
sarsar = sar - BB



