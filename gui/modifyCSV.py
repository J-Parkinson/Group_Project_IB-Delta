import pathlib

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, \
    QStackedWidget, QBoxLayout, QHBoxLayout, QFileDialog, QCheckBox, QComboBox, QLineEdit, QScrollArea, QStyle, \
    QMessageBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QLinearGradient, QBrush, QPalette, QFont, QPixmap

from utils.csv import matrix_to_csv
from gui.subpages import Mappings


def warning(title, text, description, two_buttons):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)

    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setInformativeText(description)

    if two_buttons:
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    return msg.exec_()


# ----------------------------------------------------------------------------------------------------------------
# Class for the widget containing everything for the modifying CSV structure feature. Uses a stacked widget to move
# between pages and has a Start Again button to allow user to restart the process.

class ModifyMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('color: black')
        self.layout = QGridLayout()
        self.main = QStackedWidget()
        upload = UploadCSV(self.main,self)
        upload.parent = self
        self.main.addWidget(upload)  # index 0
        self.main.setCurrentIndex(0)

        reset_btn = QPushButton("Start Again")
        reset_btn.clicked.connect(lambda: self.reset(True))
        self.layout.addWidget(reset_btn, 0, 0)
        self.layout.addWidget(self.main, 1, 0)
        self.setLayout(self.layout)

    # ----------------------------------------------------------------------------------------------------------------
    # interrupt: boolean, true if pressing the Start Again button during the process of filling in the mappings, gives
    # the user a pop-up warning that their progress will not be saved and then returns to the upload CSV page; false
    # when the resulting CSV has been saved so no warning is given and user is returned to the upload CSV page again
    def reset(self, interrupt):
        if interrupt:
            if warning("Leave Now?", "WARNING:",
                       "Are you sure you want to leave this page?\n"
                       "Your progress will not be saved.\n\n"
                       "Click 'yes' to continue. ",
                       1) == QMessageBox.No:
                return
        self.layout.removeWidget(self.main)
        self.main.deleteLater()
        new_main = QStackedWidget()
        new_main.addWidget(UploadCSV(new_main,self))  # index 0
        new_main.setCurrentIndex(0)
        self.layout.addWidget(new_main, 1, 0)
        self.main = new_main


# ----------------------------------------------------------------------------------------------------------------
# Class for the widget to upload a CSV file, contains a pointer to the ModifyMainWindow object (parent) that created it
class UploadCSV(QWidget):
    def __init__(self, stack,parent):
        super().__init__()
        self.setStyleSheet('color: black')
        self.parent = parent
        self.table = None
        self.stack_wid = stack
        layout = QGridLayout()
        title = QLabel("Rules and Mappings")
        layout.addWidget(title)
        welc_text = QLabel("Welcome to the Rules and Mappings feature.\nHere you will be able to modify the structure "
                           "of the CSV file and convert it to a standard format. \nGet started by clicking the file "
                           "icon to browse and select the CSV file!")
        layout.addWidget(welc_text)
        click_input_button = QPushButton()
        click_input_button.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogOpenButton))
        click_input_button.setIconSize(QSize(30, 30))
        click_input_button.clicked.connect(self.open_file_window)
        layout.addWidget(click_input_button)

        next_btn = QPushButton("Next")
        next_btn.clicked.connect(self.goto_rules)
        layout.addWidget(next_btn)

        self.setLayout(layout)

    # ----------------------------------------------------------------------------------------------------------------
    # Function to provide pop-up window for user to choose a CSV file which is then converted to a matrix representation
    # and stored as internal state 'self.table'

    def open_file_window(self):

        file_name, _ = QFileDialog.getOpenFileName(self, "Choose a file to open", "", "CSV (*.csv)", "")
        if file_name:
            self.table = matrix_to_csv.read_csv(file_name)

    # ----------------------------------------------------------------------------------------------------------------
    # Function to link to button to move on to the Rules window, first checks that a valid CSV has been selected and
    # provides a pop up warning if not. Creates instance of RulesWindow and assigns it's parent to the same parent of
    # this object
    def goto_rules(self):
        if self.table is not None:
            rules_window = RulesWindow(self.stack_wid, self.table,self.parent)
            rules_window.parent = self.parent
            self.stack_wid.addWidget(rules_window)

            self.stack_wid.setCurrentIndex(1)
        else:
            warning('Error', 'No CSV selected!', 'Please select a CSV file to import', False)


# ----------------------------------------------------------------------------------------------------------------
# Class for the RulesWindow widget. Has a scrollable area so that when lots of rules are added the user can scroll
# through whole page rather than all widgets adjusting their size and getting smaller.
class RulesWindow(QWidget):

    def __init__(self, stack, table,parent):
        super().__init__()
        self.parent = parent
        self.table = table
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        self.scroll = QScrollArea(self)
        main_layout.addWidget(self.scroll)
        self.scroll.setWidgetResizable(True)
        self.scroll_area_content = QWidget(self.scroll)
        self.grid = QGridLayout(self.scroll_area_content)
        self.scroll_area_content.setLayout(self.grid)

        self.scroll.setWidget(self.scroll_area_content)

        # where to start the rules within the grid
        self.col_index_y = 3

        self.grid.setHorizontalSpacing(10)
        self.setStyleSheet('color: black; background-color: rgb(248, 246, 238)')

        self.rule_list = []
        self.rules = 0

        self.stack_wid = stack

        self.initUI()

    # ----------------------------------------------------------------------------------------------------------------
    # Initialises the main components of the rule window. Includes help text to provide user with guidance.
    def initUI(self):

        title = QLabel("Create Rules to Split Columns")
        help_text = QLabel()
        help_text.setFont(QFont('Courier', 12))
        try:
            path = pathlib.Path(__file__).parent
            with open(path / 'resources' / 'Splitting_rules.txt', mode='r') as reader:
                desc = ''
                for line in reader:
                    desc += line
                help_text.setText(desc)
        except IOError:
            print('Failed to find file')

        self.grid.addWidget(title, 0, 0, 1, 2, Qt.AlignCenter)
        self.grid.addWidget(help_text, 1, 0, 1, 2, Qt.AlignTop)

        rule1 = NewRule(self.table)

        self.rules += 1
        rule1.rule_wind = self
        self.rule_list.append(rule1)
        self.grid.addWidget(rule1, self.rules + 2, 0, 1, 2)

        new_rule_btn = QPushButton("Add new rule")
        new_rule_btn.clicked.connect(self.new_rule)

        cont_btn = QPushButton("Confirm all Rules and Continue ")
        cont_btn.clicked.connect(self.next)

        self.grid.addWidget(new_rule_btn, 2, 0, 1, 1)
        self.grid.addWidget(cont_btn, 2, 1, 1, 1)

    # ----------------------------------------------------------------------------------------------------------------
    # Adds a rule to the window, increments the count of the current rules and appends a pointer to this new rule to
    # the list of pointers to all current rules
    def new_rule(self):

        self.rules += 1
        rule = NewRule(self.table)
        rule.rule_wind = self
        self.rule_list.append(rule)

        self.grid.addWidget(rule, self.rules + 2, 0, 1, 2)

    # ----------------------------------------------------------------------------------------------------------------
    # Function for applying the rules and moving to the Mappings page. Provides error messge to the user if they have
    # incorrectly filled in the rules.
    def next(self):

        table_before = self.table

        try:
            if self.rules > 0:
                for i in self.rule_list:
                    col_index, new_names, advanced, res_index, splitter, joiner = i.getAttributes()
                    matrix_to_csv.split_col(self.table, col_index, new_names, which_words=advanced,
                                            resolution_type=matrix_to_csv.ResolutionType(res_index),
                                            separator=splitter, joiner=joiner)
            map_window = Mappings.MapWindow(self.stack_wid, self.table, self.parent)
            map_window.parent = self.parent
            self.stack_wid.addWidget(map_window)
            self.stack_wid.setCurrentIndex(2)
        except Exception as e:
            self.table = table_before
            warning('Error', 'Failed to apply the rules!', str(e), False)
            return


# ----------------------------------------------------------------------------------------------------------------
# Class for the UI of a rule. Has drop down boxes and fields for user to fill in to provide information for the
# splitting rules they wish to create
class NewRule(QWidget):
    def __init__(self, table):
        super().__init__()
        rule_layout = QGridLayout()
        col_label = QLabel("Choose a column to split:")
        self.rule_wind = None
        self.col_to_split = QComboBox()
        self.col_to_split.addItems(table[0])

        new_col_label = QLabel("Type name of new column:")
        self.new_col = NewCol(rule_layout)
        self.new_col.rule = self

        res_lab = QLabel("Resolution:")
        self.res = QComboBox()
        self.res.addItems([name for name, _ in matrix_to_csv.ResolutionType.__members__.items()])

        split_char_lab = QLabel("Split on:")
        self.split_char = QLineEdit()
        self.split_char.setPlaceholderText("Default is a space")

        join_char_lab = QLabel("Join on:")
        self.join_char = QLineEdit()
        self.join_char.setPlaceholderText("Default is a space")

        # row, column Adding all the widgets to the layout

        rule_layout.addWidget(col_label, 0, 0, Qt.AlignTop)
        rule_layout.addWidget(self.col_to_split, 1, 0, Qt.AlignTop)
        rule_layout.addWidget(new_col_label, 0, 1, Qt.AlignTop)
        rule_layout.addWidget(self.new_col, 1, 1, Qt.AlignTop)
        rule_layout.addWidget(res_lab, 0, 2, Qt.AlignTop)
        rule_layout.addWidget(self.res, 1, 2, Qt.AlignTop)
        rule_layout.addWidget(split_char_lab, 0, 3, Qt.AlignTop)
        rule_layout.addWidget(self.split_char, 1, 3, Qt.AlignTop)
        rule_layout.addWidget(join_char_lab, 0, 4, Qt.AlignTop)
        rule_layout.addWidget(self.join_char, 1, 4, Qt.AlignTop)

        self.setLayout(rule_layout)

    # ----------------------------------------------------------------------------------------------------------------
    # Function for collecting all the user filled in information and returning it in the format needed for backend
    # function calls
    def getAttributes(self):

        # column to split
        col_index = self.col_to_split.currentIndex()

        # column names
        new_names, advanced = self.new_col.getCols()
        if '' in advanced:
            for option in advanced:
                if option != '':
                    raise Exception('Advanced parameters are required for all columns if used')
            advanced = None

        # resolution type
        res_index = self.res.currentIndex() + 1

        # split char
        split = self.split_char.text()
        if split == '':
            split = ' '

        # join char
        join = self.join_char.text()
        if join == '':
            join = ' '

        return col_index, new_names, advanced, res_index, split, join


# ----------------------------------------------------------------------------------------------------------------
# The NewCol class provides the UI for dynamically adding or deleting new columns within a rule
class NewCol(QWidget):
    def __init__(self, grid_layout):
        super().__init__()
        self.rule = None

        self.main_layout = QGridLayout()

        self.col_count = 0
        # a list of all new column layouts
        self.col_list = []
        self.new_col()

        self.setLayout(self.main_layout)
        self.grid_layout = grid_layout

    # ----------------------------------------------------------------------------------------------------------------
    # Adds widgets for user to input a new column name and buttons to delete this input or add a new column
    def new_col(self):
        self.col_count += 1
        layout = QGridLayout()

        new_col1 = QLineEdit()
        new_col1.setPlaceholderText("Column Name")

        advanced_lab = QLabel("Advanced:")
        advanced = QLineEdit()
        advanced.setPlaceholderText("Advanced settings")

        new_col_btn = QPushButton("+")
        new_col_btn.clicked.connect(self.new_col)

        del_col_btn = QPushButton("x")
        del_col_btn.clicked.connect(lambda: self.del_col(layout))

        layout.addWidget(new_col1, 0, 0, 1, 2)
        layout.addWidget(advanced_lab, 1, 0, 1, 2)
        layout.addWidget(advanced, 2, 0, 1, 2)
        layout.addWidget(new_col_btn, 3, 0, 1, 1)
        layout.addWidget(del_col_btn, 3, 1, 1, 1)

        self.main_layout.addLayout(layout, self.col_count, 0)

        # add this layout to the list
        self.col_list.append(layout)

    # ----------------------------------------------------------------------------------------------------------------
    # Deletes this current column input layout, if it is the only new column in the rule then the whole rule will be
    # deleted.
    def del_col(self, layout):

        if self.col_count == 1:
            for i in reversed(range(self.grid_layout.count())):
                self.grid_layout.itemAt(i).widget().deleteLater()
                self.rule.rule_wind.rules -= 1

        else:
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().deleteLater()
            self.col_count -= 1

    # ----------------------------------------------------------------------------------------------------------------
    # Returns list of column names and list of advanced options, one for each new column that has been created
    def getCols(self):
        column_names = []
        advanced = []
        for x in self.col_list:
            name = x.itemAtPosition(0, 0).widget().text()
            column_names.append(name)

            adv = x.itemAtPosition(2, 0).widget().text()
            advanced.append(adv)

        return column_names, advanced
