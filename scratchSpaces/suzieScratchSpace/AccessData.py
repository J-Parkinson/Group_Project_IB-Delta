from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, \
    QStackedWidget, QBoxLayout, QHBoxLayout, QFileDialog, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QLinearGradient, QBrush, QPalette, QFont, QPixmap


class AccessData(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def enterPress(self, text):
        print("edited" + text)

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        searchBar = QLineEdit()
        searchBar.setPlaceholderText("Search...")
        input = "sample"
        searchBar.editingFinished.connect(self.enterPress)



        go_button = QPushButton()
        go_button.setText("Go")

        viewAll = QPushButton()
        viewAll.setText("View All")


        grid.addWidget(searchBar, 1, 0)
        grid.addWidget(go_button, 1, 1)
        grid.addWidget(viewAll, 1, 2)

        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 300)

        self.show()




