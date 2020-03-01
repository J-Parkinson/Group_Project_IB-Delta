from imagePreprocessing.imageScanningAndPreprocessing import splitCellsAndNormaliseFromArray, concatenateImages
from imagePreprocessing.CellsToWords import cellsToWords
from neuralNetwork.src.Model import Model, DecoderType
from neuralNetwork.src.main import inferEverything, makeStringFromOneCell
from pdf2image import convert_from_path as ReadPDF
from numpy import array
import numpy as np
from PIL import Image
from utils.csv.matrix_to_csv import matrix_to_csv
import pathlib

class FilePaths:
    "filenames and paths to data"
    path = pathlib.Path(__file__).parent
    fnCharList = path / '..'/ 'neuralNetwork' / 'model' / 'charList.txt'
    fnAccuracy = path / '..'/ 'neuralNetwork' / 'model' / 'accuracy.txt'# '../neuralNetwork/model/accuracy.txt'

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
    print(open(FilePaths.fnAccuracy).read())
    model = Model(open(FilePaths.fnCharList).read(), DecoderType.BestPath, mustRestore=True,
                  dump=None)  # change dump to

    # Jack's splitCellsAndNormalise returns [CellOfWords]
    allImages = ReadPDF(pdfLocation, dpi=400)
    percentageColLocations = array(columnLocations) / widthOfPreviewImage

    buffer = []
    wordsDecoded = []

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
                inputs = cellsToWords(cellOfWordsList, int(resultingImage.shape[1]/noPageSpread))

                # Francesca's neuralNetOutput
                wordsDecoded += inferEverything(model, inputs)

                print("PLS WORK")
                print(wordsDecoded)
        else:
            normalisedColLocations = list((percentageColLocations * (resultingImage.shape[1])).astype(int))
            print(columnLocations, normalisedColLocations)
            # Jack's code to find rows, split
            cellOfWordsList = splitCellsAndNormaliseFromArray(resultingImage, colLocs=normalisedColLocations)

            '''for x, word in enumerate(cellOfWordsList):
                image = Image.fromarray(word.words[0].image)
                image.save("segmentedcells/cell" + str(x) + ".png")'''



            print("Cell of Words List:", printListOfCellOfWords(cellOfWordsList))

            # Abi's CellsToWords
            print("width:", resultingImage.shape[1]/noPageSpread)
            inputs = cellsToWords(cellOfWordsList, resultingImage.shape[1]/noPageSpread)
            listOfCells, cols, rows = inputs
            print(f"THE NUMBER OF COLS IS \n", cols)
            print(f"THE NUMBER OF ROWS IS %d\n", rows)
            print("FIRST CELL")
            print(makeStringFromOneCell(model, listOfCells[6]))
            print(makeStringFromOneCell(model, listOfCells[12]))
            print(makeStringFromOneCell(model, listOfCells[18]))
            print(makeStringFromOneCell(model, listOfCells[24]))

            '''for cellno, cell in enumerate(inputs[0]):
                for wordno, word in enumerate(cell.words):
                    image = Image.fromarray(word.image)
                    image.save("segmentedwords/word " + str(word.row) + " - " + str(word.col) + " - " + str(wordno) + ".png")'''

            # Francesca's neuralNetOutput
            wordsDecoded += inferEverything(model, inputs)
            print("LAST PAGE")
            print(wordsDecoded)

            matrix_to_csv(wordsDecoded, "test10.csv")

    matrix_to_csv(wordsDecoded, "test10.csv")
    return


def createTable(pdfLocation, columnLocations=[], rowLocations = [], widthOfPreviewImage=1,
                heightOfPreviewImage =1, noPageSpread=1):
    print(open(FilePaths.fnAccuracy).read())
    model = Model(open(FilePaths.fnCharList).read(), DecoderType.BestPath, mustRestore=True,
                  dump=None)  # change dump to

    # Jack's splitCellsAndNormalise returns [CellOfWords]
    allImages = ReadPDF(pdfLocation, dpi=400)
    percentageColLocations = array(columnLocations) / widthOfPreviewImage

    buffer = []
    wordsDecoded = []
    print("yes")

    for x, page in enumerate(allImages):
        image = array(page)
        resultingImage = image
        if (noPageSpread > 1):
            buffer.append(image)
            if (len(buffer) == noPageSpread):
                resultingImage = codeToMergeImages(buffer)
                scaleFactorX = resultingImage.shape[0] / widthOfPreviewImage
                scaleFactorY = resultingImage.shape[1] / heightOfPreviewImage
                resultingImage = resultingImage[(columnLocations[0] * scaleFactorX):(columnLocations[-1] * scaleFactorX), (rowLocations[0] * scaleFactorY):(rowLocations[1] * scaleFactorY)]
                buffer = []

                normalisedColLocations = list((percentageColLocations * (resultingImage.shape[1])).astype(int))
                print(columnLocations, normalisedColLocations)
                # Jack's code to find rows, split
                cellOfWordsList = splitCellsAndNormaliseFromArray(resultingImage, colLocs=normalisedColLocations)

                print("Cell of Words List:", printListOfCellOfWords(cellOfWordsList))

                # Abi's CellsToWords
                inputs = cellsToWords(cellOfWordsList, resultingImage.shape[1] / noPageSpread)

                # Francesca's neuralNetOutput
                wordsDecoded += inferEverything(model, inputs)
                print("PLS WORK")
                print(wordsDecoded)
        else:
            '''scaleFactorX = resultingImage.shape[0] / widthOfPreviewImage
            scaleFactorY = resultingImage.shape[1] / heightOfPreviewImage
            resultingImage = resultingImage[(columnLocations[0] * scaleFactorX):(columnLocations[-1] * scaleFactorX),
                             (rowLocations[0] * scaleFactorY):(rowLocations[1] * scaleFactorY)]'''
            normalisedColLocations = list((percentageColLocations * (resultingImage.shape[1])).astype(int))
            print(columnLocations, normalisedColLocations)
            # Jack's code to find rows, split
            cellOfWordsList = splitCellsAndNormaliseFromArray(resultingImage, colLocs=normalisedColLocations)

            for x, word in enumerate(cellOfWordsList):
                image = Image.fromarray(word.words[0].image)
                image.save("segmentedcells/cell" + str(x) + ".png")

            print("Cell of Words List:", printListOfCellOfWords(cellOfWordsList))

            # Abi's CellsToWords
            print("width:", resultingImage.shape[1] / noPageSpread)
            inputs = cellsToWords(cellOfWordsList, resultingImage.shape[1] / noPageSpread)
            listOfCells, cols, rows = inputs
            print(f"THE NUMBER OF COLS IS \n", cols)
            print(f"THE NUMBER OF ROWS IS %d\n", rows)
            print("FIRST CELL")
            #print(makeStringFromOneCell(model, listOfCells[6]))
            #print(makeStringFromOneCell(model, listOfCells[12]))
            #print(makeStringFromOneCell(model, listOfCells[13]))
            #print(makeStringFromOneCell(model, listOfCells[14]))
            #print(makeStringFromOneCell(model, listOfCells[15]))
            #print(makeStringFromOneCell(model, listOfCells[16]))
            #print(makeStringFromOneCell(model, listOfCells[18]))
            #print(makeStringFromOneCell(model, listOfCells[24]))

            for cellno, cell in enumerate(inputs[0]):
                for wordno, word in enumerate(cell.words):
                    print("segmentedwords/word5 " + str(word.row) + " - " + str(word.col) + " - " + str(wordno) + ".png")
                    img = word.image
                    print("L1")
                    print(len(img))
                    print("L2")
                    print(len(img[0]))
                    image = Image.fromarray(word.image)
                    image.save("segmentedwords/word8 " + str(word.row) + " - " + str(word.col) + " - " + str(wordno) + ".png")
                    #image.show()

            # Francesca's neuralNetOutput
            wordsDecoded += inferEverything(model, inputs)
            print("PLS WORK")
            print(wordsDecoded)

            matrix_to_csv(wordsDecoded, "test16.csv")

    return wordsDecoded



#createCSVFile("C:\\Users\Jack\Documents\Cambridge University\Year IB\Group_Project_IB-Delta\imagePreprocessing\images\scantest2.pdf", columnLocations=[375, 790, 1690, 2100, 2520], widthOfPreviewImage=3122)
#createCSVFile('../imagePreprocessing/images/scantest2.pdf', columnLocations=[375, 790, 1690, 2100, 2520], widthOfPreviewImage=3122)



#createTable("C:\\Users\Jack\Documents\Cambridge University\Year IB\Group_Project_IB-Delta\imagePreprocessing\images\scantest2.pdf", columnLocations=[375, 790, 1690, 2100, 2520], widthOfPreviewImage=3122)
createTable('../imagePreprocessing/images/scantest2.pdf', columnLocations=[375, 790, 1690, 2100, 2520], widthOfPreviewImage=3122)

#matrix_to_csv(Lala.lala, "C:/Users/Francesca/Book1.csv")


