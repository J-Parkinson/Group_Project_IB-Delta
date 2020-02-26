from imagePreprocessing.imageScanningAndPreprocessing import splitCellsAndNormaliseFromArray
from imagePreprocessing.CellsToWords import cellsToWords
from neuralNetwork.NeuralNetworkCode.src.toCall import forFrontend
from pdf2image import convert_from_path as ReadPDF
from numpy import array
from scratchSpaces.jamesScratchSpace.matrix_to_csv import matrix_to_csv
# Jacks code to get pdfs/images from frontend
# Abi's code to convert cells to words ([CellOfWords], numberOfRows, numberOfCols)
# Francesca [[String]] for James
# Jame

class Lala:
    lala = [['Argyresthia 09352', ' " " " " '],
            ['" " "', 'Argyresthia 09353'],
            ['" " "', 'Argyresthia 09352']]

def printListOfCellOfWords(lst):
    return "[" + ", \n".join([str(x) for x in lst]) + "]"

def createCSVFile(pdfLocation, columnLocations = [], noPageSpread=1):
    # Jack's splitCellsAndNormalise returns [CellOfWords]
    #TODO: ADD SUPPORT FOR PAGE SPREADS
    allImages = ReadPDF(pdfLocation, dpi=400)
    for x, page in enumerate(allImages):
        image = array(page)

        #Jack's code to find rows, split
        cellOfWordsList = splitCellsAndNormaliseFromArray(image, colLocs=columnLocations, perPageSpread=noPageSpread)

        print("Cell of Words List:" , printListOfCellOfWords(cellOfWordsList))

        # Abi's CellsToWords
        wordListEncoded, maxRow, maxCol = cellsToWords(cellOfWordsList)
        abi = cellsToWords(cellOfWordsList)

        # Francesca's neuralNetOutput
        wordsDecoded = forFrontend(abi)

        print(wordsDecoded)


#createCSVFile("C:/Users/Francesca/Documents/Cambridge University/Year IB/Group_Project_IB-Delta/imagePreprocessing/images/scantest2.pdf", columnLocations=[400, 848, 1805, 2239, 2678])
createCSVFile('.../imagePreprocessing/images/scantest2.pdf', columnLocations=[400, 848, 1805, 2239, 2678])



#matrix_to_csv(Lala.lala, "C:/Users/Francesca/Book1.csv")


