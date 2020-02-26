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
from main import inferEverything, FilePaths



def forFrontend(abi): # getRidOfTheArgument
    # TODO: read in Abi's function and replace FilePaths.fnInferTotal
    open(FilePaths.fnAccuracy).read()
    model = Model(open(FilePaths.fnCharList).read(), DecoderType.BestPath, mustRestore=True, dump=None)  # make list of lists of lists
    return inferEverything(model, abi)



