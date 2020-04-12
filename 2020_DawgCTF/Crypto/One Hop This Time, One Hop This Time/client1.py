# -*- coding: utf-8 -*-
"""
Created for Spring 2020 CTF
Cryptography 1 
40 Points
Welcome to the one time pad oracle! 
Our oracle's function is enc := key ^ msg | dec := key ^ ct
The oracle is found at umbccd.io:13371, and your methods are:
    flg - returns the encrypted flag
    enc - returns the encryption of the message after the : in "enc:..."
    dec - returns the decryption of the ciphertext after the : in "dec:..."
    
@author: pleoxconfusa
"""

import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('crypto.ctf.umbccd.io', 13371)
sock.connect(server_address)

#available methods: flg, enc, dec.


msg = 'flg'.encode()
sock.sendall(msg)
flg = sock.recv(1024)
print(flg) #not decoded, because now the oracle sends encrypted bytes.

msg = 'enc:LET ME IN!!!'.encode()
sock.sendall(msg)
enc = sock.recv(1024) 

msg = b'dec:' + enc
sock.sendall(msg)
dec = sock.recv(1024)
print(dec) #sanity check

    
sock.close()