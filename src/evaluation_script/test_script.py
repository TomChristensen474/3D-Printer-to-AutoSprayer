from pathlib import Path

import cv2 as cv
import os

# Load the first image
path = Path(__file__).parent
image1_path = path / "image_1.jpg"
image1 = cv.imread(str(image1_path))

# Load the second image
image2_path = path / "image_2.jpg"
image2 = cv.imread(str(image2_path))

# Iterate over all images in the current directory
for image_path in os.listdir():
    if image_path.endswith(".jpg"):
        # Load the image
        image = cv.imread(image_path)

        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        std_dev = cv.meanStdDev(image)

        print(std_dev)

        image = cv.resize(image, (600, 400))
        # Display the image
        cv.imshow("Image", image)
        cv.waitKey(0)