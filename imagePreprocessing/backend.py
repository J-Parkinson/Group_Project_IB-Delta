from imagePreprocessing.imageScanningAndPreprocessing import splitCellsAndNormaliseFromArray
from imagePreprocessing.CellsToWords import cellsToWords
from neuralNetwork.NeuralNetworkCode.src.toCall import forFrontend
from pdf2image import convert_from_path as ReadPDF
from numpy import array
# Jacks code to get pdfs/images from frontend
# Abi's code to convert cells to words ([CellOfWords], numberOfRows, numberOfCols)
# Francesca [[String]] for James
# Jame

def createCSVFile(pdfLocation, columnLocations, noPageSpread):
    # Jack's splitCellsAndNormalise returns [CellOfWords]
    #TODO: ADD SUPPORT FOR PAGE SPREADS
    allImages = ReadPDF(pdfLocation, dpi=400)
    for x, page in enumerate(allImages):
        page.show()
        image = array(page)

        #Jack's code to find rows, split
        cellOfWords = splitCellsAndNormaliseFromArray(image, columnLocations)

        # Abi's CellsToWords
        wordListEncoded, maxRow, maxCol = cellsToWords(cellOfWords)

        # Francesca's neuralNetOutput
        wordsDecoded = forFrontend(wordListEncoded)

        print(wordsDecoded)


createCSVFile("C:\\Users\Jack\Documents\Cambridge University\Year IB\Group_Project_IB-Delta\imagePreprocessing\images\scantest2.pdf", )



