from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QMouseEvent, QPainter
from PyQt5.QtWidgets import (QPushButton, QWidget,
                             QLineEdit, QApplication, QLabel, QMessageBox)
import sys


class window(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.resize(800, 640)
        but = QPushButton("but",self)
        but.move(400,320)
        but.clicked.connect(self.open)

    def open(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        msg.setText("This is a message box")
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        msg.setStandardButtons(QMessageBox.Ok)

        msg.exec_()

app = QApplication(sys.argv)
window = window()
window.show()
app.exec_()