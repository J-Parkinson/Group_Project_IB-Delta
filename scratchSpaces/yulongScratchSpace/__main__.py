from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QLinearGradient, QBrush, QPalette, QFont, QPixmap

application = QApplication([])


class Window(QWidget):



    def __init__(self):
        QWidget.__init__(self)
        self.resize(1080, 800)
        self.setWindowTitle("Dingy Skippers")
        self.setAutoFillBackground(True)

        background = QColor.fromRgb(248,246,238)

        title_font = QFont("Georgia", 25)

        p = self.palette()
        p.setColor(self.backgroundRole(), background)
        self.setPalette(p)

        h = self.height()
        w = self.width()

        topLeft = QWidget(self)
        topRight = QWidget(self)
        bottomLeft = QWidget(self)
        bottomRight = QWidget(self)

        # The top left corner
        '''
        trying to add an image but it's not showing up - not sure why 
        '''
        bFlyImage = QLabel(topLeft)
        bFlyImage.setGeometry(10,10,60,60)
        bFlyImage.setPixmap(QPixmap("../suzieScratchSpace/caterpillar.png"))

        #bFlyImage.move(50, 50)
        #topLeft.resize(w * 0.25, h * 0.1)

        # The top right corner
        l = QLabel(topRight)
        l.setText("Butterfly Logbook Scanner")
        l.setFont(title_font)
        l.setStyleSheet('color:#6D214F')
        l.move(w * 0.25, 50)

        topRight.resize(w * 0.75, h * 0.1)
        topRight.move(w * 0.25, 0)

        # The bottom right corner
        br_label = QLabel("Initial Page", bottomRight)
        br_label.setStyleSheet('color:#6D214F')
        br_label.move(100, 100)
        br_label.resize(500, 500)
        bottomRight.resize(w * 0.75, h * 0.9)
        bottomRight.move(w * 0.25, h * 0.1)

        def update(message):
            br_label.setText(message)

        # The bottom left corner
        bottomLeftLayout = QVBoxLayout()
        buttons = [QPushButton() for _ in range(6)]

        # function for changing all buttons back to default when a new one is clicked
        def reset_buttons_color():
            for b in buttons:
                b.setStyleSheet('background-color:rgb(248,154,121); color:black')

        for b in buttons:
            b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            bottomLeftLayout.addWidget(b)

        reset_buttons_color()

        def button0_signal():
            print("button 0 pressed")
            reset_buttons_color()
            buttons[0].setStyleSheet("background-color: rgb(248,246,238); color:#6D214F")
            update("Upload PDF page")

        buttons[0].setText("Upload PDF")
        buttons[0].clicked.connect(button0_signal)

        def button1_signal():
            print("button 1 pressed")
            reset_buttons_color()
            buttons[1].setStyleSheet("background-color: rgb(248,246,238); color:#6D214F")
            update("Access data page")

        buttons[1].setText("Access Data")
        buttons[1].clicked.connect(button1_signal)

        def button2_signal():
            print("button 2 pressed")
            reset_buttons_color()
            buttons[2].setStyleSheet("background-color: rgb(248,246,238); color:#6D214F")
            update("Tutorial page")

        buttons[2].setText("How to Use?")
        buttons[2].clicked.connect(button2_signal)

        bottomLeft.setLayout(bottomLeftLayout)
        bottomLeft.move(0, h * 0.1)
        bottomLeft.resize(w * 0.25, h * 0.9)
        bottomLeft.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        application.setStyle('Windows')

    def run(self):
        self.show()
        application.exec_()


if __name__ == "__main__":
    app = Window()
    app.run()
