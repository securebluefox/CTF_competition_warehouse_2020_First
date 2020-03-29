#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socket
import sys
import msgpack
import base64
import hashlib
import fastecdsa
from Crypto.Random import random
from Crypto.Cipher import AES
from fastecdsa.curve import Curve
from fastecdsa.point import Point


# region Params

BITS = 56
INPUTSIZE = 1024

a = 1
b = 0
p = 3009944491747103173592552029257669572283120430367
order = 3009944491747103173592552029257669572283120430368
gx = 2900641855339024752663919275085178630626065454884
gy = 1803317565451817334919844936679231131166218238368

curve = Curve("Super Secure Elliptic Curve", p, a, b, order, gx, gy)
P = Point(gx, gy, curve)

# endregion Params


# region Communication utils

def intToBytes(number):
    return number.to_bytes(24,byteorder = 'big')

def bytesToInt(b):
    return int.from_bytes(b,byteorder = 'big')


def pointEncoder(obj):
    if isinstance(obj, Point):
        obj = [intToBytes(obj.x),intToBytes(obj.y)]
    return obj


def pointDecoder(obj):
    obj = Point(bytesToInt(obj[0]),bytesToInt(obj[1]),curve)
    return obj


def sendMessageToServer(socket, data):
	packed = msgpack.packb(data, use_bin_type = True)
	socket.sendall(packed)


def getMessageFromServer():
    message = sock.recv(INPUTSIZE)
    return msgpack.unpackb(message, raw = True)


def sendPointToServer(socket, point):
    packed = msgpack.packb(point, default = pointEncoder, use_bin_type = True)
    socket.sendall(packed)


def getPointFromServer():
    point = sock.recv(INPUTSIZE)
    return msgpack.unpackb(point, list_hook = pointDecoder, raw = True)

# endregion Communication utils


# region Encryption utils

def decrypt(enc, password):
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]
    private_key = hashlib.sha256(str(password).encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return bytes.decode(unpad(cipher.decrypt(enc[16:])))

# endregion Encryption utils


if __name__ == "__main__":
    HOST, PORT = sys.argv[1], int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST,PORT))

        secureNumber = random.getrandbits(BITS)
        sendPointToServer(sock, P * secureNumber)
        point = getPointFromServer()
        securePoint = secureNumber * point
        encrytpedFlag = getMessageFromServer()
        flag = decrypt(encrytpedFlag,securePoint.x)
        print('Your flag: {0}'.format(flag))
