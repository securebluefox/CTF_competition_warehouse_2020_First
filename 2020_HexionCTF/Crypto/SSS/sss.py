from Crypto.Util.number import bytes_to_long, getPrime
from random import randint
from secret import flag

MIN = randint(0x30, 0x40)
P = 2**521 - 1

def eval_at(poly, x, prime):
    """Evaluates polynomial (coefficient tuple) at x"""
    accum = 0
    for coeff in reversed(poly):
        accum *= x
        accum += coeff
        accum %= prime
    return accum

def main():
    poly = [bytes_to_long(flag.encode())]
    poly.extend(set([randint(1, P - 1) for i in range(MIN)]))
    print("┌───────────────┐")
    print("│ SSS Encryptor │")
    print("└───────────────┘")
    print("Enter text to encrypt, leave empty to quit.")
    while True:
        data = input(">>> ")
        if bytes_to_long(data.encode()) % P == 0:
            break
        print(eval_at(poly, bytes_to_long(data.encode()), P))  

if __name__ == "__main__":
    main()