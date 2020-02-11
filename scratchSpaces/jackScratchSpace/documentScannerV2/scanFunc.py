# USAGE

from argparse import ArgumentParser
from contextlib import suppress

from numpy import array
from cv2 import imshow, waitKey, getStructuringElement, GaussianBlur, Canny, destroyAllWindows, erode, cvtColor, \
    arcLength, COLOR_BGR2GRAY, approxPolyDP, CHAIN_APPROX_SIMPLE, drawContours, dilate, imread, MORPH_RECT, contourArea, \
    findContours, RETR_LIST, line, imwrite
from imutils import resize, grab_contours
# import the necessary packages
from pyimagesearch.transform import four_point_transform
from scipy.ndimage import convolve1d
from skimage.filters import threshold_sauvola


def scanImage(filename, destoffset="-new"):

    # load the image and compute the ratio of the old height
    # to the new height, clone it, and resize it
    image = imread(filename)

    orig = image.copy()
    image = resize(image, height=image.shape[0])

    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cvtColor(image, COLOR_BGR2GRAY)
    gray = GaussianBlur(gray, (7, 7), 0)
    edged = Canny(gray, 75, 200)

    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour
    first = (image.shape[0] // 100)
    second = ((image.shape[0] // 100)) // 2
    element = getStructuringElement(MORPH_RECT, (first // 2, first // 2), (second // 2, second // 2))
    edged = dilate(edged, element, iterations=3)
    edged = erode(edged, element, iterations=2)


    cnts = findContours(edged.copy(), RETR_LIST, CHAIN_APPROX_SIMPLE)

    cnts = grab_contours(cnts)
    cnts = sorted(cnts, key=contourArea, reverse=True)[:5]

    screenCnt = array([])

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


    if (screenCnt.size != 0):

        # apply the four point transform to obtain a top-down
        # view of the original image
        transformed = four_point_transform(orig, screenCnt.reshape(4, 2))

    else:
        transformed = orig


    # convert the warped image to grayscale, then threshold it
    # to give it that 'black and white' paper effect
    transformed = cvtColor(transformed, COLOR_BGR2GRAY)
    threshold = threshold_sauvola(transformed, 11, 0.15)
    transformed = (transformed > threshold).astype("uint8") * 255

    imwrite(".".join(filename.split(".")[:-1]) + destoffset + "." +  filename.split(".")[-1], transformed)
    return



scanImage("images/logbook.png")