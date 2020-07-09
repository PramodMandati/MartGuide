from PyQt5.QtWidgets import (
    QWidget,QPushButton,QLabel,QVBoxLayout,QHBoxLayout,QApplication,QComboBox,QMessageBox
)
import sqlite3
import sys
import os

class ItemRemove(QWidget):
    def __init__(self,stack=None,id=1):
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
                outline:0px
            }
            QPushButton:pressed{
                background-color:green;
                border-style:inset;
            }
            QComboBox{
                padding:6px;
                outline:0px;
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

        self.com=QComboBox()
        self.addItemsss()
        
        
        main.addWidget(wid)
        main.addSpacing(44)
        main.addWidget(QLabel("Select Item:"))
        main.addWidget(self.com)
        h=QHBoxLayout()
        self.rmbtn=QPushButton("Remove")
        self.rmbtn.clicked.connect(self.remove_item)
        h.addStretch()
        h.addWidget(self.rmbtn)
        h.addStretch()
        main.addLayout(h)
        
        main.addStretch()
        self.setLayout(main)
    def addItemsss(self):
        my_path = os.path.join(os.getcwd(), 'Additional')
        my_path2 = os.path.join(my_path, 'My.db')
        self.con=sqlite3.connect(my_path2)
        self.con.execute("PRAGMA foreign_keys=1")
        self.cur=self.con.cursor()
        self.cur.execute("select i_name from items where id=?",(self.id,))
        a=self.cur.fetchall()
        a=[i[0] for i in a]
        self.com.addItems(a)
    def remove_item(self):
        if self.com.currentText():
            self.cur.execute("delete from items where i_name like ?",(self.com.currentText(),))
            self.con.commit()
            self.con.close()
            QMessageBox.about(self,'Remove',"Item is Successfully Removed")
            self.page_back()
        else:
            QMessageBox.warning(self,'Remove',"No items are selected")
    def page_back(self):
        self.stack.setCurrentIndex(2)

