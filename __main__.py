#################################################
# Modules import
#################################################

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, \
    QStackedWidget, QBoxLayout, QHBoxLayout, QFileDialog, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QLinearGradient, QBrush, QPalette, QFont, QPixmap, QPainter, QImage
from pathlib import Path
import platform
import os
import subprocess

from gui import upload_widget, modifyCSV

application = QApplication([])


class State:
    Normal = 0
    Loading = 1
    First_time = 2


class Window(QWidget):

    def __init__(self):
        #################################################
        # Initialization
        #################################################

        # Layout
        QWidget.__init__(self)
        self.resize(1080, 800)
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Dingy Skippers")

        main_layout = QGridLayout()

        # Style
        self.setAutoFillBackground(True)
        # noinspection PyTypeChecker,PyCallByClass
        background = QColor.fromRgb(248, 246, 238)
        title_font = QFont("Georgia", 25)

        p = self.palette()
        p.setColor(self.backgroundRole(), background)
        self.setPalette(p)

        # Preference
        self.state = State.Normal

        # Components
        top_left = QMainWindow()
        top_right = QWidget()
        bottom_left = QWidget()
        bottom_right = QStackedWidget()

        #################################################
        # The top left corner:
        # Should be some butterfly icons
        #################################################

        pic = QLabel(top_left)

        # use full ABSOLUTE path to the image, not relative
        bPM = QPixmap(os.getcwd() + "/gui/resources/butterfly.png")
        bPM = bPM.scaledToWidth(150)
        pic.setPixmap(bPM)
        pic.setGeometry(0, 0, 10, 10)
        main_layout.addWidget(pic, 0, 0)
        #################################################
        # The top right corner:
        # Just a label
        #################################################
        title = QLabel()
        title.setText("Butterfly Logbook Scanner")
        title.setFont(title_font)
        title.setStyleSheet('color:#6D214F')

        top_right_layout = QVBoxLayout()
        top_right_layout.addWidget(title)
        top_right_layout.setAlignment(title, Qt.AlignCenter)

        top_right.setLayout(top_right_layout)
        main_layout.addWidget(top_right, 0, 1)

        #################################################
        # The bottom right corner:
        # A stack of useful pages
        #################################################
        # Todo: design an initial page

        # Initial page
        ini_label = QLabel("Initial Page")
        ini_label.setStyleSheet('color:#6D214F')
        ini_label.move(100, 100)
        ini_label.resize(500, 500)

        # Upload page
        upload_page = upload_widget.upload_page(self)

        # Data page

        # Todo: This window is buggy, fix it
        data_page = modifyCSV.ModifyMainWindow()

        # Tutorial page, working atm
        # Todo: design a tutorial page, we've finally got our hands on it
        tutorial_page = QLabel()
        #QPushButton("tutorial", tutorial_page)

        # Finally, add all those pages to the stack
        bottom_right.addWidget(upload_page)
        bottom_right.addWidget(data_page)
        bottom_right.addWidget(tutorial_page)
        bottom_right.addWidget(ini_label)

        if self.state == State.First_time:
            bottom_right.setCurrentIndex(2)
        else:
            bottom_right.setCurrentIndex(3)
        main_layout.addWidget(bottom_right, 1, 1)

        #################################################
        # The bottom left corner:
        # A bunch of functional buttons
        #################################################
        #todo: can we change the size of the buttons so that they are a bit smaller? -> theres not enough space for all the
        # mappings and rule drop downs etc without having to scroll -> not essential, would just look nicer

        # Initialize buttons
        bottom_leftLayout = QVBoxLayout()
        buttons = [QPushButton() for _ in range(3)]
        for b in buttons:
            b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            bottom_leftLayout.addWidget(b)

        # function for changing all buttons back to default when a new one is clicked
        # noinspection PyShadowingNames
        def reset_buttons_color():
            for b in buttons:
                b.setStyleSheet('background-color:rgb(248,154,121); color:black')

        reset_buttons_color()

        # Upload page -- button 0
        def upload_signal():
            if self.load_warning():
                print("button 0 pressed")
                reset_buttons_color()
                buttons[0].setStyleSheet("background-color: rgb(248,246,238); color:#6D214F")
                bottom_right.setCurrentIndex(0)
                upload_page.state = 0  # Unloaded
                upload_page.setCurrentIndex(0)
                self.state = State.Normal

        buttons[0].setText("Upload PDF")
        buttons[0].clicked.connect(upload_signal)

        # Data page -- button 1
        def data_signal():
            if self.load_warning():
                print("button 1 pressed")
                bottom_right.setCurrentIndex(1)
                reset_buttons_color()
                buttons[1].setStyleSheet("background-color: rgb(248,246,238); color:#6D214F")
                self.state = State.Normal


        buttons[1].setText("Convert CSV to Standard Format")
        buttons[1].clicked.connect(data_signal)

        # Tutorial page -- button 2
        def tutorial_signal():
            if self.load_warning():
                print("button 2 pressed")
                filepath = os.getcwd() + "\gui\\resources\loadThisFile.docx"
                os.startfile(filepath)



        buttons[2].setText("View Help Guide")
        buttons[2].clicked.connect(tutorial_signal)

        # Dummies to make it looks good
        for _ in range(3):
            dummy = QLabel()
            dummy.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            bottom_leftLayout.addWidget(dummy)

        bottom_left.setLayout(bottom_leftLayout)
        main_layout.addWidget(bottom_left, 1, 0)

        #################################################
        # Things about the main layout
        #################################################
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 3)
        main_layout.setRowStretch(0, 1)
        main_layout.setRowStretch(1, 9)
        self.setLayout(main_layout)
        p = platform.system()
        if p == "Windows":
            print(1)
            application.setStyle("Windows")
        elif p == "Darwin":
            application.setStyle("Macintosh")
        else:
            application.setStyle("Plastique")

    def preference(self):
        return 0

    def load_warning(self):
        if not self.state == State.Loading:
            return 1

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        msg.setWindowTitle("Warning!")
        msg.setText("File not saved yet!")
        msg.setInformativeText("You will lose your loaded file if you go to another window now.\n"
                               "Are you sure you want to abort?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        return_value = msg.exec_()
        return return_value == QMessageBox.Yes

    def run(self):
        self.show()
        application.exec_()



    def closeEvent(self, e):
        if self.state == State.Loading:
            if self.load_warning():
                e.accept()
            else:
                e.ignore()
        else:
            e.accept()


if __name__ == "__main__":
    app = Window()
    app.run()
