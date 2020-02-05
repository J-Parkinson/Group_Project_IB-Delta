from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QSizePolicy

application = QApplication([])


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.resize(1080, 800)
        self.setWindowTitle("Dingy Skippers")

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
        for b in buttons:
            b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            bottomLeftLayout.addWidget(b)

        def button0_signal():
            print("button 0 pressed")
            update("Upload PDF page")

        buttons[0].setText("Upload PDF")
        buttons[0].clicked.connect(button0_signal)

        def button1_signal():
            print("button 1 pressed")
            update("Access data page")

        buttons[1].setText("Access Data")
        buttons[1].clicked.connect(button1_signal)

        def button2_signal():
            print("button 2 pressed")
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
