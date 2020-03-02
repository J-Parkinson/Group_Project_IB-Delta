from enum import Enum

from PyQt5.QtGui import QIntValidator, QPainter, QColor, QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QPushButton, QFileDialog, \
    QMessageBox, QProgressBar, QDialog, QListWidget, QLineEdit, QGridLayout, QSpinBox, QApplication, QStyle, \
    QMainWindow, QInputDialog, QProgressBar
from PyQt5.QtCore import Qt, QSize
import time

from utils.structures import logbookScan as Scan, states
from utils.spelling.spell_check import correct_table


from imagePreprocessing import backendnew


def newPreset():
    page = Scan.PageLayout(1)
    page.addColumn(Scan.Column((0, 0), (50, 200), 1, ""))
    page.addColumn(Scan.Column((50, 0), (100, 200), 1, ""))
    page.addColumn(Scan.Column((100, 0), (150, 200), 1, ""))
    page.addColumn(Scan.Column((150, 0), (200, 200), 1, ""))
    return page


class preview(QWidget):
    class State(Enum):
        Normal = 0
        OnV = 1
        OnH = 2
        ClickedV = 3
        ClickedH = 4
        OnVUp = 5
        ClickedVUp = 6
        OnLeftMost = 7
        ClickedLeftMost = 8

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.page = None
        self.control = None
        self.state = self.State.Normal
        self.onColumn = 0
        self.setMouseTracking(1)
        self.offset = 10
        self.pixMap = QPixmap("gui/resources/tempBg.png")
        self.pixSize = self.pixMap.size()

        # In memory of the lovely stress-reducing button.
        # b = QPushButton("Working atm\nClick me to reduce stress :-)", self)
        # b.move(500, 350)

    def reset(self, page):
        # draw the boxes
        self.page = page
        self.update()
        return

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        pixMap = self.pixMap.scaled(QSize(self.width(),self.height()-self.offset), Qt.KeepAspectRatio)
        self.pixSize = pixMap.size()

        qp.drawPixmap(0, self.offset, pixMap)

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
        elif self.state == self.State.OnVUp:
            self.state = self.State.ClickedVUp
        elif self.state == self.State.OnLeftMost:
            self.state = self.State.ClickedLeftMost
        self.update_cursor()

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()

        if self.state == self.State.ClickedLeftMost:
            self.control.columns.setCurrentRow(self.onColumn)
            self.control.edit.tlx.setValue(x)
            return

        if self.state == self.State.ClickedH:
            self.control.columns.setCurrentRow(self.onColumn)
            self.control.edit.brx.setValue(x)
            return

        if self.state == self.State.ClickedVUp:
            self.control.edit.tly.setValue(y)
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
                if abs(x - self.page.columnList[0].tlCoord[0]) < 10:
                    self.state = self.State.OnLeftMost
                    self.update_cursor()
                    self.onColumn = 0
                    return

            # Lower Row Dragging test
            x1, y1 = self.page.columnList[-1].brCoord
            if x < x1 and abs(y - self.offset - y1) < 5:
                self.state = self.State.OnV
                self.update_cursor()
                return

            # Upper Row Dragging test
            x1 = self.page.columnList[-1].brCoord[0]
            y1 = self.page.columnList[-1].tlCoord[1]
            if x < x1 and abs(y - self.offset - y1) < 5:
                self.state = self.State.OnVUp
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
        elif self.state == self.State.OnV or self.state == self.State.OnVUp:
            QApplication.setOverrideCursor(Qt.SplitVCursor)
        elif self.state == self.State.OnH or self.state == self.State.OnLeftMost:
            QApplication.setOverrideCursor(Qt.SplitHCursor)
        else:
            QApplication.setOverrideCursor(Qt.ClosedHandCursor)

    def sanCheck(self):
        errors = 0

        # check for y coords
        if self.page.columnList[0].brCoord[1] < self.page.columnList[0].tlCoord[1]:
            errors += 1

        # check for x coords
        n = len(self.page.columnList)
        i = 0
        for c in self.page.columnList:
            if i == n-1:
                if c.brCoord[0] >= self.pixSize.width():
                    errors += 1
            else:
                next = self.page.columnList[i+1]
                if next.tlCoord[0] <= c.tlCoord[0]:
                    errors += 1
                i += 1

        return errors

    def scaleBack(self):
        w_factor = self.pixMap.width() / self.pixSize.width()
        h_factor = self.pixMap.height() / self.pixSize.height()
        for c in self.page.columnList:
            c.tlCoord = (c.tlCoord[0]*w_factor, c.tlCoord[1]*h_factor)
            c.brCoord = (c.brCoord[0] * w_factor, c.brCoord[1] * h_factor)


class control(QWidget):
    def __init__(self, parent):
        super().__init__()
        layout = QHBoxLayout()

        self.parent = parent
        self.columns = QListWidget()
        self.page = None
        self.preview = None
        self.name_index = 0
        self.edit = self.init_lines()
        self.buttons = self.init_buttons()
        self.warn_count = 0

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

        layout.addWidget(QLabel("Spelling correction dictionary:"), 3, 0)

        lines.dic_path = QLineEdit()
        lines.dic_path.setReadOnly(1)

        lines.dic_button = QPushButton("Add dictionary")
        lines.dic_button.clicked.connect(self.open_file_window)
        layout.addWidget(lines.dic_path, 4, 0, 1, 2)
        layout.addWidget(lines.dic_button, 4, 2)

        lines.setLayout(layout)
        return lines

    def open_file_window(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose a file to open", "",
                                                  "PDF (*.pdf)", "")
        if fileName:
            self.edit.dic_path.setText(fileName)
            self.page.columnList[self.columns.currentRow()].dictionary = fileName

    def show_coords(self):
        row = self.columns.currentRow()
        if self.page is not None and self.columns.currentItem() is not None:
            c = self.page.columnList[row]
            self.edit.tlx.setValue(c.tlCoord[0])
            self.edit.tly.setValue(c.tlCoord[1])
            self.edit.brx.setValue(c.brCoord[0])
            self.edit.bry.setValue(c.brCoord[1])
            if c.fieldName == "":
                c.fieldName = self.columns.currentItem().text()
            self.edit.title.setText(c.fieldName)
            if c.dictionary is not None:
                self.edit.dic_path.setText(c.dictionary)
            else:
                self.edit.dic_path.setText("")

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
        upload = self.parent.parent

        if self.warn_count < 2:
            self.warn_count += 1
            if upload.warning("Confirming the changes?", "WARNING:",
                            "The program's output DEPENDS ALMOST ENTIRELY on your indication.\n\n"
                            "Click 'yes' to continue. ",
                            1) == QMessageBox.No:
                return

        errors = self.preview.sanCheck()
        if errors > 0:
            upload.warning("Column san-check failed!", "ERROR:",
                           "You have " + str(errors)  + " misplaced columns.\n"
                           "Please remove overlapped or out-of-bound columns to continue.\n",
                            0)
            return

        self.preview.scaleBack()

        columnLocations = []
        for c in self.page.columnList:
            columnLocations.append(c.tlCoord[0])
        columnLocations.append(self.page.columnList[-1].brCoord[0])

        rowLocations = [self.page.columnList[0].tlCoord[1], self.page.columnList[0].brCoord[1]]

        column_dicts = {}
        for i, c in enumerate(self.page.columnList):
            if c.dictionary is not None:
                column_dicts[i] = c.dictionary

        table = backendnew.createTable(self.parent.parent.filename,
                                       #columnLocations,
                                       [375, 790, 1690, 2100, 2520],
                                       rowLocations,
                                       #[0, self.parent.preview.pixSize.height()],
                                       self.parent.preview.pixSize.width(),
                                       self.parent.preview.pixSize.height(),
                                       self.parent.parent.noPages)
        correct_table(table, column_dicts)
        # transfer table to saveCSV

        upload.save_page.table = table
        upload.state = states.uploadState.Saving
        upload.setCurrentIndex(2)

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
        self.columns.setCurrentRow(0)
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
        self.page = newPreset()
        self.preview.reset(self.page)
        self.control.reset(self.page)
