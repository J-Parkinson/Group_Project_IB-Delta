from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout,QGridLayout

application = QApplication([])
window = QWidget()
layout = QGridLayout()
buttons = [QPushButton() for _ in range(4)]
layout.addWidget(buttons[0],0,0)
layout.addWidget(buttons[1],0,1)
layout.addWidget(buttons[2],1,0)
layout.addWidget(buttons[3],1,1)
layout.setColumnStretch(0,2)
layout.setColumnStretch(1,3)
layout.setRowStretch(0,2)
layout.setRowStretch(1,3)
window.setLayout(layout)

window.show()
application.exec_()
