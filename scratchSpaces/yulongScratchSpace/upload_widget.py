from enum import Enum

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QPushButton, QFileDialog, \
    QMessageBox, QProgressBar, QDialog, QListWidget, QLineEdit
from PyQt5.QtCore import Qt

import dataStructures.logbookScan as Scan

import time

test = Scan.PageLayout(1)
test.addColumn(Scan.Column(0,50,0,""))


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
        self.parent.parent.filename = filename
        print(filename)


class file_select(QWidget):

    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout()
        self.parent = parent
        self.state = State.Unloaded

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
        # Todo: PDF preview

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
            self.parent.filename = fileName
            print(fileName)

    def upload(self):
        '''
        Commented out for easy testing
        '''
        self.show_progress_bar()
        self.state = State.Running
        self.parent.parent.state = 1  # Loading
        self.parent.setCurrentIndex(1)
        self.parent.drag.reset()

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
        #'''

    def show_progress_bar(self):
        # Todo: add a fake progress bar
        return


class preview(QWidget):
    def __init__(self):
        super().__init__()
        b = QPushButton("Working atm\nClick me to go back", self)

    def reset(self, page):
        # draw the boxes
        return


class control(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        self.buttons = self.init_buttons()
        layout.addWidget(self.buttons)

        self.columns = QListWidget()
        self.edit = QLineEdit()

        layout.addWidget(self.columns)
        layout.addWidget(self.edit)
        self.setLayout(layout)

    def init_buttons(self):
        buttons = QWidget()
        buttons_layout = QVBoxLayout()

        add_button = QPushButton("Add")
        del_button = QPushButton("Delete")
        cfm_button = QPushButton("Confirm")

        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(del_button)
        buttons_layout.addWidget(cfm_button)

        buttons.setLayout(buttons_layout)
        return buttons

    def add(self):
        # Add a new box
        return

    def delete(self):
        # Delete current box
        return

    def confirm(self):
        # Confirm boxes, go to backend
        return

    def reset(self,page):
        # fetch things
        return


class drag_page(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        layout = QVBoxLayout()
        self.preview = preview()
        self.control = control()

        layout.addWidget(self.preview)
        layout.addWidget(self.control)
        layout.setStretch(1, 1)
        layout.setStretch(0, 2.5)
        self.setLayout(layout)

    def reset(self):
        print(1)
        # To backend function: filename -> page layout


class upload_page(QStackedWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.filename = ""
        self.file_select_page = file_select(self)

        self.drag = drag_page(self)

        self.addWidget(self.file_select_page)
        self.addWidget(self.drag)
        self.setCurrentIndex(0)
