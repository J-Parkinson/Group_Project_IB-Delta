from __future__ import division
from __future__ import print_function

import sys
import argparse
import cv2
import editdistance
from DataLoader import DataLoader, Batch
from Model import Model, DecoderType
from SamplePreprocessor import preprocess
import os  # mine
import numpy as np
from main import inferPages


#TODO: get rid of this once you get the function
class FilePaths:
    "filenames and paths to data"
    fnInfer = '../data/latinTest.png'
    #fnInferCell = ['../data/latinTest.png', '../data/09352.PNG', '../data/quote.png']
    #fnInferRow = [['../data/latinTest.png', '../data/09352.PNG'], ['../data/quote.png', '../data/quote.png']]
    fnInferTotal = [
        [ ['../data/latinTest.png', '../data/09352.PNG'], ['../data/quote.png','../data/quote.png' ] ],
        [ ['../data/latinTest.png', '../data/09352.PNG'], ['../data/quote.png','../data/quote.png' ] ]
                     ]

def forFrontend():
    # TODO: read in Abi's function and replace FilePaths.fnInferTotal
    open(FilePaths.fnAccuracy).read()
    model = Model(open(FilePaths.fnCharList).read(), DecoderType.BestPath, mustRestore=True, dump=None)
    return inferPages(model, FilePaths.fnInferTotal)


