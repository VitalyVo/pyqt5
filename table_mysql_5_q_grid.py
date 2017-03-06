#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import pymysql
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTableWidget,QTableWidgetItem,
    QTextEdit, QGridLayout, QApplication, QPushButton, QHBoxLayout)



class Tabl(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.tableWidget = QTableWidget()
        #result = QLabel('Result')
        #table_label=QLabel('Tables')
        databases_n = QLineEdit()
        databases_n.setPlaceholderText('A name of databases')
        self.table_n = QLineEdit()
        self.table_n.setPlaceholderText('Enter or copy/paste name of table')
        self.result_text = QTextEdit()
        self.result_text.setPlaceholderText('*** R E S U L T   A R E A ***')
        self.tableWidget = QTableWidget()
        self.Cleartab()
        #self.tableWidget.setPlaceholderText('sdfgsdfsdfgsdf')

        button01=QPushButton('Show databases')
        button01.clicked.connect(self.Select_databases)
        self.sqlparameters=QLineEdit()
        self.sqlparameters.setPlaceholderText('Enter host (localhost or sqldatabase.com)')
        self.sqlparameters2=QLineEdit()
        self.sqlparameters2.setPlaceholderText('Enter username (User)')
        self.sqlparameters3=QLineEdit()
        self.sqlparameters3.setEchoMode(QLineEdit.Password)
        self.sqlparameters3.setPlaceholderText('Enter the password(maybe blank)')

        button1= QPushButton('Select databases')
        button1.clicked.connect(self.Select_databases)
        button11=QPushButton('Use database')
        button11.clicked.connect(self.UseDatabase)
        self.use_database=QLineEdit()
        self.use_database.setPlaceholderText('Enter or copy/paste a database name')

        button2= QPushButton('Select table')
        button2.clicked.connect(self.Select_Table)

        button_clear=QPushButton('Clear Result Area')
        button_clear.clicked.connect(self.Clearfun)

        button_clear_tab=QPushButton('Clear Tables Area')
        button_clear_tab.clicked.connect(self.Cleartab)

        button_exit=QPushButton('Exit')
        button_exit.clicked.connect(self.Exit)
###########################
        vhbox = QHBoxLayout()
        vhbox.addWidget(self.sqlparameters)
        vhbox.addWidget(self.sqlparameters2)
        vhbox.addWidget(self.sqlparameters3)

        grid = QGridLayout()
        grid.setSpacing(10)


        grid.addWidget(button01, 1, 0)
        grid.addLayout(vhbox, 1, 1)

        #grid.addWidget(button1, 2, 0)
        #grid.addWidget(databases_n, 2, 1)

        grid.addWidget(button11, 2, 0)
        grid.addWidget(self.use_database, 2, 1)

        grid.addWidget(button2, 3, 0)
        grid.addWidget(self.table_n, 3, 1)

        #grid.addWidget(button_clear, 5,0)
        #grid.addWidget(button_clear_tab, 5,1)


        #grid.addWidget(result, 6, 0)
        grid.addWidget(button_clear, 4,0)
        grid.addWidget(self.result_text, 4, 1)

        #grid.addWidget(table_label, 7, 0)
        grid.addWidget(button_clear_tab, 5,0)
        grid.addWidget(self.tableWidget, 5, 1)

        grid.addWidget(button_exit, 6, 0)


        self.setLayout(grid)

        self.setGeometry(300, 300, 700, 700)
        self.setWindowTitle('--= MySQL Tables =--')
        self.show()


    def Select_databases(self):
        #self.db=pymysql.connect("ensembldb.ensembl.org","anonymous","")
        #self.db=pymysql.connect("localhost","root","123")
        if self.sqlparameters.text()=='' and self.sqlparameters2.text()=='' and self.sqlparameters3.text()=='':
            sqlp='localhost'
            sqlp2='root'
            sqlp3='123'
        else:
            sqlp=self.sqlparameters.text()
            sqlp2=self.sqlparameters2.text()
            sqlp3=self.sqlparameters3.text()
        #print(sqlp+sqlp2+sqlp3)
        #self.db=pymysql.connect(*(("{0},{1},{2}".format(sqlp, sqlp2, sqlp3)).split(',')))
        self.db=pymysql.connect(('{0}'.format(sqlp)), ('{0}'.format(sqlp2)),('{0}'.format(sqlp3)))
        self.cursor=self.db.cursor()
        # Select Name of tables
        self.cursor.execute('show databases')
        self.b1=[]
        for row in self.cursor:
            self.a1=[]
            for i in row:
                self.a1.append(str(i))
                self.b1.append(' '.join(self.a1))
        self.text_= '\n'.join(self.b1)
        #print(self.text_)
        self.result_text.append('\n ***Databases*** \n \n'+self.text_)
        ### Close the Base!
        #self.db.close()

    def UseDatabase(self):
        if self.use_database.text()=='':
            return
        database_use=self.use_database.text()
        #self.db=pymysql.connect("localhost","root","123","forum")
        self.cursor=self.db.cursor()
        self.cursor.execute('use {}'.format(database_use))
        self.cursor.execute('show tables')
        self.b1=[]
        for row in self.cursor:
            self.a1=[]
            for i in row:
                self.a1.append(str(i))
                self.b1.append(' '.join(self.a1))
        self.text_= '\n'.join(self.b1)
        print(self.text_)
        self.result_text.append('\n ***Tables*** \n \n'+self.text_)


    def Select_Table(self):
        if self.table_n.text()=='':
            return
        self.table_sel=self.table_n.text()
        print ("**"+ self.table_sel)

        #self.db=pymysql.connect("localhost","root","123","forum")
        self.cursor=self.db.cursor()
        self.cursor.execute ("select * from {0}".format(self.table_sel))
        #del self.aa
        self.aa=[]
        try:
            for row in self.cursor:
                print(row)
                self.aa.append(str(row))
                print (self.aa)

            for i in range(len(self.aa)):
                self.tableWidget.setRowCount(len(self.aa))
                self.tableWidget.setColumnCount(1)
                self.tableWidget.resizeColumnsToContents()
                self.tableWidget.setItem(i,0, QTableWidgetItem(self.aa[i]))
        finally:
            return


    def Clearfun(self):
        self.result_text.clear()

    def Cleartab(self):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(2)

    def Exit(self):
        if self.cursor!=None or self.db!=None:
            time.sleep=3
            self.db.close()
            self.cursor.close()

        sys.exit(0)
        #pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Tabl()
    sys.exit(app.exec_())
