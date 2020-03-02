from __future__ import division
from __future__ import print_function

import sys
import argparse
import cv2
import editdistance
from neuralNetwork.src.DataLoader import DataLoader, Batch
from neuralNetwork.src.Model import Model, DecoderType
from neuralNetwork.src.SamplePreprocessor import preprocess
from dataStructures.logbookScan import CellOfWords, Word


class FilePaths:
    "filenames and paths to data"
    fnDitto1 = '../data/ditto1.png'
    fnDitto2 = '../data/ditto2.png'
    fnCharList = '../model/charList.txt'
    fnAccuracy = '../model/accuracy.txt'
    fnTrain = '../data/'
    fnCorpus = '../data/corpus.txt'
    fnInfer = '../data/latinTest.png'


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
        recognized = model.inferBatch(batch)

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


def convertFromFilenameToImage(fnImg):
    '''
    Converting a file path name into an image
    Used purely for testing purposes
    :param fnImg: a path to an image
    :return: an image = a list of lists of numbers
    '''
    return cv2.imread(fnImg, cv2.IMREAD_GRAYSCALE)

def inferImage(model, img):
    '''
    Infer the string out of an image using the trained model
    Get rid of images that are too small on either side since they're most likely to just be column or row lines,
    or dittos
    We get rid of dittos because the NN could only identify most of the ditto image as dittos but the rest would just be
    random letters or symbols making the output too noisy
    :param model: a Model object
    :param img: an image
    :return: a string
    '''
    if len(img) < 25 or len(img[0]) < 25:
        return ''
    img = preprocess(img, Model.imgSize)
    batch = Batch(None, [img])
    recognized = model.inferBatch(batch, True)
    return recognized[0]


def takeOutImagesfromOneCell(cellOfWords):
    '''
    Turn a CellOfWords into a list of the images of its words
    :param cellOfWords:  CellOfWords object
    :return: a list of images
    '''
    toReturn = []
    words = cellOfWords.words
    if len(words) == 0:
        return []
    word: Word
    for word in words:
        toReturn.append(word.image)
    return toReturn


def makeStringFromOneCell(model, cellOfWords):
    '''
    Turn one CellOfWords into its corresponding string
    :param model: a Model object
    :param cellOfWords: a CellOfWords object
    :return: a string
    '''
    images = takeOutImagesfromOneCell(cellOfWords)
    if len(images) == 0:
        return ''
    toConcatinate = []
    for img in images:
        recognized = inferImage(model, img)
        if recognized!='':
            toConcatinate.append(recognized)
    return ' '.join(toConcatinate)


def makeStringsFromAllCells(model, listOfCellsOfWords):
    '''
    Convert each cell into a list of words
    :param model: a Model object
    :param listOfCellsOfWords: list of CellOfWords objects
    :return: list of strings
    '''
    toReturn = []
    for cellOfWords in listOfCellsOfWords:
        string = makeStringFromOneCell(model, cellOfWords)
        toReturn.append(string)
    return toReturn


def makeListOfLists(wordsFromAllCells, numberOfCols):
    '''
    Spliting a list of strings into chunks of size numberOfCols each
    :param wordsFromAllCells: list of strings
    :param numberOfCols: integer
    :return: list of lists of words
    '''
    numberOfCols = numberOfCols + 1;
    for i in range(0, len(wordsFromAllCells), numberOfCols):
        yield wordsFromAllCells[i:i + numberOfCols]  # this is a list of lists of lists of image


def inferEverything(model, abi):
    '''
    Final function
    :param model: a Model object
    :param abi: a list of CellOfWords objects
    :return: list of lists of words
    '''
    listOfCells, rows, cols = abi
    finalList = makeStringsFromAllCells(model, listOfCells)
    finalList = list(
        makeListOfLists(finalList, rows))
    return finalList;


def main():
    '''
    Do whatever you want:
    - can retrain the NN with a different decoding algorithm than best path decoding
    Warning: that will take 20 hours at least on a CPU and this code works with the CPU version of tensorflow
    We decided current decoding is best since we want to decode latin words, not english
    :return: string
    '''
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
        print(inferImage(model, convertFromFilenameToImage(FilePaths.fnInfer)))


if __name__ == '__main__':
    main()