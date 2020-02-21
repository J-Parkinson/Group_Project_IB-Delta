from enum import Enum

class ColumnContents(Enum):
    UPPER = "Upper"
    LOWER = "Lower"
    SYMBOL = "Symbol"
    DIGIT = "Digit"
    DITTO = "Ditto"

class Column:

    def __init__(self, tl, br, pageNo, fieldName):
        self.tlCoord = tl
        self.brCoord = br
        self.pageNo = 0
        #self.contents = {"Upper": True, "Lower": True, "Symbol": True, "Digit": True, "Ditto": True}
        self.fieldName = fieldName

    '''def getContents(self, contentValue):
        return self.contents[contentValue.value]

    def setContents(self, contentValue, value):
        self.contents[contentValue.value] = value

    # Please use with caution!
    def setContents(self, contents):
        self.contents = contents'''

    def getCoords(self):
        return self.tlCoord, self.brCoord

    def setTLCoord(self, value):
        self.tlCoord = value

    def setBRCoord(self, value):
        self.brCoord = value

    def getPageNo(self):
        return self.pageNo


class PageLayout:

    def __init__(self, noPagesPerPageSpread):
        self.noPagesPerPageSpread = noPagesPerPageSpread
        self.columnList = []

    def addColumn(self, column):
        self.columnList.append(column)

    def removeColumn(self, column):
        self.columnList.remove(column)


class Word:

    def __init__(self, image, row, col):
        self.image = image
        self.row = row
        self.col = col

class CellOfWords:

    def __init__(self, words, row=None, col=None):

        if row is None:
            row = words.get(0).row
        if col is None:
            col = words.get(0).col

        self.words = words
        self.row = row
        self.col = col


