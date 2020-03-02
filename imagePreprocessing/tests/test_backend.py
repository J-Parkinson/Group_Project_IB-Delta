import unittest
from imagePreprocessing.backendnew import createTable
import pathlib
from pdf2image import convert_from_path as ReadPDF


class MyTestCase(unittest.TestCase):

    def test_createTable(self):
        self.expected = [['1', '', '', '', '', ''], ['', '', '', '', '', ''], ['', 't 9090', '', 'MHEuCEor', 'Br191', ''], ['', '0909s', 'E. Eelra-onand', '', '', ''], ['', '09093', 'E. Cynosbatella', '', '1816191', ''], ['', 'G30', '', '', '', ''], ['', '09095', '', '', '', ''], ['', 'G9096', '', '', '', ''], ['', '09599', '', '', '', ''], ['', '8909', '', '', '', ''], ['', '09099', 'heiraphera rasoburpianae', '', '', ''], ['', 't 91400d', '', '', '', ''], ['', '0920s', '', '', '', ''], ['', 'd9102', 'Epinalid mercuriasa', '', '', ''], ['Al', 'G9103', 'Eetraphera ingertana', '', '', ''], ['i3l', '691ol', '', '', '', ''], ['', '0010s', '', '', '', ''], ['', '09106', '', '', '', ''], ['', 'G9109', '', '', '', ''], ['', '0910s', '', '', '', ''], ['', '03199', 'Epinotian Erimaculona', '', '', ''], ['', '01210', '', '', '', ''], ['', 'ore', '', '', '', ''], ['', '0112', '', '', '', ''], ['', '09113', '', '', '', ''], ['', '89iely', '', '', '', ''], ['', '6945', '', '', '', ''], ['', 'G9116', 'Bactra TuFfurana', '', '', ''], ['83"l', '091n', '', '', '', ''], ['', 'aGH118', '', '', '', ''], ['', 'G9119', '', '', '', ''], ['', '09120', 'Epiblema pt-hgiana', '', '', ''], ['', '0912.2', 't costipuncana', '', '', ''], ['', '89123', '', '', '', ''], ['', '0912', '', '', '', ''], ['', '89125', '', '', '', ''], ['', '09126', 'Epinotion subocellana', '', '', ''], ['', '8912', '', '', '', ''], ['', '0128', '', '', '', ''], ['', '09129', '', '', '', ''], ['', '09130', '.. Eenerana', '', '', ''], ['', '09131', '', '', '', ''], ['', '091 32', '', '', '', ''], ['', '0939', '', '', '', ''], ['', '', '', '', '', ''], ['', '', '', '', '', '']]

        path = pathlib.Path(__file__).parent
        testImage = str(path / '..' / 'images' / 'scantest2.pdf')
        self.result = createTable(testImage, columnLocations=[375, 790, 1690, 2100, 2520],
                    widthOfPreviewImage=3122)
        self.assertListEqual(self.result, self.expected)


if __name__ == '__main__':
    unittest.main()
