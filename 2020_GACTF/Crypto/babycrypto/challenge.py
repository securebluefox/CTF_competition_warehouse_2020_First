from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random
from hashlib import sha256
from secret import flag, p


def add_points(P, Q):
    return ((P[0]*Q[0]-P[1]*Q[1]) % p, (P[0]*Q[1]+P[1]*Q[0]) % p)


def multiply(P, n):
    Q = (1, 0)
    while n > 0:
        if n % 2 == 1:
            Q = add_points(Q, P)
        P = add_points(P, P)
        n = n//2
    return Q


def gen_key():
   g = （29223879291878505213325643878338189297997503744039619988987863719655098，32188620669315455017576071518169599806490004123869726364682284676721556）
    sk = random.randint(0, 2**256)
    pk = multiply(g, sk)
    return sk, pk


a, A = gen_key()
b, B = gen_key()
print(A)
print(B)

shared = multiply(A, b)[0]
key = sha256(long_to_bytes(shared)).digest()
aes = AES.new(key, AES.MODE_ECB)
ciphertext = aes.encrypt(pad(flag.encode(), AES.block_size))
print(ciphertext.hex())


"""
(68279847973010227567437241690876400434176575735647388141445319082120661, 36521392659318312718307506287199839545959127964141955928297920414981390)
(84698630137710906531637499064120297563999383201108850561060383338482806, 10975400339031190591877824767290004140780471215800442883565278903964109)
26b1b05962d188f1f2abdfad2cef049d45cfc27d9e46f40ebe52e367941bcfa05dd0ef698f528375be2185759e663431
"""