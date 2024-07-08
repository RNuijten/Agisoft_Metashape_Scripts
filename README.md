# Agisoft Metashape Scripts

## Author
Rik Nuijten

## Overview
This repository includes scripts designed to be run in Agisoft Metashape for processing and analyzing image datasets.

## Scripts:
### 1. Full Processing Pipeline
This script executes the complete processing pipeline in Agisoft Metashape, from Image Alignment to the generation of Point Clouds and Orthomosaics. Key features include:
* Tie Point Filtering & Camera Optimization: Utilizes gradual selection to filter tie points using recommended parameters from a USGS best practices guide.
* Sensor/Use-Case pecific Parameters: Configured for datasets from the Zenmuse P1 sensor and optimized for high-resolution applications such as flowering plants, using higher settings than standard use cases.

### 2. Export Reflectance Data and Spectral Indices
This script exports various data products from Agisoft Metashape using the Micasense RedEdge-MX Dual Camera, including:
* Reflectance Data: Provides calibrated spectral data.
* Spectral Vegetation Indices: Calculates indices such as NDVI for vegetation analysis.
* (False) Color Composites: Generates color composite images for visual analysis.

### 3. Select and Copy Subsets of Photos
Using this script subsets of photos (i.e., very i-th photo) can be selected and copy-pasted to a new directory. This helps creating a smaller image dataset, where images have less overlap, which is more conventient for image inspections in GIS software (e.g., QGIS, ArcGIS, Project Kiwi, DroneDB)