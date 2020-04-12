# -*- coding: utf-8 -*-
"""
Created for Spring 2020 CTF
300 Points
Welcome to the CBC-MAC oracle!
Our oracle's function is a CBC message authentication code function!
The oracle is found at umbccd.io:13375, and your methods are:
    tst - returns a 16 byte MAC followed by its message
    vfy - verifies the contents of the message after the : in "vfy:...",
          returning a status message of the result.

@author: pleoxconfusa
"""

import socket

BLOCK_SIZE = 16
pad = lambda s: s + ((BLOCK_SIZE - len(s) % BLOCK_SIZE) % BLOCK_SIZE) * b'\0'


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('crypto.ctf.umbccd.io', 13375)
sock.connect(server_address)

#available methods: tst, vfy.


msg = 'tst'.encode()
sock.sendall(msg)
tst = sock.recv(1024)
print(tst)#not decoded, because now the oracle sends encrypted bytes.

mac = tst[:BLOCK_SIZE]
txt = tst[BLOCK_SIZE:]

msg = 'vfy:'.encode() + mac + txt #sanity check.
sock.sendall(msg)
res = sock.recv(1024)#receive the encryption as 16 bytes of iv followed by ct.
print(res)

msg = 'vfy:'.encode() + mac + pad(txt) #sanity double check, trying to win by padding.
sock.sendall(msg)
res = sock.recv(1024)#receive the encryption as 16 bytes of iv followed by ct.
print(res)

msg = b'vfy:' + mac + b'The first 16 bytes do not authenticate this message.' #sanity triple check
sock.sendall(msg)
res = sock.recv(1024)
print(res) 
    
sock.close()