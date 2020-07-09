from PyQt5.QtWidgets import (
    QMainWindow,QApplication,QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QLineEdit,QLabel,QGridLayout,QMessageBox
)
from PyQt5.QtCore import Qt,QPoint,QRegExp
from PyQt5.QtGui import QRegExpValidator
import sqlite3
import sys
import re

class SignUp(QWidget):
    def __init__(self,stack):
        super().__init__()
        self.stack=stack
        self.setStyleSheet('''
            *{
                font-size:18px;
                padding-top:4px;
                padding-bottom:4px;
            }
            QWidget#topSign{
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
        wid.setObjectName("topSign")
        h=QHBoxLayout()
        btn=QPushButton("Back")
        btn.clicked.connect(self.page_back)
        h.addWidget(btn)
        h.addStretch()
        wid.setLayout(h)

        signup=QGridLayout()
        fname=QLabel("First Name:")
        lname=QLabel("Last Name:")
        self.fname_edit=QLineEdit()
        self.lname_edit=QLineEdit()
        email=QLabel("Email:")
        self.email_edit=QLineEdit()
        self.email_inv=QLabel("<span style='color:red;font-size:12px'>invalid email or email already exists</span>")
        self.email_inv.setHidden(True)
        phone=QLabel("Phone:")
        self.phone_edit=QLineEdit()
        no_vali=QRegExp(r'[0-9]{10}')
        self.phone_edit.setValidator(QRegExpValidator(no_vali))
        self.phone_inv=QLabel("<span style='color:red;font-size:12px'>invalid phone number or phone number already exists</span>")
        self.phone_inv.setHidden(True)
        pwd=QLabel("Password:")
        self.pwd_edit=QLineEdit()
        self.pwd_inv=QLabel("<span style='color:red;font-size:12px'>Password not strong</span>")
        self.pwd_inv.setHidden(True)
        shop=QLabel("Shop Type:")
        self.shoptype_edit=QLineEdit()
        self.inv=QLabel("<center style='color:red;font-size:12px'>Enter All details</center>")
        self.inv.setHidden(True)

        h2=QHBoxLayout()
        self.regi=QPushButton("Register")
        h2.addStretch()
        h2.addWidget(self.regi)
        self.regi.clicked.connect(self.registration)
        h2.addStretch()

        signup.addWidget(fname,0,0)
        signup.addWidget(lname,0,1)
        signup.addWidget(self.fname_edit,1,0)
        signup.addWidget(self.lname_edit,1,1)
        signup.addWidget(email,2,0,1,2)
        signup.addWidget(self.email_edit,3,0,1,2)
        signup.addWidget(self.email_inv,4,0,1,2)
        signup.addWidget(phone,5,0,1,2)
        signup.addWidget(self.phone_edit,6,0,1,2)
        signup.addWidget(self.phone_inv,7,0,1,2)
        signup.addWidget(pwd,8,0,1,2)
        signup.addWidget(self.pwd_edit,9,0,1,2)
        signup.addWidget(self.pwd_inv,10,0,1,2)
        signup.addWidget(shop,11,0,1,2)
        signup.addWidget(self.shoptype_edit,12,0,1,2)
        signup.addWidget(self.inv,13,0,1,2)
        signup.addLayout(h2,14,0,1,2)
        
        
        
        signup.setContentsMargins(11,44,11,11)

        

        main.addWidget(wid)
        main.addLayout(signup)
        main.addStretch()
        self.setLayout(main)
    
    def page_back(self):
        li=(self.fname_edit,self.lname_edit,self.email_edit,self.phone_edit,self.pwd_edit,self.shoptype_edit)
        for i in li:
            i.setText('')
        self.all_true()
        self.stack.setCurrentIndex(0)
    def all_true(self):
        self.inv.setHidden(True)
        self.pwd_inv.setHidden(True)
        self.email_inv.setHidden(True)
        self.phone_inv.setHidden(True)
    def registration(self):
        self.all_true()
        con=sqlite3.connect('C:/Program Files/MartGuide/Addition/My.db')
        con.execute('PRAGMA foreign_keys=1')
        cur=con.cursor()
        if self.len_ver() + self.email_ver(cur) + self.phone_ver(cur) + self.pwd_ver() == 4:
            try:
                cur.execute('''INSERT INTO users(first_name,last_name,email,phone,password,shop_type) values(
                    ?,?,?,?,?,?)''',(
                        self.fname_edit.text(),
                        self.lname_edit.text(),
                        self.email_edit.text(),
                        self.phone_edit.text(),
                        self.pwd_edit.text(),
                        self.shoptype_edit.text()
                    ))
                con.commit()
                QMessageBox.about(self,'Success','User successfully registered')
                self.page_back()
            except Exception as e:
                pass
            
           
    def len_ver(self):
        li=(self.fname_edit,self.lname_edit,self.email_edit,self.phone_edit,self.pwd_edit,self.shoptype_edit)
        for i in li:
            if not len(i.text())>0:
                self.inv.setHidden(False) 
                return False
        return True   
            
            
    def email_ver(self,cur):
        cur.execute("select *from users where email like ?",(self.email_edit.text(),))
        if not len(cur.fetchall())==0:
            self.email_inv.setHidden(False)
            return False
        if not re.match(r'[a-z A-Z][a-z A-Z 0-9 _ .]+@(gmail|GMAIL|email|EMAIL).(com|COM)$',self.email_edit.text()):
                self.email_inv.setHidden(False)
                return False
        return True
    def phone_ver(self,cur):
        cur.execute("select *from users where phone=?",(self.phone_edit.text(),))
        if not len(cur.fetchall())==0:
            self.phone_inv.setHidden(False)
            return False
        if not len(self.phone_edit.text())==10:
            self.phone_inv.setHidden(False)
            return False
        return True
    def pwd_ver(self):
        if not len(self.pwd_edit.text())>=8:
            self.pwd_inv.setHidden(False)
            return False
        return True
                
# app=QApplication([])
# win=SignUp(None)
# win.show()
# sys.exit(app.exec_())
