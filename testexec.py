# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 08:48:55 2019

@author: C00075
"""
#import sys
#sys.path.append(r'C:\Users\c00075\.spyder-py3\sqlite')
import deal_database_fun as dfun
import time
t1=time.time()
#loc=locals()
c=dfun.select_display()
t2=time.time()
dt1=t2-t1
print('dt1= ',dt1)


t3=time.time()
loc=locals()
exec('c=dfun.select_display()')
c=loc['c']
t4=time.time()
dt2=t4-t3
print('dt2= ',dt2)