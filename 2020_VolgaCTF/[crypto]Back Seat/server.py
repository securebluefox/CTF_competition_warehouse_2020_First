#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import time
import base64
from cipher import Cipher
from key_file import key


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
            cipher = Cipher(key)
            send_message('Enter your your data to encrypt (in base64 format):')
            message: bytes = base64.b64decode(read_message().strip())
            eprint('[{0}][INFO] Message {1} (Base64: {2}) was received.'.format(time.strftime("%Y-%m-%d. %H:%M:%S"), message, base64.b64encode(message)))
            message = int.from_bytes(message, byteorder='big')
            key_block = 0
            n = message.bit_length()

            for _ in range(n):
                key_block = (key_block << 1) + cipher.next_bit()

            ciphertext = message ^ key_block
            ciphertext = int.to_bytes(ciphertext, length=int(n / 8) + 1, byteorder='big')
            ciphertext = base64.b64encode(ciphertext)
            send_message(ciphertext)
            eprint('[{0}][INFO] Ciphertext {1} (Base64: {2}) was sent.'.format(time.strftime("%Y-%m-%d. %H:%M:%S"), base64.b64decode(ciphertext), ciphertext))

    except Exception as ex:
        send_message('Something must have gone very, very wrong...')
        eprint('[{0}][ERROR] {1}'.format(time.strftime("%Y-%m-%d. %H:%M:%S"), ex))

    finally:
        pass