import os
import numpy as np
import iio
import math
import glob
from osgeo import gdal

def find_mode(im,m,width=2):
    m = m > 0
    counts,bins = np.histogram(im[m],bins=200)
    vals = (bins[:-1]+bins[1:])/2 # Average value of bin
    where = np.logical_and.reduce([counts >= np.roll(counts,w) for w in range(-width,width+1)])
    where = np.logical_and(where,counts>=np.max(counts))
    return float(vals[where][0])

def volume(im_orig, mask):
    im = 1.0*im_orig*mask
    xmin = np.percentile(im[mask > 0].flatten(), 5)
    xmax = np.percentile(im[mask > 0].flatten(), 95)
    med = np.percentile(im[mask > 0].flatten(), 50)
    im[im < xmin] = xmin
    im[im > xmax] = xmax
    return np.sum(im[mask>0].flatten())# - med * np.sum(mask.flatten()>0)

def volume_mode(im_orig, mask):
    im = 1.0*im_orig*mask
    mode = find_mode(im,mask)
    im[im < mode] = mode
    xmax = np.percentile(im[mask > 0].flatten(), 95)
    xmin = np.percentile(im[im > mode].flatten(), 20)
    im[im > xmax] = xmax
    im[im < xmin] = mode
    im = 18*(im - mode)/(xmax - mode)
   # return np.sum(im[mask>0].flatten()) - mode * np.sum(mask.flatten()>0)
    return np.sum(im[mask>0].flatten())

def volume_zero(im_orig, mask):
    im = 1.0*im_orig*mask
    xmin = np.percentile(im[mask > 0].flatten(), 5)
    xmax = np.percentile(im[mask > 0].flatten(), 98)
    med = np.percentile(im[mask > 0].flatten(), 50)
    im[im < 0 ] = 0
    im[im > xmax] = xmax
    return np.sum(im[mask>0].flatten()) 

def get_el(i):
    ds = gdal.Open(i)
    meta = ds.GetMetadata()
    keys = list(k.lower() for k in meta)
    combined = '\t'.join(keys)

    if (('SUN_EL').lower() not in combined):
        sys.exit("elevation not found in metadata. "
             "Provide sun informations and try again.")


    el = [value for key, value in meta.items() if 'SUN_EL' in key.upper()]
    return el[0]

def get_az(i):
    ds = gdal.Open(i)
    meta = ds.GetMetadata()
    keys = list(k.lower() for k in meta)
    combined = '\t'.join(keys)

    if (('SUN_AZ').lower() not in combined):
        sys.exit("elevation not found in metadata. "
             "Provide sun informations and try again.")


    az = [value for key, value in meta.items() if 'SUN_AZ' in key.upper()]
    return az[0]

def main_vol(hdir, images_dir, m, outfile):
    mask = iio.read(m)
    if (len(mask.shape) == 3):
        mask = mask[:,:,0]
    mask = (mask > 0.5).astype(float)

    os.chdir(hdir)
    cdir = os.getcwd()
    images = glob.glob('*.tif')

    vf = open(outfile,"w")
    vf.write('date' + ',' + 'time' + ',' + 'volume' + ',' + 'elevation' + ',' + 'azimuth' + '\n')
#    vf.write('azimuth' + ',' + 'elevation' + ',' + 'volume' + '\n')
    for k in range(0, len(images)):
        i = images[k]
        im = iio.read(i)
        input_image = images_dir + '/' + i
        el = float(get_el(input_image))
        az = float(get_az(input_image))
        im = im[:,:,0]
        vf.write(i[6:8] + '/' + i[4:6] + '/' + i[0:4] + ',' + i[9:11] + ':' + i[11:13] + ':' + i[13:15] + ',' + str(volume_mode(im, mask)) + ',' + str(el) + ',' + str(az) +  '\n')
#        vf.write( str(az) + ',' + str(el) + ',' +  str(volume(im, mask)) + '\n')
    vf.close()
    os.chdir(cdir)
   


def main_vol_mode(hdir, images_dir, m, outfile):
    mask = iio.read(m)
    if (len(mask.shape) == 3):
        mask = mask[:,:,0]
    mask = (mask > 0.5).astype(float)

    os.chdir(hdir)
    cdir = os.getcwd()
    images = glob.glob('*.tif')

    vf = open(outfile,"w")
    vf.write('date' + ',' + 'time' + ',' + 'volume' + ',' + 'elevation' + ',' + 'azimuth' + '\n')
#    vf.write('azimuth' + ',' + 'elevation' + ',' + 'volume' + '\n')
    for k in range(0, len(images)):
        i = images[k]
        im = iio.read(i)
        input_image = images_dir + '/' + i
        el = float(get_el(input_image))
        az = float(get_az(input_image))
        im = im[:,:,0]
        vf.write(i[6:8] + '/' + i[4:6] + '/' + i[0:4] + ',' + i[9:11] + ':' + i[11:13] + ':' + i[13:15] + ',' + str(volume_mode(im, mask)) + ',' + str(el) + ',' + str(az) +  '\n')
#        vf.write( str(az) + ',' + str(el) + ',' +  str(volume(im, mask)) + '\n')
    vf.close()
    os.chdir(cdir)
   


