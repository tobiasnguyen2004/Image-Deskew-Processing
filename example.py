import cv2

image_path = "/Users/tungnguyen/Desktop/FPT Internship/GitHub Repositories/deskew/research/error_categorization/Error Range 0.5-90/MOI_1_CDKT51_11_1_-50.jpg_60.49248747913189.jpg"

# image = cv2.imread(image_path, cv2.IMREAD_COLOR)
image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
from jdeskew.estimator import get_angle

angle = get_angle(image)
print(angle)

from jdeskew.utility import rotate
output_image = rotate(image, angle)

# Filename
directory = '/Users/tungnguyen/Desktop/FPT Internship/GitHub Repositories/deskew/testsets'
filename = f'{directory}/{angle}.jpg'
  
# Using cv2.imwrite() method
# Saving the image
cv2.imwrite(filename, output_image)

