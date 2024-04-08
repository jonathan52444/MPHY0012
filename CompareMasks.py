#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 00:03:31 2024

@author: jonathanfung
"""


#Compares Masks 
import numpy as np
from skimage.io import imread
from skimage.measure import label, regionprops

#Read the manual segmented image and the output from Ilastik's Object Classification workflow
manual = imread("") #Manual Segmentation Path
ilastik = imread("") #Ilastik Segmentation Path

#Create function which calculates IoU between the two masks
def calculate_iou(mask1, mask2):
    intersection = np.logical_and(mask1, mask2)
    union = np.logical_or(mask1, mask2)
    return np.sum(intersection) / np.sum(union)

#Create function which checks if the boxes overlap
#If any of the statements are true, the boxes do not overlap 
#If operand is false, the function returns true 
#bbox is from regionprops- 'bbox': Bounding box (min_row, min_col, max_row, max_col)
def check_overlap(bbox1, bbox2):
    return not (bbox1[2] < bbox2[0] or bbox1[0] > bbox2[2] or bbox1[3] < bbox2[1] or bbox1[1] > bbox2[3])

#Label the images (From skimage.measure module, label function)
manual = label(manual)
ilastik = label(ilastik)

#Regionprops module function is used to measure properties of labelled image regions
#When calling regionprops, it returns a list of 'RegionProperties' objects
#Regionprops gives properties such as bbox, area, and perimeter 
manual_props = regionprops(manual)
ilastik_props = regionprops(ilastik)

#Initialise TP,FN,FN values to 0
TP = 0
FP = 0
FN = 0

#Print out actual number of cells from the manual segmentation
print(len(manual_props)) 

#Compare cells
#Count TP and FN by iterating over each region in manual segmentation ('manual_props') and check how well it matches regions in Ilastik segmentation('ilastik_props')
#check_overlap function returns 'True' if there's an overlap, and false otherwise 
#This avoids unnecessary computations- If no overlap, IoU would be zero and no point computing
for m_prop in manual_props:
    ious = []
    for i_prop in ilastik_props:
        if check_overlap(m_prop.bbox, i_prop.bbox):
            mask1 = manual == m_prop.label
            mask2 = ilastik == i_prop.label
            iou = calculate_iou(mask1, mask2)
            ious.append(iou)
    if ious and np.max(ious) > 0.5:
        TP += 1
    else:
        FN += 1

#Iterate over each region in the Ilastik segmetnation
#Initialise an empty list'ious' to store IoU values
#Iterate over each region in manual segmentation and check if bounding boxes overlap
#If overlap, calcualte IoU between the regions and append resulting value to ious
#Iterate over all regions in manual segmentation, and if ious is empty/ max value is <=0.5, no region in manual segmentation significantly overalsp, so increment FP
 
for i_prop in ilastik_props:
    ious = []
    for m_prop in manual_props:
        if check_overlap(m_prop.bbox, i_prop.bbox):
            mask1 = manual == m_prop.label
            mask2 = ilastik == i_prop.label
            iou = calculate_iou(mask1, mask2)
            ious.append(iou)
    if not ious or np.max(ious) <= 0.5:
        FP += 1

#Print out values
print(f"TP:{TP} FP:{FP} FN:{FN}" )
