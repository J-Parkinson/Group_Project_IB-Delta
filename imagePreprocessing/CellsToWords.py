import numpy as np
from dataStructures.logbookScan import Word, CellOfWords
from scipy import ndimage

def cellsToWords(cells, width):
    '''
    :param cells: [CellOfWords], with words attribute a list of Word objects of length 1 (image of the entire cell)
    :param width: Convolution width, proportional to the page width
    :return: [CellOfWords], with words attribute a list of Word objects where each Word corresponds to a word detected in the cell
    '''
    newCells = []
    maxRow = 0
    maxCol = 0
    for x in cells:
        newp, row, col = cellToWords(x, width)
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
    arrayToUse = np.ones(width)
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
    toRemove = [-8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7]
    newImage = image
    if newImage.shape[0] > 8:
        newImage = np.delete(newImage, toRemove[4::11], 0)
    if newImage.shape[1] > 4:
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
