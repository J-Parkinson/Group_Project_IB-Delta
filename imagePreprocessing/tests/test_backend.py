import unittest
from imagePreprocessing.backendnew import createTable
import pathlib
from pdf2image import convert_from_path as ReadPDF


class MyTestCase(unittest.TestCase):

    def test_createTable(self):
        self.expected = [['18r', '', '', '', '', ''],
                         ['', '', '', '', '', ''],
                         ['', '89090', '', 'MHEuCEor', 'Bra1', ''],
                         ['', '0909s', 'E. Eelragonane', '', '', ''],
                         ['', '09093', 'E. Cynosbatella', '', '1816191', ''],
                         ['', 'G30', '', '', '', ''],
                         ['', '09095', '', '', '', ''],
                         ['', 'G9096', '', '', '', ''],
                         ['', '09599', '', '', '', ''],
                         ['', '8909', '', '', '', ''],
                         ['', '09099', 'Ineiraphera rasoburpiane', '', '', ''],
                         ['', '092d', '', '', '', ''],
                         ['', '0920s', '', '', '', ''],
                         ['', 'd2102', 'Epinotid mercuriasa', '', '', ''],
                         ['Al', 'G9103', 'EeNraphera insertana', '', '', ''],
                         ['i3l', '8r0l', '', '', '', ''], ['', '0910s', '', '', '', ''],
                         ['', '09106', '', '', '', ''],
                         ['', 'G9109', '', '', '', ''],
                         ['', '0910s', '', '', '', ''],
                         ['', '03199', 'Fpinoticn Erimaculona', '', '', ''],
                         ['', '01210', '', '', '', ''],
                         ['', 'ore', '', '', '', ''],
                         ['', '0112', '', '', '', ''],
                         ['', '09113', '', '', '', ''],
                         ['', '89iely', '', '', '', ''],
                         ['', '6945', '', '', '', ''],
                         ['', 'G9116', 'Bactra PuFfurona', '', '', ''],
                         ['8B"l', '091n', '', '', '', ''],
                         ['', 'aGH118', '', '', '', ''],
                         ['', 'G9119', '', '', '', ''],
                         ['', '09120', 'Epiblema pfihgiana', '', '', ''],
                         ['', '0912.2', 'E coslipunelana', '', '', ''],
                         ['', '89123', '', '', '', ''],
                         ['', '0912', '', '', '', ''],
                         ['', '89125', '', '', '', ''],
                         ['', '09126', 'IRpinotio subocellaa', '', '', ''],
                         ['', '8912', '', '', '', ''],
                         ['', '09128', '', '', '', ''],
                         ['', '09129', '', '', '', ''],
                         ['', '09130', 'Er. Eenerana', '', '', ''],
                         ['', '09131', '', '', '', ''],
                         ['', '0932', '', '', '', ''],
                         ['', '0939', '', '', '', ''],
                         ['', '', '', '', '', ''],
                         ['wn', '', '', '', '-', 'id']]
        path = pathlib.Path(__file__).parent
        testImage = str(path / '..' / 'images' / 'scantest2.pdf')
        self.result = createTable(testImage, columnLocations=[375, 790, 1690, 2100, 2520],
                    widthOfPreviewImage=3122)
        self.assertListEqual(self.result, self.expected)

    #def test_something(self):
     #   self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
