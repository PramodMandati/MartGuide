from PyQt5.QtWidgets import QWidget,QPushButton,QLabel,QVBoxLayout,QHBoxLayout,QGridLayout,QLineEdit,QComboBox,QMessageBox

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
import sqlite3

class ItemAdd(QWidget):
    def __init__(self,stack,id):
        super().__init__()
        self.stack=stack
        self.id=id
        self.setStyleSheet('''
            *{
                font-size:18px;
                padding-top:4px;
                padding-bottom:4px;
            }
            QWidget{
                border-bottom:1px solid black;
            }
            QLineEdit{
                background-color:transparent;
                border:2px solid green;
                border-radius:10px;
                padding:6px;
                color:white;
            }
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
        main=QVBoxLayout()

        wid=QWidget()
        head=QHBoxLayout()
        btn=QPushButton("Back")
        btn.clicked.connect(self.page_back)
        head.addWidget(btn)
        head.addStretch()
        wid.setLayout(head)

        body=QGridLayout()
        iname=QLabel("Item Name:")
        self.iname_edit=QLineEdit()
        price=QLabel("Price:")
        self.price_edit=QLineEdit()
        reg=QRegExp('[0-9]+\.[0-9]{2}')
        self.price_edit.setValidator(QRegExpValidator(reg))
        htmp=QHBoxLayout()
        btn=QPushButton("Add")
        btn.clicked.connect(self.adding_item)
        htmp.addStretch()
        htmp.addWidget(btn)
        htmp.addStretch()
        body.addWidget(iname,0,0)
        body.addWidget(self.iname_edit,0,1)
        body.addWidget(price,1,0)
        body.addWidget(self.price_edit,1,1)
        body.addLayout(htmp,2,0,1,2)
        body.setContentsMargins(11,44,11,11)



        main.addWidget(wid)
        main.addLayout(body)
        main.addStretch()
        self.setLayout(main)
    
    def page_back(self):
        self.stack.setCurrentIndex(2)
    def clear_al(self):
        self.iname_edit.setText("")
        self.price_edit.setText("")
    def adding_item(self):
        try:
            if self.iname_edit.text() and float(self.price_edit.text()):
                import os
                my_path = os.path.join(os.getcwd(), 'Additional')
                my_path2 = os.path.join(my_path, 'My.db')
                con=sqlite3.connect(my_path2)
                con.execute('PRAGMA foreign_keys=1')
                cur = con.cursor()
                try:
                    cur.execute('''INSERT INTO items(i_name,i_price,id) values(
                        ?,?,?)''', (
                        self.iname_edit.text().title(),
                        float(self.price_edit.text()),
                        self.id
                    ))
                    con.commit()
                    QMessageBox.about(self, "Add", "Item is added")
                    self.clear_al()
                except sqlite3.IntegrityError as e:
                    QMessageBox.warning(self, 'Error', 'Item is already existed')
            else:
                QMessageBox.warning(self, 'Items', "Enter all details")
        except:
            QMessageBox.warning(self, 'Items', "Enter all details")
