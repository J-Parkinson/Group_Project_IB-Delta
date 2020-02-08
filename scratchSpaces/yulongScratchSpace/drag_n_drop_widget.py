from PyQt5.QtWidgets import QLabel, QWidget, QPushButton


class dnd_widget(QLabel):
    file_name = ""

    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):

        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.file_name = e.mimeData().text()
        print(self.file_name)

    def get_name(self):
        return self.file_name


