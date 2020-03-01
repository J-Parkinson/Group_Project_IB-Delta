import pathlib

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from random import randint
from textwrap import fill


class initial_page(QWidget):

    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout()
        self.parent = parent

        #################################################
        # Welcome text (start page)
        #################################################
        top_text = QLabel("Welcome to the Butterfly Logbook Scanner!")
        top_text.setStyleSheet('color: black; font: bold 20px')
        layout.addWidget(top_text, alignment=Qt.AlignCenter)

        #################################################
        # Instructions text (start page)
        #################################################

        inst_text = QLabel("Please choose either to upload a PDF or convert a CSV to a standardised format, or\n"
                           "view our help guides for more information on how to use our app.")
        inst_text.setStyleSheet('color: black')
        layout.addWidget(inst_text, alignment=Qt.AlignCenter)

        #################################################
        # Butterfly/insect fact (start page)
        #################################################
        with open(pathlib.Path(__file__).parent / 'resources' / 'butterflyfacts.txt', "r") as facts:
            factlist = facts.read().split("\n")
            fact_text = QLabel(fill("Butterfly fact: " + factlist[randint(0, len(factlist) - 1)], 85))
        fact_text.setStyleSheet('color: black')
        layout.addWidget(fact_text, alignment=Qt.AlignCenter)

        #################################################
        # Acknowledgement text (start page)
        #################################################
        ackn_text = QLabel(
            "Made by Group Delta as part of the University of Cambridge Part IB Group Project,\n"
            "on behalf of the Zoology Museum, Cambridge.\n"
            "Coded by Francesca Iovu, Abigail Wilkinson, Jack Parkinson, Yulong Huang, \n"
            "Suzie Welby, and James Alner")
        ackn_text.setStyleSheet('color: grey')
        layout.addWidget(ackn_text, alignment=Qt.AlignCenter)

        #################################################
        # Some dummy label (upload page)
        #################################################
        #layout.addWidget(QLabel())

        self.setLayout(layout)