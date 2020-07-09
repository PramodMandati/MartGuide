from PyQt5.QtWidgets import QWidget,QPushButton,QLabel,QVBoxLayout,QHBoxLayout

class ItemEdit(QWidget):
    def __init__(self,stack,id):
        super().__init__()
        self.stack=stack
        self.id=id
        self.setStyleSheet('''
            *{
                font-size:14px;
            }
            QWidget{
                border-bottom:1px solid black;
            }
        ''')
        main=QVBoxLayout()

        wid=QWidget()
        head=QHBoxLayout()
        btn=QPushButton("Back")
        btn.clicked.connect(self.page_back)
        head.addWidget(btn)
        head.addStretch()
        wid.setLayout(head)

        main.addWidget(wid)
        main.addWidget(QLabel("Edit"))
        main.addStretch()
        self.setLayout(main)
    
    def page_back(self):
        self.stack.setCurrentIndex(2)