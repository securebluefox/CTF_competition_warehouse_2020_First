import sys
import socket
import time
from Crypto.Cipher import AES
from Crypto import Random
import base64
import binascii
import threading

def pad(plaintext):
    length = 16 - (len(plaintext) % 16)
    return plaintext + bytes([length]) * length

def check_pad(padded_plaintext):
    padding_number = padded_plaintext[-1]
    if padding_number == 0:
        return None
    for i in range(0, padding_number):
        if padded_plaintext[-i - 1] != padding_number:
            return None
    return padded_plaintext[:-padding_number]

def recvall(c):
    plaintext = b''
    max_size = 1024
    while len(plaintext) < max_size:
        b = c.recv(1)
        if b == b'\n':
            return plaintext
        plaintext += b
    return None

def encrypt_plaintext(key, plaintext):
    iv = Random.new().read(16)
    aes = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = pad(plaintext)
    return base64.b64encode(iv + aes.encrypt(padded_plaintext))

def decrypt(key, c):
    b64_ciphertext = recvall(c)
    if not b64_ciphertext:
        c.send(b'Ciphertext too large\n')
        return
    elif len(b64_ciphertext) % 4 != 0:
        c.send(b'Ciphertext not encoded correctly\n')
        return
    try:
        ciphertext = base64.b64decode(b64_ciphertext)
    except binascii.Error:
        c.send(b'Ciphertext not encoding correctly\n')
        return
    if len(ciphertext) <= 16:
        c.send(b'Ciphertext too small\n')
        return
    elif len(ciphertext) % 16 != 0:
        c.send(b'Ciphertext not encoding correctly\n')
        return

    iv = ciphertext[:16]
    aes = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = aes.decrypt(ciphertext[16:])

    plaintext = check_pad(padded_plaintext)
    if plaintext != None:
        c.send(b'You are not allowed to decrypt!\n')
    else:
        c.send(b'Error in padding\n')

def create_ciphertext(key, flag):
    ciphertext = encrypt_plaintext(key, flag)
    f = open('ciphertext', 'wb')
    f.write(ciphertext)
    f.close()
    return ciphertext

def single_connection(c, key):
    try:
        c.send(b'what would you like to decrypt\n')
        decrypt(key, c)
        c.close()
    except ConnectionResetError:
        return


address = sys.argv[1]
port = int(sys.argv[2])
s = socket.socket()
key_file = sys.argv[3]
flag = bytes(sys.argv[4], 'utf-8')
f = open(key_file, 'rb')
key = f.read()
f.close()
create_ciphertext(key, flag)

s.bind((address, port))
s.listen()
while True:
    c, addr = s.accept()
    single_connection(c, key)
    #threading.Thread(target=single_connection, args=(c, key)).start()
