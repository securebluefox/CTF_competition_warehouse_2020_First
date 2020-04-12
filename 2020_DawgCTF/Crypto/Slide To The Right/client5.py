# -*- coding: utf-8 -*-
"""
Created for Spring 2020 CTF
350 Points
Welcome to the AES-CTR oracle!
Our oracle's function is AES-GCM.
Our oracle has a consistent header.
The oracle is found at umbccd.io:13376, and your methods are:
    flg - returns the 16 byte nonce followed by the encrypted and authenticated flag
    enc - returns the encryption of the message after the : in "enc:..." with
          the first 16 bytes interpreted to be the nonce, which is represented
          as a 16 byte nonce followed by the authenticated ciphertext (16b tag)
    dec - returns the decryption of the authenticated ciphertext after the : in 
          "dec:<16 byte nonce>..." as a bytes string.
          
@author: pleoxconfusa
"""

import socket

BLOCK_SIZE = 16
pad = lambda s: s + ((BLOCK_SIZE - len(s) % BLOCK_SIZE) % BLOCK_SIZE) * b'\0'


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('crypto.ctf.umbccd.io', 13376)
sock.connect(server_address)

#available methods: flg, enc, dec.

msg = 'flg'.encode()
sock.sendall(msg)
ct = sock.recv(1024)
print(ct)#not decoded, because now the oracle sends encrypted bytes.

pt = "LET ME IN!!!".encode()
nonce = b"this is a nonce." #16 bytes, inconsistent for demonstration

msg = b'enc:' + nonce + pt
sock.sendall(msg)
enc = sock.recv(1024)#receive the encryption as 16 bytes of iv followed by ct.
print(enc)

print("The nonce is the same?", enc[:16] == nonce)

ct = enc[16:]

msg = b'dec:' + nonce + ct #sanity check, also other way to encode
sock.sendall(msg)
dec = sock.recv(1024)
print(dec) 
    
sock.close()