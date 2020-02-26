import unittest
from main import inferImage, convertFromFilenameToImage, \
    makeStringsFromAllCells, makeStringFromOneCell, inferEverything, takeOutImagesfromOneCell
from Model import Model, DecoderType
from dataStructures.logbookScan import CellOfWords, Word

class TestFilePaths:
    fnCharList = '../model/charList.txt'
    fnAccuracy = '../model/accuracy.txt'

class TestModel:
      model = Model(open(TestFilePaths.fnCharList).read(), DecoderType.BestPath, mustRestore=True, dump=None)

#TODO: test for empty word list

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
    cell0word2 = Word(convertFromFilenameToImage('../data/quote.png'), 0, 0)
    cellOfWords0: CellOfWords = CellOfWords([cell0word0, cell0word1, cell0word2], 0, 0)
    return cellOfWords0

class Expected:
    expected_infer = convertFromFilenameToImage('../data/latinTest.png')
    expected_takeOutImagesfromOneCell = [convertFromFilenameToImage('../data/latinTest.png'),
                                         convertFromFilenameToImage('../data/09352.PNG'),
                                         convertFromFilenameToImage('../data/quote.png')]

class Data:
    image = convertFromFilenameToImage('../data/latinTest.png')
    aCellOfWords = makeACellOfWords()
    someAbiInput = makeSomeAbiInput()
    listOfCells, rows, cols = someAbiInput

class TestMain(unittest.TestCase):

    def test_infer(self):
        self.expected = 'Argyresthia'
        self.result = inferImage(TestModel.model, Data.image)
        self.assertEqual(self.result, self.expected)

    #def test_takeOutImagesfromOneCell(self):
      #  self.expected = Expected.expected_takeOutImagesfromOneCell
     #   self.result = takeOutImagesfromOneCell(Data.aCellOfWords)
    #    self.assertListEqual(self.result, self.expected)
        #print(self.result)

    def test_makeStringFromOneCell(self):
        self.result = makeStringFromOneCell(TestModel.model, Data.aCellOfWords)
        self.expected = 'Argyresthia 09352 "'
        self.assertEqual(self.result, self.expected)


    def test_makeStringsFromAllCells(self):
        self.result = makeStringsFromAllCells(TestModel.model, Data.listOfCells)
        self.expected = ['Argyresthia 09352', '" " "', '" " "', 'Argyresthia 09352']
        self.assertListEqual(self.result, self.expected)

    def test_inferEverything(self):
        self.result = inferEverything(TestModel.model, Data.someAbiInput)
        self.expected = [['Argyresthia 09352', '" " "'], ['" " "', 'Argyresthia 09352']]
        self.assertListEqual(self.result, self.expected)

    #def test_inferRow(self):
    #    self.result = inferRow(TestModel.model, TestFilePaths.fnInferRow)
    #    self.expected = ['Argyresthia 09352', '" "']
    #    self.assertEqual(self.result, self.expected)

   # def test_inferFinal(self):
   #     self.result = inferPages(TestModel.model, TestFilePaths.fnInferTotal)
   #     self.expected = [['Argyresthia 09352', '" "'], ['Argyresthia 09352', '" "']]
   #     self.assertListEqual(self.result, self.expected)


if __name__ == '__main__':
    unittest.main()