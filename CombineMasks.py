#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: jonathanfung
"""
#Combine multiple masks from different channesl
from PIL import Image
import numpy as np
from scipy.ndimage import label

#Function to process and label each mask
def label_mask(file_name):
    mask_image = Image.open(file_name)
    mask_array = np.array(mask_image)
    
    #Convert to binary mask (Non-zero values are cells)
    #Each pixel, check if >0, if so,then mark as 1, otherwise 0
    binary_mask = np.where(mask_array > 0, 1, 0) 
    
    #Label the cells by finding connected pixels
    #label() considers the 8 pixels connected in square pattern
    #Assigns a unique label to each connected component in binary mask
    #Background is 0, each distinct object unique integer starting from 1 
    labelled_mask, _ = label(binary_mask)
    
    return labelled_mask

#Intialise
combined_mask = np.zeros_like(labelled_mask)
next_label = 1

#Process each mask file
for i in range(1, 4):
    file_name = f"{i}.png" #Change accordingly
    labelled_mask = label_mask(file_name)
 
    #Add the labelled mask to the combined mask with offset to ensure unique labels
    #After processsing each mask, next_label is incremented by max label value in current mask
    combined_mask[labelled_mask > 0] = labelled_mask[labelled_mask > 0] + next_label
    next_label += labelled_mask.max()

#Save the combined mask to a new file
combined_mask_image = Image.fromarray(combined_mask)
combined_mask_image.save('combined_mask.png')
