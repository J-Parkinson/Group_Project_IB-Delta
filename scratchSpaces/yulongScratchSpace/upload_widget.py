from enum import Enum

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QPushButton, QFileDialog, \
    QMessageBox, QProgressBar, QDialog
from PyQt5.QtCore import Qt

import time


class State(Enum):
    Unloaded = 0
    Loaded = 1
    Running = 2


class dnd_widget(QLabel):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        filename = e.mimeData().text()
        self.parent.state = State.Loaded
        self.parent.filename = filename
        print(filename)


class file_select(QWidget):

    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout()
        self.parent = parent
        self.state = State.Unloaded
        self.filename = ""
        #################################################
        # Welcome text (upload page)
        #################################################
        top_text = QLabel("Welcome to the Butterfly Logbook Scanner\n"
                          "Upload a file below then press the Read Page\n"
                          "button to begin transcription")
        top_text.setStyleSheet('color: black')
        layout.addWidget(top_text)
        layout.setAlignment(top_text, Qt.AlignCenter)

        #################################################
        # Drag-n-drop / preview window (upload page)
        #################################################
        drag_n_drop = dnd_widget(self)
        drag_n_drop.setFixedSize(650, 250)
        drag_n_drop.setStyleSheet('background-color:grey')

        d_n_p = QStackedWidget()
        d_n_p.addWidget(drag_n_drop)
        d_n_p.setCurrentIndex(0)

        layout.addWidget(d_n_p)
        layout.setAlignment(d_n_p, Qt.AlignCenter)

        #################################################
        # The clicking input (upload page)
        #################################################
        click_input = QWidget()
        click_input_layout = QHBoxLayout()

        click_input_text = QLabel("Or click the folder icon to browse a file to upload")
        click_input_text.setStyleSheet('color: black')
        click_input_layout.addWidget(click_input_text)

        click_input_button = QPushButton("Icon!")
        click_input_button.clicked.connect(self.open_file_window)
        click_input_button.setFixedSize(50, 50)
        click_input_layout.addWidget(click_input_button)

        click_input_layout.setAlignment(Qt.AlignCenter)
        click_input.setLayout(click_input_layout)
        layout.addWidget(click_input)

        #################################################
        # The button confirming input (upload page)
        #################################################
        upload_button = QPushButton("Read Page")
        upload_button.setFixedSize(200, 50)
        upload_button.clicked.connect(self.upload)
        layout.addWidget(upload_button)
        layout.setAlignment(upload_button, Qt.AlignCenter)

        #################################################
        # Some dummy label (upload page)
        #################################################
        layout.addWidget(QLabel())

        #################################################
        # Todo: connect input to backend
        #################################################

        self.setLayout(layout)

    def open_file_window(self):
        # noinspection PyCallByClass
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose a file to open", "",
                                                  "PDF (*.pdf)", "")
        if fileName:
            # Todo: Do something here! Load the file! Show a pretty preview!
            self.state = State.Loaded
            self.filename = fileName
            print(fileName)

    def upload(self):
        '''
        Commented out for easy testing
        self.show_progress_bar()
        self.state = State.Running
        self.parent.parent.state = 1  # Loading
        self.parent.setCurrentIndex(1)
        '''
        if self.state == State.Loaded:
            self.show_progress_bar()
            self.state = State.Running
            self.parent.parent.state = 1  # Loading
            self.parent.setCurrentIndex(1)

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)

            msg.setWindowTitle("Warning")
            msg.setText("No file loaded!")
            msg.setInformativeText("Please select a file to load")
            # msg.setStandardButtons(QMessageBox.Ok)

            msg.exec_()

    def show_progress_bar(self):
        # Todo: add a fake progress bar
        return


class drag_page(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()
        preview = QWidget()
        b = QPushButton("Working atm\nClick me to go back", preview)
        b.clicked.connect(lambda x:self.parent.setCurrentIndex(0))
        control = QWidget()
        layout.addWidget(preview)
        layout.addWidget(control)
        self.setLayout(layout)


class upload_page(QStackedWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        file_select_page = file_select(self)

        drag = drag_page(self)


        self.addWidget(file_select_page)
        self.addWidget(drag)
        self.setCurrentIndex(0)
