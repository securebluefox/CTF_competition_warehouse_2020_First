from Crypto.Util.number import *
from random import randint
flag = int('SCTF{*******************}'.encode('hex'), 16)
d = getPrime(randint(380, 385))

for _ in range(3):
    p = getPrime(512)
    q = getPrime(512)
    n = p * q
    fn = (p - 1) * (q - 1)
    e = inverse(d, fn)
    c = pow(flag, e, n)
    print 'e'+str(_)+str('=')+hex(e)
    print 'n'+str(_)+str('=')+hex(n)
    print 'c'+str(_)+str('=')+hex(c)
    print '-' * 350