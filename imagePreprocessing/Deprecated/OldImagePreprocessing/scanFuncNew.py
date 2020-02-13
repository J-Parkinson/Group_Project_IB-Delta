# USAGE

from cv2 import waitKey, getStructuringElement, GaussianBlur, Canny, erode, cvtColor, \
    arcLength, COLOR_BGR2GRAY, approxPolyDP, CHAIN_APPROX_SIMPLE, dilate, imread, MORPH_RECT, contourArea, \
    findContours, RETR_LIST, imwrite, merge
from imutils import grab_contours
from matplotlib import pyplot as plt
from numpy import array, zeros, greater, hsplit, vsplit, greater_equal, diff, delete, insert, int32
# import the necessary packages
from pyimagesearch.transform import four_point_transform
from scipy.ndimage import convolve1d
from scipy.signal import argrelextrema
from skimage.filters import threshold_sauvola


def showImage(img, lines=array([]), wait=True):
    plt.plot(img)

    for coord in lines:
        plt.axvline(x=coord)

    if wait:
        plt.show()
        waitKey()
    return


'''def scanImage(source, dest):
    # load the image and compute the ratio of the old height
    # to the new height, clone it, and resize it
    image = imread(source)
    if image is None:
        return
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
    imwrite(dest, transformed)

    return'''


# TODO: Write code to read in column data
# def readColumnData(Column)

def findLinesandNormalise(source, dest=""):
    # load the image and compute the ratio of the old height
    # to the new height, clone it, and resize it
    image = imread(source)
    orig = image.copy()
    # image = resize(image, height=image.shape[0])

    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cvtColor(image, COLOR_BGR2GRAY)
    imwrite(dest + "original.png", gray)
    gray = GaussianBlur(gray, (7, 7), 0)
    edged = Canny(gray, 75, 200)
    imwrite(dest + "edged.png", edged)

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
        transformed = four_point_transform(orig, screenCnt.reshape(4, 2))

    else:
        transformed = orig

    # convert the warped image to grayscale, then threshold it
    # to give it that 'black and white' paper effect
    transformed = cvtColor(transformed, COLOR_BGR2GRAY)
    threshold = threshold_sauvola(transformed, 11, 0.15)
    transformed = (transformed > threshold).astype("uint8") * 255

    '''nlabel, labels, stats, centroids = connectedComponentsWithStats(transformed, connectivity=8)
    print(nlabel, labels, stats, len(centroids))
    biggestComponent = zeros(transformed.shape)

    sizes = stats[:, -1]
    sizessorted = sorted(sizes, reverse=True)
    sizeorder = [sizessorted.index(i) for i in sizes]

    biggestComponent[labels == sizeorder[1]] = 255
    showImage(biggestComponent)'''

    '''value = findContours(transformed, RETR_EXTERNAL, CHAIN_APPROX_TC89_L1)
    cols = map(lambda x: x[0], [approxPolyDP(x, 0.02 * arcLength(x, True), True) for x in grab_contours(value)])

    drawContours(transformed, cnts, -1, (0, 255, 0), 2)
    imwrite("shit.png", transformed)'''

    transformedColour = merge([transformed, transformed, transformed])
    imwrite(dest + "pagelayout.png", transformedColour)
    colLocations = calculateColumns(transformed)
    for i in colLocations:
        transformedColour[:, i] = (255, 0, 0)
        try:
            transformedColour[:, i + 1] = (255, 0, 0)
            # transformedColour[:, i+2] = (255, 0, 0)
        except:
            continue
        try:
            transformedColour[:, i - 1] = (255, 0, 0)
            # transformedColour[:, i - 2] = (255, 0, 0)
        except:
            continue
    # imwrite("images/columns.png", transformedColour)

    # transformedColour = merge([transformed, transformed, transformed])
    rowLocations = calculateRows(transformed)
    for i in rowLocations:
        transformedColour[i] = (255, 0, 0)
        try:
            transformedColour[i + 1] = (255, 0, 0)
            # transformedColour[i+2] = (255, 0, 0)
        except:
            continue
        try:
            transformedColour[i - 1] = (255, 0, 0)
            # transformedColour[i - 2] = (255, 0, 0)
        except:
            continue
    # imwrite("images/rows.png", transformedColour)
    # imwrite("images/rowsandcols.png", transformedColour)
    imwrite(dest + "rowsandcols.png", transformedColour)
    print(dest + "rowsandcols.png")

    cells = splitIntoCells(transformed, rowLocations, colLocations)

    if dest == "":
        dest = "images/out/"

    # for x, image in enumerate(cells):

    #    imwrite(dest + "cell-" + str(x//len(colLocations)) + "-" + str(x % len(colLocations)) + ".png", image)

    return


def splitIntoCells(image, rows, cols):
    splitRows = vsplit(image, rows)

    return [a for b in [hsplit(row, cols) for row in splitRows] for a in b]


# splitRows = vsplit(image, rows)

# return [a for b in [hsplit(row, cols) for row in splitRows] for a in b]


# print(splitIntoCells(array([[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16]]), [1, 3], [1,2]))

def calculateColumns(transformed):
    transformedsumx = transformed.sum(axis=0)
    # print(transformedsumx)
    # showImage(transformedsumx)
    threshold = transformedsumx.max() * 0.99
    columns = zeros(transformedsumx.shape)
    columns[transformedsumx < threshold] = 255
    columns = array(columns).astype(int)
    columns = convolve1d(convolve1d(columns, array([1, 1, 1, 3, 5, 8, 4, 3, 1, 1, 1]), mode="nearest"),
                         array([1, 1, 1, 3, 5, 8, 4, 3, 1, 1, 1]), mode="nearest")
    columnsfiltered = argrelextrema(columns, greater)[0] + 2
    # columnsfiltered = concatenate(([0], columnsfiltered, [transformedsumx.shape[0] - 1]))
    return columnsfiltered


def refactorRows(rowsfiltered):
    rowsdiff = diff(rowsfiltered)
    rowsdiffaverage = (rowsfiltered.max() - rowsfiltered.min()) / (rowsfiltered.shape[0] - 1)

    print("Average:", rowsdiffaverage)

    print("Old:", rowsfiltered)

    # for j in range(0,2):
    i = 0
    while (i < rowsdiff.shape[0]):

        dif = rowsdiff[i]

        if ((0.6 * rowsdiffaverage) > dif or dif > (1.6 * rowsdiffaverage)):

            if ((0.6 * rowsdiffaverage) > dif):
                try:
                    # print(rowsfiltered[i+1])
                    newVal = (rowsfiltered[i] + rowsfiltered[i + 1]) / 2
                    rowsfiltered = delete(rowsfiltered, i + 1)
                    rowsfiltered = delete(rowsfiltered, i)
                    rowsfiltered = insert(rowsfiltered, i, int32(newVal))
                    # print(rowsfiltered)
                    rowsdiff = delete(rowsdiff, i)
                    rowsdiff[i] += dif
                except:
                    continue
                if (i < rowsdiff.shape[0] - 1):
                    i += 1
                continue


            elif (dif > (1.6 * rowsdiffaverage)):
                # print(rowsfiltered[i+1])
                rowsfiltered = insert(rowsfiltered, i + 1, int32(rowsfiltered[i] + rowsdiffaverage))
                # print(rowsfiltered)
                rowsdiff = insert(rowsdiff, i + 1, int32(dif - rowsdiffaverage))

        i += 1

    print("New:", rowsfiltered)

    return rowsfiltered


def calculateRows(transformed):
    transformedsumy = transformed.sum(axis=1)[1:-1].astype("int64")

    tsy2 = convolve1d(convolve1d(transformedsumy, array([1, 1, 1, 3, 5, 8, 4, 3, 1, 1, 1]), mode="nearest"),
                      array([1, 1, 1, 3, 5, 8, 4, 3, 1, 1, 1]), mode="nearest")
    rowsfiltered = argrelextrema(tsy2, greater_equal)[0]

    rowsfiltered = refactorRows(rowsfiltered)

    # Rows are evenly spread along a page by a set interval - let us guess that interval
    # intervals = diff(rowsfiltered)
    # averageInterval = (mode(intervals)[0] + intervals.mean()) / 2
    # return arange(rowsfiltered[0], rowsfiltered[-1], averageInterval, uint16)
    # print(transformedsumy)
    return rowsfiltered

# findLinesandNormalise("images/logbook.png")
# findLinesandNormalise("images/logbook2test.png")
