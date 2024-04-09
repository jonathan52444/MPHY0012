#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 19:28:29 2024

@author: jonathanfung
"""

import matplotlib.pyplot as plt
import numpy as np


#Get the maximum number of frames a cell is observed
max_frames = max(lineagedata[:, 2] - lineagedata[:, 1]) + 1

#Initialise an array to store the sum of nuclear areas for each frame
sum_nuclear_areas = np.zeros(max_frames)

#Initialise an array to store the count of cells for each frame
cell_counts = np.zeros(max_frames)

# Iterate over each cell
for i in range(len(lineagedata)):
    birth_frame = lineagedata[i, 1]
    death_frame = lineagedata[i, 2]
    
    #Normalize the frame numbers relative to the cell's birth frame
    normalised_frames = np.arange(death_frame - birth_frame + 1)
    
    #Extract the nuclear areas for the current cell
    nuclear_areas = cellwisefeatureevol[i]
    
    #Accumulate the nuclear areas and cell counts for each normalised frame
    sum_nuclear_areas[normalised_frames] += nuclear_areas
    cell_counts[normalised_frames] += 1
    
#Calculate the average nuclear area for each normalised frame
avg_nuclear_areas = sum_nuclear_areas / cell_counts

#Create a new figure and axis
fig, ax = plt.subplots(figsize=(8, 6))

#Plot the average nuclear area
normalised_frames = np.arange(max_frames)
ax.plot(normalised_frames, avg_nuclear_areas, marker='o', linestyle='-', color='b')

#Set labels and title
ax.set_xlabel('Normalised Frame Number (Frame 0 = Cell Birth)')
ax.set_ylabel('Average Nuclear Area')
ax.set_title('Average Nuclear Area Across Normalised Frames')

#Display the plot
plt.tight_layout()
plt.show()