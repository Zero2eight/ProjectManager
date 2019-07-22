# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 11:14:58 2019

@author: C00075
"""

import sqlite3
import time
#from PyQt5.QtWidgets import QFileDialog,QApplication
import os
import re
############
#class openfile(QFileDialog):
#    def openfile(self):
#        fname = QFileDialog.getOpenFileName(self, '打开文件','./')
#        if fname!='':
#            print('database is selected')
#            return fname
#    
#app=QApplication(sys.argv)
#file=openfile()
#db_name=file.openfile()
#db_name=db_name[0]
#print(db_name)
#file.close()
##############
#sys.exit(app.exec_())

db_name='V03.db'

def alter_db_name(dbname):
    global db_name
    db_name=dbname

def search_db():
    cw=os.getcwd()
#    print(cw)
    files=os.listdir(cw)
#    print(files)
    dbfiles=[]
    for i in files:
#        print(i)
        temp=i.split('.')
#        print(temp)
        if temp[-1]=='db':
            dbfiles.append(i)
    return dbfiles

def create_database():
    db_name=input('input the dataname--name.suffix.  ')
    db=sqlite3.connect(db_name)
    dbc=db.cursor()
    print('successfully connect the database')
    try:
        dbc.execute('''CREATE TABLE PROJECT
           (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
           'PROJECT_NAME' TEXT    NOT NULL UNIQUE,
           'STATE' TEXT DEFAULT 'UNCHARTED',
           'DESIGN_ENGINEER'  TEXT,
           'CAE_ENGINEER'   TEXT,
           'MODIFY_TIME'   TEXT);''')
        db.commit()
        print('Successfully created database')
    except:
        print('database already existed')
    db.close()

#simple function
###############################################################################
def built_line(PROJECT_NAME,STATE,DESIGN_EG,CAE_EG):
    db=sqlite3.connect(db_name)
    local=time.localtime()
    MODIFY_TIME=time.strftime('%Y-%m-%d %H:%M:%S',local)
    dbc=db.cursor()
    dbc.execute('''INSERT INTO PROJECT 
                ('PROJECT_NAME','STATE','DESIGN_ENGINEER','CAE_ENGINEER','MODIFY_TIME')
                VALUES (?,?,?,?,?);''',(PROJECT_NAME,STATE,DESIGN_EG,CAE_EG,MODIFY_TIME))
    db.commit()    
    db.close()
    print('successfully added the entry')
    
def select_display():
    db=sqlite3.connect(db_name)
    dbc=db.cursor()
    back=dbc.execute('select * from PROJECT order by PROJECT_NAME ASC;')
    data_list=[]
    for i in back:
        content={}
#        print('ID = ',i[0])
        content['ID']=i[0]
#        print('PROJECT_NAME = ',i[1])
        content['PROJECT_NAME']=i[1]
#        print('STATE = ',i[2])
        content['STATE']=i[2]
#        print('DESIGN_ENGINEER = ',i[3])
        content['DESIGN_ENGINEER']=i[3]
#        print('CAE_ENGINEER = ',i[4])
        content['CAE_ENGINEER']=i[4]
#        print('MODIFY_TIME = ',i[5])
        content['MODIFY_TIME']=i[5]
        data_list.append(content)
    db.close()
    return data_list

def drop_table():
    db=sqlite3.connect(db_name)
    dbc=db.cursor()
    dbc.execute('drop table PROJECT;')
    db.commit()
    db.close()
    
def select_max_id_display():    
    return select_display()[-1]
    
def search(COLUMN,VALUE):
    #此函数旨在查找COLUMN列是否存在VALUE值
    data=select_display()
    flag=False
    for e in data:
        if str(e[COLUMN])==str(VALUE):
            flag=True
            break            
    return flag
    
    
def built_continuum_line(PROJECT_NAME,STATE,DESIGN_EG,CAE_EG):
    try:
        latest_project=select_max_id_display()['PROJECT_NAME'][:7]
    except:
        latest_project=PROJECT_NAME[:3]+'R'+'000' #如果数据库里面是空的
    print(latest_project)        
    if PROJECT_NAME[:3]==latest_project[:3]: #如果前3位匹配，例如V03R001与V03R002
        if re.match(r'^{}R\d\d\d$'.format(latest_project[:3]),PROJECT_NAME): #如果输入的项目名称是类似V03R019这种格式
            delta=int(PROJECT_NAME[-3:])-int(latest_project[-3:]) #计算要创建的项目和当前最后项目名之间的间隔
            if delta==1:
                built_line(PROJECT_NAME,STATE,DESIGN_EG,CAE_EG) 
            elif delta<=0:
                print('Wrong project name')
            else:
                for add in range(delta):
                    if add==delta-1:
                        add+=1
                        built_line(PROJECT_NAME,STATE,DESIGN_EG,CAE_EG)
                    else:
                        add+=1
                        fix=str(int(latest_project[-3:])+add)
                        name=PROJECT_NAME[:3]+'R'+fix.zfill(3)
                        built_line(name,'UNCHARTED','NULL','NULL')
                        print('name is ',name)
        elif re.match(r'^{}R\d\d\d-\d*$'.format(latest_project[:3]),PROJECT_NAME): #如果项目名是V03R020-3这种格式
            formalname=PROJECT_NAME.split('-')[0]
            if search('PROJECT_NAME',formalname): #如果-号前的版本号在数据库中有记录才创建这个版本号
                built_line(PROJECT_NAME,STATE,DESIGN_EG,CAE_EG)

            
def lookup(PROJECT_NAME,COLUMN):
    #此函数旨在查找PROJECT_NAME中COLUMN列所对应的值
    db=sqlite3.connect(db_name)
    dbc=db.cursor()
    data=dbc.execute('''select {} from PROJECT where PROJECT_NAME glob '{}' '''.format(COLUMN,PROJECT_NAME))
#    print(data)
    for i in data:
        col=i[0]
    db.close()
    return col

            
def alter_table(PROJECT_NAME,COLUMN,NEW_VALUE):
    value=lookup(PROJECT_NAME,COLUMN)
    if COLUMN=='STATE' and value=='PROCESSING' and NEW_VALUE=='PROCESSING':
        return 'reject'
    else:
        db=sqlite3.connect(db_name)
        dbc=db.cursor()
        local=time.localtime()
        MODIFY_TIME=time.strftime('%Y-%m-%d %H:%M:%S',local)
        COMMAND1='''UPDATE PROJECT 
                       SET %s = '%s',MODIFY_TIME= '%s'
                       WHERE PROJECT_NAME = '%s';''' % (COLUMN,NEW_VALUE,MODIFY_TIME,PROJECT_NAME)
    #    dbc.execute('''UPDATA PROJECT 
    #                   SET '?' = '?'
    #                   WHERE 'PROJECT NAME' = '?';''',(COLUMN,NEW_VALUE,PROJECT_NAME))
    #    print(COMMAND1)  
        dbc.execute(COMMAND1)
        db.commit()     
        db.close()  
        return 'accept'
###############################################################################


#complex function
###############################################################################
#for design engineer
def create_project(PROJECT_NAME,DESIGN_ENGINEER):
    built_continuum_line(PROJECT_NAME,'WAITING',DESIGN_ENGINEER,'')

#for CAE engineer
def modify_state(PROJECT_NAME,NEW_STATE,CAE_ENGINEER):
    alter_table(PROJECT_NAME,'STATE',NEW_STATE)
    alter_table(PROJECT_NAME,'CAE_ENGINEER',CAE_ENGINEER)
    
    
    
    
#def testfun():
##    built_line('V03R001','WAITING','TANG','GUAN')
##    built_line('V03R002','WAITING','TANG','GUAN')
##    built_line('V03R003','WAITING','TANG','GUAN')
##    built_line('V03R004','WAITING','TANG','GUAN')
##    built_line('V03R005','WAITING','TANG','GUAN')
#    built_continuum_line('V03R045','WAITING','YU','LIU')
#    alter_table('V03R004','STATE','PROCESSING')
#alter_table('V03R035','STATE','PROCESSING')
    
    
    
    
    
    
    
    