from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QLinearGradient, QBrush, QPalette

application = QApplication([])


class Window(QWidget):



    def __init__(self):
        QWidget.__init__(self)
        self.resize(1080, 800)
        self.setWindowTitle("Dingy Skippers")
        self.setAutoFillBackground(True)
        ''' trying to make a gradient background and failing
        
         linGrad = QLinearGradient(QPointF(100, 100), QPointF(200, 200));
        linearGrad.setColorAt(0, Qt.black);
        linearGrad.setColorAt(1, Qt.white);
         QRadialGradient gradient(50, 50, 50, 50, 50);
        gradient.setColorAt(0, QColor.fromRgbF(0, 1, 0, 1));
        gradient.setColorAt(1, QColor.fromRgbF(0, 0, 0, 0));

        QBrush brush(gradient);

        QBrush
        
        '''

        background = QColor.fromRgb(100, 149, 237)
        default_button = QColor.fromRgb(252,230,201)

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
        l = QLabel(topLeft)
        l.setText("Put some butterfly here")
        l.move(50, 50)
        topLeft.resize(w * 0.25, h * 0.1)

        # The top right corner
        l = QLabel(topRight)
        l.setText("Butterfly Logbook Scanner")
        l.move(w * 0.25, 50)

        topRight.resize(w * 0.75, h * 0.1)
        topRight.move(w * 0.25, 0)

        # The bottom right corner
        br_label = QLabel("Initial Page", bottomRight)
        br_label.move(100, 100)
        br_label.resize(500, 500)
        bottomRight.resize(w * 0.75, h * 0.9)
        bottomRight.move(w * 0.25, h * 0.1)

        def update(message):
            br_label.setText(message)

        # The bottom left corner
        bottomLeftLayout = QVBoxLayout()
        buttons = [QPushButton() for _ in range(6)]

        def reset_buttons_color():
            for b in buttons:
                b.setStyleSheet('background-color:rgb(252,230,201); color:black')

        for b in buttons:
            b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            bottomLeftLayout.addWidget(b)

        reset_buttons_color()

        def button0_signal():
            print("button 0 pressed")
            reset_buttons_color()
            buttons[0].setStyleSheet("background-color: rgb(100, 149, 237)")
            update("Upload PDF page")

        buttons[0].setText("Upload PDF")
        buttons[0].clicked.connect(button0_signal)

        def button1_signal():
            print("button 1 pressed")
            reset_buttons_color()
            buttons[1].setStyleSheet("background-color: rgb(100, 149, 237)")
            update("Access data page")

        buttons[1].setText("Access Data")
        buttons[1].clicked.connect(button1_signal)

        def button2_signal():
            print("button 2 pressed")
            reset_buttons_color()
            buttons[2].setStyleSheet("background-color: rgb(100, 149, 237)")
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
