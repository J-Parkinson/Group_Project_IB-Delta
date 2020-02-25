from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, \
    QStackedWidget, QBoxLayout, QHBoxLayout, QFileDialog, QCheckBox, QComboBox, QLineEdit, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QLinearGradient, QBrush, QPalette, QFont, QPixmap
from ..jamesScratchSpace import matrix_to_csv


class MapWindow(QWidget):
    def __init__(self, stack, table):
        super().__init__()
        self.setStyleSheet('color: black; background-color: rgb(248, 246, 238)')

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
        self.maps_dict = {}
        self.const_dict = {}
        # number of mappings
        self.maps = 0
        self.const = 0

        self.stack_wid = stack

        self.initUI()

    def initUI(self):
        title = QLabel("Create Mappings to Split Columns")

        help_text = QLabel("** help text and information ** \n * \n * \n *")

        self.grid.addWidget(title, 0, 0, 1, 3, Qt.AlignCenter)
        self.grid.addWidget(help_text, 1, 0, 1, 3, Qt.AlignTop)

        #map1 = NewMap()

        new_map_btn = QPushButton("Add New Mapping")
        new_map_btn.clicked.connect(self.new_map)

        new_const_btn = QPushButton("Add New Constant")
        new_const_btn.clicked.connect(self.new_const_map)

        cont_btn = QPushButton("Confirm all Mappings and Continue")
        cont_btn.clicked.connect(self.next)

        self.grid.addWidget(new_map_btn, 2, 0, 1, 1)
        self.grid.addWidget(new_const_btn,2,1,1,1)
        self.grid.addWidget(cont_btn, 2, 2, 1, 1)

    def new_map(self):
        self.maps += 1
        map = NewMap(self.table)
        #todo: this

    def new_const_map(self):
        self.maps += 1
        #todo: this

    def next(self):
        #todo: move to save page
        return 0



class NewMap(QWidget):
    def __init__(self,table):
        super().__init__()
        #todo something else
        return 1



