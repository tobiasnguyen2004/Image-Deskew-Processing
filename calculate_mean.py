# # Calculate the mean/std/max/min of the error of the angles
import cv2
import numpy as np
import os
import re
import shutil

# Read the input image and correct output image
folder_path = "/Users/tungnguyen/Desktop/FPT Internship/GitHub Repositories/deskew/research/testset2"  

#This is the value we want to compare to the angle obtained from the filename
#Iterate over all the files and append each "get_angle" to a list, and compare 
# each element of the list to each element of the other list

from jdeskew.estimator import get_angle

def get_output_angles(folder_path):
    output_angles = []

    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        angle = get_angle(image)
        output_angles.append(angle)

    return output_angles
 
def extract_correct_angle(folder_path):
    pattern = r"_([^_]+)\.jpg"
    correct_angle_list = []

    for filename in os.listdir(folder_path):
        match = re.search(pattern, filename)
        if match:
            correct_angle = int(match.group(1))
            correct_angle_list.append(correct_angle)

    return correct_angle_list

# Calculate the absolute difference between the angle of the rotated 
# image and the correct output image

output_angles = get_output_angles(folder_path)
correct_angles = extract_correct_angle(folder_path)

def compare_angles(output_angles, correct_angles):
    error_list = []

    for i in range(len(output_angles)):
        output_angle = output_angles[i]
        correct_angle = correct_angles[i]
        error = abs(output_angle - correct_angle)
        error_list.append(error)

    return error_list

error_list_final = compare_angles(output_angles, correct_angles)
print(len(error_list_final))

# Calculate the mean, standard deviation, and other statistics of the errors
mean_error = np.mean(error_list_final)
std_deviation = np.std(error_list_final)
max_error = np.max(error_list_final)
min_error = np.min(error_list_final)

# Print the statistics
print("Mean Error:", mean_error)
print("Standard Deviation:", std_deviation)
print("Maximum Error:", max_error)
print("Minimum Error:", min_error)


# def count_files_in_subfolders(folder_path):
#     file_counts = {}

#     for root, dirs, files in os.walk(folder_path):
#         folder_name = os.path.relpath(root, folder_path)
#         file_counts[folder_name] = len(files)

#     return file_counts

# # Example usage
# folder_path = "/Users/tungnguyen/Desktop/FPT Internship/GitHub Repositories/deskew/research/error_categorization"
# file_counts = count_files_in_subfolders(folder_path)

# # Print the file counts for each subfolder
# for folder, count in file_counts.items():
#     print(f"Subfolder: {folder}, File Count: {count}")



