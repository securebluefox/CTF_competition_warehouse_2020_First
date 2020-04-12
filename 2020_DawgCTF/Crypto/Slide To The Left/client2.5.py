# -*- coding: utf-8 -*-
"""
Created for Spring 2020 CTF
Cryptography 2.5
200 Points
Welcome to the AES-CBC oracle!
Our oracle's function is AES-CBC.
The oracle is found at umbccd.io:13373, and your methods are:
    flg - returns the encrypted flag
    enc - returns the encryption of the message after the : in "enc:..."
          as 16 bytes of initialization vector followed by the ciphertext.
    dec - returns the decryption of the ciphertext after the : in "dec:<16 bytes iv>..."
          as a bytes string.
    
@author: pleoxconfusa
"""

import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('crypto.ctf.umbccd.io', 13373)
sock.connect(server_address)

#available methods: flg, enc, dec.

msg = 'flg'.encode()
sock.sendall(msg)
ct = sock.recv(1024)
print(ct)#not decoded, because now the oracle sends encrypted bytes.

msg = 'enc:LET ME IN!!!'.encode()
sock.sendall(msg)
enc = sock.recv(1024)#receive the encryption as 16 bytes of iv followed by ct.
print(enc)

iv = enc[:16]
ct = enc[16:]

msg = b'dec:' + iv + ct #sanity check, also other way to encode
sock.sendall(msg)
dec = sock.recv(1024)
print(dec) 
    
sock.close()