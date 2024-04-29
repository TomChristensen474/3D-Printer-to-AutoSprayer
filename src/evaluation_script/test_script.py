from pathlib import Path
from sklearn.cluster import KMeans

import csv
import cv2 as cv
import numpy as np
import os


# Load the first image
path = Path(__file__).parent
image1_path = path / "hand_spray_images/IMG_20240426_180703.jpg"
image1 = cv.imread(str(image1_path))

# # Load the second image
# image2_path = path / "image_2.jpg"
# image2 = cv.imread(str(image2_path))

def unify_lines(lines, rho_threshold=60, theta_threshold=np.pi/180*50):
    # Group lines that are similar based on thresholds
    unified_lines = []
    for line in lines:
        for rho, theta in line:
            if not unified_lines:
                unified_lines.append((rho, theta))
            else:
                matched = False
                for u_rho, u_theta in unified_lines:
                    if abs(u_rho - rho) < rho_threshold and abs(u_theta - theta) < theta_threshold:
                        average_rho = (u_rho + rho) / 2
                        average_theta = (u_theta + theta) / 2
                        unified_lines[unified_lines.index((u_rho, u_theta))] = (average_rho, average_theta)
                        matched = True
                        break
                if not matched:
                    unified_lines.append((rho, theta))
    return np.array([[line] for line in unified_lines], dtype=np.float32)

def find_intersection_points(lines):
    # Find the intersection points of the lines
    intersection_points = []
    for i, line1 in enumerate(lines):
        for j, line2 in enumerate(lines):
            if i == j:
                continue
            rho1, theta1 = line1[0]
            rho2, theta2 = line2[0]
            a = np.array([[np.cos(theta1), np.sin(theta1)], [np.cos(theta2), np.sin(theta2)]])
            b = np.array([[rho1], [rho2]])
            x0, y0 = np.linalg.solve(a, b)
            intersection_points.append((x0, y0))
    return intersection_points

# def cluster_points(points):
#     nclusters = 4
#     criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
#     labels = np.random.randint(nclusters,
#                                size=(points.shape[0], points.shape[1]),
#                                dtype=np.int32)
#     reshaped_labels = np.reshape(labels, (labels.shape[0] * labels.shape[1], 1))

#     _, _, centers = cv.kmeans(points, nclusters, reshaped_labels ,criteria, 10, cv.KMEANS_RANDOM_CENTERS)

#     return centers

# def cluster_points(points):
#     kmeans = KMeans(n_clusters=4, random_state=0).fit(points)
#     return kmeans.cluster_centers_

def get_4_corners(image, points):
    # Split the image into cells and cast a vote if a point is in that cell
    cell_size = 25
    cells = []
    for i in range(0, image.shape[0], cell_size):
        for j in range(0, image.shape[1], cell_size):
            cells.append([i, j, i + cell_size, j + cell_size])

    # cast a vote for each point in each cell
    votes = np.zeros(len(cells))
    for point in points:
        for i, cell in enumerate(cells):
            if point[0] >= cell[0] and point[0] <= cell[2] and point[1] >= cell[1] and point[1] <= cell[3]:
                votes[i] += 1
    
    # return 4 most voted for cells
    centers = []
    for i in np.argsort(votes)[-8:]:
        center = ((cells[i][0] + cells[i][2]) / 2, (cells[i][1] + cells[i][3]) / 2)
        centers.append(center)

    # # if centers aren't far enough apart, remove the closest one
    # for i, center in enumerate(centers):
    #     for j, other_center in enumerate(centers):
    #         if i == j:
    #             continue
    #         if np.linalg.norm(np.array(center) - np.array(other_center)) < 100:
    #             centers.pop(j)
    #             break

    # Filter out centers that aren't in corners

    # Get top left center
    top_left_center = None
    for center in centers:
        if center[0] < 200 and center[1] < 300:
            if top_left_center is None:
                top_left_center = center
            elif center[0] < top_left_center[0] and center[1] < top_left_center[1]:
                top_left_center = center

    # Get top right center
    top_right_center = None
    for center in centers:
        if center[0] > 200 and center[1] < 300:
            if top_right_center is None:
                top_right_center = center
            elif center[0] > top_right_center[0] and center[1] < top_right_center[1]:
                top_right_center = center

    # Get bottom left center
    bottom_left_center = None 
    for center in centers:
        if center[0] < 200 and center[1] > 300:
            if bottom_left_center is None:
                bottom_left_center = center
            elif center[0] < bottom_left_center[0] and center[1] > bottom_left_center[1]:
                bottom_left_center = center

    # Get bottom right center
    bottom_right_center = None
    for center in centers:
        if center[0] > 200 and center[1] > 300:
            if bottom_right_center is None:
                bottom_right_center = center
            elif center[0] > bottom_right_center[0] and center[1] > bottom_right_center[1]:
                bottom_right_center = center

    return [top_left_center, top_right_center, bottom_left_center, bottom_right_center]
    # for i, center in enumerate(centers):
    #     if (center[0] > 100  and center[0] < 300) or (center[1] > 200 and center[1] < 350):
    #         centers.pop(i)
    #         continue
    # cv.circle(img_copy, (100, 200), 5, (0, 0, 255), 3)
    # cv.circle(img_copy, (100, 350), 5, (0, 0, 255), 3)
    # cv.circle(img_copy, (300, 200), 5, (0, 0, 255), 3)
    # cv.circle(img_copy, (300, 350), 5, (0, 0, 255), 3)


    # return centers[-4:]


def isolate_square(image_path):
    # Load the image
    image = cv.imread(image_path)
    image = cv.resize(image, (400, 600))

    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    binary = cv.threshold(image, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    canny = cv.Canny(image, 65, 225)
    cv.imshow("Canny", canny)

    hough_lines = cv.HoughLines(canny, 0.3, np.pi / 720, 30)
    unified_lines = unify_lines(hough_lines)
    intersection_points = find_intersection_points(unified_lines)

    image = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
    img_copy = image.copy()

    for line in hough_lines:
        rho = line[0][0]
        theta = line[0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    for line in unified_lines:

        rho = line[0][0]
        theta = line[0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv.line(img_copy, (x1, y1), (x2, y2), (255, 0, 0), 2)

    for point in intersection_points:
        cv.circle(img_copy, (int(point[0]), int(point[1])), 3, (0, 255, 0), 1)

    corners = get_4_corners(img_copy, intersection_points)
    # for corner in corners:
        # cv.circle(img_copy, (int(corner[0]), int(corner[1])), 5, (0, 0, 255), 3)

    # sorted_corners = sorted(corners, key=lambda x: x[0])

    # cropped_image = img_copy[int(corners[0][1]):int(corners[2][1]), int(corners[0][0]):int(corners[2][0])].astype(np.float32)

    # cv.circle(img_copy, (100, 200), 5, (0, 0, 255), 3)
    # cv.circle(img_copy, (100, 350), 5, (0, 0, 255), 3)
    # cv.circle(img_copy, (300, 200), 5, (0, 0, 255), 3)
    # cv.circle(img_copy, (300, 350), 5, (0, 0, 255), 3)


    # centers = cluster_points(np.array(intersection_points))
    # for center in centers:
    #     print(center)
    #     cv.circle(img_copy, (int(center[0]), int(center[1])), 5, (0, 0, 255), 3)
    
    # std_dev = cv.meanStdDev(image)
    # print(std_dev)
    # image = cv.resize(image, (400, 600))
    # Display the image
    # cv.imshow("Image", image)
    # cv.imshow("Unified", img_copy)

    # cv.waitKey(0)

    # stdev = cv.meanStdDev(cropped_image)
    # # mean = np.mean(cropped_image)
    # # variance = np.mean((cropped_image - mean) ** 2, axis=0)
    # # stdev = np.sqrt(variance)

    # print(stdev)
    # return stdev


# image_path = path / "machine_spray_images" / "IMG_20240426_180615.jpg"
# isolate_square(str(image_path))

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
        