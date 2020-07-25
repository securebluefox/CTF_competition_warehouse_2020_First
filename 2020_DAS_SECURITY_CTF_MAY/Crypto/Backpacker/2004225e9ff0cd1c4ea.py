import signal
import string
from hashlib import sha256
from Crypto.Util.number import *
from Crypto.Random import random
from secret import flag

banner = '''
 ____             _                     _             _       _   _ 
| __ )  __ _  ___| | ___ __   __ _  ___| | _____ _ __( )___  | | | | ___  _ __ ___   ___
|  _ \ / _` |/ __| |/ / '_ \ / _` |/ __| |/ / _ \ '__|// __| | |_| |/ _ \| '_ ` _ \ / _ \\
| |_) | (_| | (__|   <| |_) | (_| | (__|   <  __/ |    \__ \ |  _  | (_) | | | | | |  __/
|____/ \__,_|\___|_|\_\ .__/ \__,_|\___|_|\_\___|_|    |___/ |_| |_|\___/|_| |_| |_|\___|
                      |_|'''


def timeout_handler(signum, frame):
    print("\n[!]Sorry, timeout...")
    raise TimeoutError


def proof_of_work():
    print("[++++++++++++++++] Proof of work [++++++++++++++++]")
    proof = ''.join(
        [random.choice(string.ascii_letters+string.digits)
         for _ in range(20)]
    )
    proof_cipher = sha256(proof.encode()).hexdigest()
    print("sha256(XXXX+{}) == {}".format(proof[4:], proof_cipher))
    guess = input("Give me XXXX: ")
    if len(guess) != 4 or sha256((guess + proof[4:]).encode()).hexdigest() != proof_cipher:
        print("[++++++++++++++++] You failed, exit... [++++++++++++++++]")
        exit(0)
    print("[++++++++++++++++] Proof of work has passed [++++++++++++++++]")


class Knapsack:
    n = None
    elements = None

    def load(self, n, nbits):
        self.n = n
        self.elements = set()
        while len(self.elements) < n:
            self.elements.add(getRandomNBitInteger(nbits))
        self.elements = list(self.elements)

    def super_load(self, n):
        self.n = n
        self.elements = [233]
        sum = 233
        while len(self.elements) < n:
            self.elements.append(sum + getRandomRange(1, 128))
            sum += self.elements[-1]

    def encrypt(self):
        if not self.n or not self.elements:
            raise ValueError("[!]Something Wrong...")
        m = getRandomNBitInteger(self.n)
        m_list = [int(_) for _ in bin(m)[2:]]
        c = 0
        for i in range(self.n):
            c += m_list[i] * self.elements[i]
        return (c, m)


def challenge_1():
    print("[++++++++++++++++] Enjoy challenge_1 [++++++++++++++++]")
    K = Knapsack()
    K.load(10, 16)
    print("[+]There are {} elements in the knapsack.".format(K.n))
    for i in range(K.n):
        print(K.elements[i])
    (c, m) = K.encrypt()
    print("[+]c = {}".format(c))
    guess = input("[-]m(hex) = ")
    try:
        guess = int(guess, 16)
        if guess == m:
            print("[++++++++++++++++] challenge_1 has passed [++++++++++++++++]")
            return
    except:
        pass
    print("[++++++++++++++++] You failed, exit... [++++++++++++++++]")
    exit(0)


def challenge_2():
    print("[++++++++++++++++] Enjoy challenge_2 [++++++++++++++++]")
    K = Knapsack()
    K.super_load(50)
    print("[+]There are {} elements in the knapsack.".format(K.n))
    for i in range(K.n):
        print(K.elements[i])
    (c, m) = K.encrypt()
    print("[+]c = {}".format(c))
    guess = input("[-]m(hex) = ")
    try:
        guess = int(guess, 16)
        if guess == m:
            print("[++++++++++++++++] challenge_2 has passed [++++++++++++++++]")
            return
    except:
        pass
    print("[++++++++++++++++] You failed, exit... [++++++++++++++++]")
    exit(0)


def challenge_3():
    print("[++++++++++++++++] Enjoy challenge_3 [++++++++++++++++]")
    K = Knapsack()
    K.load(100, 312)
    print("[+]There are {} elements in the knapsack.".format(K.n))
    for i in range(K.n):
        print(K.elements[i])
    (c, m) = K.encrypt()
    print("[+]c = {}".format(c))
    guess = input("[-]m(hex) = ")
    try:
        guess = int(guess, 16)
        if guess == m:
            print("[++++++++++++++++] challenge_3 has passed [++++++++++++++++]")
            print("[+]Excellent Backpacker, your flag is {}".format(flag))
            return
    except:
        pass
    print("[++++++++++++++++] You failed, exit... [++++++++++++++++]")
    exit(0)


def main():
    proof_of_work()
    challenge_1()
    challenge_2()
    challenge_3()


if __name__ == "__main__":
    try:
        print(banner)
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(60)
        main()
    except:
        pass
