import numpy as np
from dataStructures.logbookScan import Word, CellOfWords
from scipy import ndimage

# list of 2d numpy arrays (each cell is a numpy array)
# replace 2D array with list of 2D array


# python list of python lists of 2D numpy array

def cellsToWords(cells):
    cellsOfWords = []
    for cell in cells:
        cellsOfWords.append(cellToWords(cell))
    return cellsOfWords
def cellToWords(cell): # takes one CellOfWords
    row = cell.row
    col = cell.col
    cellImage = cell.words[0].image
    newWords = []
    rows = cellToRows(cellImage)
    for row in rows:
        words = rowToWords(row)
        for word in words:
            newWords.append(removeWhiteSpaceFromWord(word))

    newCell = CellOfWords([], row, col)
    for x in newWords:
        word = Word(x, row, col)
        newCell.words.append(word)
    return newCell

def rowToWords(row):
    columnVals = np.sum(row, axis=0)
    maxValCol = np.amax(columnVals)
    x = ndimage.convolve1d(columnVals, np.array([1, 1, 1, 1]), mode="nearest")

    indicesToSplit = np.array(np.where(x > 0.95 * maxValCol))
    indicesToSplit = np.ndarray.flatten(indicesToSplit)

    words = np.split(x, indicesToSplit)
    words = [word for word in words if word.size > 0]
    return words


def cellToRows(cell):
    rowVals = np.sum(cell, axis=1)
    maxValRow = np.amax(rowVals)
    x = ndimage.convolve1d(rowVals, np.array([1, 1, 1, 1]), mode="nearest")

    indicesToSplit = np.array(np.where(x > 0.95 * maxValRow))
    indicesToSplit = np.ndarray.flatten(indicesToSplit)

    rows = np.split(x, indicesToSplit)
    rows = [row for row in rows if row.size > 0]
    return rows


def removeWhiteSpaceFromWord(word):
    horizontalVals = np.sum(word, axis=1)
    maxValHorizontal = np.amax(horizontalVals)
    x = ndimage.convolve1d(horizontalVals, np.array([1, 1, 1, 1]), mode="nearest")

    indicesToSplit = np.array(np.where(x > 0.95 * maxValHorizontal))
    indicesToSplit = np.ndarray.flatten(indicesToSplit)

    word = np.split(x, indicesToSplit)
    word = [row for row in rows if row.size > 0]
    return word
