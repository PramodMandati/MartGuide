from PyQt5.QtWidgets import (
        QApplication,QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QLineEdit,QLabel,QCheckBox,QMessageBox
    )
from PyQt5.QtCore import Qt,QPoint
import requests
import sqlite3
import sys
import os

from FirstPage import LoginHomePage

class HomePage(QWidget):
    def __init__(self,stack):
        super().__init__()
        self.stack=stack
        self.setStyleSheet('''
            *{
                font-size:18px;
                padding-top:4px;
                padding-bottom:4px;
            }
            QWidget#signup{
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
        # self.setFixedSize(800,500)


        main=QVBoxLayout()
        
        signwid=QWidget()
        signwid.setObjectName('signup')
        signup=QHBoxLayout()
        btns=QPushButton("Sign Up")
        # btns.clicked.connect(self.set_page)
        btns.setObjectName('signupbtn')
        signup.addStretch()
        ll=QLabel("<h2>MartGuide</h2>")
        signup.addWidget(ll)
        signup.addStretch()
        signwid.setLayout(signup)

        login=QVBoxLayout()
        email=QLabel("Username:")
        self.emailedit=QLineEdit()
        pwd=QLabel("Password:")
        self.pwdedit=QLineEdit()
        self.pwdedit.setEchoMode(QLineEdit.Password)
        self.inc = QLabel("<center style='color:red;font-size:14px'> Invalid Username/Password < /center >")
        self.inc.setHidden(True)
        btnh=QHBoxLayout()
        btnl=QPushButton("Login")
        btnl.setShortcut("Return")
        btnl.clicked.connect(self.loginver)
        btnh.addStretch()
        btnh.addWidget(btnl)
        btnh.addStretch()
        login.setAlignment(Qt.AlignCenter)
        login.addWidget(email)
        login.addWidget(self.emailedit)
        login.addWidget(pwd)
        login.addWidget(self.pwdedit)
        h=QHBoxLayout()
        self.sho_pwd=QCheckBox("Show Password")
        self.sho_pwd.toggled.connect(self.show_pwd_met)
        h.addStretch()
        h.addWidget(self.sho_pwd)
        h.addStretch()
        login.addLayout(h)
        login.addWidget(self.inc)
        login.addLayout(btnh)
        login.setContentsMargins(11,44,11,11)
        

        main.addWidget(signwid)
        main.addLayout(login)
        main.addStretch()
        self.setLayout(main)
    def show_pwd_met(self):
        if self.sho_pwd.isChecked():
            self.pwdedit.setEchoMode(QLineEdit.Normal)
        else:
            self.pwdedit.setEchoMode(QLineEdit.Password)
    def all_clear(self):
        self.emailedit.setText('')
        self.pwdedit.setText('')
    def loginver(self):
        try:
            requests.get('https://www.google.com')
            self.inc.setText("<center style='color:red;font-size:14px'>Invalid Username/Password</center>")
            self.inc.setHidden(True)
            if self.emailedit.text() and self.pwdedit.text():
                url = 'http://127.0.0.1:8000/desktop'
                data = {'username': self.emailedit.text(), 'pwd': self.pwdedit.text(), 'status': 'login_first'}
                a = requests.post(url, data).text
                a = a.split('@')
                if a[0] == 'login':
                    my_path = os.path.join(os.getcwd(), 'Additional')
                    my_path2 = os.path.join(my_path, 'cred.txt')
                    f = open(my_path2, 'w')
                    f.write(a[2])
                    f.close()
                    self.inc.setHidden(True)
                    data = {'token':a[2], 'status': 'logout'}
                    self.stack.insertWidget(2, LoginHomePage(self.stack, int(a[1]), data))
                    self.all_clear()
                    self.stack.setCurrentIndex(2)
                elif a[0] == 'already loggedin':
                    self.inc.setText("<center style='color:red;font-size:14px'>Already Logged in, please logout in other device</center>")
                    self.inc.setHidden(False)
                elif a[0] == 'invalid username/password':
                    self.inc.setHidden(False)
                elif a[0]=='not a premium account':
                    self.inc.setText(
                        "<center style='color:red;font-size:14px'>Not a premium account</center>")
                    self.inc.setHidden(0)
            else:
                self.inc.setHidden(False)
        except:
            QMessageBox.warning(self, "Internet", "Check your internet Connectivity")


    def set_page(self):
        self.all_clear()
        self.stack.setCurrentIndex(1)
