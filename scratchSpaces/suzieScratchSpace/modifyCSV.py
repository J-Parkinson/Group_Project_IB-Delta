from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, \
    QStackedWidget, QBoxLayout, QHBoxLayout, QFileDialog, QCheckBox, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QLinearGradient, QBrush, QPalette, QFont, QPixmap


class modifyCSVWindow(QWidget):

    topx= 1
    topy = 1

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.setStyleSheet('color: black; background-color:white')

        test = QPushButton("push to add a new button")
        test.clicked.connect(self.addnewButton)
        self.grid.addWidget(test, 0, 0)

        plus = QPushButton("+")
# TODO: find paper with layout on and work out layout grid and how to add to grid
        plush.clicked.connect(self.addnewDropDown(plus1, ))

        dropDown = QComboBox()
        dropDown.addItems(["item 1", "item 2", "item 3"])
        self.grid.addWidget(dropDown, 1,0)


        self.setLayout(self.grid)

    def addnewButton(self):
        newBtn = QPushButton("new button", self)
        self.grid.addWidget(newBtn, 0,1)
        #newBtn.move(0,0)
        #newBtn.show()

    def addnewDropDown(self):
        newDrop = QComboBox()
        newDrop.addItems(["new 1", "new 2", "new 3"])

        self.grid.addWidget(newDrop,topx, topy)


