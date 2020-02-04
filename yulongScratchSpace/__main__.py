from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout

application = QApplication([])


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.resize(800, 600)
        main_layout = QGridLayout()

        topLeft = QWidget()
        topRight = QWidget()
        bottomLeft = QWidget()
        bottomRight = QWidget()

        topRightLayout = QVBoxLayout()
        topRightLayout.addWidget(QPushButton("asdfss"))
        topRight.setLayout(topRightLayout)

        bottomRightLayout = QVBoxLayout()
        bottomRightLayout.addWidget(QPushButton("asdf"))
        bottomRight.setLayout(bottomRightLayout)

        bottomLeftLayout = QVBoxLayout()
        bottomLeftLayout.addWidget(QPushButton("button1"))
        bottomLeftLayout.addWidget(QPushButton("button2"))
        bottomLeftLayout.addWidget(QPushButton("button3"))
        bottomLeftLayout.addWidget(QPushButton("button4"))
        bottomLeft.setLayout(bottomLeftLayout)

        main_layout.addWidget(topLeft, 0, 0)
        main_layout.addWidget(topRight, 0, 1, 1, 2)
        main_layout.addWidget(bottomLeft, 1, 0, 3, 1)
        main_layout.addWidget(bottomRight, 1, 1, 3, 2)

        self.setLayout(main_layout)
        application.setStyle('Windows')

    def run(self):
        self.show()
        application.exec_()


app = Window()
app.run()
