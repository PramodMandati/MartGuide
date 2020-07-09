from PyQt5.QtWidgets import QWidget,QApplication,QVBoxLayout,QLabel,QPushButton,QHBoxLayout
import requests
import sys

class NetAvail(QWidget):
    def __init__(self,stack):
        super().__init__()
        self.stack=stack
        self.setStyleSheet('''
            QPushButton{
                border:2px solid green;
                background-color:transparent;
                border-radius:10px;
                min-width:6em;
                padding:6px;
                outline:0px;
            }
            QPushButton:pressed{
                background-color:green;
                border-style:inset;
            }
        ''')
        v=QVBoxLayout()
        la=QLabel("<center><h2>Check your internet connectivity</h2></center>")
        h=QHBoxLayout()
        self.btn=QPushButton('Retry')
        # self.btn.clicked.connect(self.net_connect)
        h.addStretch()
        h.addWidget(self.btn)
        h.addStretch()
        v.setContentsMargins(0,220,0,0)

        v.addWidget(la)
        v.addLayout(h)
        v.addStretch()
        self.setLayout(v)

    def net_connect(self):
        try:
            requests.get('https://www.google.com')
            self.stack.setCurrentIndex(0)
        except:
            pass



#
# app=QApplication([])
# win=NetAvail()
# win.show()
# sys.exit(app.exec_())