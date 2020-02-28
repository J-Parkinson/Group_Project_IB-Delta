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
paths = ["../../imagePreprocessing/segmentedcells/cell27.png", "../../imagePreprocessing/segmentedcells/cell28.png", "../../imagePreprocessing/segmentedcells/cell30.png", "../../imagePreprocessing/segmentedcells/cell31.png"]
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

def cellsToWords(cells, width):
    newCells = []
    maxRow = 0
    maxCol = 0
    for x in cells:
        newp, row, col = cellToWords(x, width)
        #maxRow = max(row, maxRow)
        #maxCol = max(col, maxCol)
        newCells.append(newp)

    return newCells, maxRow, maxCol

def cellToWords(cellOfWords, width): # takes one CellOfWords
    newWords = []
    cell = cellOfWords.words[0].image
    row = cellOfWords.row
    col = cellOfWords.col
    rows = cellToRows(cell, width) # LIST OF NP ARRAYS
    for rowArr in rows: # NP ARRAY
        words = rowToWords(rowArr, width)
        for word in words:
            if word.shape[0]>0 and word.shape[1]>0:
                newWord = removeWhiteSpaceFromWord(word)
                if  newWord.shape[0]>4 and newWord.shape[1]>4:
                    newWords.append(newWord)

    newWordList = []
    for x in newWords:
        newWordList.append(Word(x, row, col))
    return CellOfWords(newWordList, row, col), row, col



def rowToWords(row, width):
    colVals = np.sum(row, axis=0)
    #print(width // 100)
    arrayToUse = np.ones(int(width // 100))
    valCols = ndimage.convolve1d(colVals, arrayToUse, mode="nearest")
    maxValRow = np.amax(valCols)
    wordsHere = np.argwhere(valCols >= maxValRow).flatten()
    cols = np.array_split(row, wordsHere, axis=1)
    cols = [x for x in cols if (x.shape[1] > 1 and x.shape[0]>1)]
    return cols



def cellToRows(cell, width):
    rowVals = np.sum(cell, axis=1)
    arrayToUse = np.ones(int(width // 100))
    valRows = ndimage.convolve1d(rowVals, arrayToUse, mode="nearest")
    maxValRow = np.amax(valRows)
    wordsHere = np.argwhere(valRows>=maxValRow*0.97).flatten()
    rows = np.array_split(cell, wordsHere, axis=0)
    rows = [row for row in rows if (row.shape[0] > 1 and row.shape[1]>1)]
    return rows



def removeWhiteSpaceFromWord(word):
    rowVals = np.sum(word, axis=1)
    maxValRow = np.amax(rowVals)

    whiteRows = np.argwhere(rowVals==maxValRow).flatten()
    currentArray = np.delete(word, whiteRows, axis=0)
    if currentArray.size != 0:
        colVals = np.sum(currentArray, axis=0)
        #print("colVal: ", colVals)
        maxValCol = np.amax(colVals)



        while (len(colVals) > 0) and (colVals[0] >= maxValCol):
            currentArray = np.delete(currentArray, 0, axis=1)
            colVals = np.delete(colVals, 0)

        while (len(colVals) > 0) and (colVals[-1] >= maxValCol):
            currentArray = np.delete(currentArray, -1, axis=1)
            colVals = np.delete(colVals, -1)

    return currentArray



x, row, col = cellsToWords(imgList, 1200)

print(x)
count = 0
for y in x:
    print(len(y.words))
    #count2 = 0
    #print(count, x[count].words)
    #for z in y.words:
    #    cv2.imwrite('test-'+str(count)+'-'+str(count2)+'.png', z.image)
    #    count2+=1
    #count+=1
