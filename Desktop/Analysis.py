from PyQt5.QtWidgets import (
    QWidget,QPushButton,QLabel,QVBoxLayout,QHBoxLayout,QGridLayout,QLineEdit,QComboBox,QMessageBox,QScrollArea
)

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
import sqlite3
import os


from apyori import *
import sqlite3
from collections import defaultdict

class Analysis_Item(QWidget):
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
            QWidget#head_name{
                border-bottom:1px solid black;
            }
            QWidget{
                background-color:transparent;
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
        wid.setObjectName('head_name')
        head=QHBoxLayout()
        btn=QPushButton("Back")
        btn.clicked.connect(self.page_back)
        head.addWidget(btn)
        head.addStretch()
        wid.setLayout(head)

        body=QVBoxLayout()
        l=QLabel("<center><h2>Analysis</h2></center>")
        body.addWidget(l)
        con=QLabel("Confidence:")
        re=QRegExp(r'^([1-9][0-9|[1][0]{2})$')
        self.con_edit=QLineEdit()
        self.con_edit.setValidator(QRegExpValidator(re))
        sup=QLabel("Support:")
        self.sup_edit=QLineEdit()
        self.sup_edit.setValidator(QRegExpValidator(re))
        h=QHBoxLayout()
        self.an_btn=QPushButton("Analysis")
        self.an_btn.clicked.connect(self.start_analysis)
        h.addStretch()
        h.addWidget(self.an_btn)
        h.addStretch()
        body.addWidget(con)
        body.addWidget(self.con_edit)
        body.addWidget(sup)
        body.addWidget(self.sup_edit)
        self.lab=QLabel("<center><span style='color:red'>Please fill the details</span></center>")
        self.lab.setHidden(True)
        body.addWidget(self.lab)
        body.addLayout(h)
        body.setContentsMargins(11,20,11,11)
        
        main.addWidget(wid)
        main.addLayout(body)
        self.body=body
        main.addStretch()
        
        self.setLayout(main)
    
    def page_back(self):
        self.stack.setCurrentIndex(2)
    
    def start_analysis(self):
        try:
            self.sc.setHidden(True)
        except:
            pass
        my_path = os.path.join(os.getcwd(), 'Additional')
        my_path2 = os.path.join(my_path, 'My.db')
        con=sqlite3.connect(my_path2)
        cur=con.cursor()
        cur.execute('select i_name from items where id=?',(self.id,))
        items=cur.fetchall()
        items=tuple([i[0] for i in items])
        cur.execute('select i_name,t_id from items inner join trans on items.i_id=trans.i_id where id=?',(self.id,))
        a=cur.fetchall()
        l=defaultdict(list)
        for i in a:
            l[i[1]].append(i[0])
        l=list(l.values())
        records=[]
        for i in l:
            tmp=[]
            for j in items:
                if j in i:
                    tmp.append(j)
                else:
                    tmp.append('nan')
            records.append(tmp)
        if (self.sup_edit.text()) and (self.con_edit.text()):
            self.lab.setHidden(True)
            sup=float(self.sup_edit.text())/100
            con=float(self.con_edit.text())/100
            ruless=apriori(records,min_support=sup,min_confidence=con,min_lift=1.2,min_length=2)
            ruless=list(ruless)
            self.v=QVBoxLayout()
            for i in ruless:
                di=i._asdict()
                self.v.addWidget(QLabel(f"<h2>{','.join(di['items'])}</h2>"))
                self.v.addWidget(QLabel(f"Support: {di['support']*100}"))
                self.v.addWidget(QLabel(f""))
                tmp=di['ordered_statistics']
                for j in tmp:
                    self.v.addWidget(QLabel(f"Item Base: {','.join(list(j.items_base))}"))
                    self.v.addWidget(QLabel(f"Item Add: {','.join(list(j.items_add))}"))
                    self.v.addWidget(QLabel(f"Lift: {round(j.lift,4)}"))
                    self.v.addWidget(QLabel(f"Confidence: {round(j.confidence*100,4)}"))
                    self.v.addWidget(QLabel(f""))
            self.sc=QScrollArea()
            self.wid=QWidget()
            self.wid.setLayout(self.v)
            self.sc.setWidget(self.wid)
            self.sc.setWidgetResizable(True)
            self.body.addWidget(self.sc)
            
        else:
            self.lab.setHidden(False)
        

        
        
                
