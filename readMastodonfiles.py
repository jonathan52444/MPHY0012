#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Peter Embacher
"""

import time                                             # for timer
import numpy as np
import pandas as pd

def readMastodonfiles() :
    # read MastodonTable_Spot.csv files to extract lineagedata
    
    # set auxiliary parameters:
    t1 = time.time()                                    # for timer
    filepath = '/Users/jonathanfung/Desktop/MastodonOutputs/'  # path of input file
    filename_spots = 'MastodonTable-Spot.csv'           # name of input file with spots-information
    filename_links = 'MastodonTable-Link.csv'           # name of input file with links-information
    feature_header = 'Spot radius'                      # header of feature of interest
    without = int(1)                                    # larger means more output
    
    # read data from spots-file:
    fullfilename_spots = filepath + filename_spots
    if( without>=1 ) :
        print( " Info - readMastodonfiles: Read spots-file %s." %(fullfilename_spots) )
    data = pd.read_csv( fullfilename_spots, low_memory=False )          # input file
    label_ind = np.array(data['Label']); label_ind = label_ind[2:-1]    # column with cell-specific labels
    frame_ind = np.array(data['Spot frame']); frame_ind = frame_ind[2:-1];          frame_ind = np.array([int(j) for j in frame_ind])   # column with frame-number
    track_ind = np.array(data['Spot track ID']); track_ind = track_ind[2:-1];       track_ind = np.array([int(j) for j in track_ind])# column with track/lineage-specific name
    feature_ind = np.array(data[feature_header]); feature_ind = feature_ind[2:-1];  feature_ind = np.array([float(j) for j in feature_ind])# column with track/lineage-specific name
    print(feature_ind)
    allcelllabels = uniquelabels(label_ind)             # list of all cells
    nocells = len(allcelllabels)
    alltracks = np.unique(track_ind)                    # list of all cells
    notracks = len(alltracks)
    badtracks = np.zeros(0,dtype=int)                   # list of ids of tracks that failed sanity checks
    if( without>=1 ) :
        print( " Info - readMastodonfiles: Got %d cells, %d tracks." %(nocells,notracks) )
    # ...output cellid-celllabel correspondence:
    if( without>=2 ) :
        print( " Info - readMastodonfiles: cellid-vs-celllabel correspondence:" )
        for j_cell in range(0,nocells) :
            print( " cellid %4d, celllabel %10s" %(j_cell+1,allcelllabels[j_cell]) )
    
    # read data from links-file:
    fullfilename_links = filepath + filename_links
    if( without>=1 ) :
        print( " Info - readMastodonfiles: Read links-file %s." %(fullfilename_links) )
    data = pd.read_csv( fullfilename_links, low_memory=False )          # input file
    label_lnk = np.array(data['Label']); label_lnk = label_lnk[2:-1]
    cellidlnk = np.zeros((2,0),dtype=int); addcellidlnk = np.zeros((2,1),dtype=int)
    delimiter = ' ' + chr(8594) + ' '
    if( without>=2 ) :
        print( " Info - readMastodonfiles: Detected links:" )
    for j_lnk in range(0,len(label_lnk)) :
        endofmother = label_lnk[j_lnk].find(delimiter)
        mother = label_lnk[j_lnk][0:endofmother]        # mother label
        daughter = label_lnk[j_lnk][(endofmother+len(delimiter)):len(label_lnk[j_lnk])] # daughter label
        motherid = np.array(range(0,nocells))[allcelllabels==mother] + 1    # cellid of mother
        daughterid = np.array(range(0,nocells))[allcelllabels==daughter] + 1# cellid of daughter
        addcellidlnk[0] = motherid; addcellidlnk[1] = daughterid
        if( motherid!=daughterid ) :
            isalreadypartof = np.any( np.all( cellidlnk==addcellidlnk, axis=0 ) )   # 'true', if this division occurred previously already
            if( ~isalreadypartof ) :
                cellidlnk = np.concatenate( (cellidlnk,addcellidlnk), axis=1 )
                if( without>=2 ) :
                    print( " %4d:  %10s --> %10s      (%4d --> %4d)" %(j_lnk+4, mother,daughter, motherid,daughterid) )
            else :
                select = (label_ind==mother); track_here = np.unique(track_ind[select]) # should be only a single track (and same for the daughters)
                if( len(track_here)!=1 ) :
                    print( " Warning - readMastodonfiles: trackid for %10s not unique: %s" %(mother, ''.join(["%4d " %(j) for j in track_here])) )
                badtracks = np.concatenate( (badtracks,track_here), axis=0 )
                print( " Warning - readMastodonfiles: Already knew %10s --> %10s before (links-row %4d, trackid %4d)" %(mother,daughter, j_lnk+4,track_here[0]) )
    # ...sanity-check, if always two daughters per division:
    allmothers = np.unique(cellidlnk[0,:])
    for j_mthr in allmothers :
        select = (cellidlnk[0,:]==j_mthr);  daughters_here = cellidlnk[1,select]
        if( len(daughters_here)!=2 ) :
            select = (label_ind==allcelllabels[j_mthr-1]); track_here = np.unique(track_ind[select]) # should be only a single track (and same for the daughters)
            if( len(track_here)!=1 ) :
                print( " Warning - readMastodonfiles: trackid for %10s not unique: %s" %(allcelllabels[j_mthr-1], ''.join(["%4d " %(j) for j in track_here])) )
            badtracks = np.concatenate( (badtracks,track_here), axis=0 )
            print( " Warning - readMastodonfiles: %10s has daughters [ %s] (trackid %d)" %(allcelllabels[j_mthr-1], ''.join(["%10s " %(allcelllabels[j-1]) for j in daughters_here]), track_here[0]) )
    
    # output ids of bad tracks:
    if( without>=1 ) :
        print( " Info - readMastodonfiles: Ignore bad tracks: [ %s]" %(''.join(["%4d " %(j) for j in np.unique(badtracks)])) )
        print( " Info - readMastodonfiles: Still good tracks: [ %s]" %(''.join(["%4d " %(j) for j in np.setdiff1d(alltracks,badtracks)])) )
    
    # create lineagedata:
    lineagedata = np.zeros((nocells,4), dtype=int)      # each cell a row; first column is cell-id, second column is first frame, cell is observed, third column is last frame, cell is observed, fourth column is mother's cell-id or zero, if unknown mother
    for j_cell in range(0,nocells) :                    # go through cells
        select = (label_ind==allcelllabels[j_cell])     # 'true' when row has current cell
        track_here = np.unique(track_ind[select])       # should be only a single track
        if( (len(track_here)!=1) | np.any(badtracks==track_here[0]) ) :
            print( " Warning - readMastodonfiles: Don't use cellid %10s, as part of a bad track." %(allcelllabels[j_cell]) )
        else :
            firstframe = np.min( frame_ind[select] )
            lastframe = np.max( frame_ind[select] )
            mother = cellidlnk[0,cellidlnk[1,:]==(j_cell+1)]
            lineagedata[j_cell,0] = j_cell + 1          # indexing starts at zero
            lineagedata[j_cell,1] = firstframe
            lineagedata[j_cell,2] = lastframe
            if( len(mother)==0 ) :
                lineagedata[j_cell,3] = 0               # indicates no mother
                if( without>=2 ) :
                    print( " Info - readMastodonfiles: cell %10s (%4d), frames %4d .. %4d, mother %10s" %(allcelllabels[j_cell],j_cell+1,firstframe,lastframe,"-unknown-") )
            elif( len(mother)==1 ) :
                lineagedata[j_cell,3] = mother[0]       # corresponding motherid
                if( without>=2 ) :
                    print( " Info - readMastodonfiles: cell %10s (%4d), frames %4d .. %4d, mother %10s (%4d)" %(allcelllabels[j_cell],j_cell+1,firstframe,lastframe,allcelllabels[mother[0]-1],mother[0]) )
            else :                                      # should not happen after removal of badtracks
                print( " Warning - readMastodonfiles: Multiple mothers for cell %4d." %(j_cell+1) )
    select = (lineagedata[:,0]>0)
    lineagedata = lineagedata[select,:]                 # throw out cells of bad tracks
    
    # create feature output:
    norelcells = np.shape(lineagedata)[0]               # number of relevant/non-discarded cells
    cellwisefeatureevol = np.array([np.zeros(1+lineagedata[j,2]-lineagedata[j,1]) for j in range(0,norelcells)], dtype=object)
    if( without>=2 ) :
        print( " Info - readMastodonfiles: feature %s:" %(feature_header) )
    for j_cell in range(0,norelcells) :
        select = (label_ind==allcelllabels[lineagedata[j_cell,0]-1])    # 'true' when row has current cell
        if( len(cellwisefeatureevol[j_cell])!=(1+lineagedata[j_cell,2]-lineagedata[j_cell,1]) ) :
            print( " Warning - readMAstodonfiles: Wrong number of features %4d vs %4d." %(len(cellwisefeatureevol[j_cell]),1+lineagedata[j_cell,2]-lineagedata[j_cell,1]) )
        else :
            cellwisefeatureevol[j_cell] = feature_ind[select]
            if( without>=2 ) :
                print( " Info - readMastodonfiles: %10s features: [ %s]." %(allcelllabels[lineagedata[j_cell,0]-1],''.join(["%+1.2e " %(j) for j in cellwisefeatureevol[j_cell]])) )
    
    print( " Info - readMastodonfiles: Done now after %1.3f sec." %(time.time()-t1) )
    return lineagedata, cellwisefeatureevol
    
def uniquelabels( label_ind ) :
    # outputs np.array of unique labels
    
    nolabels = len(label_ind)
    select = (np.zeros(nolabels)==1)
    for j_ind in range(0,nolabels) :
        if( ~np.any(label_ind[select]==label_ind[j_ind]) ) :
            select[j_ind] = True
    return label_ind[select]

if( __name__ == "__main__" ) :
    readMastodonfiles()
    