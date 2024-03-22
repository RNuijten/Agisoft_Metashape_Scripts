##### Generate various raster exports from Agisoft for Micasense data (Rededge-MX Dual Sensor) #####

## Set up ##
import Metashape
doc = Metashape.app.document
chunk = doc.chunk
path = Metashape.app.getString(label='Enter output directory ending with //', value='Path here') # Pop up window for user input
name = Metashape.app.getString(label='Enter project name (for example, data acquisition date)', value='Path here') # Pop up window for user input 
compression = Metashape.ImageCompression()
compression.tiff_big = True
compression.tiff_compression = Metashape.ImageCompression.TiffCompressionLZW

## Export Red-Green-Blue orthomosaic (8bit data?) ##
chunk.raster_transform.formula=["B5/10000","B4/10000","B2/10000"]
chunk.raster_transform.false_color = [0, 1, 2] #this defines R-G-B channels order in the output
chunk.exportRaster(path = path + "Micasense_RGB_" + name + ".tif", 
                   source_data=Metashape.OrthomosaicData,
                   image_format = Metashape.ImageFormatTIFF, 
                   raster_transform=Metashape.RasterTransformPalette,
                   image_compression=compression,
                   save_alpha=True)
chunk.raster_transform.reset() # Reset transformation


## Export NIR-Red-Green false color false-color orthomaic (8bit data?) ##
chunk.raster_transform.formula=["B10/10000","B5/10000","B4/10000"]
chunk.raster_transform.false_color = [0, 1, 2] #this defines R-G-B channels order in the output
chunk.exportRaster(path + "Micasense_NirRG_" + name + ".tif",
                   source_data=Metashape.OrthomosaicData,
                   image_format = Metashape.ImageFormatTIFF, 
                   raster_transform=Metashape.RasterTransformPalette,
                   image_compression=compression,
                   save_alpha=True)
chunk.raster_transform.reset() # Reset transformation

## Export 10-band reflectance (12bit data?) ##
chunk.raster_transform.formula=["B1/32768","B2/32768","B3/32768","B4/32768","B5/32768","B6/32768","B7/32768","B8/32768","B9/32768","B10/32768"]
chunk.raster_transform.calibrateRange()
chunk.raster_transform.enabled = True
chunk.exportRaster(path=path + "Micasense_Reflectance_" + name + ".tif", 
                   source_data=Metashape.OrthomosaicData,
                   image_format = Metashape.ImageFormatTIFF,
                   raster_transform = Metashape.RasterTransformValue,
                   image_compression=compression,
                   save_alpha=False)
chunk.raster_transform.reset() # Reset transformation

## Export Spectral Vegetation Indices ##
# 1. NDVI (float, values between 0-1)
chunk.raster_transform.formula=["((B10 / 32768) + (B5 / 32768)) / ((B10 / 32768) - (B5 / 32768))"]
chunk.raster_transform.calibrateRange()
chunk.raster_transform.enabled = True
saveOrtho = "D:/ortho.tif"
chunk.exportRaster(path=path + "Micasense_NDVI_" + name + ".tif",
                   source_data=Metashape.OrthomosaicData,
                   image_format = Metashape.ImageFormatTIFF, 
                   raster_transform = Metashape.RasterTransformValue,
                   image_compression=compression,
                   save_alpha=False)
chunk.raster_transform.reset() # Reset transformation

# 2. NDRE (float, values between 0-1)
chunk.raster_transform.formula=["((B10 / 32768) + (B8 / 32768)) / ((B10 / 32768) - (B8 / 32768))"]
chunk.raster_transform.calibrateRange()
chunk.raster_transform.enabled = True
saveOrtho = "D:/ortho.tif"
chunk.exportRaster(path=path + "Micasense_NDRE_" + name + ".tif",
                   source_data=Metashape.OrthomosaicData,
                   image_format = Metashape.ImageFormatTIFF, 
                   raster_transform = Metashape.RasterTransformValue,
                   image_compression=compression,
                   save_alpha=False)
chunk.raster_transform.reset() # Reset transformation

# 3. PSRI (float, values between 0-1)
chunk.raster_transform.formula=["((B5 / 32768) - (B4 / 32768)) / (B10 / 32768)"]
chunk.raster_transform.calibrateRange()
chunk.raster_transform.enabled = True
saveOrtho = "D:/ortho.tif"
chunk.exportRaster(path=path + "Micasense_PSRI_" + name + ".tif",
                   source_data=Metashape.OrthomosaicData,
                   image_format = Metashape.ImageFormatTIFF, 
                   raster_transform = Metashape.RasterTransformValue,
                   image_compression=compression,
                   save_alpha=False)
chunk.raster_transform.reset() # Reset transformation

# # 4. NIRv (float, values between 0-1)
# chunk.raster_transform.formula=["((B10+B5)/(B10-B5))*B10"]
# etc. 