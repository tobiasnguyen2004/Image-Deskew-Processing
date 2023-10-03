from PIL import Image
import os
import math
import numpy as np
    
def rotateAndScaleWithBBox(bbox_coords, rotation_angle):
    # Convert the bounding box coordinates from string to float
    bbox_coords = [float(coord) for coord in bbox_coords.split()]

    # Extract original coordinates
    orig_x, orig_y, orig_width, orig_height = bbox_coords[1:]

    # Calculate the center of the bounding box
    center_x = orig_x + orig_width / 2
    center_y = orig_y + orig_height / 2

    # Convert the rotation angle to radians
    radians = np.deg2rad(rotation_angle)

    # Calculate the new bounding box coordinates that will fit the table entirely within the rotated image
    rotated_center_x = center_x * np.cos(radians) - center_y * np.sin(radians)
    rotated_center_y = center_x * np.sin(radians) + center_y * np.cos(radians)

    # Calculate the new width and height of the bounding box
    new_width = orig_width * np.cos(radians) - orig_height * np.sin(radians)
    new_height = orig_width * np.sin(radians) + orig_height * np.cos(radians)

    # Calculate the new coordinates of the bounding box
    new_x = rotated_center_x - new_width / 2
    new_y = rotated_center_y - new_height / 2

    return new_x, new_y, new_width, new_height

def rotate_image_with_bbox(image_path, bbox_coords, output_folder, rotation_angle):
    # Read the image
    image = Image.open(image_path)

    # Rotate the image
    rotated_image = image.rotate(rotation_angle, expand=True)

    # Get the size of the rotated image
    new_width, new_height = rotated_image.size

    # Calculate the adjusted bounding box coordinates after rotation
    rotated_x, rotated_y, rotated_width, rotated_height = rotateAndScaleWithBBox(bbox_coords, rotation_angle)

    # Save the rotated image
    filename, _ = os.path.splitext(os.path.basename(image_path))
    output_path = os.path.join(output_folder, f"{filename}_rotated.jpg")
    rotated_image.save(output_path)

    # Save the adjusted bounding box coordinates
    output_txt_path = os.path.join(output_folder, f"{filename}_bbox.txt")
    with open(output_txt_path, "w") as f:
        f.write(f"0 {rotated_x} {rotated_y} {rotated_width} {rotated_height}")
        
# Input folder containing bounding box coordinate files
bbox_folder = "/Users/tungnguyen/Desktop/FPT Internship/GitHub Repositories/deskew/extracted_table_set/coords_file"
# Input folder containing the table images
image_folder = "/Users/tungnguyen/Desktop/FPT Internship/GitHub Repositories/deskew/extracted_table_set/original_images"
# Output folder for the rotated images and adjusted bounding box coordinates
output_folder = "/Users/tungnguyen/Desktop/FPT Internship/GitHub Repositories/deskew/extracted_table_set/output_folder"
# Rotation angle (in degrees), adjust as needed
rotation_angle = 45

# Get a list of all files in the bounding box coordinates folder
bbox_files = os.listdir(bbox_folder)

# Process each bounding box coordinate file
for bbox_file in bbox_files:
    if bbox_file.endswith(".xml.txt"):
        bbox_file_path = os.path.join(bbox_folder, bbox_file)
        with open(bbox_file_path, "r") as f:
            bbox_coords_list = f.readlines()

        # Extract the main name of the bounding box coordinate file (without the extension)
        bbox_main_name = os.path.splitext(os.path.splitext(bbox_file)[0])[0]

        # Search for the image file in the image folder with the same main name
        found_image = False
        for image_file in os.listdir(image_folder):
            image_main_name, image_extension = os.path.splitext(image_file)
            if image_extension.lower() == ".jpg" and image_main_name == bbox_main_name:
                image_file_path = os.path.join(image_folder, image_file)
                found_image = True
                break

        if found_image:
            # Generate rotated images and adjust bounding box coordinates
            for i, bbox_coords in enumerate(bbox_coords_list):
                rotate_image_with_bbox(image_file_path, bbox_coords, output_folder, rotation_angle)
        else:
            print(f"Image file for '{bbox_file}' not found in the image folder.")


