#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from hashlib import md5
from secret import flag
assert flag.startswith(b'hgame) and flag.endswith(b')

class Oo0:
    def __init__(self):
        self.O0 = [0] * 256
        self.Ooo = 0
        self.Ooo0 = [0] * 256
        for i in range(256):
            self.O0[i] = i
        self.oO0 = 0
    
    def OO0(self, oO0):
        l = len(oO0)
        for i in range(256):
            self.Ooo0[i] = oO0[i%l]
        for i in range(256):
            self.oO0 = ( self.oO0 + self.O0[i] + self.Ooo0[i] ) % 256
            self.O0[i], self.O0[self.oO0] = self.O0[self.oO0], self.O0[i]
        self.Ooo = self.oO0 = 0
    
    def OO0o(self, length):
        O = []
        for _ in range(length):
            self.Ooo = ( self.Ooo + 1 ) % 256
            self.oO0 = ( self.oO0 + self.O0[self.Ooo] ) % 256
            self.O0[self.Ooo], self.O0[self.oO0] = self.O0[self.oO0], self.O0[self.Ooo]
            t = ( self.O0[self.Ooo] + self.O0[self.oO0] ) % 256
            O.append( self.O0[t] )
        print(self.O0)
        return O

def xor(s1, s2):
    return bytes(map( (lambda x: x[0]^x[1]), zip(s1, s2) ))

def enc(msg):
    Oo0oO = Oo0()
    Oo0oO.OO0( md5(msg).digest()[:8] )
    O0O = Oo0oO.OO0o( len(msg) )
    return xor(msg, O0O)

print( enc(flag) )

# [52, 83, 211, 164, 151, 50, 94, 103, 154, 183, 216, 62, 162, 161, 208, 232, 113, 221, 79, 139, 54, 29, 147, 238, 226, 75, 100, 20, 89, 101, 25, 172, 110, 158, 228, 9, 18, 7, 254, 237, 174, 194, 87, 192, 53, 115, 71, 30, 33, 102, 135, 105, 37, 241, 249, 64, 190, 49, 165, 145, 197, 239, 73, 67, 93, 77, 88, 61, 116, 252, 149, 204, 141, 184, 108, 131, 43, 255, 245, 96, 38, 244, 117, 24, 13, 119, 195, 182, 92, 233, 91, 35, 109, 171, 41, 111, 153, 213, 140, 160, 16, 146, 81, 231, 224, 107, 207, 125, 39, 185, 138, 1, 198, 104, 78, 137, 82, 127, 181, 80, 27, 229, 169, 86, 118, 176, 59, 28, 250, 193, 22, 134, 168, 95, 148, 136, 128, 66, 196, 209, 222, 85, 210, 36, 157, 51, 199, 3, 155, 2, 4, 247, 173, 175, 227, 48, 177, 189, 223, 65, 19, 159, 150, 188, 220, 6, 205, 251, 120, 56, 121, 133, 170, 126, 167, 34, 40, 60, 156, 179, 214, 26, 240, 42, 112, 63, 215, 187, 90, 106, 212, 152, 166, 84, 11, 69, 98, 10, 76, 202, 122, 58, 253, 178, 31, 46, 163, 225, 132, 15, 129, 242, 144, 99, 248, 217, 201, 114, 74, 97, 191, 21, 47, 55, 32, 219, 218, 206, 0, 200, 180, 57, 235, 8, 186, 124, 243, 203, 123, 17, 23, 5, 72, 230, 142, 143, 14, 130, 236, 12, 44, 45, 70, 246, 234, 68]
# b'[\xfe\xdb\x84\r&\xb5\xb6\xe3\x89O\x97,\x94L\xc7\xc5\xd7gr\xbf\xe581\xf6\x16Qh\xcd\xef\x96.\xb4\x12&\xacLa\xde\xff^R- \x0b\xac\x85\x8e \xdf'
