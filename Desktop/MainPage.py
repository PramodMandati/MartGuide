from PyQt5.QtWidgets import QMainWindow,QWidget,QApplication,QStackedWidget,QVBoxLayout,QListView,QPushButton,QDesktopWidget,QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import requests
import sqlite3
import sys

from LoginPage import HomePage
from SignUpPage import SignUp
from FirstPage import LoginHomePage
from NetNotAvail import NetAvail
import requests
import os


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('''
            QStackedWidget{
                background-color:#EBD5BE;
                background-image:url("my3.jpg");
            }
            QScrollArea{
                background-color:transparent;
                border:2px solid black;
            }
            Frame{
                background-color:red;
            }
        ''')
        self.setMinimumHeight(700)
        self.setWindowIcon(QIcon('logo.png'))
        self.setMinimumWidth(1100)
        self.stack=QStackedWidget()
        self.setWindowTitle("YRP Tech")
        self.stack.addWidget(HomePage(self.stack))
        self.stack.addWidget(NetAvail((self.stack)))
        self.setCentralWidget(self.stack)

        my_path=os.path.join(os.getcwd(),'Additional')
        my_path2=os.path.join(my_path,'cred.txt')
        if not os.path.exists(my_path):
            os.makedirs(my_path)
        self.create_table()
        if not os.path.exists(my_path2):
            f=open(my_path2,'w')
            f.close()
        else:
            try:
                a_temp=0
                requests.get('https://www.google.com')
                f = open(my_path2, 'r')
                token = f.read()
                a_temp=1
                f.close()
                t=requests.get('http://127.0.0.1:8000/desktop')
                if token:
                    url = 'http://127.0.0.1:8000/desktop'
                    data = {'token': token, 'status': 'login'}
                    a = requests.post(url, data).text
                    a = a.split('@')
                    if a[0] == 'login':
                        data = {'token': a[2], 'status': 'logout'}
                        f = open(my_path2, 'w')
                        f.write(a[2])
                        f.close()
                        self.stack.insertWidget(2, LoginHomePage(self.stack, int(a[1]), data))
                        self.stack.setCurrentIndex(2)
            except:
                if a_temp==1:
                    QMessageBox.warning(self,'Tech Support',"Issue with the server")
                else:
                    QMessageBox.warning(self,'Internet2',"Check your internet connectivity")
                sys.exit()




    def create_table(self):
        con=sqlite3.connect(os.path.join(os.getcwd(),'Additional/My.db'))
        con.execute('PRAGMA foreign_keys=1')
        cur=con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS items(
            i_id INTEGER PRIMARY KEY AUTOINCREMENT,
            i_name VARCHAR2(20) UNIQUE,
            i_price NUMBER(100,2),
            id INTEGER
            )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS trans(
            t_id INTEGER,
            i_id INTEGER REFERENCES items(i_id) ON DELETE CASCADE ON UPDATE CASCADE,
            quantity INTERGER,
            date_buy DATE
            )''')
        con.commit()
        


app=QApplication([])
win=Window()
win.show()
sys.exit(app.exec_())
