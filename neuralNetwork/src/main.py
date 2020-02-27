from __future__ import division
from __future__ import print_function

import sys
import argparse
import cv2
import editdistance
from DataLoader import DataLoader, Batch
from Model import Model, DecoderType
from SamplePreprocessor import preprocess
from dataStructures import logbookScan
import os  # mine
import numpy as np
from collections import Iterable
from dataStructures.logbookScan import CellOfWords, Word


class FilePaths:
    "filenames and paths to data"
    fnCharList = '../model/charList.txt'
    fnAccuracy = '../model/accuracy.txt'
    fnTrain = '../data/'
    fnInfer = '../data/latinTest.png'
    # fnInfer = '../data/quote.png'
    # fnInfer = '../data/miller.PNG'
    # fnInfer = '../data/fuckup1.PNG'
    # fnInfer = '../data/09352.PNG'
    fnCorpus = '../data/corpus.txt'
    # mine
    fnFile = '../data/a01/a01-000u/'
    fnInferCell = ['../data/latinTest.png', '../data/09352.PNG', '../data/quote.png']
    fnInferCell1 = ['../data/latinTest.png', '../data/09352.PNG', '../data/quote.png']
    fnInferCell2 = ['../data/latinTest.png', '../data/quote.png', '../data/09352.PNG', ]
    fnInferRow = [['../data/latinTest.png', '../data/09352.PNG'], ['../data/quote.png', '../data/quote.png']]
    fnInferTotal = [
        [['../data/latinTest.png', '../data/09352.PNG'], ['../data/quote.png', '../data/quote.png']],
        [['../data/latinTest.png', '../data/09352.PNG'], ['../data/quote.png', '../data/quote.png']]
    ]
    ### NOT IN FILE PATHS


def train(model, loader):
    "train NN"
    epoch = 0  # number of training epochs since start
    bestCharErrorRate = float('inf')  # best valdiation character error rate
    noImprovementSince = 0  # number of epochs no improvement of character error rate occured
    earlyStopping = 5  # stop training after this number of epochs without improvement
    while True:
        epoch += 1
        print('Epoch:', epoch)

        # train
        print('Train NN')
        loader.trainSet()
        while loader.hasNext():
            iterInfo = loader.getIteratorInfo()
            batch = loader.getNext()
            loss = model.trainBatch(batch)
            print('Batch:', iterInfo[0], '/', iterInfo[1], 'Loss:', loss)

        # validate
        charErrorRate = validate(model, loader)

        # if best validation accuracy so far, save model parameters
        if charErrorRate < bestCharErrorRate:
            print('Character error rate improved, save model')
            bestCharErrorRate = charErrorRate
            noImprovementSince = 0
            model.save()
            open(FilePaths.fnAccuracy, 'w').write(
                'Validation character error rate of saved model: %f%%' % (charErrorRate * 100.0))
        else:
            print('Character error rate not improved')
            noImprovementSince += 1

        # stop training if no more improvement in the last x epochs
        if noImprovementSince >= earlyStopping:
            print('No more improvement since %d epochs. Training stopped.' % earlyStopping)
            break

def validate(model, loader):
    "validate NN"
    print('Validate NN')
    loader.validationSet()
    numCharErr = 0
    numCharTotal = 0
    numWordOK = 0
    numWordTotal = 0
    while loader.hasNext():
        iterInfo = loader.getIteratorInfo()
        print('Batch:', iterInfo[0], '/', iterInfo[1])
        batch = loader.getNext()
        (recognized, _) = model.inferBatch(batch)

        print('Ground truth -> Recognized')
        for i in range(len(recognized)):
            numWordOK += 1 if batch.gtTexts[i] == recognized[i] else 0
            numWordTotal += 1
            dist = editdistance.eval(recognized[i], batch.gtTexts[i])
            numCharErr += dist
            numCharTotal += len(batch.gtTexts[i])
            print('[OK]' if dist == 0 else '[ERR:%d]' % dist, '"' + batch.gtTexts[i] + '"', '->',
                  '"' + recognized[i] + '"')

    # print validation result
    charErrorRate = numCharErr / numCharTotal
    wordAccuracy = numWordOK / numWordTotal
    print('Character error rate: %f%%. Word accuracy: %f%%.' % (charErrorRate * 100.0, wordAccuracy * 100.0))
    return charErrorRate

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
    listOfCellsOfWords = [cellOfWords0, cellOfWords1, cellOfWords2, cellOfWords3]
    return (listOfCellsOfWords, 2, 2)

def makeACellOfWords():
    cell0word0 = Word(convertFromFilenameToImage('../data/latinTest.png'), 0, 0)
    cell0word1 = Word(convertFromFilenameToImage('../data/09352.PNG'), 0, 0)
    cellOfWords0: CellOfWords = CellOfWords([cell0word0, cell0word1], 0, 0)
    return cellOfWords0

def convertFromFilenameToImage(fnImg):
    return cv2.imread(fnImg, cv2.IMREAD_GRAYSCALE)

def infer(model, fnImg):
    "recognize text in image provided by file path"
    img = preprocess(cv2.imread(fnImg, cv2.IMREAD_GRAYSCALE), Model.imgSize)
    batch = Batch(None, [img])
    (recognized, probability) = model.inferBatch(batch, True)
    print('Recognized:', '"' + recognized[0] + '"')
    print('Probability:', probability[0])

# MINE

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
        return ""
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
    l = list(makeListOfLists(l, cols)) #split list into rows: each row has the length of the number of columns in the thing
    return l;

def main():
    "main function"
    # optional command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', help='train the NN', action='store_true')
    parser.add_argument('--validate', help='validate the NN', action='store_true')
    parser.add_argument('--beamsearch', help='use beam search instead of best path decoding', action='store_true')
    parser.add_argument('--wordbeamsearch', help='use word beam search instead of best path decoding',
                        action='store_true')
    parser.add_argument('--dump', help='dump output of NN to CSV file(s)', action='store_true')

    args = parser.parse_args()

    decoderType = DecoderType.BestPath  # decided BestPath is the way to go
    if args.beamsearch:
        decoderType = DecoderType.BeamSearch
    elif args.wordbeamsearch:
        decoderType = DecoderType.WordBeamSearch

    # train or validate on IAM dataset
    if args.train or args.validate:
        # load training data, create TF model
        loader = DataLoader(FilePaths.fnTrain, Model.batchSize, Model.imgSize, Model.maxTextLen)

        # save characters of model for inference mode
        open(FilePaths.fnCharList, 'w').write(str().join(loader.charList))

        # save words contained in dataset into file
        open(FilePaths.fnCorpus, 'w').write(str(' ').join(loader.trainWords + loader.validationWords))

        # execute training or validation
        if args.train:
            model = Model(loader.charList, decoderType)
            train(model, loader)
        elif args.validate:
            model = Model(loader.charList, decoderType, mustRestore=True)
            validate(model, loader)

    else:
        print(open(FilePaths.fnAccuracy).read())
        model = Model(open(FilePaths.fnCharList).read(), DecoderType.BestPath, mustRestore=True,
                      dump=None)  # change dump to
        # arg.dump if needed
        # TODO: call Abi's function
        # TODO: Get rid of all this main stuff, have function ready for frontend

        # the combined notebook has latin names and numbers
        # maybe try to use word beam search for the

        # infer1(model, FilePaths.fnFile)
        # infer(model, FilePaths.fnInfer)
        # print(inferImage(model, FilePaths.fnInfer)
        # print(inferCell(model, FilePaths.fnInferCell))
        # print(inferRow(model, FilePaths.fnInferRow))
        # print(inferPages(model, FilePaths.fnInferTotal))
        # print(convertFromFilenameToImage(FilePaths.fnInfer))
        # print(FilePaths.fnInfer)

        # abi = makeSomeAbiInput()
        # input = makePreferredInput(abi)
        # preferredInput = makePreferredInput(input)  # make list of lists of lists
        # return inferPages(model, preferredInput)
        # print(makeSomeInput())
        #
        #cell = makeACellOfWords()
        #string = makeStringFromOneCell(model, cell)
        #print(string)
        abi = makeSomeAbiInput()
        #l = list(makeListOfLists(list1, cols)) #this is a void call
        l = inferEverything(model, abi)
        print(l)

        #l = [1,2,3,4,5,6]
        #l = list(makeListOfLists(l,2))
        #print(l)
        # abi = makeSomeAbiInput()
        # print(takeOutWordsfromAllCells(abi[0]))
        # in1 = takeOutWordsfromAllCells(abi[0])
        # in2 = makeListOfListsOfLists(in1, 2)
        # print(in1)
        # print(inferPages(model, in1))
        #print(takeOutImagesfromOneCell(makeACellOfWords()))
        #print(convertFromFilenameToImage('../data/latinTest.png'))



if __name__ == '__main__':
    main()
