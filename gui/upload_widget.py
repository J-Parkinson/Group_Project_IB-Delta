from enum import Enum

from PyQt5.QtGui import QIntValidator, QPainter, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QPushButton, QFileDialog, \
    QMessageBox, QProgressBar, QDialog, QListWidget, QLineEdit, QGridLayout, QSpinBox, QApplication, QStyle, \
    QMainWindow, QInputDialog, QProgressBar
from PyQt5.QtCore import Qt, QSize
import time

import dataStructures.logbookScan as Scan
import imagePreprocessing.imageScanningAndPreprocessing as ImageProcess
from gui.subpages import saveCSV, fileSelectPage, dragPage

test = Scan.PageLayout(1)
test.addColumn(Scan.Column((0, 0), (50, 200), 1, ""))
test.addColumn(Scan.Column((50, 0), (100, 200), 1, ""))
test.addColumn(Scan.Column((100, 0), (150, 200), 1, ""))
test.addColumn(Scan.Column((150, 0), (200, 200), 1, ""))





# Todo: make this work, but not hurry lol
class ProgressBar(QMainWindow):
    def __init__(self, noSteps=1):
        # super(ProgressBar, self).__init__(parent)
        super(ProgressBar, self).__init__()

        self.window = QWidget()
        self.setWindowTitle("Loading page preview..")

        self.layout = QVBoxLayout()

        self.text = QLabel(self)
        self.text.setText("")

        self.progress = QProgressBar(self)
        self.progress.setGeometry(200, 80, 250, 20)

        self.noSteps = noSteps
        self.currentStep = 0

        self.layout.addWidget(self.text)
        self.layout.addWidget(self.progress)

        self.window.setLayout(self.layout)
        self.window.show()

    def hide(self):
        self.close()
        return

    def update(self, string):
        self.currentStep += 1
        self.progress.setValue(self.currentStep / self.noSteps)
        self.text.setText(string)
        return


class upload_page(QStackedWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.filename = ""

        self.file_select_page = fileSelectPage.file_select(self)
        self.drag = dragPage.drag_page(self)
        self.save_page = saveCSV.saveCSVWindow([])

        self.addWidget(self.file_select_page)
        self.addWidget(self.drag)
        self.addWidget(self.save_page)
        self.setCurrentIndex(0)

    def warning(self,title, text, description, two_buttons):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setInformativeText(description)

        if two_buttons:
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        return msg.exec_()