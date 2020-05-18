from Crypto.Util.number import *
q=getPrime(1024)
f=getPrime(511)
g=getPrime(511)
while g>pow(q/4,0.5) and g<pow(q/2,0.5):
	g=getPrime(511)
f_inv_q=inverse(f,q)
h=f_inv_q*g%q
m=bytes_to_long(b'flag')#flag=flag.itself
r=getPrime(510)
e=(r*h+m)%q
print q
print h
print e