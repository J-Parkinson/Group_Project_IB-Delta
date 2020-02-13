from enum import Enum

class ColumnContents(Enum):
    UPPER = "Upper"
    LOWER = "Lower"
    SYMBOL = "Symbol"
    DIGIT = "Digit"
    DITTO = "Ditto"

class Column:

    def __init__(self, tl, br, pageNo, fN,  *args):
        self.tlCoord = tl
        self.brCoord = br
        self.pageNo = 0
        self.contents = {"Upper": False, "Lower": False, "Symbol": False, "Digit": False, "Ditto": False}
        self.fieldName = fN
        for contentValue in args:
            self.contents[contentValue.value] = True

    def getContents(self, contentValue):
        return self.contents[contentValue.value]

    def setContents(self, contentValue, value):
        self.contents[contentValue.value] = value

    def getCoords(self):
        return self.tlCoord, self.brCoord

    def setTLCoord(self, value):
        self.tlCoord = value

    def setBRCoord(self, value):
        self.brCoord = value

    def getPageNo(self):
        return self.pageNo




#TODO: FINISH THIS DEFINITION
#TODO: SHOULD WE DO IT THIS WAY?

class PageLayout:

    noPagesPerPage = 1
    columnList = []
    pageYCoords = []

    def __init__(self, noPagesPerPage, pageYCoords, columnList):
        noPagesPerPage = noPagesPerPage
        self.pageYCoords = pageYCoords
        self.columnList = columnList

    @staticmethod
    def addColumn(self, column):
        self.columnList.append(column)

    def addColumn(self):
        self.columnList.add(self)


    @staticmethod
    def removeColumn(self, column):
        self.columnList.remove(column)

    #def changeCoord(self, ):