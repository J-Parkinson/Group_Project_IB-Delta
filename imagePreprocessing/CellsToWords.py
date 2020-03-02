import numpy as np
from dataStructures.logbookScan import Word, CellOfWords
from scipy import ndimage

def cellsToWords(cells, width):
    '''
    PRECONDITIONS:
        - Each CellOfWords must have a list of Words (words) of length 1, where the Word's image is the image is the
    :param cells: [CellOfWords]
    :param width: Convolution width, proportional to the page width
    :return: [CellOfWords], with words attribute a list of Word objects where each Word corresponds to a word detected in the cell
    '''
    newCells = []
    maxRow = 0
    maxCol = 0
    for x in cells:
        # goes through each cell in the list and splits into words
        newp, row, col = cellToWords(x, width)

        # calculates number of rows and columns in the entire list of cells
        maxRow = max(row, maxRow)
        maxCol = max(col, maxCol)
        newCells.append(newp)

    return newCells, maxRow, maxCol

def cellToWords(cellOfWords, width):
    '''
    :param cellOfWords: A single CellOfWords object, where the first Word's image attribute is the image of the entire cell
    :param width: Convolution width, proportional to the page width
    :return: A single CellOfWords object, where the list of Word objects corresponds to the words found in the cell
    '''
    newWords = []

    # Takes the image of the cell from the CellOfWord object
    cell = cellOfWords.words[0].image
    row = cellOfWords.row
    col = cellOfWords.col

    # Strips cell of edges and then converts to a list of row images
    rows = cellToRows(stripCell(cell), width)

    for rowArr in rows:
        # Goes through each row of words in the cell and splits into an array of words
        words = rowToWords(rowArr, width)
        for word in words:
            # Goes through each word in the list of words, removes whitespace, and eliminates small marks
            if word.shape[0]>0 and word.shape[1]>0:
                newWord = removeWhiteSpaceFromWord(word)
                if newWord.shape[0]>5 and newWord.shape[1]>5:
                    newWords.append(newWord)

    newWordList = []
    for x in newWords:
        # Turns images of words into Word objects
        newWordList.append(Word(x, row, col))

    # Returns a new cell with a list of words found in the cell
    return CellOfWords(newWordList, row, col), row, col



def rowToWords(row, width):
    '''
    :param row: One npArray (image), which represents a row of words within a cell
    :param width: Convolution width, proportional to the page width
    :return: List of npArrays (images) corresponding to the words found within the row
    '''
    # Flattens the array into a vertical sum
    colVals = np.sum(row, axis=0)

    # Convolves the summation array (performs a moving average to smooth out peaks and troughs)
    arrayToUse = np.ones(int(width // 100))
    valCols = ndimage.convolve1d(colVals, arrayToUse, mode="nearest")

    # Determines where white gaps are in the image, and uses these to split the image into words
    maxValRow = np.amax(valCols)
    gapsHere = np.argwhere(valCols >= maxValRow).flatten()
    cols = np.array_split(row, gapsHere, axis=1)

    # Filters out the small marks/empty columns
    cols = [x for x in cols if (x.shape[1] > 1 and x.shape[0]>1)]
    return cols



def cellToRows(cell, width):
    '''
    :param cell: NpArray (image) of cell
    :return: List of npArrays (images) of rows of words within cells
    '''
    # Flattens the array into a horizontal sum
    rowVals = np.sum(cell, axis=1)

    # Convolves the summation array (performs a moving average to smooth out peaks and troughs)
    arrayToUse = np.ones(int(width // 100))
    valRows = ndimage.convolve1d(rowVals, arrayToUse, mode="nearest")

    # Filters out rows that are (mostly) made up of white pixels, need 0.97 because of letter tails
    maxValRow = np.amax(valRows)
    gapsHere = np.argwhere(valRows>=maxValRow*0.97).flatten()
    rows = np.array_split(cell, gapsHere, axis=0)

    # Filters out the small marks/empty columns
    rows = [row for row in rows if (row.shape[0] > 1 and row.shape[1]>1)]
    return rows

def stripCell(image):
    '''
    :param image: Image to be stripped of top & bottom rows and left & right columns
    :return: Image with edges stripped
    '''
    toRemove = []
    newImage = image

    # Adds row indices to be deleted, i.e. 4 from the top and 4 from the bottom of the image
    for x in range(newImage.shape[0]):
        if x - 1 < min(4, newImage.shape[0]) or x - 1 > max(newImage.shape[0] - 5, 0):
            toRemove.append(x)

    # Removes the leading and trailing rows from the image
    if newImage.shape[0] > 8:
        newImage = np.delete(newImage, toRemove, 0)
    toRemove = []

    # Adds column indices to be deleted, i.e. 8 from the left and 8 from the right of the image
    for x in range(newImage.shape[1]):
        if x - 1 < min(8, newImage.shape[1]) or x - 1 > max(newImage.shape[1] - 9, 0):
            toRemove.append(x)

    # Removes the leading and trailing columns from the image
    if newImage.shape[1] > 8:
        newImage = np.delete(newImage, toRemove, 1)
    return newImage


def removeWhiteSpaceFromWord(word):
    '''
    :param word: NpArray (image) of word
    :return: NpArray (image) of word with whitespace stripped from edges
    '''
    # Flattens the array into a horizontal sum
    rowVals = np.sum(word, axis=1)
    maxValRow = np.amax(rowVals)

    # Removes white rows from the image
    whiteRows = np.argwhere(rowVals==maxValRow).flatten()
    currentArray = np.delete(word, whiteRows, axis=0)

    if currentArray.size != 0:
        # Flattens the array into a vertical sum
        colVals = np.sum(currentArray, axis=0)
        maxValCol = np.amax(colVals)

        # Removes the leading whitespace of the word
        while (len(colVals) > 0) and (colVals[0] >= maxValCol):
            currentArray = np.delete(currentArray, 0, axis=1)
            colVals = np.delete(colVals, 0)

        # Removes the trailing whitespace of the word
        while (len(colVals) > 0) and (colVals[-1] >= maxValCol):
            currentArray = np.delete(currentArray, -1, axis=1)
            colVals = np.delete(colVals, -1)

    return currentArray

