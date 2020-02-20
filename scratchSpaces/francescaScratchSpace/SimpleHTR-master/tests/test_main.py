import unittest

import unittest
from main import inferImage, inferRow, inferCell, inferPages
from Model import Model, DecoderType


class TestFilePaths:
    fnCharList = '../model/charList.txt'
    fnAccuracy = '../model/accuracy.txt'
    fnInfer = '../data/latinTest.png'
    fnInferCell = ['../data/latinTest.png', '../data/09352.PNG', '../data/quote.png']
    fnInferRow = [['../data/latinTest.png', '../data/09352.PNG'], ['../data/quote.png', '../data/quote.png']]
    fnInferTotal = [
        [['../data/latinTest.png', '../data/09352.PNG'], ['../data/quote.png', '../data/quote.png']],
        [['../data/latinTest.png', '../data/09352.PNG'], ['../data/quote.png', '../data/quote.png']]
    ]
    # fnInfer = '../data/quote.png'
    # fnInfer = '../data/miller.PNG'
    # fnInfer = '../data/fuckup1.PNG'
    # fnInfer = '../data/09352.PNG'



class TestModel:
    model = Model(open(TestFilePaths.fnCharList).read(), DecoderType.BestPath, mustRestore=True, dump=None)


class TestMain(unittest.TestCase):

    def test_infer(self):
        self.assertEqual(inferImage(TestModel.model, TestFilePaths.fnInfer), 'Argyresthia')

    def test_inferCell(self):
        self.result = inferCell(TestModel.model, TestFilePaths.fnInferCell)
        self.expected = 'Argyresthia 09352 "'
        self.assertEqual(self.result, self.expected)

    def test_inferRow(self):
        self.result = inferRow(TestModel.model, TestFilePaths.fnInferRow)
        self.expected = ['Argyresthia 09352', '" "']
        self.assertEqual(self.result, self.expected)

    def test_inferFinal(self):
        self.result = inferPages(TestModel.model, TestFilePaths.fnInferTotal)
        self.expected = [['Argyresthia 09352', '" "'], ['Argyresthia 09352', '" "']]
        self.assertListEqual(self.result, self.expected)


if __name__ == '__main__':
    unittest.main()
