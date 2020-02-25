import numpy as np
from dataStructures.logbookScan import Word, CellOfWords
from scipy import ndimage
import cv2 as cv2

def cellsToWords(cells):
    newCells = []
    for x in cells:
        newCells.append(cellToWords(x))
    return newCells

def cellToWords(cellOfWords): # takes one CellOfWords
    newWords = []
    cell = cellOfWords.words[0].image
    row = cellOfWords.row
    col = cellOfWords.col
    rows = cellToRows(cell) # LIST OF NP ARRAYS
    for row in rows: # NP ARRAY
        words = rowToWords(row)
        count = 0
        for word in words:
            if word.shape[0]>0 and word.shape[1]>0:
                newWord = removeWhiteSpaceFromWord(word,count)
                if  newWord.shape[0]>2 and newWord.shape[1]>2:
                    newWords.append(newWord)
            count+=1

    newWordList = []
    for x in newWords:
        newWordList.append(Word(x, row, col))
    return CellOfWords(newWordList, row, col)



def rowToWords(row):
    colVals = np.sum(row, axis=0)
    valCols = ndimage.convolve1d(colVals, np.array([1, 1, 1, 1, 1]), mode="nearest")
    maxValRow = np.amax(valCols)
    wordsHere = np.argwhere(valCols >= maxValRow).flatten()
    cols = np.array_split(row, wordsHere, axis=1)
    cols = [x for x in cols if (x.shape[1] > 1 and x.shape[0]>1)]
    return cols



def cellToRows(cell):
    rowVals = np.sum(cell, axis=1)
    valRows = ndimage.convolve1d(rowVals, np.array([1, 1, 1, 1, 1]), mode="nearest")
    maxValRow = np.amax(valRows)
    wordsHere = np.argwhere(valRows>=maxValRow*0.97).flatten()
    rows = np.array_split(cell, wordsHere, axis=0)
    rows = [row for row in rows if (row.shape[0] > 1 and row.shape[1]>1)]
    return rows



def removeWhiteSpaceFromWord(word,i):
    rowVals = np.sum(word, axis=1)
    maxValRow = np.amax(rowVals)

    whiteRows = np.argwhere(rowVals==maxValRow).flatten()
    currentArray = np.delete(word, whiteRows, axis=0)
    if currentArray.size != 0:
        colVals = np.sum(currentArray, axis=0)
        maxValCol = np.amax(colVals)

        while colVals[0] >= maxValCol:
            currentArray = np.delete(currentArray, 0, axis=1)
            colVals = np.delete(colVals, 0)

        while colVals[-1] >= maxValCol:
            currentArray = np.delete(currentArray, -1, axis=1)
            colVals = np.delete(colVals, -1)

    return currentArray
