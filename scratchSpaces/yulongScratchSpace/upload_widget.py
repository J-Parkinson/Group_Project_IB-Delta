from enum import Enum

from PyQt5.QtGui import QIntValidator, QPainter, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QPushButton, QFileDialog, \
    QMessageBox, QProgressBar, QDialog, QListWidget, QLineEdit, QGridLayout, QSpinBox, QApplication, QStyle, \
    QMainWindow, QInputDialog, QProgressBar
from PyQt5.QtCore import Qt, QSize, pyqtSignal as QSignal, QThread

import dataStructures.logbookScan as Scan
import imagePreprocessing.imageScanningAndPreprocessing as ImageProcess
from PIL import Image

from concurrent.futures import ThreadPoolExecutor

import time

from scratchSpaces.suzieScratchSpace import saveCSV

test = Scan.PageLayout(1)
test.addColumn(Scan.Column((0, 0), (50, 200), 1, ""))
test.addColumn(Scan.Column((50, 0), (100, 200), 1, ""))
test.addColumn(Scan.Column((100, 0), (150, 200), 1, ""))
test.addColumn(Scan.Column((150, 0), (200, 200), 1, ""))


def warning(title, text, description,two_buttons):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)

    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setInformativeText(description)

    if two_buttons:
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    return msg.exec_()


class State(Enum):
    Unloaded = 0
    Loaded = 1
    Running = 2
    Saving = 3


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
            warning("Warning", "Wrong file type!", "Please select a .pdf or .jpeg file!",0)
            return
        self.parent.state = State.Loaded
        self.parent.parent.filename = filename[8:]
        print(filename[8:])


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
            self.state = State.Loaded
            self.parent.filename = fileName
            print(fileName)

    def askForPages(self):

        ok = False
        num = 0

        # Todo: very problematic behavior, fix it
        while (not ok) or (num < 1):
            num, ok = QInputDialog.getInt(self, "Set page span",
                                          "Enter the number of adjacent pages that make up one logbook table.", 1)

        return num

    def upload(self):
        '''
        Commented out for easy testing
        '''
        noPages = noPageSpread = max(self.askForPages(), 1)

        '''progressBar = ProgressBar()
        progressBar.start()'''
        '''with ThreadPoolExecutor() as executor:
            thread = executor.submit(ImageProcess.handleColumnGUI(self.parent.filename, noPages), 'columnMerge')
            (columnImage, width, height) = thread.result()'''

        columnImage, width, height = ImageProcess.handleColumnGUI(self.parent.filename, noPages)#, progressBar)
        #Image.frombytes("RGB", (width, height), columnImage.read()).show()
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
            self.parent.drag.reset()
        else:
            warning("Warning","No file loaded!","Please select a file to load",0)
        #'''


'''class ProgressBar(QMainWindow, QThread):
    def __init__(self, thread, noSteps=1):
        # super(ProgressBar, self).__init__(parent)
        super(ProgressBar, self).__init__(QThread)

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

        self.connect()

    def hide(self):
        self.close()
        return

    def update(self, string):
        self.currentStep += 1
        self.progress.setValue(self.currentStep / self.noSteps)
        self.text.setText(string)
        return'''


class preview(QWidget):
    class State(Enum):
        Normal = 0
        OnV = 1
        OnH = 2
        ClickedV = 3
        ClickedH = 4

    def __init__(self,parent):
        super().__init__()

        self.parent = parent
        self.page = None
        self.control = None
        self.state = self.State.Normal
        self.onColumn = 0
        self.setMouseTracking(1)
        self.offset = 10

        b = QPushButton("Working atm\nClick me to reduce stress :-)", self)
        b.move(500, 350)

    def reset(self, page):
        # draw the boxes
        self.page = page
        self.update()
        return

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        qp.setBrush(QColor(93, 173, 226))  # Light blue, ideally
        qp.setOpacity(0.6)  # Some lovely opaque, ideally
        for c in self.page.columnList:
            (x1, y1), (x2, y2) = c.tlCoord, c.brCoord
            qp.drawRect(x1, y1 + self.offset, x2 - x1, y2 - y1)

        qp.setBrush(QColor(100, 100, 100))
        qp.drawRect(0, 0, self.width(), self.offset)

        qp.setBrush((QColor(0, 0, 0)))
        qp.setOpacity(1.0)
        for c in self.page.columnList:
            (x1, y1), (x2, y2) = c.tlCoord, c.brCoord
            qp.drawLine(x1, 0, x1, self.offset)
            qp.drawLine(x2, 0, x2, self.offset)

        qp.end()

    def mousePressEvent(self, e):
        if self.state == self.State.OnH:
            self.state = self.State.ClickedH
        elif self.state == self.State.OnV:
            self.state = self.State.ClickedV
        self.update_cursor()

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()

        # Todo: some bad behaviors here, fix it !!!!!!

        if self.state == self.State.ClickedH:
            self.control.columns.setCurrentRow(self.onColumn)
            self.control.edit.brx.setValue(x)
            return

        if self.state == self.State.ClickedV:
            self.control.edit.bry.setValue(y)
            return

        if self.state == self.State.Normal:
            # Column Dragging test
            if y < self.offset + 4:
                i = 0
                for c in self.page.columnList:
                    if abs(x - c.brCoord[0]) < 10:
                        self.state = self.State.OnH
                        self.update_cursor()
                        self.onColumn = i
                        return
                    else:
                        i += 1

            # Row Dragging test
            x1, y1 = self.page.columnList[len(self.page.columnList) - 1].brCoord
            if x < x1 and abs(y - self.offset - y1) < 5:
                self.state = self.State.OnV
                self.update_cursor()
                return

        self.state = self.State.Normal
        self.update_cursor()

    def mouseReleaseEvent(self, e):
        self.state = self.State.Normal
        self.mouseMoveEvent(e)

    def update_cursor(self):
        if self.state == self.State.Normal:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
        elif self.state == self.State.OnV:
            QApplication.setOverrideCursor(Qt.SplitVCursor)
        elif self.state == self.State.OnH:
            QApplication.setOverrideCursor(Qt.SplitHCursor)
        else:
            QApplication.setOverrideCursor(Qt.ClosedHandCursor)


class control(QWidget):
    def __init__(self,parent):
        super().__init__()
        layout = QHBoxLayout()

        self.parent = parent
        self.columns = QListWidget()
        self.page = None
        self.preview = None
        self.name_index = 0
        self.edit = self.init_lines()
        self.buttons = self.init_buttons()

        self.columns.currentItemChanged.connect(self.show_coords)
        layout.addWidget(self.buttons)
        layout.addWidget(self.columns)
        layout.addWidget(self.edit)
        self.setLayout(layout)



    def init_lines(self):
        lines = QWidget()
        layout = QGridLayout()

        layout.addWidget(QLabel("Top-left Corner:"), 0, 0)

        lines.tlx = QSpinBox()
        lines.tlx.setRange(0, 9999)
        lines.tlx.valueChanged.connect(self.update_tlx_coords)
        layout.addWidget(lines.tlx, 0, 1)

        lines.tly = QSpinBox()
        lines.tly.setRange(0, 9999)
        lines.tly.valueChanged.connect(self.update_tly_coords)
        layout.addWidget(lines.tly, 0, 2)

        layout.addWidget(QLabel("Bottom-right Corner:"), 1, 0)

        lines.brx = QSpinBox()
        lines.brx.setRange(0, 9999)
        lines.brx.valueChanged.connect(self.update_brx_coords)
        layout.addWidget(lines.brx, 1, 1)

        lines.bry = QSpinBox()
        lines.bry.setRange(0, 9999)
        lines.bry.valueChanged.connect(self.update_bry_coords)
        layout.addWidget(lines.bry, 1, 2)

        layout.addWidget(QLabel("Column Title:"), 2, 0)
        lines.title = QLineEdit()
        lines.title.textChanged.connect(self.update_text)
        layout.addWidget(lines.title, 2, 1, 1, 2)

        lines.setLayout(layout)
        return lines

    def show_coords(self):
        row = self.columns.currentRow()
        if self.page is not None:
            c = self.page.columnList[row]
            self.edit.tlx.setValue(c.tlCoord[0])
            self.edit.tly.setValue(c.tlCoord[1])
            self.edit.brx.setValue(c.brCoord[0])
            self.edit.bry.setValue(c.brCoord[1])
            if c.fieldName == "":
                c.fieldName = self.columns.currentItem().text()
            self.edit.title.setText(c.fieldName)

    def update_tlx_coords(self, i):
        row = self.columns.currentRow()
        c = self.page.columnList[row]
        c.tlCoord = i, c.tlCoord[1]
        if not row == 0:
            self.page.columnList[row - 1].brCoord = i, self.page.columnList[row - 1].brCoord[1]
        self.preview.reset(self.page)

    def update_tly_coords(self, i):
        for c in self.page.columnList:
            c.tlCoord = c.tlCoord[0], i
        self.preview.reset(self.page)

    def update_brx_coords(self, i):
        row = self.columns.currentRow()
        c = self.page.columnList[row]
        c.brCoord = i, c.brCoord[1]
        if row < len(self.page.columnList) - 1:
            self.page.columnList[row + 1].tlCoord = i, self.page.columnList[row + 1].tlCoord[1]
        self.preview.reset(self.page)

    def update_bry_coords(self, i):
        for c in self.page.columnList:
            c.brCoord = c.brCoord[0], i
        self.preview.reset(self.page)

    def update_text(self, text):
        row = self.columns.currentRow()
        self.page.columnList[row].fieldName = text
        self.columns.currentItem().setText(text)
        self.preview.reset(self.page)

    def init_buttons(self):
        buttons = QWidget()
        buttons_layout = QVBoxLayout()

        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add)

        del_button = QPushButton("Delete")
        del_button.clicked.connect(self.delete)
        cfm_button = QPushButton("Confirm")
        cfm_button.clicked.connect(self.confirm)

        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(del_button)
        buttons_layout.addWidget(cfm_button)

        buttons.setLayout(buttons_layout)
        return buttons

    def add(self):
        # Add a new box
        last = self.page.columnList[self.columns.count() - 1]
        self.columns.addItem("new column " + str(self.name_index))
        self.name_index += 1
        self.page.addColumn(Scan.Column((last.brCoord[0], last.tlCoord[1]),
                                        (last.brCoord[0] + 50, last.brCoord[1]),
                                        1, "new column " + str(self.name_index)))
        self.preview.reset(self.page)
        self.name_index += 1
        return

    def delete(self):
        # Delete current box
        row = self.columns.currentRow()
        if not ((row == 0) or (row == self.columns.count() - 1)):
            self.page.columnList[row + 1].tlCoord = \
                (self.page.columnList[row - 1].brCoord[0], self.page.columnList[row + 1].tlCoord[1])
        self.columns.takeItem(row)
        self.page.removeColumn(self.page.columnList[row])
        self.preview.reset(self.page)
        return

    def confirm(self):
        # todo: switch to sate 3 in upload page to make stack have the save page
        self.parent.parent.state = State.Saving
        self.parent.parent.setCurrentIndex(2)
        return

    def reset(self, page):
        self.page = page
        self.name_index = 0
        self.columns.clear()

        for c in page.columnList:
            if not c.fieldName == "":
                self.columns.addItem(c.fieldName)
            else:
                self.columns.addItem("new column " + str(self.name_index))
                self.name_index += 1
        return


class drag_page(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.page = None

        layout = QVBoxLayout()
        self.control = control(self)
        self.preview = preview(self)
        self.control.preview = self.preview
        self.preview.control = self.control

        layout.addWidget(self.preview)
        layout.addWidget(self.control)
        layout.setStretch(1, 1)
        layout.setStretch(0, 2.5)
        self.setLayout(layout)

    def reset(self):
        # To backend function: filename -> page layout
        self.page = test
        self.preview.reset(self.page)
        self.control.reset(self.page)


class upload_page(QStackedWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.filename = ""

        self.file_select_page = file_select(self)
        self.drag = drag_page(self)
        self.save_page = saveCSV.saveCSVWindow([])

        self.addWidget(self.file_select_page)
        self.addWidget(self.drag)
        self.addWidget(self.save_page)
        self.setCurrentIndex(0)
