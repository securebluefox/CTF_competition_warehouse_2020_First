import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from secret import flag

KEY = get_random_bytes(16)
NONCE = get_random_bytes(16)


def aes_gcm_encrypt(plaintext):
    cipher = AES.new(KEY, AES.MODE_GCM, nonce=NONCE)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return ciphertext.hex(), tag.hex()


def aes_gcm_decrypt(ciphertext, tag):
    cipher = AES.new(KEY, AES.MODE_GCM, nonce=NONCE)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext


if __name__ == '__main__':
    options = '''Welcome to the AES GCM encryption and decryption tool!
        1. Encrypt message
        2. Decrypt message
        3. Quit
    '''

    def encrypt_msg():
        print("Input a string to encrypt (must be at least 32 characters):")
        user_input = input()
        if len(user_input) < 32:
            sys.exit()
        output = aes_gcm_encrypt(user_input.encode())
        print("Here is your encrypted string & tag, have a nice day :)")
        print(output)


    def decrypt_msg():
        print("Input a hex string and its tag to decrypt:")
        user_input = bytearray.fromhex(input())
        tag = bytearray.fromhex(input())
        try:
            output = aes_gcm_decrypt(user_input, tag)
        except ValueError:
            print("Decryption failed :(")
            return
        print("Here is your decrypted string, have a nice day :)")
        print(output)


    def quit():
        sys.exit()

    menu = {
        '1' : encrypt_msg,
        '2' : decrypt_msg,
        '3' : quit
    }
    
    i = 0
    print('flag', aes_gcm_encrypt(flag)[0])
    while i < 10:
        print(options)
        print('Select option: ')
        choice = input()
        if choice not in menu.keys():
            print("Not a valid choice...")
            sys.exit()
        menu[choice]()
        i += 1



