from unittest import TestCase
from imagePreprocessing.imageScanningAndPreprocessing import concatenateImages, normaliseImage, convertToCellOfWords, splitIntoCells
from PIL import Image
import numpy as np
import cv2

from dataStructures.logbookScan import CellOfWords, Word


class Test(TestCase):
    def test_concatenate_images(self):
        #Checking merged images sizes stay the same
        self.assertEqual(concatenateImages([Image.open("pagelayout1.png"),
                                            Image.open("pagelayout2.png")]).size,
                                            Image.open("test1.png").size)

    def test_normalise_image(self):
        #Exploiting fact that a well-normalised page will have a large no of white pixels hence the average brightness of the image will be high (but not >250 as that would indicate we cropped too small)
        img = cv2.imread("test2.png")
        self.assertAlmostEqual(np.mean(normaliseImage(img, img).flatten()), 240.0, delta=10)

    def test_convert_to_cell_of_words(self):
        self.assertEqual(convertToCellOfWords(
                            [np.array(
                                    [[0, 255,   0,   0,   0],
                                     [0, 255, 255, 255,   0],
                                     [0,   0,   0,   0, 255],
                                     [0, 255,   0, 255,   0]]),

                             np.array(
                                    [[0, 255,   0,   0,   0],
                                     [0, 255,   0, 255,   0],
                                     [0,   0,   0,   0, 255],
                                     [0,   0, 255, 255,   0]]),

                             np.array(
                                    [[255,   0,   0,   0,   0],
                                     [255,   0,   0,   0, 255],
                                     [  0, 255,   0,   0,   0]]),


                             np.array(
                                    [[255,   0, 255, 255,   0],
                                     [255,   0,   0,   0, 255],
                                     [  0, 255,   0, 255,   0]])]

                            , 2),

                            [CellOfWords([Word(np.array(
                                    [[0, 255,   0,   0,   0],
                                     [0, 255, 255, 255,   0],
                                     [0,   0,   0,   0, 255],
                                     [0, 255,   0, 255,   0]]), 0, 0)], 0, 0),

                             CellOfWords([Word(np.array(
                                    [[0, 255,   0,   0,   0],
                                     [0, 255,   0, 255,   0],
                                     [0,   0,   0,   0, 255],
                                     [0,   0, 255, 255,   0]]), 0, 1)], 0, 1),

                             CellOfWords([Word(np.array(
                                    [[255,   0,   0,   0,   0],
                                     [255,   0,   0,   0, 255],
                                     [  0, 255,   0,   0,   0]]), 1, 0)], 1, 0),

                             CellOfWords([Word(np.array(
                                    [[255,   0, 255, 255,   0],
                                     [255,   0,   0,   0, 255],
                                     [  0, 255,   0, 255,   0]]), 1, 1)], 1, 1)])

    def test_split_into_cells(self):
        compare1 = splitIntoCells(np.array([[0, 255,   0,   0,   0], [0, 255, 255, 255,   0], [0,   0,   0,   0, 255], [0, 255,   0, 255,   0]]), [2], [1,3])
        compare2 = [np.array([[0], [0]]), np.array([[255, 0], [255, 255]]), np.array([[0, 0], [255, 0]]), np.array([[0], [0]]), np.array([[0, 0], [255, 0]]), np.array([[0, 255], [255, 0]])]
        self.assertTrue(all(compare1[i].all() == compare2[i].all() for i in range(len(compare1))))