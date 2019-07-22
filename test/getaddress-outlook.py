# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 15:27:34 2019

@author: C00075
"""

import codecs, win32com.client

# This example dumps the items in the default address book

# needed for converting Unicode->Ansi (in local system codepage)
DecodeUnicodeString = lambda x: codecs.latin_1_encode(x)[0]

def DumpDefaultAddressBook():
    # Create instance of Outlook
    o = win32com.client.Dispatch("Outlook.Application")
    mapi = o.GetNamespace("MAPI")
    folder = mapi.GetDefaultFolder(win32com.client.constants.olFolderContacts)
    print("The default address book contains",folder.Items.Count,"items")

    # see Outlook object model for more available properties on ContactItem objects
    attributes = [ 'FullName', 'Email1Address']    
    for i in range(1,folder.Items.Count+1):
        print("~~~ Entry %d ~~~" % i)
        item = folder.Items[i]
        for attribute in attributes:
            print(attribute, eval('item.%s' % attribute))
        
    o = None

DumpDefaultAddressBook()  