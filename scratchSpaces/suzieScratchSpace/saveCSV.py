from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, \
    QStackedWidget, QBoxLayout, QHBoxLayout, QFileDialog, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QLinearGradient, QBrush, QPalette, QFont, QPixmap


class saveCSVWindow(QWidget):
# TODO: make pretty
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        grid.setSpacing(10)

        self.setStyleSheet('color: black; background-color:white')
        title = QLabel("The file has successfully been transcribed! \n Select a folder to save the transcribed file into and then press Save.")

        location_button = QPushButton()
        location_button.setText("Choose Location")

        grid.addWidget(title,1,0, 1,2)
        grid.addWidget(location_button, 2, 0)

        cancel_button = QPushButton()
        cancel_button.setText("Cancel")

        grid.addWidget(cancel_button,2,1)

        cont_button = QPushButton()
        cont_button.setText("Save")

        check_box = QCheckBox("Open file once saved")
        check_box.setStyleSheet('background-color: white')
        grid.addWidget(check_box, 4, 0)
        grid.addWidget(cont_button, 4, 1)
        grid.addWidget(cancel_button, 3, 1)

        location_button.clicked.connect(self.chooseDir)
        cont_button.clicked.connect(lambda: self.saveFile(check_box))

        self.setLayout(grid)


    def chooseDir(self):
        dir = QFileDialog.getExistingDirectory(self, "Open Directory to Save File into", "")
        print(dir)


    def saveFile(self, b):

        if b.isChecked():
            print("will open file")
        else:
            print("will not open file")

        print("saving file")

        saved = QLabel("Saved!")
        saved.show()






