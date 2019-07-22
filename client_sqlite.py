# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 09:04:44 2019

@author: Administrator
"""

import socket;

def exec_command_in_service(command,target_ip,port):
    client_end_flag='this_is_the_end_of_cilent'  #length is 25
    service_end_flag='this_is_the_end_of_service' #length is 26
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    sock.connect((target_ip, port));
    send_mes=command+client_end_flag
    sock.sendall(send_mes.encode());  
    rev_mes=''
    while True:
        szBuf = sock.recv(1024).decode(); 
        rev_mes=rev_mes+szBuf
    #    print("recv " + szBuf);
        if rev_mes[-26:]==service_end_flag:
            try:
                sock.close()
            except:
                pass
            break
    rev_data=rev_mes[:-26]
    return rev_data
    #    print("end of connect");

if __name__=='__main__':
    
    target='192.168.0.104'
    port=1994
    data=exec_command_in_service('''dfun.select_display()''',target,port)