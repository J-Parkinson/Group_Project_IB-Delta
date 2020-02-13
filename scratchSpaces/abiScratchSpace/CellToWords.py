import numpy as np
from scipy import ndimage
import cv2

from PIL import Image
import matplotlib.pyplot as plt

img = cv2.imread("../../imagePreprocessing/images/segmentedImagesOut/Page 13/cell-1-2.png")

arr = np.array(img)
height, width, channels = img.shape
arr.shape = (height, width, channels)
arr = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)

def cellToWords(cell): # takes one numpy array
    newWords = []
    rows = cellToRows(cell)
    for row in rows:
        words = rowToWords(row)
        for word in words:
            newWords.append(removeWhiteSpaceFromWord(word))

    # **do the stuff with the temp directory here**


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


cellToWords(arr)