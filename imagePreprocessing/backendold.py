from imagePreprocessing.imageScanningAndPreprocessing import splitCellsAndNormaliseFromArray, concatenateImages
from imagePreprocessing.CellsToWords import cellsToWords
from neuralNetwork.NeuralNetworkCode.src.toCall import forFrontend
from pdf2image import convert_from_path as ReadPDF
from numpy import array
import numpy as np
from PIL import Image
from scratchSpaces.jamesScratchSpace.matrix_to_csv import matrix_to_csv
# Jacks code to get pdfs/images from frontend
# Abi's code to convert cells to words ([CellOfWords], numberOfRows, numberOfCols)
# Francesca [[String]] for James
# Jame

class Lala:
    lala = [['Argyresthia 09352', '" " "'],
            ['" " "', 'Argyresthia 09352'],
            ['" " "', 'Argyresthia 09352']]

def printListOfCellOfWords(lst):
    return "[" + ", \n".join([str(x) for x in lst]) + "]"

def codeToMergeImages(imageList):
    newImages = map(lambda x: Image.fromarray(x), imageList)
    mergedImage = concatenateImages(newImages)
    return array(mergedImage)

def createCSVFile(pdfLocation, columnLocations = [], widthOfPreviewImage=1, noPageSpread=1):
    # Jack's splitCellsAndNormalise returns [CellOfWords]
    allImages = ReadPDF(pdfLocation, dpi=400)
    percentageColLocations = array(columnLocations) / widthOfPreviewImage

    buffer = []

    for x, page in enumerate(allImages):
        image = array(page)
        resultingImage = image
        if (noPageSpread > 1):
            buffer.append(image)
            if (len(buffer) == noPageSpread):
                resultingImage = codeToMergeImages(buffer)
                buffer = []

                normalisedColLocations = list((percentageColLocations*(resultingImage.shape[1])).astype(int))
                print(columnLocations, normalisedColLocations)
                # Jack's code to find rows, split
                cellOfWordsList = splitCellsAndNormaliseFromArray(resultingImage, colLocs=normalisedColLocations)

                print("Cell of Words List:", printListOfCellOfWords(cellOfWordsList))

                # Abi's CellsToWords
                wordListEncoded, maxRow, maxCol = cellsToWords(cellOfWordsList)

                # Francesca's neuralNetOutput
                wordsDecoded = forFrontend(wordListEncoded)

                print(wordsDecoded)
        else:
            normalisedColLocations = list((percentageColLocations * (resultingImage.shape[1])).astype(int))
            print(columnLocations, normalisedColLocations)
            # Jack's code to find rows, split
            cellOfWordsList = splitCellsAndNormaliseFromArray(resultingImage, colLocs=normalisedColLocations)

            print("Cell of Words List:", printListOfCellOfWords(cellOfWordsList))

            # Abi's CellsToWords
            wordListEncoded, maxRow, maxCol = cellsToWords(cellOfWordsList)

            # Francesca's neuralNetOutput
            wordsDecoded = forFrontend(wordListEncoded)

            print(wordsDecoded)




createCSVFile("C:\\Users\Jack\Documents\Cambridge University\Year IB\Group_Project_IB-Delta\imagePreprocessing\images\scantest2.pdf", columnLocations=[400, 848, 1805, 2239, 2678], widthOfPreviewImage=3122)




#matrix_to_csv(Lala.lala, "C:/Users/Francesca/Book1.csv")


