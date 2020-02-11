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
    newImages = []
    columnVals = np.sum(cell, axis=0)
    maxValCol = np.amax(columnVals)
    x = ndimage.convolve1d(columnVals, np.array([1,1,1,1]), mode="nearest")
    print(x.shape)
    indicesToSplit = np.array(np.where(x >0.95*maxValCol))
    indicesToSplit = np.ndarray.flatten(indicesToSplit)
    #indicesToSplit.astype(int)
    words = np.split(x, indicesToSplit)

    rowVals = np.sum(cell, axis=1)
    maxValRow = np.amax(rowVals)
    y = ndimage.convolve1d(rowVals, np.array([1, 1, 1, 1]), mode="nearest")
    #plt.plot(x)
    plt.show()


cellToWords(arr)