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
import sys
import argparse
import cv2
import editdistance
from DataLoader import DataLoader, Batch
from Model import Model, DecoderType
from SamplePreprocessor import preprocess
from dataStructures.logbookScan import CellOfWords, Word


class FilePaths:
    "filenames and paths to data"
    fnCharList = '../model/charList.txt'
    fnAccuracy = '../model/accuracy.txt'


class TrainedModel:
    model = Model(open(FilePaths.fnCharList).read(), DecoderType.BestPath, mustRestore=True, dump=None)


def convertFromFilenameToImage(fnImg):
    return cv2.imread(fnImg, cv2.IMREAD_GRAYSCALE)


def makeSomeAbiInput():
    cell0word0 = Word(convertFromFilenameToImage('../data/latinTest.png'), 0, 0)
    cell0word1 = Word(convertFromFilenameToImage('../data/09352.PNG'), 0, 0)
    cellOfWords0 = CellOfWords([cell0word0, cell0word1], 0, 0)
    cell1word0 = Word(convertFromFilenameToImage('../data/quote.png'), 0, 0)
    cell1word1 = Word(convertFromFilenameToImage('../data/quote.png'), 0, 0)
    cell1word2 = Word(convertFromFilenameToImage('../data/quote.png'), 0, 0)
    cellOfWords1 = CellOfWords([cell1word0, cell1word1, cell1word2], 0, 1)
    cellOfWords2 = CellOfWords([cell1word0, cell1word1, cell1word2], 0, 1)
    cellOfWords3 = CellOfWords([cell0word0, cell0word1], 1, 1)
    cellOfWords4 = CellOfWords([], 1, 1)
    listOfCellsOfWords = [cellOfWords0, cellOfWords1, cellOfWords2, cellOfWords3, cellOfWords4]
    return (listOfCellsOfWords, 2, 2)


def inferImage(model, img):  # TODO: CAN be optimzed to take in a list for batch to have size of the list
    img = preprocess(img, Model.imgSize)
    batch = Batch(None, [img])
    (recognized, probability) = model.inferBatch(batch, True)
    return recognized[0]


def takeOutImagesfromOneCell(cellOfWords):
    """

    :type cellOfWords: CellOfWords
    """
    toReturn = []
    words = cellOfWords.words
    word: Word
    for word in words:
        toReturn.append(word.image)
    return toReturn  # this is a list of images


def makeStringFromOneCell(model, cellOfWords):
    images = takeOutImagesfromOneCell(cellOfWords)  # check if list of images is empty!!
    if len(images) == 0:
        return ''
    toConcatinate = []
    for img in images:
        recognized = inferImage(model, img)
        toConcatinate.append(recognized)
    return ' '.join(toConcatinate)


def makeStringsFromAllCells(model, listOfCellsOfWords):
    toReturn = []
    for cellOfWords in listOfCellsOfWords:
        string = makeStringFromOneCell(model, cellOfWords)
        toReturn.append(string)
    return toReturn


def makeListOfLists(wordsFromAllCells, numberOfCols):
    for i in range(0, len(wordsFromAllCells), numberOfCols):
        yield wordsFromAllCells[i:i + numberOfCols]  # this is a list of lists of lists of image


def inferEverything(model, abi):
    listOfCells, rows, cols = abi
    l = makeStringsFromAllCells(model, listOfCells)
    l = list(
        makeListOfLists(l, cols))  # split list into rows: each row has the length of the number of columns in the thing
    return l;


def forFrontend(abi):  # getRidOfTheArgument
    # TODO: read in Abi's function and replace FilePaths.fnInferTotal
    open(FilePaths.fnAccuracy).read()
    return inferEverything(TrainedModel.model, abi)


print(forFrontend(makeSomeAbiInput()))
