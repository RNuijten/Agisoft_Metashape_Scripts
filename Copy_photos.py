## Copy every xth photo to new directory
# This subset has lower overlap is and can be uploaded to web services

import glob as glob
import tqdm as tqdm
import shutil

# Directories
main_dir = "D:/Projects/Cowichan_2023/_cowichan_jen/P1/May28_2023/"
out_dir = "D:/Projects/Cowichan_2023/_cowichan_jen/P1/May3_2023_ProjectKiwi/"

# List file paths
photos = glob.glob(main_dir+'/**/*.jpg', recursive=True)
photos = photos[0::4] # select every fifth photo

# Read EXIF metadate
# ... code here

# Only keep photos on north facing flight paths
# ... code here

# Copy each photo to the destination directory
for file in photos:
   shutil.copy2(file, out_dir) # Note that 'copy2' preserves the original metadata