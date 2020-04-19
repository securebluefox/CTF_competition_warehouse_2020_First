from Crypto.PublicKey import RSA

def encrypt_flag(plaintext_bytes):
    RSAkey = RSA.generate(1024)
    n = getattr(RSAkey.key, 'n')
    e = 5
    plaintext_bytes += b'\x00'
    plaintext = int.from_bytes(plaintext_bytes, 'big')
    ciphertext = pow(plaintext, e, n)
    open('ciphertext', 'w').write(str(ciphertext))
    public_key = str(n) + ":" + str(e)
    open('public_key', 'w').write(public_key)
