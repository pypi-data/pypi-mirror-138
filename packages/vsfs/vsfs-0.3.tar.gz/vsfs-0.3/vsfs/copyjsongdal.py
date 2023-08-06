#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 12:09:46 2021

@author: mariedautume
"""

import sys
from osgeo import gdal
import json

if len(sys.argv) < 3:
    print("Usage: copyjsongdal.py json_file geotiff_file")
    sys.exit(1)
    
input = sys.argv[1]
f = open(input)
try:
    json_data = json.load(f)
except:
    print('Unable to open {input} for reading.')
    
json_metadata = json_data['properties']
if json_metadata is None:
    print('No properties metadata found on file {input}.')
    sys.exit(1)

output = sys.argv[2]
im_data = gdal.Open(output)
if im_data is None:
    print('Unable to open {output} for reading.')
    sys.exit(1)
    
im_metadata = im_data.GetMetadata()
im_metadata.update(json_metadata)
im_data.SetMetadata(im_metadata)
    


        