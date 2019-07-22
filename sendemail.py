# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:23:40 2019

@author: C00075
"""

import win32com.client as win32
import warnings
#import sys
import pythoncom

#reload(sys)
#sys.setdefaultencoding('utf8')
warnings.filterwarnings('ignore')
pythoncom.CoInitialize()

#Design Engineers
YU='Yulinmeng@frdch.com'
WANG='wangsongjun@frdch.com'
MAI='maibinghui@frdch.com'
TANG='tanggaoxiao@frdch.com'

#CAE Engineers
LIU='liuwanghao@frdch.com'
GUAN='Guanchuanfeng@frdch.com'

HOU='houyue@frdch.com'


def sendmail(To,Copy,Subject,Body):     #All the arguments are string.
    sub = Subject #邮件主题
    body = Body #邮件内容
    outlook = win32.Dispatch('outlook.application')
    receivers = To #邮件收件人
    copy=Copy #邮件抄送至
    mail = outlook.CreateItem(0)
    mail.To = receivers
    mail.Cc = copy
    mail.Subject = sub
    mail.Body = body
#    mail.Attachments.Add(r"C:\Users\c00075\.spyder-py3\sqlite\新建 Microsoft Word 文档.docx")
    mail.Send()

def gen_To_Copy_Subject_Body(person,project_name,path=None,base=None):
    Subject='{}解析依赖'.format(project_name)
    Body='''各位工作辛苦了！
针对GAC_A55_FR SUB_{0}解析依赖
文件路径：{1}
对应版本号为：{0}(基于{2})
主要变更内容见链接中ppt
此版本责任设计工程师是{3}
以上提供的依赖信息如果有不足或者任务传递方式上有任何意见请提出，麻烦各位了,谢谢!
    '''.format(project_name,path,base,person)
    if person=='MAI':
        To='{};{}'.format(LIU,GUAN)
        Copy='{};{};{}'.format(YU,WANG,TANG)
    elif person=='TANG':
        To='{};{}'.format(LIU,GUAN)
        Copy='{};{};{}'.format(YU,WANG,MAI)
    elif person=='YU':
        To='{};{}'.format(LIU,GUAN)
        Copy='{};{};{}'.format(MAI,WANG,TANG)
    elif person=='WANG':
        To='{};{}'.format(LIU,GUAN)
        Copy='{};{};{}'.format(YU,MAI,TANG)
    else:
        person=='TEAM'
        To='{};{}'.format(LIU,GUAN)
        Copy='{};{};{}'.format(YU,MAI,TANG,MAI)
    return To,Copy,Subject,Body
    
#sendmail()
#sendmail()
#a=gen_To_Copy_Subject_Body('YU','V03R074')

