# -*- coding: utf-8 -*-
"""
Created for Spring 2020 CTF
Cryptography 0
10 Points
Welcome to my sanity check.  You'll find this to be fairly easy.  
The oracle is found at umbccd.io:13370, and your methods are:
    flg - returns the flag
    tst - returns the message after the : in "tst:..."
    
@author: pleoxconfusa
"""

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('crypto.ctf.umbccd.io', 13370)
sock.connect(server_address)

#available methods: flg, tst.


msg = 'tst:hello'


sock.sendall(msg.encode())
data = sock.recv(1024)
print(data.decode())
    
sock.close()