#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from cipher import Cipher
from key_file import key
import base64


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
    Main
"""

if __name__ == '__main__':
    try:
        while True:
            send_message('Enter your your data to encrypt (in base64 format):')
            message: bytes = base64.b64decode(read_message().strip())
            n_blocks = int(len(message) / 15) + 1
            ciphertext = b''
            for frame in range(n_blocks):
                p_block = message[frame*15:(frame+1)*15]
                p_block = int.from_bytes(p_block, byteorder='big')
                cipher = Cipher(key, frame)
                k_block = 0
                for _ in range(114):
                    k_block = (k_block << 1) + cipher.next_bit()
                k_block = k_block << 6
                c_block = p_block ^ k_block
                ciphertext += int.to_bytes(c_block, length=15, byteorder='big')
            ciphertext = base64.b64encode(ciphertext)
            send_message(ciphertext)

    except Exception as ex:
        send_message('Something must have gone very, very wrong...')
        eprint(str(ex))

    finally:
        pass