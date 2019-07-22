# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 13:58:59 2019

@author: C00075
"""

import sqlite3
conn = sqlite3.connect('test2.db')
c = conn.cursor()
#c.execute('''CREATE TABLE COMPANY
#       (ID INT PRIMARY KEY     NOT NULL,
#       NAME           TEXT    NOT NULL,
#       AGE            INT     NOT NULL,
#       ADDRESS        CHAR(50),
#       SALARY         REAL);''')
#print("Table created successfully");
s=c.execute('''select datetime('now','localtime')''')
conn.commit()
conn.close()