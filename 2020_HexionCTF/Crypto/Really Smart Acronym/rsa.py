from Crypto.Util.number import bytes_to_long
from Crypto.PublicKey import RSA
from secret import flag
import os

key = RSA.generate(1024)
print("Flag:", pow(bytes_to_long(flag), key.e, key.n))

print("One encrypt:")
m = int(input("m => "))
print(pow(m, key.e, key.n))

print("Alot of unhelpful decrypts:")
for i in range(int(os.getenv("MAX_TRIES") or 1024)):
    c = int(input("> "))
    print(bin(pow(c, key.d, key.n))[-1])