from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, \
    QStackedWidget, QBoxLayout, QHBoxLayout, QFileDialog, QCheckBox, QComboBox, QLineEdit, QScrollArea, QStyle, \
    QMessageBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QLinearGradient, QBrush, QPalette, QFont, QPixmap

from utils.csv import matrix_to_csv
from gui.subpages import Mappings


# TODO: make page for uploading CSV pretty
# done: pg1 for adding rules
# TODO: pg2 for creating mappings

def warning(title, text, description):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)

    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setInformativeText(description)

    return msg.exec_()

class ModifyMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        main = QStackedWidget()
        main.addWidget(UploadCSV(main))  # index 0
        main.setCurrentIndex(0)
        layout.addWidget(main)
        self.setLayout(layout)


class UploadCSV(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.setStyleSheet('color: black')
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

    def open_file_window(self):
        # noinspection PyCallByClass

        file_name, _ = QFileDialog.getOpenFileName(self, "Choose a file to open", "", "CSV (*.csv)", "")
        if file_name:
            self.table = matrix_to_csv.read_csv(file_name)

    def goto_rules(self):
        if self.table is not None:
            self.stack_wid.addWidget(RulesWindow(self.stack_wid, self.table))

            self.stack_wid.setCurrentIndex(1)
        else:
            warning('Error', 'No CSV selected!', 'Please select a CSV file to import')


class RulesWindow(QWidget):

    def __init__(self, stack, table):
        super().__init__()
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

        self.rules = 1

        self.grid.setHorizontalSpacing(10)
        self.setStyleSheet('color: black; background-color: rgb(248, 246, 238)')

        self.rule_list = []

        self.stack_wid = stack

        self.initUI()

    def initUI(self):

        title = QLabel("Create Rules to Split Columns")

        help_text = QLabel("This page allows you to split any existing columns in your notebook into new columns.\n"
                           "These new columns can then be combined to build a spreadsheet in your standard format "
                           "using the mapping page.\n\n"
                           "When creating a rule, select the column to split and then add 1 or more new columns to "
                           "split into.\n\n"
                           "You can provide a ‘separator’, such as a comma and space (“, ”), however the default is "
                           "just a space.\n"
                           "You can also provide a ‘joiner’, which is used when combining multiple words into a "
                           "single new column. "
                           "The default for this is also a space.\n\n"
                           "The default expectation is that for each word in cells in the row to be split, there is a "
                           "single new column. The first word then maps to the first new column and so on.\n"
                           "In order to define a more sophisticated split, the advanced parameter can be used.\n\n"
                           "This parameter can take multiple forms:\n"
                           "- 	A single index (i.e. “0” to select the first word in each cell), with indices starting "
                           "from 0.\n"
                           "- 	A set of indices (i.e. “[0, 1, 3]” selects the 1st, 2nd and 4th words and joins them "
                           "in that order with the joiner).\n"
                           "- 	A range of indices (i.e. “1:5” selects the 2nd to 6th words and joins them with the "
                           "joiner).\n"
                           "-	A wildcard “*” which will take the words which are not assigned to any other column "
                           "for each cell.\n\n"
                           "Note that negative indices can be used to index from the end (i.e. “-2” refers to the 2nd "
                           "to last word).\n\n"
                           "When using these advanced parameters, it is important to specify the way in which index "
                           "clashes should be dealt with; this is done by selecting the resolution type. These types "
                           "are:\n"
                           "-	no_clash (default option):      any index clashes will result in an error\n"
                           "- 	just_first:                     only the first new column to use that index will have that word added\n"
                           "- 	just_last:                      only the last new column to use that index will have that word added\n"
                           "- 	all:                            clashes are ignored, so multiple new columns can refer to the same word\n\n"
                           "Usage example:\n"
                           "Split:              New Column:         Resolution:         Split on:           Join on:\n"
                           "Full Name       First Name           no_clash            (default)           (default)\n"
                           "                    Advanced:\n"
                           "                    0\n\n"
                           "                    New Column:\n"
                           "                    Middle Name(s)\n"
                           "                    Advanced:\n"
                           "                    *\n\n"
                           "                    New Column:\n"
                           "                    Last Name\n"
                           "                    Advanced:\n"
                           "                    -1\n\n"
                           "This rule will split the ‘Full Name’ column into 3 new columns, with the first word in the "
                           "‘First Name’ column, the last word in the ‘Last Name’ column and any other words in the "
                           "‘Middle Name(s)’ column\n\n")

        self.grid.addWidget(title, 0, 0, 1, 2, Qt.AlignCenter)
        self.grid.addWidget(help_text, 1, 0, 1, 2, Qt.AlignTop)

        rule1 = NewRule(self.table)
        self.rule_list.append(rule1)
        self.grid.addWidget(rule1, self.rules + 2, 0, 1, 2)

        new_rule_btn = QPushButton("Add new rule")
        new_rule_btn.clicked.connect(self.new_rule)

        cont_btn = QPushButton("Confirm all Rules and Continue ")
        cont_btn.clicked.connect(self.next)

        self.grid.addWidget(new_rule_btn, 2, 0, 1, 1)
        self.grid.addWidget(cont_btn, 2, 1, 1, 1)

    def new_rule(self):
        self.rules += 1
        print(self.rules)
        print(self.rule_list)

        rule = NewRule(self.table)
        self.rule_list.append(rule)

        self.grid.addWidget(rule, self.rules + 2, 0, 1, 2)

    def next(self):
        print("confirmed, moving to mappings page")
        table_before = self.table



        try:
            if len(self.rule_list) == 1:
                self.stack_wid.addWidget(Mappings.MapWindow(self.stack_wid, self.table))
                self.stack_wid.setCurrentIndex(2)
            else:
                for i in self.rule_list:

                    col_index, new_names, advanced, res_index, splitter, joiner = i.getAttributes()
                    matrix_to_csv.split_col(self.table, col_index, new_names, which_words=advanced,
                                                    resolution_type=matrix_to_csv.ResolutionType(res_index),
                                                    separator=splitter, joiner=joiner)
                self.stack_wid.addWidget(Mappings.MapWindow(self.stack_wid, self.table))
                self.stack_wid.setCurrentIndex(2)
        except Exception as e:
            self.table = table_before
            warning('Error', 'Failed to apply the rules!', str(e))
            return




class NewRule(QWidget):
    def __init__(self,table):
        super().__init__()
        rule_layout = QGridLayout()
        col_label = QLabel("Choose a column to split:")
        self.col_to_split = QComboBox()
        self.col_to_split.addItems(table[0])

        new_col_label = QLabel("Type name of new column:")
        self.new_col = NewCol(rule_layout)

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

    def getAttributes(self):
        print("get att")

        # column to split
        col_index = self.col_to_split.currentIndex()

        # column names
        new_names, advanced = self.new_col.getCols()
        if '' in advanced:
            for option in advanced:
                if option != '':
                    raise Exception('Advanced parameters are required for all columns if used')
            advanced = None

        # res
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


class NewCol(QWidget):
    def __init__(self, grid_layout):
        super().__init__()

        self.main_layout = QGridLayout()

        self.col_count = 0
        # a list of all new column layouts
        self.col_list = []
        self.new_col()

        self.setLayout(self.main_layout)
        self.grid_layout = grid_layout

    def new_col(self):

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
        self.col_count += 1
        # add this layout to the list
        self.col_list.append(layout)

    def del_col(self, layout):
        print("delete col")
        if len(self.col_list) == 1:
            for i in reversed(range(self.grid_layout.count())):
                self.grid_layout.itemAt(i).widget().deleteLater()

        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def getCols(self):
        column_names = []
        advanced = []
        for x in self.col_list:
            name = x.itemAtPosition(0, 0).widget().text()
            column_names.append(name)

            adv = x.itemAtPosition(2, 0).widget().text()
            advanced.append(adv)

        return column_names, advanced



