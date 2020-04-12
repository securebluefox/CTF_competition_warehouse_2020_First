#!/usr/bin/env python3
from cryptography.fernet import Fernet
from secrets import token_bytes
from base64 import b64encode
import requests

# Our own PQ encryption algorithm
# This should be safe against quantum computers
from post_quantum import pq_encrypt

from config import server_addr


def get(path, data=None):
    return requests.get(f"{server_addr}/{path}", data=data)


def decrypt(cipher, key):
    return Fernet(b64encode(key)).decrypt(cipher)


def main():
    sym_key = token_bytes(32)
    pub_key = get("key").text
    cipher = pq_encrypt(pub_key, sym_key)
    enc_flag = get("flag", data=cipher)
    print(decrypt(enc_flag.text.encode(), sym_key).decode())


if __name__ == "__main__":
    main()
