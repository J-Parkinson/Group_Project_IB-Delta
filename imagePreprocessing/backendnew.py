from imagePreprocessing.imageScanningAndPreprocessing import normaliseImageToArray, calculateRowsAndSplit, concatenateImages, handleColumnGUI
from imagePreprocessing.CellsToWords import cellsToWords
from neuralNetwork.src.Model import Model, DecoderType
from neuralNetwork.src.main import inferEverything, makeStringFromOneCell
from pdf2image import convert_from_path as ReadPDF
from numpy import array
from cv2 import resize, INTER_NEAREST
import numpy as np
from PIL import Image, ImageDraw
from utils.csv.matrix_to_csv import matrix_to_csv
import pathlib

class FilePaths:
    "filenames and paths to data"
    path = pathlib.Path(__file__).parent
    fnCharList = path / '..'/ 'neuralNetwork' / 'model' / 'charList.txt'
    fnAccuracy = path / '..'/ 'neuralNetwork' / 'model' / 'accuracy.txt'# '../neuralNetwork/model/accuracy.txt'

class Lala:
    '''Used for test output of table'''
    lala = [['Argyresthia 09352', '" " "'],
            ['" " "', 'Argyresthia 09352'],
            ['" " "', 'Argyresthia 09352']]

def printListOfCellOfWords(lst):
    return "[" + ", \n".join([str(x) for x in lst]) + "]"

def codeToMergeImages(imageList):
    """
    codeToMergeImages
    Converts all array cells to PIL images, then concatenates and creates new numpy array of image
    :param imageList: list of numpy 2d array images
    :type imageList: numpy.array(2d)[]
    :return: new numpy 2d image
    :rtype: numpy.array(2d)
    """
    newImages = map(lambda x: Image.fromarray(x), imageList)
    mergedImage = concatenateImages(newImages)
    return array(mergedImage)

#Need to fix issue where when resizing the pages will resize as per ratios of y axis


def colLocToPagePerc(location, cumLoc):
    if location < 0:
        raise ValueError
    for x, upper in enumerate(cumLoc):
        if upper > location:
            page = x
            lower = cumLoc[x-1]
            perc = (location - lower) / (upper - lower)
            return (page, perc)
    raise ValueError

def colPercToNewPage(location, pagePerc, newPage):
    if location < 0 or location >= len(pagePerc):
        raise ValueError
    page = pagePerc[location][0]
    perc = pagePerc[location][1]
    return newPage[page] + ((newPage[page+1] - newPage[page]) * perc)


def columnTransform(oldPageDimensions, newPageDimensions, columnLocations):
    #First calculate page and percentage location of each column
    oldPageWidthCumulative = np.cumsum(np.array([0] + [val[1] for val in oldPageDimensions]))
    smallestHeight = min([array[0] for array in newPageDimensions])
    print(newPageDimensions)
    adjustedNewPageDimensions = [(val[0], val[1] * smallestHeight / val[0]) for val in newPageDimensions]
    newPageWidthCumulative = np.cumsum(np.array([0] + [val[1] for val in adjustedNewPageDimensions]))
    pagePercentages = [colLocToPagePerc(loc, oldPageWidthCumulative) for loc in columnLocations]
    #Then apply proportions to new pages
    newPageLocs = [colPercToNewPage(n, pagePercentages, newPageWidthCumulative) for n in range(len(columnLocations))]
    return newPageLocs

#def displayImageForTestingPurposes(image, cols):
#
#    for col in cols:
#        ImageDraw.Draw(img).line([(col, 0), (col, img.height - 1)], (255, 0, 0))
#    img.show()



def createTable(pdfLocation, columnLocations=[], rowLocations = [], widthOfPreviewImage=1,
                heightOfPreviewImage=1, noPageSpread=1):
    """
    Takes in a pdf location string, column locations on where to split, row locations specifying top and bottom of page excluding headers
    :param pdfLocation: String denoting path of file
    :type pdfLocation: str
    :param columnLocations: Locations in pixels of columns on the smaller preview image - we scale up here to size of each merged image.
    :type columnLocations: int[]
    :param rowLocations: List of [top of records, bottom of records]
    :type rowLocations: int[]
    :param widthOfPreviewImage: Used for scaling of col/row locs,  integer in terms of pixels
    :type widthOfPreviewImage: int
    :param heightOfPreviewImage: Used for scaling of col/row locs,  integer in terms of pixels - aspect ratio may not be same
    :type heightOfPreviewImage: int
    :param noPageSpread: no of pages that are required next to each other to complete a record
    :type noPageSpread: int
    :return: table of guessed words ready for PDF conversion
    :rtype: str[][][]
    """
    model = Model(open(FilePaths.fnCharList).read(), DecoderType.BestPath, mustRestore=True,
                  dump=None)  # change dump to

    # Jack's splitCellsAndNormalise returns [CellOfWords]
    allImages = ReadPDF(pdfLocation, dpi=400)

    buffer = []
    wordsDecoded = []

    # First we need to calculate the first page spread dimensions
    initialPageSpreadDimensions = handleColumnGUI(pdfLocation, noPageSpread)[1]

    for x, page in enumerate(allImages):
        image = array(page)
        if (noPageSpread > 1):
            buffer.append(image)
            if (len(buffer) == noPageSpread):

                '''scaleFactorX = resultingImage.shape[0] / widthOfPreviewImage
                scaleFactorY = resultingImage.shape[1] / heightOfPreviewImage
                resultingImage = resultingImage[(columnLocations[0] * scaleFactorX):(columnLocations[-1] * scaleFactorX), (rowLocations[0] * scaleFactorY):(rowLocations[1] * scaleFactorY)]
                '''
                # Jack's code to find rows, split
                buffer = [normaliseImageToArray(image) for image in buffer]

                imageCoords = [image.shape[::-1] for image in buffer]

                normalisedCols = columnTransform(initialPageSpreadDimensions, imageCoords, columnLocations)

                resultingImage = codeToMergeImages(buffer)

                displayImageForTestingPurposes(resultingImage, normalisedCols)

                cellOfWordsList = calculateRowsAndSplit(resultingImage, normalisedCols)

                # Abi's CellsToWords
                inputs = cellsToWords(cellOfWordsList, resultingImage.shape[1] / noPageSpread)

                # Francesca's neuralNetOutput
                wordsDecoded += inferEverything(model, inputs)
                print(wordsDecoded)
                buffer = []
        else:
            '''scaleFactorX = resultingImage.shape[0] / widthOfPreviewImage
            scaleFactorY = resultingImage.shape[1] / heightOfPreviewImage
            resultingImage = resultingImage[(columnLocations[0] * scaleFactorX):(columnLocations[-1] * scaleFactorX),
                             (rowLocations[0] * scaleFactorY):(rowLocations[1] * scaleFactorY)]'''

            # Jack's code to find rows, split
            norm = normaliseImageToArray(image)

            norm = resize(norm, dsize=initialPageSpreadDimensions[0], interpolation=INTER_NEAREST)

            cellOfWordsList = calculateRowsAndSplit(norm, initialPageSpreadDimensions)

            # Abi's CellsToWords
            inputs = cellsToWords(cellOfWordsList, resultingImage.shape[1] / noPageSpread)

            # Francesca's neuralNetOutput
            wordsDecoded += inferEverything(model, inputs)

    return wordsDecoded

#createTable('../imagePreprocessing/images/scantest2.pdf', columnLocations=[375, 790, 1690, 2100, 2520], widthOfPreviewImage=3122)


