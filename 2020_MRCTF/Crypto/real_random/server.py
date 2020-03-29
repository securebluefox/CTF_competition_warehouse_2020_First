#!/usr/bin/python3.6
# -*-coding:utf-8 -*-

from Crypto.Util.number import getPrime

with open('./flag.txt') as f:
    flag = f.readline()
flag = bytes(flag.encode('utf-8'))


random = [[] for _ in range(len(flag))]
M = [0 for _ in range(len(flag))]
D = [0 for _ in range(len(flag))]


def gcd(a,b):
    while a!=0:
        a, b = b % a, a
    return b


def invert(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3//v3
        v1, v2, v3, u1, u2, u3 = (u1-q*v1), (u2-q*v2), (u3-q*v3), v1, v2, v3
    return u1%m


def gen_N(flag):
    return (flag * 16**2) + flag


def generate_random():
    for t in range(len(flag)):
        p = getPrime(6)
        q = getPrime(6)
        m = p * q * 2 ** 5
        b = 4 * p * q + 1
        c = getPrime(10)
        d = getPrime(4)
        times = getPrime(18)
        random[t] = [0 for _ in range(times)]
        M[t] = (p-1) * (q-1)
        D[t] = d
        _b = invert(b, m)
        x = ((gen_N(flag[t]) - c) * _b) % m
        for i in range(2**d):
            x = (b * x + c) % m
        for i in range(times):
            x = (b * x + c) % m
            random[t][i] = x


if __name__ == '__main__':
    print("Loading...")
    generate_random()
    print("GAME START : )")
    for t in range(len(flag)):
        print('m: ', M[t])
        print('d: ', D[t])
        print('Now guess where the flag is ^_^ ')
        number = int(input())
        flag_part = gen_N(flag[t])
        if random[t][number] == flag_part:
            print(flag_part)
        else:
            print("You're wrong : (")
            break
    print('GAME OVER : )')


