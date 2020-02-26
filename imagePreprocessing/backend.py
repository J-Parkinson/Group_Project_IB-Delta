from imagePreprocessing.imageScanningAndPreprocessing import splitCellsAndNormaliseFromArray
from imagePreprocessing.CellsToWords import cellsToWords
from pdf2image import convert_from_path as ReadPDF
from numpy import array
# Jacks code to get pdfs/images from frontend
# Abi's code to convert cells to words ([CellOfWords], numberOfRows, numberOfCols)
# Francesca [[String]] for James
# Jame

def createCSVFile(pdfLocation, columnLocations):
    # Jack's splitCellsAndNormalise returns [CellOfWords]
    allImages = ReadPDF(pdfLocation, dpi=400)
    for x, page in enumerate(allImages):
        image = array(page)

        #Jack's code to find rows, split
        cellOfWords = splitCellsAndNormaliseFromArray(image, columnLocations)

        # Abi's CellsToWords
        wordList = cellsToWords(cellOfWords)

        # Francesca's neuralNetOutput



