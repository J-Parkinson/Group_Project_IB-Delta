from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, \
    QStackedWidget, QBoxLayout, QHBoxLayout, QFileDialog, QCheckBox, QComboBox, QLineEdit, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QLinearGradient, QBrush, QPalette, QFont, QPixmap


# TODO: create page for uploading CSV
# TODO: pg1 for adding rules
# TODO: pg2 for creating mappings


class RulesWindow(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        self.scroll = QScrollArea(self)
        main_layout.addWidget(self.scroll)
        self.scroll.setWidgetResizable(True)
        self.scroll_area_content = QWidget(self.scroll)
        self.grid = QGridLayout(self.scroll_area_content)
        self.scroll_area_content.setLayout(self.grid)

        self.scroll.setWidget(self.scroll_area_content)

        #where to start the rules within the grid
        self.col_index_y = 3

        self.rules = 1

        self.grid.setHorizontalSpacing(10)
        self.setStyleSheet('color: black; background-color: rgb(248, 246, 238)')



        self.initUI()

    def initUI(self):

        title = QLabel("Create Rules to Split Columns")

        help_text = QLabel("** help text and information ** \n * \n * \n *")

        self.grid.addWidget(title, 0, 0, 1, 2, Qt.AlignCenter)
        self.grid.addWidget(help_text, 1, 0, 1, 2, Qt.AlignTop)

        rule1 = NewRule()
        self.grid.addWidget(rule1, self.rules + 2, 0, 1, 2)

        new_rule_btn = QPushButton("Add new rule")
        new_rule_btn.clicked.connect(self.new_rule)

        cont_btn = QPushButton("Confirm all buttons and Continue ")
        cont_btn.clicked.connect(self.next)

        self.grid.addWidget(new_rule_btn, 2, 0, 1, 1)
        self.grid.addWidget(cont_btn, 2, 1, 1, 1)

    def new_rule(self):
        self.rules += 1

        rule = NewRule()

        self.grid.addWidget(rule, self.rules+2, 0, 1, 2)

    def next(self):
        print("confirmed, moving to mappings page")


class NewCol(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QGridLayout()

        self.col_count = 0
        self.new_col()

        self.setLayout(self.main_layout)

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
        del_col_btn.clicked.connect(self.del_col)

        layout.addWidget(new_col1, 0, 0, 1, 2)
        layout.addWidget(advanced_lab, 1, 0, 1, 2)
        layout.addWidget(advanced, 2, 0, 1, 2)
        layout.addWidget(new_col_btn, 3, 0, 1, 1)
        layout.addWidget(del_col_btn, 3, 1, 1, 1)

        self.main_layout.addLayout(layout, self.col_count, 0)
        self.col_count += 1

    def del_col(self):
        #do something
        print ("delete col")



class NewRule(QWidget):
    def __init__(self):
        super().__init__()
        rule_layout = QGridLayout()
        col_label = QLabel("Choose a column to split:")
        col_to_split = QComboBox()
        col_to_split.addItems(["field 1", "field 2", "field 3", "etc"])

        new_col_label = QLabel("Type name of new column:")
        new_col = NewCol()

        res_lab = QLabel("Resolution:")
        res = QComboBox()
        res.addItems(["enum1", "enum2", "enum3", "etc"])

        split_char_lab = QLabel("Split on:")
        split_char = QLineEdit()
        split_char.setPlaceholderText("Default is a space")

        join_char_lab = QLabel("Join on:")
        join_char = QLineEdit()
        join_char.setPlaceholderText("Default is a space")

        # row, column Adding all the widgets to the layout

        rule_layout.addWidget(col_label, 0, 0, Qt.AlignTop)
        rule_layout.addWidget(col_to_split, 1, 0, Qt.AlignTop)
        rule_layout.addWidget(new_col_label, 0, 1, Qt.AlignTop)
        rule_layout.addWidget(new_col, 1, 1, Qt.AlignTop)
        rule_layout.addWidget(res_lab, 0, 2, Qt.AlignTop)
        rule_layout.addWidget(res, 1, 2, Qt.AlignTop)
        rule_layout.addWidget(split_char_lab, 0, 3, Qt.AlignTop)
        rule_layout.addWidget(split_char, 1, 3, Qt.AlignTop)
        rule_layout.addWidget(join_char_lab, 0, 4, Qt.AlignTop)
        rule_layout.addWidget(join_char, 1, 4, Qt.AlignTop)

        self.setLayout(rule_layout)

