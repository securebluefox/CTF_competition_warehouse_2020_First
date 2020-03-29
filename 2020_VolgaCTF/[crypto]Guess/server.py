#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from Crypto.PublicKey import ElGamal
from Crypto import Random
from flag_file import flag
import Crypto.Random.random
import time
import sys


"""
    Communication utils
"""

def read_message():
    return sys.stdin.readline()


def send_message(message):
    sys.stdout.write('{0}\r\n'.format(message))
    sys.stdout.flush()


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


"""
    Algebra
"""

def kronecker(x, p):
    q = (p - 1) / 2
    return pow(x, q, p)


def findQNR(p):
    r = Crypto.Random.random.randrange(2, p - 1)
    while kronecker(r, p) == 1:
        r = Crypto.Random.random.randrange(2, p-1)
    return r


def findQR(p):
    r = Crypto.Random.random.randrange(2, p - 1) 
    return pow(r, 2, p)


"""
    Main
"""

if __name__ == '__main__':
    try:
        while True:
            key = ElGamal.generate(512, Random.new().read)
            runs = 1000
            successful_tries = 0

            send_message('(y, p) = ({0}, {1})'.format(key.y, key.p))

            for i in xrange(runs):
                plaintexts = dict()
                plaintexts[0] = findQNR(key.p)
                plaintexts[1] = findQR(key.p)

                challenge_bit = Crypto.Random.random.randrange(0,2)
                eprint('[{0}][INFO] Bit {1} was generated.'.format(time.strftime("%Y-%m-%d. %H:%M:%S"), challenge_bit))
                r = Crypto.Random.random.randrange(1,key.p-1) 
                challenge = key.encrypt(plaintexts[challenge_bit], r)

                # Send challenge
                send_message(challenge)

                # Receive challenge_bit
                received_bit = read_message()
                eprint('[{0}][INFO] Bit {1} was received.'.format(time.strftime("%Y-%m-%d. %H:%M:%S"), received_bit))
                if int(received_bit) == challenge_bit:
                    successful_tries += 1
                    eprint(successful_tries)
                    
            if successful_tries == runs:
                send_message(flag)

    except Exception as ex:
        send_message('Something must have gone very, very wrong...')
        eprint('[{0}][ERROR] {1}'.format(time.strftime("%Y-%m-%d. %H:%M:%S"), ex))

    finally:
        pass