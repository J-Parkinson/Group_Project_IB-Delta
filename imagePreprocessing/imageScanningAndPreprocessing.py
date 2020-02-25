from tempfile import TemporaryDirectory

import cv2
import numpy as np
from cv2 import getStructuringElement, GaussianBlur, Canny, erode, cvtColor, arcLength, COLOR_BGR2GRAY, approxPolyDP, \
    CHAIN_APPROX_SIMPLE, dilate, imread, MORPH_RECT, contourArea, findContours, RETR_LIST, imwrite
from imutils import resize, grab_contours
from numpy import array, zeros, greater, hsplit, vsplit, greater_equal, diff, delete, insert, int32
from scipy.ndimage import convolve1d
from scipy.signal import argrelextrema
from skimage.filters import threshold_sauvola
from PIL import Image
from tempfile import NamedTemporaryFile
import fitz
from pdf2image import convert_from_path as loadPDF
import CellsToWords
from os import makedirs, path
from sys import stderr

from dataStructures.logbookScan import Column, PageLayout, CellOfWords
#from frontend.ColumnScreen import queryUserAboutColumns

# Imports for testing - showing histogram of columns
'''
def showImage(img, lines=array([]), wait=True):
    plt.plot(img)

    for coord in lines:
        plt.axvline(x=coord)

    if wait:
        plt.show()
        waitKey()
    return
'''

# Imports for testing - scanning in PDFs
'''
import fitz
from os import makedirs, listdir
from sys import stderr
from tempfile import NamedTemporaryFile

def safeMakeDir(dir):
    if not path.exists(dir):
        makedirs(dir)
    else:
        stderr.write("Path " + dir + " already exists.\n")
        stderr.flush()

def pdfToImages(source, destFolder, filename, suffix, offset=0):

    safeMakeDir(destFolder[:-1])

    allImages = fitz.open(source)
    for x, page in enumerate(allImages):
        with NamedTemporaryFile(suffix=suffix) as temp:
            page.getPixmap().writePNG(temp.name)
            #scanImage(temp.name, destFolder + filename + str(x + offset) + suffix)
            safeMakeDir(destFolder + "Page " + str(x + offset))
            findLinesandNormalise(temp.name, destFolder + "Page " + str(x + offset) + "/")
    return len(allImages)

def directoryMixedToDirectoryImages(directory, destFolder, filename, suffix):
    countNoImages = 0

    for file in listdir(directory):
        currentFilename = file.lower()

        if currentFilename.endswith(".pdf"):

            countNoImages += pdfToImages(directory + currentFilename, destFolder, filename, suffix, countNoImages)

        elif currentFilename.endswith((".png", ".jpg", ".jpeg")):

            safeMakeDir(destFolder + "Page " + str(countNoImages))

            #scanImage(directory + currentFilename, destFolder + filename + str(countNoImages) + suffix)
            findLinesandNormalise(directory + currentFilename, destFolder + "Page " + str(countNoImages) + "/")
            countNoImages += 1

        else:
            continue
    return

pdfToImages("images/scantest.pdf", "images/pdftest/", "image", ".png")

#directoryMixedToDirectoryImages("images/New Scans Small/", "images/segmentedImagesOut/", "image", ".png")
'''

''' splitCellsAndNormalise
    Normalises the image, splits into cells, performs word detection, deslants words, and resizes ready for our NN.
    Returns a directory for the images to be word-detected.
'''

'''def safeMakeDir(dir):
    if not path.exists(dir):
        makedirs(dir)
    else:
        stderr.write("Path " + dir + " already exists.\n")
        stderr.flush()'''

'''def pdfToImages(source, destFolder, filename, suffix, offset=0):

    safeMakeDir(destFolder[:-1])

    allImages = fitz.open(source)
    for x, page in enumerate(allImages):
        with NamedTemporaryFile(suffix=suffix) as temp:
            page.getPixmap().writePNG(temp.name)
            #scanImage(temp.name, destFolder + filename + str(x + offset) + suffix)
            safeMakeDir(destFolder + "Page " + str(x + offset))
            findLinesandNormalise(temp.name, destFolder + "Page " + str(x + offset) + "/")
    return len(allImages)'''

def concatenateImages(images, resample=Image.BICUBIC):
    minHeight = min(image.height for image in images)
    imageResize = [image.resize((int(image.width * minHeight / image.height), minHeight), resample=resample)
                      for image in images]
    totalWidth = sum(image.width for image in imageResize)
    dest = Image.new('RGB', (totalWidth, minHeight))
    xPosition = 0
    for image in imageResize:
        dest.paste(image, (xPosition, 0))
        xPosition += image.width
    return dest


def splitCellsAndNormalise(source, noPages):
    # load the image and compute the ratio of the old height
    # to the new height, clone it, and resize it

    '''Step 1 - load image'''
    image = imread(source)
    image = resize(image, width=image.shape[1] * 3)
    orig = image.copy()

    # deslants page into a rectangle - perspective transform
    '''Step 2 - normalise page'''
    transformed = normaliseImage(image, orig)

    # determines where the columns are
    '''Step 3 - columns'''
    colLocations = calculateColumns(transformed)

    # determines where the rows are - interpolation used (so assuming equally spaced lines)
    '''Step 4 - rows'''
    rowLocations = calculateRows(transformed)

    # splits image along col and row locations
    '''Step 5 - cell splitting'''
    cells = convertToCellOfWords(splitIntoCells(transformed, rowLocations, colLocations), len(rowLocations) + 1)

    '''dir = storeFilesTemporarily(cells, len(colLocations))'''

    ''' So at the moment we have it split into cells, and a flat 1d Python list of cells (1d list of 2d Numpy arrays of B/W cells)
        Row number = x // len(colLocations)
        Col number = x % len(colLocations)
        Run your code on each element in that and yh should work :D
    '''

    return cells # will eventually return string representing the location of the dir Francesca is using to read in cells and


''' handleColumns
    Checks with the user if the columns are in the correct location, and returns the new user-made columns
    Returns user-checked columns
'''


'''def handleColumns(cols, height, image):
    columnObjects = PageLayout(1)
    for x in range(0, len(cols) - 2):
        newColumn = Column((cols[x], 0), (cols[x + 1], height), 0, "COLUMN NAME HERE")
        columnObjects.addColumn(newColumn)

    newCols = queryUserAboutColumns(columnObjects)

    maxY, maxX, minY, minX = 0

    for columm in newCols:
        maxY = max(maxY, columm.getCoords()[0][1], columm.getCoords()[1][1])
        minY = min(minY, columm.getCoords()[0][1], columm.getCoords()[1][1])
        maxX = max(maxX, columm.getCoords()[0][0], columm.getCoords()[1][0])
        minX = min(minX, columm.getCoords()[0][0], columm.getCoords()[1][0])

    allColX = [col[0][0] - minX for col in newCols.getCoords()] + [col[1][0] - minX for col in newCols.getCoords()]

    newImage = image[minY:maxY][minX:maxX]

    return (newImage, newCols, minX, maxX, minY, maxY, allColX)'''


''' orderPoints
    Calculates which of the four coordinates provided are which (TL, BR, TR, BL)
    Returns rect, with coords in CW direction, and the first coordinate being the top left coord
'''


def orderPoints(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect


''' fourPointTransform
    Finds the points which we can pass to cv2.PerspectiveTransform/warpPerspective
    Returns warped image
'''
def fourPointTransform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = orderPoints(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped


''' normaliseImage
    Takes our original image, converts to greyscale, finds the contours of the page and performs a perspective transform on the original image
    Returns B/W thresholded, transformed image
'''
def normaliseImage(image, orig):
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
        approx = approxPolyDP(c, 0.01 * peri, True)

        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
        break

    if (screenCnt.size != 0):

        # apply the four point transform to obtain a top-down
        # view of the original image
        transformed = fourPointTransform(orig, screenCnt.reshape(4, 2))

    else:
        transformed = orig

    # convert the warped image to grayscale, then threshold it
    # to give it that 'black and white' paper effect
    # also resize to try and increase fidelity of output

    transformed = resize(transformed, height=image.shape[0])
    transformed = cvtColor(transformed, COLOR_BGR2GRAY)
    threshold = threshold_sauvola(transformed, 11, 0.15)
    transformed = (transformed > threshold).astype("uint8") * 255

    return transformed


''' storeFilesTemporarily these cells in a temp dir
    Returns the string of the dir
    Not used - for testing purposes'''
def storeFilesTemporarily(cells, noCols):
    # create new temp directory
    with TemporaryDirectory() as dir:
        for x, image in enumerate(cells):
            # w
            #     Takes cells and storesrite to temp dir, with name referencing position in image
            imwrite(dir + "/cell-" + str(x // noCols) + "-" + str(x % noCols) + ".png", image)
    return dir


''' splitIntoCells
    Splits a large image at the prescribed locations given by [rows] and [cols], and returns a flat list of each sub-image (cell)
    Returns a list of binary cell images
'''
def splitIntoCells(image, rows, cols):
    return [a for b in [hsplit(row, cols) for row in vsplit(image, rows)] for a in b]


''' convertToCellOfWords
    Converts a list of 2d arrays to CellOfWords[]
    Each CellOfWords[] contains a row, col and image (2D Numpy array)
'''
def convertToCellOfWords(images, noCols):
    returnList = []
    for n, image in images:
        newWord = CellOfWords(image, n//noCols, n%noCols)
        returnList.append(newWord)
    return returnList


''' calculateColumns
    Calculates the column locations
    Returns a list of binary cell images
'''
def calculateColumns(transformed):
    # find the sum of the columns of pixels - white given as 255, black given as 0
    transformedsumx = transformed.sum(axis=0)

    # find the threshold
    threshold = transformedsumx.max() * 0.99
    columns = zeros(transformedsumx.shape)
    # Set non-columns to 255
    columns[transformedsumx < threshold] = 255

    '''#TODO: REMOVE- USED FOR TESTING
    showImage(columns)'''

    # Create new column Numpy array (for convolutions)
    columns = array(columns).astype(int)
    # Convolve to smooth spikes and remove adjacent spikes (by smoothing into each other)
    # Asymmetric to try and combat dual spikes
    columns = convolve1d(convolve1d(columns, array([1, 1, 1, 3, 5, 8, 4, 3, 1, 1, 1]), mode="nearest"),
                         array([1, 1, 1, 3, 5, 8, 4, 3, 1, 1, 1]), mode="nearest")
    # +2 used to combat asymmetry of convolutions
    # find max vals (i.e. most probable cols)

    columnsfiltered = argrelextrema(columns, greater)[0] + 2
    columnsfiltered = [0] + columnsfiltered + [len(transformedsumx)]
    return columnsfiltered


''' refactorRows
    Takes the suggested rows, and interpolates in order to fill in gaps or remove thin lines
    Returns interpolated rows
'''
def refactorRows(rowsfiltered):
    # Find difference between adjacent row lines (i.e. row thicknesses)
    rowsdiff = diff(rowsfiltered)
    # Find average
    rowsdiffaverage = (rowsfiltered.max() - rowsfiltered.min()) / (rowsfiltered.shape[0] - 1)

    i = 0
    # Loop over shape of rowsdiff
    while (i < rowsdiff.shape[0]):

        dif = rowsdiff[i]

        if ((0.6 * rowsdiffaverage) > dif or dif > (1.6 * rowsdiffaverage)):

            #if too small interpolate row in middle of existing rows
            if ((0.6 * rowsdiffaverage) > dif):
                try:
                    newVal = (rowsfiltered[i] + rowsfiltered[i + 1]) / 2
                    rowsfiltered = delete(rowsfiltered, i + 1)
                    rowsfiltered = delete(rowsfiltered, i)
                    rowsfiltered = insert(rowsfiltered, i, int32(newVal))
                    rowsdiff = delete(rowsdiff, i)
                    rowsdiff[i] += dif
                except:
                    continue
                if (i < rowsdiff.shape[0] - 1):
                    i += 1
                continue

            # if too large insert one row with average thickness
            elif (dif > (1.6 * rowsdiffaverage)):
                rowsfiltered = insert(rowsfiltered, i + 1, int32(rowsfiltered[i] + rowsdiffaverage))
                rowsdiff = insert(rowsdiff, i + 1, int32(dif - rowsdiffaverage))

        i += 1

    return rowsfiltered


''' calculateRows
    Calculates position of rows using histogram analysis
    Returns locations of rows in list
'''
def calculateRows(transformed):
    # Find the sum of each row - white = 255, black = 0
    transformedsumy = transformed.sum(axis=1)[1:-1].astype("int64")

    # convolve - smooth out response, remove small rows next to each other
    tsy2 = convolve1d(convolve1d(transformedsumy, array([1, 1, 1, 3, 5, 8, 4, 3, 1, 1, 1]), mode="nearest"),
                      array([1, 1, 1, 3, 5, 8, 4, 3, 1, 1, 1]), mode="nearest")

    # find max vals (i.e. most probable rows)
    rowsfiltered = argrelextrema(tsy2, greater_equal)[0]

    # interpolate rows to remove anomalies
    rowsfiltered = refactorRows(rowsfiltered)
    return rowsfiltered



''' handleColumnGUI
    Handles GUI call from frontend to fetch column stuff '''
def handleColumnGUI(source, noPages, progressBar=None):
    # load the image and compute the ratio of the old height
    # to the new height, clone it, and resize it
    if progressBar:
        progressBar.update("Load images")

    allImages = loadPDF(source)
    imagesToMerge = []
    for x, page in enumerate(allImages):
        if x < noPages:
            imagesToMerge.append(array(page))
        else:
            break
    '''Step 1 - load image'''

    transformedImageToMerge = []

    for n, image in enumerate(imagesToMerge, 1):
        orig = image.copy()

        # deslants page into a rectangle - perspective transform
        '''Step 2 - normalise page'''
        if progressBar:
            progressBar.update("Normalise page " + str(n))

        transformed = normaliseImage(image, orig)

        transformedImageToMerge.append(Image.fromarray(transformed))

    if progressBar:
        progressBar.update("Merge adjacent pages")

    singleImage = concatenateImages(transformedImageToMerge)

    with open("testfile.png", "wb") as imageOutput:#NamedTemporaryFile(suffix=".png") as imageOutput:
        imageOutput.write(singleImage.tobytes())

    if progressBar:
        progressBar.hide()
    return imageOutput.name # will eventually return string representing the location of the dir Francesca is using to read in cells and

print(handleColumnGUI("C:/Users/jrp32/PycharmProjects/Group_Project_IB-Delta/imagePreprocessing/Deprecated/OldImagePreprocessing/images/scantest.pdf", 2, None))