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
        self.contents = {"Upper": True, "Lower": True, "Symbol": True, "Digit": True, "Ditto": True}
        self.fieldName = fieldName

    def getContents(self, contentValue):
        return self.contents[contentValue.value]

    def setContents(self, contentValue, value):
        self.contents[contentValue.value] = value

    # Please use with caution!
    def setContents(self, contents):
        self.contents = contents

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
        self.columnList.add(column)

    def removeColumn(self, column):
        self.columnList.remove(column)
