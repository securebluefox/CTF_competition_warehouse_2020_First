from Crypto.Cipher import AES
import binascii, sys
import hashlib

key = b'T0EyZaLRzQmNe2**'
KEYSIZE = len(key)
assert(KEYSIZE==16)


def pad(message):
    p = bytes((KEYSIZE - len(message) % KEYSIZE) * chr(KEYSIZE - len(message) % KEYSIZE),encoding='utf-8')
    return message + p


def encrypt(message,passphrase,iv):
	aes = AES.new(passphrase, AES.MODE_CBC, iv)
	return aes.encrypt(message)


h = hashlib.md5(key).hexdigest()
SECRET = binascii.unhexlify(h)[:10]


with open('flag','rb') as f:
	IV = f.read().strip(b'gactf{').strip(b'}')	

message = b'AES CBC Mode is commonly used in data encryption. What do you know about it?'+SECRET

print("Encrypted data: ", binascii.hexlify(encrypt(pad(message),key,IV)))

'''
Encrypted data: b'a8**************************b1a923**************************011147**************************6e094e**************************cdb1c7**********a32c412a3e7474e584cd72481dab9dd83141706925d92bdd39e4'
'''