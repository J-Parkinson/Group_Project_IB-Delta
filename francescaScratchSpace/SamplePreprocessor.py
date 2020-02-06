# Prepares the images from the IAM dataset for the NN

from __future__ import division
from __future__ import print_function

import random
import numpy as np
import cv2


def preprocess(img, imgSize, dataAugmentation=False):
    "put img into target img of size imgSize, transpose for TF and normalize gray-values"

    # there are damaged files in IAM dataset - just use black image instead
    if img is None:
        img = np.zeros([imgSize[1], imgSize[0]])

    # increase dataset size by applying random stretches to the images
    #"What is the fucking purpose of this????? Also, dataAugmentation=False on line 9 sooo
    if dataAugmentation:
        stretch = (random.random() - 0.5)  # a random number in  [-0.5, +0.5]
        wStretched = max(int(img.shape[1] * (1 + stretch)), 1)  # random width, but at least 1
        img = cv2.resize(img, (wStretched, img.shape[0]))  # stretch horizontally by factor in [0.5, 1.5]

    # create target image and copy sample image into it
    (wt, ht) = imgSize  # target size = size we want
    (h, w) = img.shape  # input image size = (rows, columns) of a grayscale image, non-grayscale returns a triple
    fx = w / wt
    fy = h / ht
    f = max(fx, fy)
    #DON'T QUITE GET THE NEXT 2 LINES SINCE FX WOULD BE REAL SOOOOOOU UM
    newSize = (max(min(wt, int(w / f)), 1),
               max(min(ht, int(h / f)), 1))  # scale according to f (result at least 1 and at most wt or ht)
    img = cv2.resize(img, newSize) # INTER_LINEAR – a bilinear interpolation (used by default)
    target = np.ones([ht, wt]) * 255
    target[0:newSize[1], 0:newSize[0]] = img #why do the rest of the elements in the matrix untouched by img have to remain 255?????

    # transpose for TF
    img = cv2.transpose(target) # what's the purpose of the transposition????????

    # normalize
    #EXCUSE ME WTF!!!!!!!!!
    (m, s) = cv2.meanStdDev(img)
    m = m[0][0]
    s = s[0][0]
    img = img - m
    img = img / s if s > 0 else img
    return img