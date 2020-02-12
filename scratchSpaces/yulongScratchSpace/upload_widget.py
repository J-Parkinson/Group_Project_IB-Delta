from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout, QPushButton, QFileDialog, \
    QMessageBox
from PyQt5.QtCore import Qt

from scratchSpaces.yulongScratchSpace import drag_n_drop_widget


class upload_page(QWidget):
    file_loaded = 0

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Welcome text (upload page)
        top_text = QLabel("Welcome to the Butterfly Logbook Scanner\n"
                          "Upload a file below then press the Read Page\n"
                          "button to begin transcription")
        layout.addWidget(top_text)
        layout.setAlignment(top_text, Qt.AlignCenter)

        # Drag-n-drop / preview window (upload page)
        drag_n_drop = drag_n_drop_widget.dnd_widget()
        drag_n_drop.setFixedSize(650, 250)
        drag_n_drop.setStyleSheet('background-color:grey')

        d_n_p = QStackedWidget()
        d_n_p.addWidget(drag_n_drop)
        d_n_p.setCurrentIndex(0)

        layout.addWidget(d_n_p)
        layout.setAlignment(d_n_p, Qt.AlignCenter)

        # The clicking input (upload page)
        click_input = QWidget()
        click_input_layout = QHBoxLayout()

        click_input_text = QLabel("Or click the folder icon to browse a file to upload")
        click_input_layout.addWidget(click_input_text)

        click_input_button = QPushButton("Icon!")
        click_input_button.clicked.connect(self.open_file_window)
        click_input_button.setFixedSize(50, 50)
        click_input_layout.addWidget(click_input_button)

        click_input_layout.setAlignment(Qt.AlignCenter)
        click_input.setLayout(click_input_layout)
        layout.addWidget(click_input)

        # The button confirming input (upload page)
        upload_button = QPushButton("Read Page")
        upload_button.setFixedSize(200, 50)
        upload_button.clicked.connect(self.upload)
        layout.addWidget(upload_button)
        layout.setAlignment(upload_button, Qt.AlignCenter)

        # Some dummy label (upload page)
        layout.addWidget(QLabel())

        # Todo: connect input to backend
        self.setLayout(layout)

    def open_file_window(self):
        # noinspection PyCallByClass
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose a file to open", "",
                                                  "PDF (*.pdf)", "")
        if fileName:
            # Do something here! Load the file!
            self.file_loaded = 1
            print(fileName)

    def upload(self):
        print(self.file_loaded)

