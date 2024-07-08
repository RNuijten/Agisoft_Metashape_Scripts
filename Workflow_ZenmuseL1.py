# -------------------------------------------------------
# -------------------------------------------------------
# -------------------------------------------------------
import Metashape
import os, sys, time, csv
from datetime import datetime
# -------------------------------------------------------

### Checking Software Compatibility ###
compatible_major_version = "2.1"
found_major_version = ".".join(Metashape.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
    raise Exception("Incompatible Metashape version: {} != {}".format(found_major_version, compatible_major_version))
# -------------------------------------------------------

### Function to get user inputs ###
def get_user_inputs():
    # Default values...
    # Gradual Selection values are based on: https://pubs.usgs.gov/of/2021/1039/ofr20211039.pdf
    def_keypoint_limit = 80000
    def_tiepoint_limit = 20000
    def_downscale_1 = 1 # For alignment
    def_downscale_2 = 2 # For depth maps
    def_reperr = 0.3
    def_recunc = 11
    def_projacc = 6
    
    # Prompt user for default image count
    keypoint_limit = Metashape.app.getInt("Enter Keypoint Limit", def_keypoint_limit)
    # Prompt user for default image count
    tiepoint_limit = Metashape.app.getInt("Enter Tiepoint Limit", def_tiepoint_limit)
    # Prompt user for default downscale
    downscale_1 = Metashape.app.getInt("Enter downscale value for IMAGE ALIGNMENT (1=high acc)", def_downscale_1)
    # Prompt user for default downscale
    downscale_2 = Metashape.app.getInt("Enter downscale value for DEPTH MAPS (1=ultra high acc)", def_downscale_2)
    # Prompt user for default reprojection error
    reperr = Metashape.app.getFloat("Enter reprojection error threshold for tie point filtering", def_reperr)
    # Prompt user for default reconstruction uncertainty
    recunc = Metashape.app.getFloat("Enter reconstruction uncertainty threshold for tie point filtering", def_recunc)
    # Prompt user for default projection accuracy
    projacc = Metashape.app.getInt("Enter projection accuracy threshold for tie point filtering", def_projacc)
    
    # Return user inputs as a dictionary
    return {'keypoint_limit': keypoint_limit, 'tiepoint_limit': tiepoint_limit, 
            'downscale_1': downscale_1, 'downscale_2': downscale_2, 
            'reperr': reperr, 'recunc': recunc, 'projacc': projacc}

# Get (User) Inputs
user_inputs = get_user_inputs()
# -------------------------------------------------------


# Get Directory of Agisoft Metashape Project
document_path = os.path.dirname(Metashape.app.document.path)
# Get the Current Date and Time
start = datetime.now().strftime("%d-%m-%Y_%H-%Mh")  

# Create a Log File in the Projects' Directory
log_file = document_path + "/_log_" + start +".txt"
with open(log_file, mode='w') as file:
    file.write("New log file \n\n\n")   
# -------------------------------------------------------


### 1. Image Alignment ###
for chunk in Metashape.app.document.chunks:
    # Write Chunk Name, Start Time, and Aligment Parameters to File
    with open(log_file, mode='a') as file:
        file.write('Processing chunk:' + chunk.label + "\n")
        file.write('Alignment process started on:' + datetime.now().strftime("%d-%m-%Y_%H-%Mh"))  
        file.write('Keypoint limit:' + str(user_inputs['keypoint_limit']) + "\n")
        file.write('Tiepoint limit:' + str(user_inputs['tiepoint_limit']) + "\n") 
    
    # Alignment
    chunk.matchPhotos(keypoint_limit = user_inputs['keypoint_limit'], 
                      tiepoint_limit = user_inputs['tiepoint_limit'], 
                      downscale = user_inputs['downscale_1'], 
                      generic_preselection = False, reference_preselection = True)
    chunk.alignCameras()
    Metashape.app.document.save()
    
    # Write the Number of Tie Points to File
    with open(log_file, mode='a') as file:
        file.write("Number of tie points:" + str(len(chunk.tie_points.points)) + "\n")
        file.write("Processing done on:" + start + "\n")   

# BREAK IN FILE
with open(log_file, mode='a') as file:
        file.write("\n\n")
# -------------------------------------------------------


## 2. Tie Point Filtering (Gradual Selection) ###

for chunk in Metashape.app.document.chunks:

    # Write Chunk Name, Start Time, and Filter Parameters to File
    with open(log_file, mode='a') as file:
        file.write('Processing chunk:' + chunk.label + "\n")
        file.write('Filter process (using ReprojectionError) started on:' + datetime.now().strftime("%d-%m-%Y_%H-%Mh"))          
    
    # Filtering (gradual selection) using ReprojectionError
    f = Metashape.TiePoints.Filter()
    f.init(chunk, Metashape.TiePoints.Filter.ReprojectionError)
    f.removePoints(user_inputs['reperr'])
    Metashape.app.document.save()
    with open(log_file, mode='a') as file:
        file.write('Filtering threshold ReprojectionError:' + str(user_inputs['reperr']) + "\n") 
        file.write("Number of tie points after filtering with ReprojectionError:" + str(len(chunk.tie_points.points)) + "\n")

    # Filtering (gradual selection) using ReconstructionUncertainty
    f = Metashape.TiePoints.Filter()
    f.init(chunk, Metashape.TiePoints.Filter.ReconstructionUncertainty)
    f.removePoints(user_inputs['recunc'])
    Metashape.app.document.save()
    with open(log_file, mode='a') as file:
        file.write('Filtering threshold ReconstructionUncertainty:' + str(user_inputs['recunc']) + "\n")
        file.write("Number of tie points after filtering with ReconstructionUncertainty:" + str(len(chunk.tie_points.points)) + "\n")


    # Filtering (gradual selection) using ProjectionAccuracy
    f = Metashape.TiePoints.Filter()
    f.init(chunk, Metashape.TiePoints.Filter.ProjectionAccuracy)
    f.removePoints(user_inputs['projacc'])
    Metashape.app.document.save()
    with open(log_file, mode='a') as file:
        file.write('Filtering threshold ProjectionAccuracy:' + str(user_inputs['projacc']) + "\n")
        file.write("Number of tie points after filtering with ProjectionAccuracy:" + str(len(chunk.tie_points.points)) + "\n")

    # Optimization
    chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True, 
                          fit_b1=False, fit_b2=False, 
                          fit_k1=True, fit_k2=True, fit_k3=True, fit_k4=False, 
                          fit_p1=True, fit_p2=True, fit_p3=False, fit_p4=False, 
                          adaptive_fitting=False, tiepoint_covariance=False)
    Metashape.app.document.save()
    
    # Write End Time to File
    with open(log_file, mode='a') as file:
        file.write("Processing done on:" + start + "\n")   

# BREAK IN FILE
with open(log_file, mode='a') as file:
        file.write("\n\n")
# -------------------------------------------------------


### 4. Build Depth Maps ###
for chunk in Metashape.app.document.chunks:
    # Write Chunk Name and Start Time to File
    with open(log_file, mode='a') as file:
        file.write('Processing chunk:' + chunk.label + "\n")
        file.write('Build depth maps process started on:' + datetime.now().strftime("%d-%m-%Y_%H-%Mh"))  
    
    # Build depth maps
    chunk.buildDepthMaps(downscale = user_inputs['downscale_2'], filter_mode = Metashape.MildFiltering)
    Metashape.app.document.save()

    # Write End Time to File
    with open(log_file, mode='a') as file:
        file.write("Processing done on:" + start + "\n")   

# BREAK IN FILE
with open(log_file, mode='a') as file:
        file.write("\n\n")
# -------------------------------------------------------


### 5. Build Point Cloud ###
for chunk in Metashape.app.document.chunks:
    # Write Chunk Name and Start Time to File
    with open(log_file, mode='a') as file:
        file.write('Processing chunk:' + chunk.label + "\n")
        file.write('Build point cloud process started on:' + datetime.now().strftime("%d-%m-%Y_%H-%Mh"))  

    # Build point cloud
    chunk.buildPointCloud()
    Metashape.app.document.save()
    
    # Write End Time to File
    with open(log_file, mode='a') as file:
        file.write("Processing done on:" + start + "\n")  

# BREAK IN FILE
with open(log_file, mode='a') as file:
        file.write("\n\n")
# -------------------------------------------------------


### 6. Build DEM ###
for chunk in Metashape.app.document.chunks:
    # Write Chunk Name and Start Time to File
    with open(log_file, mode='a') as file:
        file.write('Processing chunk:' + chunk.label + "\n")
        file.write('Build DEM process started on:' + datetime.now().strftime("%d-%m-%Y_%H-%Mh"))  
    
    # Build dem
    chunk.buildDem(source_data=Metashape.PointCloudData)
    Metashape.app.document.save()
    
    # Write End Time to File
    with open(log_file, mode='a') as file:
        file.write("Processing done on:" + start + "\n")      

# BREAK IN FILE
with open(log_file, mode='a') as file:
        file.write("\n\n")
# -------------------------------------------------------


### 7. Build Orthomosaic ###
for chunk in Metashape.app.document.chunks:
    # Write Chunk Name and Start Time to File
    with open(log_file, mode='a') as file:
        file.write('Processing chunk:' + chunk.label + "\n")
        file.write('Build orthomosaic started on:' + datetime.now().strftime("%d-%m-%Y_%H-%Mh"))  
    
    # Build orthomosaic
    chunk.buildOrthomosaic(surface_data=Metashape.ElevationData)
    Metashape.app.document.save()
    
    # Write End Time to File
    with open(log_file, mode='a') as file:
        file.write("Processing done on:" + start + "\n")  

# BREAK IN FILE
with open(log_file, mode='a') as file:
        file.write("\n\n")
# -------------------------------------------------------

