# MPHY0012: Research Project in Medical Physics and Biomedical Engineering 

## Overview
Cellular heterogeneity in cancer poses significant challenges in treatment due to the development of resistant subpopulations. Live-cell imaging has emerged as a powerful tool for capturing longitudinal data on cancer cell dynamics, enabling the reconstruction of lineage trees to study non-genetic factors that contribute to this heterogeneity. Combined with mathematical modelling, it provides a powerful approach to discovering mechanisms of variability in the proliferation and therapy response of cells. To capture this variability, it is necessary to process a large number of cells over many generations accurately. However, manual analysis of live-cell images is both time-consuming and prone to error, necessitating the use of automated computational tools.'

In this project, we developed a robust automated image analysis pipeline that transforms series of live-cell images into lineage trees suitable for quantitative analysis.

The protocol for this pipeline is included in this repository, alongside some useful supplementary code.

## Files

- `CombineMasks.py`: Combines segmentation masks from multiple channels
- `CompareMasks.py`: Compares ground truth mask against an algorithm's segmented mask
- `Crop.py`: Crops input images to a smaller field of view
- `ReadMastodonFiles.py`: Extracts lineage trees from Mastodon
- 'CellPopulation.py`: Takes extracted information from lineage trees, plot cell population over time
- 'CellNuclearArea.py`: Takes extracted information from lineage trees, plot cell nuclear area over time


