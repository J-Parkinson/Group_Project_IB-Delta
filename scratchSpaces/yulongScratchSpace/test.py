from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QMouseEvent, QPainter
from PyQt5.QtWidgets import (QPushButton, QWidget,
                             QLineEdit, QApplication, QLabel)
import sys


class window(QWidget):
    click_x,click_y = 0,0
    now_x,now_y = 0,0

    def __init__(self):
        QWidget.__init__(self)
        self.resize(800, 640)

        self.setStyleSheet('background-color:grey;')

    def mousePressEvent(self, e):
        print("pressed:", e.x(), e.y())
        self.click_x, self.click_y = e.x(), e.y()
        self.now_x, self.now_y = e.x(), e.y()
        self.setStyleSheet('background-color:white;')

    def mouseMoveEvent(self, e):
        self.now_x,self.now_y = e.x(), e.y()
        self.update()

    def mouseReleaseEvent(self, e):
        print("released:", e.x(), e.y())
        self.setStyleSheet('background-color:grey;')

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        start_x = self.click_x if self.click_x < self.now_x else self.now_x
        start_y = self.click_y if self.click_y < self.now_y else self.now_y
        ex = self.click_x if self.click_x >= self.now_x else self.now_x
        ey = self.click_y if self.click_y >= self.now_y else self.now_y
        qp.drawRect(self.now_x, self.now_y, -20, 30)
        qp.end()


app = QApplication(sys.argv)
window = window()
window.show()
app.exec_()
