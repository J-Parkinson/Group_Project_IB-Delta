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

    #
    cell = cellOfWords.words[0].image
    row = cellOfWords.row
    col = cellOfWords.col
    rows = cellToRows(stripCell(cell)) # LIST OF NP ARRAYS
    for rowArr in rows: # NP ARRAY
        words = rowToWords(rowArr, width)
        for word in words:
            if word.shape[0]>0 and word.shape[1]>0:
                newWord = removeWhiteSpaceFromWord(word)
                if  (newWord.shape[1]*3> newWord.shape[0]) and  (newWord.shape[0]>6 and newWord.shape[1]>6):
                    newWords.append(newWord)

    newWordList = []
    for x in newWords:
        newWordList.append(Word(x, row, col))
    return CellOfWords(newWordList, row, col), row, col



def rowToWords(row, width):
    '''
    :param row: One npArray (image), which represents a row of words within a cell
    :param width: Convolution width, proportional to the page width
    :return: List of npArrays (images) corresponding to the words found within the row
    '''
    colVals = np.sum(row, axis=0)
    arrayToUse = np.ones(int(width)//75)
    valCols = ndimage.convolve1d(colVals, arrayToUse, mode="nearest")
    maxValRow = np.amax(valCols)
    wordsHere = np.argwhere(valCols >= maxValRow).flatten()
    cols = np.array_split(row, wordsHere, axis=1)
    cols = [x for x in cols if (x.shape[1] > 1 and x.shape[0]>1)]
    return cols


def stripCell(image):
    '''
    :param image: Image to be stripped of top & bottom rows and left & right columns
    :return: Image with edges stripped
    '''
    toRemove = []
    newImage = image
    for x in range(newImage.shape[0]):
        if x - 1 < min(4, newImage.shape[0]) or x - 1 > max(newImage.shape[0] - 5, 0):
            toRemove.append(x)
    if newImage.shape[0] > 8:
        newImage = np.delete(newImage, toRemove, 0)
    toRemove = []
    for x in range(newImage.shape[1]):
        if x - 1 < min(8, newImage.shape[1]) or x - 1 > max(newImage.shape[1] - 9, 0):
            toRemove.append(x)
    if newImage.shape[1] > 8:
        newImage = np.delete(newImage, toRemove, 1)
    return newImage


def cellToRows(cell):
    '''
    :param cell: NpArray (image) of cell
    :return: List of npArrays (images) of rows of words within cells
    '''
    rowVals = np.sum(cell, axis=1)
    arrayToUse = np.ones(4)
    valRows = ndimage.convolve1d(rowVals, arrayToUse, mode="nearest")
    maxValRow = np.amax(valRows)
    wordsHere = np.argwhere(valRows>=maxValRow*0.97).flatten()
    rows = np.array_split(cell, wordsHere, axis=0)
    rows = [row for row in rows if (row.shape[0] > 1 and row.shape[1]>1)]
    return rows



def removeWhiteSpaceFromWord(word):
    '''
    :param word: NpArray (image) of word
    :return: NpArray (image) of word with whitespace stripped from edges
    '''
    rowVals = np.sum(word, axis=1)
    maxValRow = np.amax(rowVals)

    whiteRows = np.argwhere(rowVals==maxValRow).flatten()
    currentArray = np.delete(word, whiteRows, axis=0)
    if currentArray.size != 0:
        colVals = np.sum(currentArray, axis=0)
        maxValCol = np.amax(colVals)

        while (len(colVals) > 0) and (colVals[0] >= maxValCol):
            currentArray = np.delete(currentArray, 0, axis=1)
            colVals = np.delete(colVals, 0)

        while (len(colVals) > 0) and (colVals[-1] >= maxValCol):
            currentArray = np.delete(currentArray, -1, axis=1)
            colVals = np.delete(colVals, -1)

    return currentArray
