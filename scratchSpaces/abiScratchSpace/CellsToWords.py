import numpy as np
import scipy.misc
from dataStructures.logbookScan import Word, CellOfWords
from scipy import ndimage

# list of 2d numpy arrays (each cell is a numpy array)
# replace 2D array with list of 2D array
from scipy import ndimage
import cv2 as cv2


# list of 2d numpy arrays (each cell is a numpy array)
# replace 2D array with list of 2D array

#################################################################
imgList = []
paths = ["../../imagePreprocessing/Deprecated/OldImagePreprocessing/images/segmentedImagesOut/Page 51/cell-0-1.png","../../imagePreprocessing/Deprecated/OldImagePreprocessing/images/segmentedImagesOut/Page 16/cell-1-5.png","../../imagePreprocessing/Deprecated/OldImagePreprocessing/images/segmentedImagesOut/Page 25/cell-1-2.png", "../../imagePreprocessing/Deprecated/OldImagePreprocessing/images/segmentedImagesOut/Page 13/cell-1-2.png", "../../imagePreprocessing/Deprecated/OldImagePreprocessing/images/segmentedImagesOut/Page 13/cell-4-2.png"]
for i in paths:
    row = i[-3]
    col = i[-1]
    img = cv2.imread(i)
    arr = np.array(img)
    height, width, channels = img.shape
    arr.shape = (height, width, channels)
    arr = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
    imgList.append(CellOfWords([Word(arr, row, col)], row, col))
#################################################################

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



x = cellsToWords(imgList)

count = 0
for y in x:
    count2 = 0
    print(count, x[count].words)
    for z in y.words:
        cv2.imwrite('test-'+str(count)+'-'+str(count2)+'.png', z.image)
        count2+=1
    count+=1
