# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 13:55:43 2019

@author: C00075
"""
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,\
                             QLabel,\
                             QTableWidget,QAbstractItemView,\
                             QHeaderView,QTableWidgetItem,QHBoxLayout,
                             QVBoxLayout,QComboBox,QLineEdit,QGridLayout,\
                             QMessageBox,QDialog,QPlainTextEdit)
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator,QBrush
import sendemail as em
import sys
#from PyQt5 import QtSql
#from PyQt5.QtSql import QSqlQuery
#import deal_database_fun as dfun
#import socket
import client_sqlite as cs

class design_UI(QWidget):
    def __init__(self):
        self.service_addr='192.168.0.104'
        self.port=1994
        super().__init__()
        input_panel=inputpanel(self.service_addr,self.port)
        flag=input_panel.reply()
        if flag:  
            print('in the if')
            self.service_addr,self.port=flag
            self.UI()            
        else:
            print('in the else')
            self.close()
            print('qwidget closed')
    def UI(self):
        self.setWindowTitle("DESIGN ENGINEER PANEL")
        self.resize(1000,300)
        ##define the items##
        self.targetIP=QLineEdit(self.service_addr,self)
        self.targetIP.textChanged.connect(self.settargetIP)
        self.port_input=QLineEdit(str(self.port),self)
        self.port_input.textChanged.connect(self.settargetIP)
        self.showdatabase()  #显示数据库中内容
        self.definelabelitem()
        self.definecontent()
        self.definebutton()
        ##define the items end##
        ##define the layout##
        Hbox=QHBoxLayout(self)
        Gbox=QGridLayout(self)
        Gbox.addWidget(self.targetIP,0,1)
        Gbox.addWidget(self.port_input,0,4)
        Gbox.addWidget(self.ID,1,1,1,3)
        Gbox.addWidget(self.PN,2,1,1,3)
        Gbox.addWidget(self.ST,3,1,1,3)
        Gbox.addWidget(self.DE,4,1,1,3)
        Gbox.addWidget(self.CE,5,1,1,3)
        Gbox.addWidget(self.MT,6,1,1,3)
        Gbox.addWidget(self.cID,1,4,1,3)
        Gbox.addWidget(self.cPN,2,4,1,3)
        Gbox.addWidget(self.cST,3,4,1,3)
        Gbox.addWidget(self.cDE,4,4,1,3)
        Gbox.addWidget(self.cCE,5,4,1,3)
        Gbox.addWidget(self.cMT,6,4,1,3)
        Gbox.addWidget(self.submit,7,2,1,1)
        Gbox.addWidget(self.refresh,7,4,1,1)
        Hbox.addLayout(Gbox)
        Hbox.addWidget(self.TableWidget)
        ##define the layout end##
        self.show()
        
    def showdatabase(self):
        self.TableWidget=QTableWidget(self)
        self.TableWidget.setHorizontalHeaderLabels(['ID',\
                        'PROJECT_NAME','STATE','DESIGN_ENGINEER',\
                        'CAE_ENGINEER','MODIFY_TIME'])
        self.TableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
#        self.TableWidget.horizontalHeader().\
#            setSectionResizeMode(QHeaderView.Stretch)
        self.TableWidget.resizeColumnsToContents()
        self.TableWidget.resizeRowsToContents()
        ####
        loc=locals()
        data=self.client_socket('''dfun.select_display()''')
        print('data==  ',data)
        exec('data='+data)
        data=loc['data']
        ####
        self.TableWidget.setRowCount(len(data));
        self.TableWidget.setColumnCount(6);
        index=0
        for elem in data:
#            print(index)
            item=QTableWidgetItem(str(elem['ID']))
            self.TableWidget.setItem(index,0,item)
            item=QTableWidgetItem(elem['PROJECT_NAME'])
            self.TableWidget.setItem(index,1,item)
            item=QTableWidgetItem(elem['STATE'])
            if item.text()=='WAITING':
#                print(item.text())
                item.setBackground(QBrush(4))
            self.TableWidget.setItem(index,2,item)
            item=QTableWidgetItem(elem['DESIGN_ENGINEER'])
            self.TableWidget.setItem(index,3,item)
            item=QTableWidgetItem(elem['CAE_ENGINEER'])
            self.TableWidget.setItem(index,4,item)
            item=QTableWidgetItem(elem['MODIFY_TIME'])
            self.TableWidget.setItem(index,5,item)
            index+=1
        self.TableWidget.cellClicked.connect(self.setdisplay)
            
    def definelabelitem(self): #定义左侧显示表格列名的label
        self.ID=QLabel('ID',self)
        self.PN=QLabel('project name',self)
        self.ST=QLabel('state',self)
        self.DE=QLabel('design engineer',self)
        self.CE=QLabel('CAE engineer',self)
        self.MT=QLabel('modify time',self)
        
    def definecontent(self):
        self.cID=QLabel('NULL',self)
        ##
        self.cPN=QLineEdit('NULL',self)
        regx = QRegExp(r"^V\d\dR\d\d\d.*$")
        validator = QRegExpValidator(regx, self.cPN)
        self.cPN.setValidator(validator)
        ##
        self.cST=QComboBox(self)
        self.cST.addItems(['NULL','UNCHARTED','WAITING','PROCESSING','FINISHED'])
        self.cST.setCurrentIndex(0)
        self.cDE=QComboBox(self)
        self.cDE.addItems(['NULL','MAI','TANG','WANG','YU','TEAM'])
        self.cDE.setCurrentIndex(0)
        self.cCE=QComboBox(self)
        self.cCE.addItems(['NULL','GUAN','LIU'])
        self.cCE.setCurrentIndex(0)
        self.cMT=QLabel('NULL',self)
    
    def definebutton(self):
        self.submit=QPushButton('submit',self)
        self.refresh=QPushButton('refresh',self)
        self.email=QPushButton('Send Email',self)
        self.submit.clicked.connect(self.button_submit)
        self.refresh.clicked.connect(self.button_refresh)
        self.email.clicked.connect(self.send_email)
    
    def setdisplay(self):
        r=self.TableWidget.currentRow()
        ID=self.TableWidget.item(r,0)
        self.cID.setText(ID.text())        
        PN=self.TableWidget.item(r,1)
        self.cPN.setText(PN.text())
        ST=self.TableWidget.item(r,2)
        self.cST.setCurrentText(ST.text())
        DE=self.TableWidget.item(r,3)
        self.cDE.setCurrentText(DE.text())
        CE=self.TableWidget.item(r,4)
        self.cCE.setCurrentText(CE.text())
        MT=self.TableWidget.item(r,5)
        self.cMT.setText(MT.text())
        
    def button_refresh(self):
        rc=[(i,j) for i in range(self.TableWidget.rowCount()) \
            for j in range(self.TableWidget.columnCount())]
        for I in rc:
            i=I[0]
            j=I[1]
            self.TableWidget.setItem(i,j,QTableWidgetItem(''))
        ####
        loc=locals()
        data=self.client_socket('''dfun.select_display()''')
        exec('data='+data)
        data=loc['data']
        ####
        self.TableWidget.setRowCount(len(data));
        self.TableWidget.setColumnCount(6);
        index=0
        for elem in data:
#            print(index)
            item=QTableWidgetItem(str(elem['ID']))
            self.TableWidget.setItem(index,0,item)
            item=QTableWidgetItem(elem['PROJECT_NAME'])
            self.TableWidget.setItem(index,1,item)
            item=QTableWidgetItem(elem['STATE'])
            if item.text()=='WAITING':
#                print(item.text())
                item.setBackground(QBrush(4))
            self.TableWidget.setItem(index,2,item)
            item=QTableWidgetItem(elem['DESIGN_ENGINEER'])
            self.TableWidget.setItem(index,3,item)
            item=QTableWidgetItem(elem['CAE_ENGINEER'])
            self.TableWidget.setItem(index,4,item)
            item=QTableWidgetItem(elem['MODIFY_TIME'])
            self.TableWidget.setItem(index,5,item)
            index+=1
    
    def send_email(self):
        PN=self.cPN.text() #choosing project's name
        ST=self.cST.currentText() #choosing project's state
        DE=self.cDE.currentText() #choosing project's design engineer
#        CE=self.cCE.currentText() #choosing project's CAE engineer
        if ST=='WAITING':
            To,Copy,Subject,Body=em.gen_To_Copy_Subject_Body(DE,PN,path=None,base=None)
            dialog=EmailContentPanel(To,Copy,Subject,Body)
            dialog.exec()
        else:
            warning=QMessageBox()
            warning.setWindowTitle('Warning')
            warning.setIcon(QMessageBox.Critical)
            warning.setText("This project is not waiting, sending email is unneccesary")
            warning.setStandardButtons(QMessageBox.Close)
            warning.exec()
        
    
    def button_submit(self):
        PN=self.cPN.text() #choosing project's name
        ####
        loc=locals()
        data=self.client_socket('''dfun.select_display()''')
        exec('data='+data)
        data=loc['data']
        ####
        PN_list=[]
        for i in data:
            PN_list.append(i['PROJECT_NAME'])
        ST=self.cST.currentText() #choosing project's state
        DE=self.cDE.currentText() #choosing project's design engineer
        CE=self.cCE.currentText() #choosing project's CAE engineer
        if PN in PN_list:
            flag=self.client_socket('''dfun.alter_table('{}','STATE','{}')'''.format(PN,ST))
            if flag=='accept':
                self.client_socket('''dfun.alter_table('{}','DESIGN_ENGINEER','{}')'''.format(PN,DE))
                self.client_socket('''dfun.alter_table('{}','CAE_ENGINEER','{}')'''.format(PN,CE))
            elif flag=='reject':
                warning=QMessageBox()
                warning.setWindowTitle('Warning')
                warning.setIcon(QMessageBox.Critical)
                warning.setText("This project is already processed by other CAE engineers")
                warning.setStandardButtons(QMessageBox.Close)
                warning.exec()
        elif PN not in PN_list:
            self.client_socket('''dfun.built_continuum_line('{}','{}','{}','{}')'''.format(PN,ST,DE,CE))
        self.button_refresh()
            
    def settargetIP(self):
        self.service_addr=self.targetIP.text()
        self.port=int(self.port_input.text())
        print(self.service_addr,self.port)
        
    def client_socket(self,command):
        try:
            return cs.exec_command_in_service(command,self.service_addr,self.port)
        except:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Error')
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Connecting abort")
            msgBox.setStandardButtons(QMessageBox.Retry | QMessageBox.Close)
            msgBox.setDefaultButton(QMessageBox.Retry)
            reply=msgBox.exec()
            if reply==QMessageBox.Retry:
                self.client_socket(command)
            else:
                try:
                    self.close()
                except:
                    pass

            
class inputpanel(QDialog):
    def __init__(self,ip,port):
        super().__init__()
        self.ip=ip
        self.port=port
        self.UI()
    def UI(self):
        self.resize(500,200)
        self.lb1= QLabel("connect ip",self)
        self.lb2= QLabel("connect port",self)
        self.ip_input=QLineEdit(self.ip,self)
        self.port_input=QLineEdit(str(self.port),self)
        self.bt1 = QPushButton("OK",self)
        self.bt1.clicked.connect(self.setipport)
        self.bt2 = QPushButton("CLOSE",self)
        self.bt2.clicked.connect(self.end)
        layout=QVBoxLayout(self)
        layout.addWidget(self.lb1)
        layout.addWidget(self.ip_input)
        layout.addWidget(self.lb2)
        layout.addWidget(self.port_input)
        layout.addWidget(self.bt1)
        layout.addWidget(self.bt2)
        self.exec()
    def setipport(self):
        ip=self.ip_input.text()
        port=int(self.port_input.text())
        self.re=ip,port
        self.close()
        print('dialog closed')
        return self.re
    def end(self):
        self.re=False
        try:
            self.close()
        except:
            pass
        print('dialog closed')
        return self.re
    def reply(self):
        return self.re
    
class EmailContentPanel(QDialog):
    def __init__(self,To,Copy,Subject,Body):
        super().__init__()
        self.To=To
        self.Copy=Copy
        self.Subject=Subject
        self.Body=Body
        self.UI()
    def UI(self):
        self.Toinput=QPlainTextEdit(self.To,self)
        self.Copyinput=QPlainTextEdit(self.Copy,self)
        self.Subjectinput=QPlainTextEdit(self.Subject,self)
        self.Bodyinput=QPlainTextEdit(self.Body,self)
        self.btsend=QPushButton("send",self)
        self.btsend.clicked.connect(self.sendemail)
        self.btclose=QPushButton('cancel',self)
        self.btclose.clicked.connect(self.close)
        H=QVBoxLayout()
        H.addWidget(self.btsend)
        H.addWidget(self.btclose)
        layout=QVBoxLayout(self)
        layout.addWidget(self.Toinput)
        layout.addWidget(self.Copyinput)
        layout.addWidget(self.Subjectinput)
        layout.addWidget(self.Bodyinput)
        layout.addLayout(H)
        self.show()
    def sendemail(self):
        self.To=self.Toinput.toPlainText()
        self.Copy=self.Copyinput.toPlainText()
        self.Subject=self.Subjectinput.toPlainText()
        self.Body=self.Bodyinput.toPlainText()
        try:
            em.sendmail(self.To,self.Copy,self.Subject,self.Body)
            inform=QMessageBox()
            inform.setWindowTitle('information')
            inform.setIcon(QMessageBox.Information)
            inform.setText("Email has been successfully sent")
            inform.setStandardButtons(QMessageBox.Close)
            inform.exec()
        except:
            inform=QMessageBox()
            inform.setWindowTitle('Warning')
            inform.setIcon(QMessageBox.Critical)
            inform.setText("Sending error, please check the input")
            inform.setStandardButtons(QMessageBox.Close)
            inform.exec()
            
    
if __name__=='__main__':
    app=QApplication(sys.argv)
    ui=design_UI()
    sys.exit(app.exec_())

