# USAGE
# python scan.py --image images/page.jpg

from argparse import ArgumentParser
from contextlib import suppress

import numpy as np
from cv2 import imshow, waitKey, getStructuringElement, GaussianBlur, Canny, destroyAllWindows, erode, cvtColor, \
    arcLength, COLOR_BGR2GRAY, approxPolyDP, CHAIN_APPROX_SIMPLE, drawContours, dilate, imread, MORPH_RECT, contourArea, \
    findContours, RETR_LIST, line
from imutils import resize, grab_contours
# import the necessary packages
from pyimagesearch.transform import four_point_transform
from scipy.ndimage import convolve1d
from skimage.filters import threshold_sauvola

# construct the argument parser and parse the arguments
ap = ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="Path to the image to be scanned")
args = vars(ap.parse_args())

# def findContours()


# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = imread(args["image"])

orig = image.copy()
image = resize(image, height=image.shape[0])

# convert the image to grayscale, blur it, and find edges
# in the image
gray = cvtColor(image, COLOR_BGR2GRAY)
gray = GaussianBlur(gray, (7, 7), 0)
edged = Canny(gray, 75, 200)

# show the original image and the edge detected image
print("STEP 1: Edge Detection")
imshow("Image", image)
imshow("Edged", edged)
waitKey(0)
destroyAllWindows()

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
first = (image.shape[0] // 100)
second = ((image.shape[0] // 100)) // 2
element = getStructuringElement(MORPH_RECT, (first // 2, first // 2), (second // 2, second // 2))
edged = dilate(edged, element, iterations=3)
edged = erode(edged, element, iterations=2)

# show the original image and the edge detected image
print("STEP 2: Dilation and Erosion")
imshow("Image", image)
imshow("Edged", edged)
waitKey(0)
destroyAllWindows()

cnts = findContours(edged.copy(), RETR_LIST, CHAIN_APPROX_SIMPLE)

cnts = grab_contours(cnts)
cnts = sorted(cnts, key=contourArea, reverse=True)[:5]

# loop over the contours
for c in cnts:
    # approximate the contour
    peri = arcLength(c, True)
    approx = approxPolyDP(c, 0.02 * peri, True)

    # if our approximated contour has four points, then we
    # can assume that we have found our screen
    if len(approx) == 4:
        screenCnt = approx
        break

# show the contour (outline) of the piece of paper
print("STEP 3: Find contours of paper")
try:
    drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
except NameError:
    print("No contours found - finish.")
    quit()

imshow("Outline", image)
waitKey(0)
destroyAllWindows()

# apply the four point transform to obtain a top-down
# view of the original image
warped = four_point_transform(orig, screenCnt.reshape(4, 2))

# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
warped = cvtColor(warped, COLOR_BGR2GRAY)
T = threshold_sauvola(warped, 11, 0.15)
warped = (warped > T).astype("uint8") * 255

# show the original and scanned images
print("STEP 4: Apply perspective transform")
imshow("Original", orig)
imshow("Scanned", warped)
waitKey(0)

print("STEP 5: Detect lines")

print(warped)
linedetection = convolve1d(warped.sum(axis=1), weights=np.array(
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]))


def findline(arr):
    ones = np.ones(arr.shape)
    for (x,), val in np.ndenumerate(arr):
        if x >= 0:
            if arr[x - 1] < val:
                ones[x] = 0
                continue

            # Check right.
        with suppress(IndexError):
            if arr[x + 1] <= val:
                ones[x] = 0
                continue
    return ones.astype(int)


lines = findline(linedetection)
print(lines)

for linedata, pos in enumerate(lines):
    if (linedata == 1):
        line(warped, (0, pos), int(image.shape[0]), [255, 0, 0])
