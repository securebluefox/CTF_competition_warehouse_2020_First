#!/usr/bin/env sage

with open('flag', 'rb') as fp:
    flag = fp.read()
assert len(flag) == 37 and flag[:5] == b'flag{' and flag[-1:] == b'}'
flag = int.from_bytes(flag[5:-1], 'big')

F = GF(2**256)
P = PolynomialRing(F, 'u, v')
u, v = P.gens()
PP = PolynomialRing(F, 'w')
w = PP.gens()[0]

h = u^2 + u
f = u^5 + u^3 + 1
c = v^2 + h*v - f
f = f(u=w)
h = h(u=w)

def encode(plain):
    assert plain < 2**256
    x = F.fetch_int(plain)
    y, k = c(u=x, v=w).roots()[0]
    assert k == 1
    return w - x, y

def decode(c):
    x, y = c
    print(list(x))
    print(y)
    x = [i.integer_representation() for i in x]
    y = [i.integer_representation() for i in y]
    return x, y

def add(p1, p2):
    a1, b1 = p1
    a2, b2 = p2
    d1, e1, e2 = xgcd(a1, a2)
    d, c1, c2 = xgcd(d1, b1+b2+h)
    di = PP(1/d)
    a = a1*a2*di*di
    b = (c1*e1*a1*b2+c1*e2*a2*b1+c2*(b1*b2+f))*di
    b %= a

    while a.degree() > 2:
        a = PP((f-b*h-b*b)/a)
        b = (-h-b)%a
    a = a.monic()
    return a, b

def mul(p, k):
    if k == 1:
        return p
    else:
        tmp = mul(p, k//2)
        tmp = add(tmp, tmp)
        if k & 1:
            tmp = add(tmp, p)
        return tmp

if __name__ == '__main__':
    e = 65537
    c = mul(encode(flag), e)
    ctext = decode(c)
    print(ctext)
    # ([113832590633816699072296178013238414056344242047498922038140127850188287361982, 107565990181246983920093578624450838959059911990845389169965709337104431186583, 1], [60811562094598445636243277376189331059312500825950206260715002194681628361141, 109257511993433204574833526052641479730322989843001720806658798963521316354418])
