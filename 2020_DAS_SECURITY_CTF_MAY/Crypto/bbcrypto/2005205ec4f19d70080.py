# -*- coding:utf-8 -*-
import A,SALT
from itertools import *

def encrypt(m, a, si):
    c=""
    for i in range(len(m)):
        c+=hex(((ord(m[i])) * a + ord(next(si))) % 128)[2:].zfill(2)
    return c
if __name__ == "__main__":
    m = 'flag{********************************}'
    a = A
    salt = SALT
    assert(len(salt)==3)
    assert(salt.isalpha())
    si = cycle(salt.lower())
    print("明文内容为：")
    print(m)
    print("加密后的密文为：")
    c=encrypt(m, a, si)
    print(c)
    #加密后的密文为：
    #177401504b0125272c122743171e2c250a602e3a7c206e014a012703273a3c0160173a73753d