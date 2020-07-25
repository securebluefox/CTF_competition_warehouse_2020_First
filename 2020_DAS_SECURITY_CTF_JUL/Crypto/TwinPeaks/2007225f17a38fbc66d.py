#!/usr/bin/python3
from socketserver import BaseRequestHandler, TCPServer, ThreadingTCPServer
import random
from flag import flag
import os
import string
from hashlib import sha256
import signal

class Twinleaks:

    def __init__(self):
        self.offset = random.getrandbits(64)
        self.mask = 0xffffffff

    def S(self, x):
        return (x + self.offset) & self.mask

    def encrypt(self, message):
        mess = [int.from_bytes(message[4 * i:4 * (i + 1)], 'big') for i in range(len(message) // 4)]
        a, b, c, d = tuple(mess)
        y2 = d ^ self.S(c ^ self.S(b ^ self.S(a)))
        y3 = a ^ self.S(y2)
        y4 = b ^ self.S(a) ^ self.S(y3)
        y1 = c ^ self.S(b ^ self.S(a)) ^ self.S(y4)

        return hex(y1).strip("0xL").rjust(8, "0") + \
               hex(y2).strip("0xL").rjust(8, "0") + \
               hex(y3).strip("0xL").rjust(8, "0") + \
               hex(y4).strip("0xL").rjust(8, "0")




def s2b(s):
    res = b''
    for i in s:
        res += bytes([ord(i)])
    return res


def b2s(b):
    s = ''
    for i in b:
        s += chr(i)
    return s

flag = flag+(16-len(flag)%16)*b'b'


class Task(BaseRequestHandler):


    def dosend(self, msg):
        try:
            self.request.sendall(msg)
        except:
            pass

    def recvall(self, sz):
        try:
            r = sz
            res = ""
            while r > 0:
                res += b2s(self.request.recv(r))
                if res.endswith("\n"):
                    r = 0
                else:
                    r = sz - len(res)
            res = res.strip()
        except:
            res = ""
        return res.strip("\n")

    def proof_of_work(self):
        random.seed(os.urandom(8))
        proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(20)])
        digest = sha256(proof.encode()).hexdigest()
        self.request.send(s2b(("sha256(XX+%s) == %s\n" % (proof[2:],digest))))
        self.request.send(b'Give me XX:')
        x = self.request.recv(10)
        x = b2s(x)
        x = x.strip()
        if len(x) != 2 or sha256((x+proof[2:]).encode()).hexdigest() != digest: 
            return False
        return True

    def handle(self):

        signal.alarm(300)
        if not self.proof_of_work():
   		    return
        signal.alarm(300)

        self.dosend(b"Enjoying TwinPeaks.\n")
        cipher = Twinleaks()
        
        self.dosend(b"Here is encrypted flag\n")


        for i in range(len(flag) // 4):
            self.dosend(s2b(cipher.encrypt(flag[i * 4:(i + 1) * 4]+os.urandom(12)) + '\n'))
        while True:
            try:
                self.dosend(b"Give me your message:\n")
                message = self.recvall(1024)
                if type(message) != str:
                    message = b2s(message)
                self.dosend(b"Here is your encrypted message\n")
                message = bytes.fromhex(message)
                message = message + b'0' * (16 - len(message) % 16)
                for j in range(len(message) // 16):
                    self.dosend(s2b(cipher.encrypt(message[j * 16:(j + 1) * 16]) + '\n'))
            except:
                self.dosend(b"error.\n")
                break


if __name__ == '__main__':
    HOST, PORT = "0.0.0.0", 9999
    server = ThreadingTCPServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()


