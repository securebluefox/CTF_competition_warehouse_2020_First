#!/usr/bin/env python3
# Potentially Eazzzy
# Author: chainsaw10

# If I screwed up and you can't generate a key for your email, I tested this
# program with info@umbccd.io and it should work with that email and an
# appropriate key. Still yell at me in Discord though ;)

try:
    FLAG = open("flag.txt", "r").read()
except:
    FLAG = "DogeCTF{Flag is different on the server}"

import itertools

ALPHABET = [chr(i) for i in range(ord("*"), ord("z")+1)]

def print_flag():
    print("Generating flag...")
    print(FLAG)

a = lambda c: ord(ALPHABET[0]) + (c % len(ALPHABET))

o = lambda c: ord(c)

oa = lambda c: a(o(c))

def indexes(s, needle):
    a = 0
    for idx, c in enumerate(s):
        if c == needle:
            a += idx
    return a

def m(one, two, three, four):
    d = len(ALPHABET)//2
    s = ord(ALPHABET[0])
    s1, s2, s3 = o(one) - s, o(two) - s, o(three) - s
    return sum([s1, s2, s3]) % d == four % d

def validate(email, key):
    email = email.strip()
    key = key.strip()

    if len(key) != 32:
        return False

    email = email[:31].ljust(31, "*")
    email += "*"

    for c in itertools.chain(email, key):
        if c not in ALPHABET:
            return False

    if email.count("@") != 1:
        return False

    if key[0] != "Z":
        return False

    dotcount = email.count(".")
    if dotcount < 0 or dotcount >= len(ALPHABET):
        return False

    if a(dotcount) != o(key[1]):
        return False

    if o(key[3]) != a(o(key[1])%30 + o(key[2])%30) + 5:
        return False

    if o(key[2]) != a(indexes(email, "*") + 7):
        return False

    if o(key[4]) != a(sum(o(i) for i in email)%60 + o(key[5])):
        return False

    if o(key[5]) != a(o(key[3]) + 52):
        return False

    if o(key[6]) != a((o(key[7])%8)*2):
        return False

    if o(key[7]) != a(o(key[1]) + o(key[2]) - o(key[3])):
        return False

    if o(key[8]) != a((o(key[6])%16) / 2):
        return False

    if o(key[9]) != a(o(key[6]) + o(key[4]) + o(key[8]) - 4):
        return False

    if o(key[10]) != a((o(key[1])%2) * 8 + o(key[2]) % 3 + o(key[3]) % 4):
        return False

    if not m(email[3], key[11], key[12], 8):
        return False
    if not m(email[7], key[13], key[4], 18):
        return False
    if not m(email[9], key[14], key[3], 23):
        return False
    if not m(email[10], key[15], key[10], 3):
        return False
    if not m(email[11], key[13], key[16], 792):
        return False
    if not m(email[12], key[17], key[4], email.count("d")):
        return False
    if not m(email[13], key[18], key[7], email.count("a")):
        return False
    if not m(email[14], key[19], key[8], email.count("w")):
        return False
    if not m(email[15], key[20], key[1], email.count("g")):
        return False
    if not m(email[16], email[17], key[21], email.count("s")):
        return False
    if not m(email[18], email[19], key[22], email.count("m")):
        return False
    if not m(email[20], key[23], key[17], 9):
        return False
    if not m(email[21], key[24], key[13], 41):
        return False
    if not m(email[22], key[25], key[10], 3):
        return False
    if not m(email[23], key[26], email[14], email.count("1")):
        return False
    if not m(email[24], email[25], key[27], email.count("*")):
        return False
    if not m(email[26], email[27], key[28], 7):
        return False
    if not m(email[28], email[29], key[29], 2):
        return False
    if not m(email[30], key[30], email[18], 4):
        return False
    if not m(email[31], key[31], email[4], 7):
        return False

    return True


def main():
    print("Welcome to Flag Generator 5000")
    print()
    print("Improving the speed quality of CTF solves since 2020")
    print()
    print("You'll need to have your email address and registration key ready.")
    print("Please note the support hotline is closed for COVID-19 and will be")
    print("unavailable until further notice.")
    print()

    email = input("Please enter your email address: ")
    key = input("Please enter your key: ")

    if validate(email, key):
        print_flag()
    else:
        print("License not valid. Please contact support.")

main()
