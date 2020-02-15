#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socketserver
import os, sys, signal
import string, random
from hashlib import sha256

from secret import FLAG

class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 2048
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline: msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'> '):
        self.send(prompt, newline=False)
        return self._recvall()

    def proof_of_work(self):
        random.seed( os.urandom(8) )
        proof = ''.join([ random.choice(string.ascii_letters+string.digits) for _ in range(20) ])
        _hexdigest = sha256(proof.encode()).hexdigest()
        self.send(str.encode( "sha256(XXXX+%s) == %s" % (proof[4:],_hexdigest) ))
        x = self.recv(prompt=b'Give me XXXX: ')
        if len(x) != 4 or sha256(x+proof[4:].encode()).hexdigest() != _hexdigest: 
            return False
        return True

    def handle(self):
        signal.alarm(60)
        if not self.proof_of_work():
            return
        self.send(b'The secret code?')
        _code = self.recv()
        if _code == b'I like playing Hgame':
            self.send(b'Ok, you find me.')
            self.send(b'Here is the flag: ' + FLAG)
            self.send(b'Bye~')
        else:
            self.send(b'Rua!!!')
        self.request.close()

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 1234
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
