#################################################
# Modules import
#################################################

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, \
    QStackedWidget, QBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QLinearGradient, QBrush, QPalette, QFont, QPixmap

application = QApplication([])


class Window(QWidget):

    def __init__(self):
        #################################################
        # Initialization
        #################################################

        # Layout
        QWidget.__init__(self)
        self.resize(1080, 800)
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Dingy Skippers")

        main_layout = QGridLayout()

        # Style
        self.setAutoFillBackground(True)
        background = QColor.fromRgb(248, 246, 238)
        title_font = QFont("Georgia", 25)

        p = self.palette()
        p.setColor(self.backgroundRole(), background)
        self.setPalette(p)

        # Components
        top_left = QWidget()
        top_right = QWidget()
        bottom_left = QWidget()
        bottom_right = QStackedWidget()

        #################################################
        # The top left corner:
        # Should be some butterfly icons
        #################################################

        # That's just a mess right now lol
        title = QLabel(top_left)
        title.setText("Put some butterfly here")
        main_layout.addWidget(top_left, 0, 0)
        '''
        trying to add an image but it's not showing up - not sure why 
        '''
        bFlyImage = QLabel(top_left)
        bFlyImage.setGeometry(10, 10, 60, 60)
        bFlyImage.setPixmap(QPixmap("../suzieScratchSpace/caterpillar.png"))

        #################################################
        # The top right corner:
        # Just a label
        #################################################
        title = QLabel()
        title.setText("Butterfly Logbook Scanner")
        title.setFont(title_font)
        title.setStyleSheet('color:#6D214F')

        top_right_layout = QVBoxLayout()
        top_right_layout.addWidget(title)
        top_right_layout.setAlignment(title,Qt.AlignCenter)

        top_right.setLayout(top_right_layout)
        main_layout.addWidget(top_right, 0, 1)

        #################################################
        # The bottom right corner:
        # A stack of useful pages
        #################################################

        # Initial page
        ini_label = QLabel("Initial Page")
        ini_label.setStyleSheet('color:#6D214F')
        ini_label.move(100, 100)
        ini_label.resize(500, 500)

        # Upload page: a bunch of things
        upload_page = QWidget()
        upload_page_layout = QVBoxLayout()

        # Welcome text (upload page)
        upload_top_text = QLabel("Welcome to the Butterfly Logbook Scanner\n"
                                 "Upload a file below then press the Read Page\n"
                                 "button to begin transcription")
        upload_page_layout.addWidget(upload_top_text)
        upload_page_layout.setAlignment(upload_top_text, Qt.AlignCenter)

        # Drag-n-drop / preview window (upload page)
        d_n_p = QStackedWidget()
        drag_n_drop = QWidget()


        upload_page_layout.addWidget(d_n_p)
        upload_page_layout.setAlignment(d_n_p, Qt.AlignCenter)

        # The clicking input (upload page)
        click_input = QWidget()
        click_input_layout = QHBoxLayout()

        click_input_text = QLabel("Or click the folder icon to browse a file to upload")
        click_input_layout.addWidget(click_input_text)

        click_input_button = QPushButton("Icon!")
        click_input_button.clicked.connect(self.open_file_window)
        click_input_button.setFixedSize(50,50)
        click_input_layout.addWidget(click_input_button)

        click_input_layout.setAlignment(Qt.AlignCenter)
        click_input.setLayout(click_input_layout)
        upload_page_layout.addWidget(click_input)

        # The button confirming input (upload page)
        upload_button = QPushButton("Read Page")
        upload_button.setFixedSize(200, 50)
        upload_page_layout.addWidget(upload_button)
        upload_page_layout.setAlignment(upload_button, Qt.AlignCenter)

        # Some dummy label (upload page)
        upload_page_layout.addWidget(QLabel())

        upload_page.setLayout(upload_page_layout)

        # Data page, working atm
        data_page = QWidget()
        QPushButton("data", data_page)

        # Tutorial page, working atm
        tutorial_page = QWidget()
        QPushButton("tutorial", tutorial_page)

        # Finally, add all those pages to the stack
        bottom_right.addWidget(upload_page)
        bottom_right.addWidget(data_page)
        bottom_right.addWidget(tutorial_page)
        bottom_right.addWidget(ini_label)

        main_layout.addWidget(bottom_right, 1, 1)

        #################################################
        # The bottom left corner:
        # A bunch of functional buttons
        #################################################

        # Initialize buttons
        bottom_leftLayout = QVBoxLayout()
        buttons = [QPushButton() for _ in range(3)]
        for b in buttons:
            b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            bottom_leftLayout.addWidget(b)

        # function for changing all buttons back to default when a new one is clicked
        def reset_buttons_color():
            for b in buttons:
                b.setStyleSheet('background-color:rgb(248,154,121); color:black')

        reset_buttons_color()

        # Upload page -- button 0
        def button0_signal():
            print("button 0 pressed")
            reset_buttons_color()
            buttons[0].setStyleSheet("background-color: rgb(248,246,238); color:#6D214F")
            bottom_right.setCurrentIndex(0)
            # update("Upload PDF page")

        buttons[0].setText("Upload PDF")
        buttons[0].clicked.connect(button0_signal)

        # Data page -- button 1
        def button1_signal():
            print("button 1 pressed")
            bottom_right.setCurrentIndex(1)
            reset_buttons_color()
            buttons[1].setStyleSheet("background-color: rgb(248,246,238); color:#6D214F")
            bottom_right.setCurrentIndex(1)
            # update("Access data page")

        buttons[1].setText("Access Data")
        buttons[1].clicked.connect(button1_signal)

        # Tutorial page -- button 2
        def button2_signal():
            print("button 2 pressed")
            bottom_right.setCurrentIndex(2)
            reset_buttons_color()
            buttons[2].setStyleSheet("background-color: rgb(248,246,238); color:#6D214F")
            bottom_right.setCurrentIndex(2)
            # update("Tutorial page")

        buttons[2].setText("How to Use?")
        buttons[2].clicked.connect(button2_signal)

        # Dummies to make it looks good
        for _ in range(3):
            dummy = QLabel()
            dummy.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            bottom_leftLayout.addWidget(dummy)

        bottom_right.setCurrentIndex(3)
        bottom_left.setLayout(bottom_leftLayout)
        main_layout.addWidget(bottom_left, 1, 0)

        #################################################
        # Things about the main layout
        #################################################
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 3)
        main_layout.setRowStretch(0, 1)
        main_layout.setRowStretch(1, 9)
        self.setLayout(main_layout)
        application.setStyle('Windows')

    def open_file_window(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose a file to open", "",
                                                  "PDF (*.pdf)","")
        if fileName:
            # Do something here! Load the file!
            print(fileName)

    def run(self):
        self.show()
        application.exec_()


if __name__ == "__main__":
    app = Window()
    app.run()
