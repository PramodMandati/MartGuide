from PyQt5.QtWidgets import (
    QWidget,QApplication,QVBoxLayout,QPushButton,QHBoxLayout,QLabel,QScrollArea,QGridLayout,QMessageBox
)
from PyQt5.QtCore import Qt
import requests
import sqlite3
import sys
import os

from AddItem import ItemAdd
from EditItem import ItemEdit
from RemoveItem import ItemRemove
from Analysis import Analysis_Item

class LoginHomePage(QWidget):
    main=None
    def __init__(self,stack,id,data):
        super().__init__()
        self.stack=stack
        self.data=data
        self.id=id
        self.setWindowTitle("Adding")
        self.setStyleSheet('''
            *{
                font-size:18px;
                padding-top:4px;
                padding-bottom:4px;
            }
            QWidget#list_obj{
                background-color:transparent;
            }
            QWidget#head_name{
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
        ''')
        main=QVBoxLayout()
        wid=QWidget()
        wid.setObjectName("head_name")
        head=QHBoxLayout()
        btn=QPushButton("Logout",self)
        btn.setObjectName('btn_nor')
        btn.clicked.connect(self.logout_opt)
        btn2=QPushButton("Add Item")
        btn2.setObjectName("btn_nor")
        btn2.clicked.connect(self.add_item)
        btn3=QPushButton("Analysis")
        btn3.setObjectName('btn_nor')
        btn3.clicked.connect(self.analysis_items)
        # btn3=QPushButton("Edit Item")
        # btn3.clicked.connect(self.edit_item)
        btn4=QPushButton("Remove Item")
        btn4.setObjectName('btn_nor')
        btn4.clicked.connect(self.remove_item)
        head.addStretch()
        head.addWidget(btn2)
        head.addWidget(btn3)
        head.addWidget(btn4)
        head.addWidget(btn)
        wid.setLayout(head)
        
        
        main.addWidget(wid)
        main.addSpacing(44)
        self.main=main
        self.after_login()

        htm2=QVBoxLayout()

        ch=QHBoxLayout()
        cbtn=QPushButton("Calculate Total")
        cbtn.setObjectName('btn_nor')
        cbtn.clicked.connect(self.cal_total)
        ch.addStretch()
        ch.addWidget(cbtn)
        ch.addStretch()
        ch2=QHBoxLayout()
        self.ltot=QLabel("Total Amount:0")
        ch2.addStretch()
        ch2.addWidget(self.ltot)
        ch2.addStretch()
        ch3=QHBoxLayout()
        fbtn=QPushButton("Fresh Transaction")
        fbtn.setObjectName('btn_nor')
        fbtn.clicked.connect(self.fresh_count)
        ch3.addStretch()
        ch3.addWidget(fbtn)
        ch3.addStretch()
        htm2.addLayout(ch)
        htm2.addLayout(ch2)
        htm2.addLayout(ch3)
        
        main.addLayout(htm2)
        # main.addStretch()
        self.setLayout(main)
        


    def add_all(self):
        self.stack.insertWidget(3,ItemAdd(self.stack,self.id))
        self.stack.insertWidget(4,Analysis_Item(self.stack,self.id))
        # self.stack.insertWidget(4,ItemEdit(self.stack,self.id))
        self.stack.insertWidget(5,ItemRemove(self.stack,self.id))
    def add_item(self):
        self.add_all()
        self.stack.setCurrentIndex(3)
    # def edit_item(self):
    #     self.add_all()
    #     self.stack.setCurrentIndex(4)
    def remove_item(self):
        self.add_all()
        self.stack.setCurrentIndex(5)
    def analysis_items(self):
        self.add_all()
        self.stack.setCurrentIndex(4)
    def after_login(self):
        try:
            my_path = os.path.join(os.getcwd(), 'Additional')
            my_path2 = os.path.join(my_path, 'My.db')
            con=sqlite3.connect(my_path2)
            con.execute('PRAGMA foreign_keys=1')
            cur=con.cursor()
            
            v=QVBoxLayout()
            v.addWidget(QLabel("<h2>Items:</h2>"))
            cur.execute('select i_name from items where id=?',(self.id,))
            a=cur.fetchall()
            
        
            h2=QVBoxLayout()
        
            self.valuee=[]
            self.total_length=len(a)
            for j in range(len(a)):
                self.minus=QPushButton("-")
                self.minus.setObjectName("minus_btn")
                self.minus.setFixedWidth(20)
                self.minus.num=j

                self.plus=QPushButton('+')
                self.plus.setObjectName("plus_btn")
                self.plus.setFixedWidth(20)
                self.plus.num=j

                l=QLabel("0")
                l.setStyleSheet('''
                    border-top:2px solid red;
                    border-bottom:2px solid red;
                    min-width:2em;
                ''')
                l.setAlignment(Qt.AlignCenter)
                l.setFixedWidth(30)
                self.valuee.append(l)

                i=QHBoxLayout()
                i.setContentsMargins(0,11,0,11)
                i.setSpacing(0)
                l=QLabel('<h4>'+a[j][0]+':  </h4>')
                l.setFixedWidth(80)
                l.setAlignment(Qt.AlignRight)
                i.addStretch()
                i.addWidget(l)
                i.addWidget(self.minus)
                i.addWidget(self.valuee[j])
                i.addWidget(self.plus)
                i.addStretch()

                h2.addLayout(i)
                self.minus.clicked.connect(self.dec)
                self.plus.clicked.connect(self.inc)

            wid=QWidget()
            wid.setObjectName("list_obj")
            wid.setStyleSheet('''
                QPushButton#minus_btn{
                    border-radius:0px;
                    border:2px solid red;
                    border-bottom-left-radius:10px;
                    border-top-left-radius:10px;
                    outline:0px;
                    min-width:1em;
                    padding-top:6px;
                    padding-bottom:6px;
                }
                QPushButton#plus_btn{
                    border-radius:0px;
                    border:2px solid red;
                    border-bottom-right-radius:10px;
                    border-top-right-radius:10px;
                    outline:0px;
                    min-width:1em;
                    padding-top:6px;
                    padding-bottom:6px;
                }
                QPushButton#plus_btn:pressed{
                    background-color:green;
                    border-style:inset;
                }
                QPushButton#minus_btn:pressed{
                    background-color:green;
                    border-style:inset;
                }
            ''')
            wid.setLayout(h2)
            sa=QScrollArea()
            sa.setWidget(wid)
            v.addWidget(sa)
            v.setContentsMargins(0,0,0,0)
        
            sa.setWidgetResizable(True)
            self.main.addLayout(v)
        except Exception as e:
            pass
        
    def inc(self):
        send=self.sender()
        self.valuee[send.num].setText(str(int(self.valuee[send.num].text())+1))
    def dec(self):
        send=self.sender()
        if int(self.valuee[send.num].text())>0:
            self.valuee[send.num].setText(str(int(self.valuee[send.num].text())-1))
    
    def fresh_count(self):
        try:
            for i in range(self.total_length):
                self.valuee[i].setText('0')
            self.ltot.setText('Total Amount:0')
        except Exception as e:
            pass
    
    def cal_total(self):
        my_path = os.path.join(os.getcwd(), 'Additional')
        my_path2 = os.path.join(my_path, 'My.db')
        con=sqlite3.connect(my_path2)
        con.execute('PRAGMA foreign_keys=1')
        cur=con.cursor()
        cur.execute('select t_id from trans ORDER by t_id DESC LIMIT 1')
        tid=cur.fetchall()
        if not tid:
            tid=1
        else:
            tid=tid[0][0]
            tid+=1
        cur.execute('select i_name,i_price,i_id from items where id=?',(self.id,))
        a=cur.fetchall()
        total=0
        import time
        for i in range(len(a)):
            if float(self.valuee[i].text()):
                try:
                    cur.execute('''INSERT INTO trans(t_id,i_id,quantity,date_buy) values(
                    ?,?,?,?)''',(
                        tid,
                        a[i][2],
                        int(self.valuee[i].text()),
                        time.strftime(r'%Y-%m-%d')
                    ))
                    con.commit()
                except Exception as e:
                    pass
                total+=(a[i][1]*float(self.valuee[i].text()))
        self.ltot.setText('Total Amount:'+str(total))

    def logout_opt(self):
        try:
            requests.get('https://www.google.com')
            url = 'http://127.0.0.1:8000/desktop'
            a=requests.post(url,self.data).text
            if a=='logout':
                my_path = os.path.join(os.getcwd(), 'Additional')
                my_path2 = os.path.join(my_path, 'cred.txt')
                f=open(my_path2,'w')
                f.close()
                self.stack.setCurrentIndex(0)
        except:
            QMessageBox.warning(self,"Internet","Check your internet connectivity")