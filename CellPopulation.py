#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""


@author: jonathanfung
"""

import matplotlib.pyplot as plt
import numpy as np


#Get the minimum and maximum frame numbers
min_frame = np.min(lineagedata[:, 1])
max_frame = np.max(lineagedata[:, 2])

#Initialise an array to store the number of cells for each frame
num_cells_per_frame = np.zeros(max_frame - min_frame + 1)

#Iterate over each frame
for frame in range(min_frame, max_frame + 1):
    #Find the cells present in the current frame
    cells_in_frame = [i for i in range(len(lineagedata)) if lineagedata[i, 1] <= frame <= lineagedata[i, 2]]
    
    #Count the number of cells in the current frame
    num_cells_per_frame[frame - min_frame] = len(cells_in_frame)
    
#Create a new figure and axis
fig, ax = plt.subplots(figsize=(8, 6))

#Plot the number of cells per frame
frames = np.arange(min_frame, max_frame + 1)
ax.plot(frames, num_cells_per_frame, marker='o', linestyle='-', color='b')

#Set labels and title
ax.set_xlabel('Frame Number')
ax.set_ylabel('Number of Cells')
ax.set_title('Number of Cells per Frame')

#Display the plot
plt.tight_layout()
plt.show()



