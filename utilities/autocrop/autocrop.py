from PIL import Image
import os

# Getting input
inputPath = input("Please enter the input directory: \n")
outputPath = input("Please enter the output directory: \n")

# Declaring a list to hold the image file names
images = []

# Looking in our directory with images and appending any .jpg files
for f_name in os.listdir(inputPath):
    if f_name.endswith('.jpg'):
        images.append(f_name)

# Cropping each of the images from/to a preset size
for image in images:
    
    # Opening each image
    im_open = Image.open(inputPath + "/" + image,mode='r')
    
    # Getting the width/height of each
    width, height = im_open.size

    # Defining the crop points
    left = 180
    top = 0
    right = 500
    bottom = height

    # Cropping the image
    im_crop = im_open.crop((left, top, right, bottom))

    # Saving the image in our output directory
    im_crop.save(outputPath + "/" + image)

print("\nDone!")

