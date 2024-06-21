import cv2
import glob
import os
from tqdm import tqdm

import tifffile as tiff

def resize_images(directory, size):
    # Get a list of all TIFF images in the directory
    images = glob.glob(os.path.join(directory, '*.tif'))

    # Loop over the images
    for image_file in tqdm(images):
        # Read the image
        image = tiff.imread(image_file)

        # Check if the image is not empty and is two-dimensional
        if image is not None and image.ndim == 2:
            # Resize the image
            resized_image = cv2.resize(image, (size, size))

            # Save the resized image
            cv2.imwrite(image_file, resized_image)
        else:
            print(f"Unable to read or resize image file: {image_file}")

# Define the size of the square
size = 520

# Resize the images in the train directory
resize_images('archive/fold_0/train', size)

# Resize the images in the val directory
resize_images('archive/fold_0/val', size)