#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: jonathanfung
"""
#Crops images into smaller field of view 

from PIL import Image
import os
import math

source_dir = ""
target_dir = ""


if not os.path.exists(target_dir):
    os.makedirs(target_dir)

#Loop over the images
for i in range(1, 41):
    # Open image
    img = Image.open(os.path.join(source_dir, f"{i}.tif"))
    
    # Get dimensions
    width, height = img.size

    # Calculate new dimensions
    new_width = int(width * math.sqrt(1 / 8))
    new_height = int(height * math.sqrt(1 / 8))

    # Calculate position to crop
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2

    # Crop the center of the image
    img_cropped = img.crop((left, top, right, bottom))

    # Save the cropped image
    img_cropped.save(os.path.join(target_dir, f"{i}.tif"))
