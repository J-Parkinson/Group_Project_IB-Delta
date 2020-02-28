from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, \
    QStackedWidget, QBoxLayout, QHBoxLayout, QFileDialog, QCheckBox, QComboBox, QLineEdit, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QLinearGradient, QBrush, QPalette, QFont, QPixmap
import os, platform, subprocess

from utils.csv import matrix_to_csv
from .. import modifyCSV


class MapWindow(QWidget):
    def __init__(self, stack, table):
        super().__init__()
        self.setStyleSheet('color: black; background-color: rgb(248, 246, 238)')
        self.parent = None
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
        self.maps_list = []
        self.const_list = []
        # dictionary mapping standard (index) to tuple ([fields from csv(indices)], joiner)
        self.maps_dict = {}
        # dictionary mapping standard header(index) to string constant
        self.const_dict = {}
        # number of mappings
        self.total_maps = 0

        self.stack_wid = stack

        self.initUI()

    def initUI(self):
        title = QLabel("Create Mappings to Split Columns")

        help_text = QLabel("This page allows you to map existing columns from the notebook and splitting into columns "
                           "in your standard CSV format.\n\n"
                           "Each column in the standard format can be mapped to either a constant text value, or 1 or "
                           "more existing columns.\n"
                           "When joining multiple existing columns, they are joined in the order they are selected "
                           "in.\n"
                           "Unmapped columns are left blank in the output CSV.\n\n"
                           "A joiner can also be specified, which is used to join together multiple existing columns "
                           "into a single column in the standard CSV format.\n\n"
                           "Usage example:\n\n"
                           "Standard column:        From column:		Joiner:\n"
                           "Scientific Name         Genus                   (default)\n"
                           "                            From column:\n"
                           "                            Species\n\n"
                           "This will map the text from the columns ‘Genus’ and ‘Species’ in the existing table to the"
                           " ‘Scientific Name’ column in the standard format, joining them with a space.")

        self.grid.addWidget(title, 0, 0, 1, 3, Qt.AlignCenter)
        self.grid.addWidget(help_text, 1, 0, 1, 3, Qt.AlignTop)

        new_map_btn = QPushButton("Add New Mapping")
        new_map_btn.clicked.connect(self.new_map)

        new_const_btn = QPushButton("Add New Constant")
        new_const_btn.clicked.connect(self.new_const)

        cont_btn = QPushButton("Confirm all Mappings and Save")
        cont_btn.clicked.connect(self.next)
        padding = QLabel("       ")

        self.grid.addWidget(new_map_btn, 2, 0, 1, 1)
        self.grid.addWidget(new_const_btn, 2, 1, 1, 1)
        self.grid.addWidget(cont_btn, 2, 2, 1, 1)
        self.grid.addWidget(padding,3,0,1,3)

    def new_map(self):
        self.total_maps += 1
        new_map = NewMap(self.table)
        self.grid.addWidget(new_map, (self.total_maps + 3), 0, 1, 3)
        self.maps_list.append(new_map)

    def new_const(self):
        self.total_maps += 1
        const = NewConst(self.table)
        self.grid.addWidget(const, self.total_maps+3, 0, 1, 3)
        self.const_list.append(const)

    def get_attributes(self):
        # build dictionaries
        for x in self.maps_list:
            self.maps_dict[x.get_standard()] = (x.get_new_cols(), x.get_joiner())

        for y in self.const_list:
            self.const_dict[y.get_standard()] = y.get_const()

    def next(self):
        self.get_attributes()
        save_path, _ = QFileDialog.getSaveFileName(self, self.tr('Save File'), 'untitled.csv', self.tr('CSV (*.csv'))
        if save_path != '':
            matrix_to_csv.matrix_to_standard_csv(self.table, save_path, field_map=self.maps_dict,
                                                 field_consts=self.const_dict)
            saved = QLabel("Saved!")
            saved.show()
            if platform.system() == 'Darwin':
                subprocess.call(('open', save_path))
            elif platform.system() == 'Windows':
                os.startfile(save_path)
            else:
                subprocess.call(('xdg-open', save_path))

        self.parent.reset(False)



class NewMap(QWidget):
    def __init__(self, table):
        super().__init__()
        self.table = table
        layout = QGridLayout()
        stand_lab = QLabel("Choose a column from\nthe standard format:")
        layout.addWidget(stand_lab, 0, 0)
        self.stand = QComboBox()
        self.stand.addItems(['', '', '', 'UI Number', 'Other Number', 'Other number type', 'Type status', 'Label Family',
                    'Label Genus', 'Label species', 'Current Family', 'Current Genus', 'Current species', 'Subspecies',
                    'Common Name', '', 'Variety', 'Preservation', 'Number of specimens', 'Description', 'Sex',
                    'Stage/Phase', '', 'Condition Rating (Good, Fair, Poor, Unacceptable)',
                    'Condition details (eg wing fallen off)', 'Level 1 eg.Country', 'Level 2 - eg.County',
                    'Level 3 - eg.Town/City/Village', 'Level 4 (eg.Nearest named place)', 'Date (DD/MM/YYYY)',
                    'Bred or not (B if bred/ blank if caught on wing)', 'Surname', 'First name', 'Middle Names',
                    'Name', 'Verbatum label data', 'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5 +6', ''])
        layout.addWidget(self.stand, 1, 0)
        self.cols = []  # list to store all the columns to map from
        new_col_lbl = QLabel("Columns to map:")
        layout.addWidget(new_col_lbl, 0, 1)
        self.col_layout = QGridLayout()
        layout.addLayout(self.col_layout, 1, 1)
        self.add_col()
        join_lbl = QLabel("Joiner:")
        self.join = QLineEdit()
        self.join.setPlaceholderText("Optional")
        layout.addWidget(join_lbl, 0, 2)
        layout.addWidget(self.join, 1, 2)
        self.setLayout(layout)

    def add_col(self):
        fields = QComboBox()
        fields.addItems(self.table[0])
        self.col_layout.addWidget(fields)
        self.cols.append(fields)

        plus = QPushButton("+")
        plus.clicked.connect(self.add_col)
        self.col_layout.addWidget(plus)

    def get_standard(self):
        return self.stand.currentIndex()

    def get_new_cols(self):
        col_indices = []
        for x in self.cols:
            col_indices.append(x.currentIndex())
        return col_indices

    def get_joiner(self):
        return self.join.text()


class NewConst(QWidget):
    def __init__(self,table):
        super().__init__()
        self.table = table
        layout = QGridLayout()
        stand_lab = QLabel("Choose a column from\nthe standard format:")
        layout.addWidget(stand_lab, 0, 0)
        self.stand = QComboBox()
        self.stand.addItems(['', '', '', 'UI Number', 'Other Number', 'Other number type', 'Type status', 'Label Family',
                    'Label Genus', 'Label species', 'Current Family', 'Current Genus', 'Current species', 'Subspecies',
                    'Common Name', '', 'Variety', 'Preservation', 'Number of specimens', 'Description', 'Sex',
                    'Stage/Phase', '', 'Condition Rating (Good, Fair, Poor, Unacceptable)',
                    'Condition details (eg wing fallen off)', 'Level 1 eg.Country', 'Level 2 - eg.County',
                    'Level 3 - eg.Town/City/Village', 'Level 4 (eg.Nearest named place)', 'Date (DD/MM/YYYY)',
                    'Bred or not (B if bred/ blank if caught on wing)', 'Surname', 'First name', 'Middle Names',
                    'Name', 'Verbatum label data', 'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5 +6', ''])
        layout.addWidget(self.stand, 1, 0)

        const_lbl = QLabel("Constant value:")
        self.const = QLineEdit()
        self.const.setPlaceholderText("e.g. Cambridge")
        layout.addWidget(const_lbl, 0, 1)
        layout.addWidget(self.const, 1, 1)
        self.setLayout(layout)

    def get_standard(self):
        return self.stand.currentIndex()

    def get_const(self):
        return self.const.text()
