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
    h,w = cell.shape
    numBlackPix = np.sum(cell, axis=0)
    maxVal = np.amax(numBlackPix)
    difference = np.subtract(np.full(numBlackPix.shape, maxVal), numBlackPix)
    x =np.gradient(numBlackPix)
    x[x > 4] = 10
    y = ndimage.convolve1d(numBlackPix, np.array([1,1,1,1]), mode="nearest")
    plt.plot(y)
    plt.show()


cellToWords(arr)