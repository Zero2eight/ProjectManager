# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 08:53:43 2019

@author: Administrator
"""

import socket
import deal_database_fun as dfun

def service_command_exec():
    client_end_flag='this_is_the_end_of_cilent'  #length is 25
    service_end_flag='this_is_the_end_of_service' #length is 26
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    print("create socket succ!");
    localhost=socket.gethostname()        
    sock.bind((localhost, 1994));
    print("bind socket succ!");        
    sock.listen(5);
    print("listen succ!");
    while True:
            rev_mes=''
            conn, addr = sock.accept();
            print("get client");
            print(addr);
            conn.settimeout(2);
            while True:
                szBuf = conn.recv(1024).decode();
                rev_mes=rev_mes+szBuf
                if rev_mes[-25:]==client_end_flag:
                    command=rev_mes[:-25]
                    break
            loc=locals()
            exec('runres={}'.format(command))
            runres=loc['runres']
            send_res=str(runres)+service_end_flag
            conn.sendall(send_res.encode())
            try:
                conn.close()
            except:
                pass
            
if __name__=='__main__':
    service_command_exec()
            
            
   
            
        
