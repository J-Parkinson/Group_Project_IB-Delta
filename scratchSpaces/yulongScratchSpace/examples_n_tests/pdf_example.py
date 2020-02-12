import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
import QtPoppler
from pictureflow import *

app = QApplication(sys.argv)

w = PictureFlow()
d = QtPoppler.Poppler.Document.load('file.pdf')
d.setRenderHint(QtPoppler.Poppler.Document.Antialiasing and QtPoppler.Poppler.Document.TextAntialiasing)

page = 0
pages = d.numPages() - 1
while page < pages:
    page += 1
    print(page)
    w.addSlide(d.page(page).renderToImage())
w.show()

sys.exit(app.exec_())
