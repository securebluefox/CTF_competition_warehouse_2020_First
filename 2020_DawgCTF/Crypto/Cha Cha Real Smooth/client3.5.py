# -*- coding: utf-8 -*-
"""
Created for Spring 2020 CTF
Cryptography 3
250 Points
Welcome to the RSA oracle!
Our oracle's function is RSA encryption!
The oracle is found at umbccd.io:13374, and your methods are:
    flg - returns the encrypted flag as bytes
    nnn - returns the N of the rsa function as bytes
    enc - returns the encryption of the message after the : in "enc:..."
          as a bytes representation of an int.
    dec - returns the decryption of the ciphertext int in bytes after the : in "dec:..."
          as a bytes string.
    
@author: pleoxconfusa
"""

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('crypto.ctf.umbccd.io', 13374)
sock.connect(server_address)

#available methods: flg, enc, dec, nnn.


#public knowledge, may be useful later.
#msg = 'nnn'.encode()
#sock.sendall(msg)
#ct = sock.recv(1024)

msg = 'flg'.encode()
sock.sendall(msg)
ct = sock.recv(1024)
print("flag ct: ",ct) 

#msg = b'dec:' + ct
#sock.sendall(msg)
#print(sock.recv(1024))
    
sock.close()