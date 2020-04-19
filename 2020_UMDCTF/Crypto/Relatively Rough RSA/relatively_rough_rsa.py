def encrypt_flag(plaintext_bytes):
    while True:
        p = number.getPrime(4096)
        if p % 4 != 3:
            continue
        q = p + 2
        while True:
            if number.isPrime(q) and q % 4 == 3:
                break
            q += 2
        break
    n = int(p * q)
    e = 0xcbfe
    plaintext_bytes += b'\x00'
    plaintext = 0
    while plaintext * 3 <= n:
        plaintext = int.from_bytes(plaintext_bytes, 'big')
        plaintext_bytes += bytes([random.getrandbits(8)])
    ciphertext = encrypt(plaintext, n, e)
    open('ciphertext', 'w').write(str(ciphertext))
    public_key = str(n) + ":" + str(e)
    open('public_key', 'w').write(public_key)
