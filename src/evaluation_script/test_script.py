from pathlib import Path
from sklearn.cluster import KMeans

import csv
import cv2 as cv
import numpy as np
import os


# Load the first image
path = Path(__file__).parent

# Iterate over all images in the current directory
with open("results.csv", "w", newline="") as csvfile:
    fieldnames = [
        "dataset",
        "test_image",
        "stdev",
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for dataset in os.listdir(path):
        if not dataset.endswith("cropped"):
            continue
        stdevs = []
        for i, image_path in enumerate(os.listdir(path / dataset)):
            if image_path.endswith(".jpg"):
                # stdev = isolate_square(str(path / dataset / image_path))
                image = cv.imread(str(path / dataset / image_path))
                image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
                stdev = cv.meanStdDev(image)[1][0][0]
                print(stdev)
                image = cv.resize(image, (400, 600))
                cv.imshow("Image", image)
                cv.waitKey(1000)
                writer.writerow({
                    "dataset": dataset,
                    "test_image": image_path,
                    "stdev": stdev,
                })
                stdevs.append(stdev)
        print(f"Dataset: {dataset}, Mean stdev: {np.mean(stdevs)}")
        