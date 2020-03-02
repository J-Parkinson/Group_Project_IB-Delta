import unittest
import numpy as np
from imagePreprocessing.CellsToWords import cellToRows, rowToWords, stripCell, removeWhiteSpaceFromWord
import pathlib
from pdf2image import convert_from_path as ReadPDF
import cv2

class TestCase1(unittest.TestCase):

    def test_rowToWords(self):
        exp = cv2.imread("row.png")
        expArr = np.array(exp)
        height, width, channels = exp.shape
        expArr.shape = (height, width, channels)
        expArr = cv2.cvtColor(expArr, cv2.COLOR_BGR2GRAY)

        res = rowToWords(expArr, 3300)
        self.result = len(res)
        self.assertEqual(3, self.result)

    def test_stripCell(self):
        img = cv2.imread("../segmentedcells/cell62.png")
        arr = np.array(img)
        height, width, channels = img.shape
        arr.shape = (height, width, channels)
        arr = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)

        img2 = cv2.imread("strippedCell.png")
        arr2 = np.array(img2)
        height2, width2, channels2 = img2.shape
        arr2.shape = (height2, width2, channels2)
        arr2 = cv2.cvtColor(arr2, cv2.COLOR_BGR2GRAY)
        self.result = stripCell(arr)
        self.expected = arr2
        self.assertListEqual(self.result.tolist(), self.expected.tolist())

    def test_removeWhiteSpaceFromWord(self):
        img = cv2.imread("word.png")
        arr = np.array(img)
        height, width, channels = img.shape
        arr.shape = (height, width, channels)
        arr = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)

        img2 = cv2.imread("word-removed.png")
        arr2 = np.array(img2)
        height2, width2, channels2 = img2.shape
        arr2.shape = (height2, width2, channels2)
        arr2 = cv2.cvtColor(arr2, cv2.COLOR_BGR2GRAY)

        self.expected = arr2
        self.result = removeWhiteSpaceFromWord(arr)

        self.assertListEqual(self.result.tolist(), self.expected.tolist())

if __name__ == '__main__':
    unittest.main()
