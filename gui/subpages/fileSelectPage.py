from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout, QPushButton, QApplication, \
    QStyle, QInputDialog, QFileDialog, QMessageBox

from PIL import Image

import imagePreprocessing.imageScanningAndPreprocessing as ImageProcess
from utils.structures import states


class dnd_widget(QLabel):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        QApplication.setOverrideCursor(Qt.DragMoveCursor)
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()
        QApplication.setOverrideCursor(Qt.ArrowCursor)

    def dropEvent(self, e):
        filename = e.mimeData().text()
        if not (filename[-4:] == ".pdf"):
            self.parent.parent.warning("Warning", "Wrong file type!", "Please select a .pdf or .jpeg file!", 0)
            return
        self.parent.state = states.uploadState.Loaded
        self.parent.parent.filename = filename[8:]
        print(filename[8:])

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setBrush(QColor(150, 150, 150))

        qp.drawRect(0,0,650,250)

class file_select(QWidget):

    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout()
        self.parent = parent
        self.state = states.uploadState.Unloaded

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
        #drag_n_drop.setStyleSheet('background-color:grey')

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

        click_input_button = QPushButton()
        click_input_button.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogOpenButton))
        click_input_button.setIconSize(QSize(30, 30))
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
            self.state = states.uploadState.Loaded
            self.parent.filename = fileName
            print(fileName)

    def askForPages(self):

        ok = False
        num = 0

        num, ok = QInputDialog.getInt(self, "Set page span",
                                          "Enter the number of adjacent pages that make up one logbook table.", 1)

        if (not ok) or (num < 1):
            return -1
        else:
            return num

    def upload(self):
        '''
        Commented out for easy testing
        
        noPages = self.askForPages()
        
        if noPages <= 0:
            return
        self.parent.noPages = noPages
        # progressBar = ProgressBar(noPages * 2 + 2)
        # columnImage = ImageProcess.handleColumnGUI(self.parent.filename, noPages, progressBar)
        #         # print(columnImage)

        self.parent.previewImg, self.parent.imgWidth, self.parent.imgHeight\
            = ImageProcess.handleColumnGUI(self.parent.filename, noPages)  # , progressBar)
        self.parent.previewImg = Image.frombytes("RGB",(self.parent.imgWidth, self.parent.imgHeight),
                                                self.parent.previewImg.read()).save("gui/resources/tempBg.png")
        self.state = states.uploadState.Running
        self.parent.parent.state = 1  # Loading
        self.parent.setCurrentIndex(1)
        self.parent.drag.reset()

        #'''
        if self.state == states.uploadState.Loaded:
            noPages = self.askForPages()

            if noPages <= 0:
                return
            self.parent.noPages = noPages
            # progressBar = ProgressBar(noPages * 2 + 2)
            # columnImage = ImageProcess.handleColumnGUI(self.parent.filename, noPages, progressBar)
            #         # print(columnImage)

            self.parent.previewImg, self.parent.imgWidth, self.parent.imgHeight \
                = ImageProcess.handleColumnGUI(self.parent.filename, noPages)[0]  # , progressBar)
            self.parent.previewImg = Image.frombytes("RGB", (self.parent.imgWidth, self.parent.imgHeight),
                                                     self.parent.previewImg.read()).save("gui/resources/tempBg.png")
            self.state = states.uploadState.Running
            self.parent.parent.state = 1  # Loading
            self.parent.setCurrentIndex(1)
            self.parent.drag.reset()

        else:
            self.parent.warning("Warning","No file loaded!","Please select a file to load",0)
        #'''
