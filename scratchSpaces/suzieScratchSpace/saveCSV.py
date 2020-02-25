from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, \
    QStackedWidget, QBoxLayout, QHBoxLayout, QFileDialog, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QLinearGradient, QBrush, QPalette, QFont, QPixmap
from PyQt5.uic.properties import QtGui

from ..jamesScratchSpace import matrix_to_csv
import os, platform, subprocess


class saveCSVWindow(QWidget):
# TODO: make pretty
    def __init__(self, table):
        super().__init__()
        self.table = table
        self.save_path = None
        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        grid.setSpacing(10)

        self.setStyleSheet('color: black; background-color:white')
        title = QLabel("The file has successfully been transcribed! \n Select a folder to save the transcribed file into and then press Save.")

        grid.addWidget(title,1,0, 1,2)

        cont_button = QPushButton()
        cont_button.setText("Save")

        check_box = QCheckBox("Open file once saved")
        check_box.setStyleSheet('background-color: white')
        grid.addWidget(check_box, 4, 0)
        grid.addWidget(cont_button, 4, 1)

        cont_button.clicked.connect(lambda: self.saveFile(check_box))

        self.setLayout(grid)


    def saveFile(self, b):
        save_path, _ = QFileDialog.getSaveFileName(self, self.tr('Save File'), 'untitled.csv', self.tr('CSV (*.csv'))
        if save_path != '':
            matrix_to_csv.matrix_to_csv(self.table, save_path)
            saved = QLabel("Saved!")
            saved.show()
            if b.isChecked():
                if platform.system() == 'Darwin':
                    subprocess.call(('open', save_path))
                elif platform.system() == 'Windows':
                    os.startfile(save_path)
                else:
                    subprocess.call(('xdg-open', save_path))








