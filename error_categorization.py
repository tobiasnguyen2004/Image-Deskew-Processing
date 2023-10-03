import cv2
import os
import re
import shutil

from jdeskew.estimator import get_angle

def move_and_rename_files(folder_path, error_range_1_path, error_range_2_path, error_range_3_path, error_range_4_path):
    for filename in os.listdir(folder_path):
        src_path = os.path.join(folder_path, filename)
        
        # Get angle from filename
        match = re.match(r".*_(\-?\d+)\.jpg", filename)
        if match:
            angle = match.group(1)
            
            # Read image and calculate output angle
            image = cv2.imread(src_path, cv2.IMREAD_UNCHANGED)
            output_angle = get_angle(image)
            
            # Calculate error
            error = abs(output_angle - int(angle))
            
            # Generate new filename with appended error
            new_filename = f"{filename}_{error}.jpg"
            
            # Determine destination path based on error range
            if error < 0.5:
                dst_path = os.path.join(error_range_1_path, new_filename)
            elif 0.5 <= error < 90:
                dst_path = os.path.join(error_range_2_path, new_filename)
            elif 90 <= error < 180:
                dst_path = os.path.join(error_range_3_path, new_filename)
            else:
                dst_path = os.path.join(error_range_4_path, new_filename)
            
            # Move and rename the file
            shutil.move(src_path, dst_path)

def empty_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

# Run program
folder_path = "/Users/tungnguyen/Desktop/FPT Internship/GitHub Repositories/deskew/testsets/testset2" 
error_range_1_path = "/Users/tungnguyen/Desktop/FPT Internship/GitHub Repositories/deskew/research/error_categorization/Error Range 0-0.5"
error_range_2_path = "/Users/tungnguyen/Desktop/FPT Internship/GitHub Repositories/deskew/research/error_categorization/Error Range 0.5-90"
error_range_3_path = "/Users/tungnguyen/Desktop/FPT Internship/GitHub Repositories/deskew/research/error_categorization/Error Range 90-180"
error_range_4_path = "/Users/tungnguyen/Desktop/FPT Internship/GitHub Repositories/deskew/research/error_categorization/Error Range >180"

# Empty destination folders
empty_folder(error_range_1_path)
empty_folder(error_range_2_path)
empty_folder(error_range_3_path)
empty_folder(error_range_4_path)

# Move and rename files
move_and_rename_files(folder_path, error_range_1_path, error_range_2_path, error_range_3_path, error_range_4_path)
