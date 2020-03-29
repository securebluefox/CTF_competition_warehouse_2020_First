#!/usr/lib/python3
# -*- coding: utf-8 -*-


class Cipher:
    def __init__(self, key: list, frame: int):
        self.key = key
        self.frame = frame
        self.br = [[13, 16, 17, 18], [20, 21], [7, 20, 21, 22], [11, 16]]
        self.majs = [[12, 14, 15], [9, 13, 16], [13, 16, 18]]
        self.regs = [[0] * 19, [0] * 22, [0] * 23, [0] * 17]
        self.tick = [3, 7, 10]
        self.complement = [1, 2, 0]

        for i in range(64):
            keybit = (self.key[int(i / 8)] >> (i & 7)) & 1
            for j in range(4):
                self.regs[j] = self.clock_r(self.regs[j], self.br[j])
                self.regs[j][0] ^= keybit

        for i in range(22):
            framebit = (self.frame >> i) & 1
            for j in range(4):
                self.regs[j] = self.clock_r(self.regs[j], self.br[j])
                self.regs[j][0] ^= framebit

        self.regs[0][15] = 1
        self.regs[1][16] = 1
        self.regs[2][18] = 1
        self.regs[3][10] = 1

        for i in range(99):
            maj = self.maj(list(map(self.regs[3].__getitem__, self.tick)))
            if self.regs[3][10] == maj:
                self.regs[0] = self.clock_r(self.regs[0], self.br[0])
            if self.regs[3][3] == maj:
                self.regs[1] = self.clock_r(self.regs[1], self.br[1])
            if self.regs[3][7] == maj:
                self.regs[2] = self.clock_r(self.regs[2], self.br[2])
            self.regs[3] = self.clock_r(self.regs[3], self.br[3])

    @staticmethod
    def maj(nums: list) -> int:
        if sum(nums) >= 2:
            return 1
        return 0

    @staticmethod
    def clock_r(reg: list, branches: list) -> list:
        new = 0
        for i in branches:
            new ^= reg[i]
        reg = [new] + reg[:-1]

        return reg

    def next_bit(self) -> int:
        output = 0
        maj = self.maj(list(map(self.regs[3].__getitem__, self.tick)))
        if self.regs[3][10] == maj:
            self.regs[0] = self.clock_r(self.regs[0], self.br[0])
        if self.regs[3][3] == maj:
            self.regs[1] = self.clock_r(self.regs[1], self.br[1])
        if self.regs[3][7] == maj:
            self.regs[2] = self.clock_r(self.regs[2], self.br[2])
        self.regs[3] = self.clock_r(self.regs[3], self.br[3])
        for i in range(3):
            bits = list(map(self.regs[i].__getitem__, self.majs[i]))
            bits[self.complement[i]] ^= 1
            output ^= self.maj(bits)
        output = output ^ self.regs[0][-1] ^ self.regs[1][-1] ^ self.regs[2][-1]

        return output


if __name__ == '__main__':
    key = [0x00, 0xfc, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
    iv = 0x21
    test_keystream1 = [0xf4, 0x51, 0x2c, 0xac, 0x13, 0x59, 0x37, 0x64, 0x46, 0x0b, 0x72, 0x2d, 0xad, 0xd5, 0x00]
    test_keystream2 = [0x48, 0x00, 0xd4, 0x32, 0x8e, 0x16, 0xa1, 0x4d, 0xcd, 0x7b, 0x97, 0x22, 0x26, 0x51, 0x00]

    cipher = Cipher(key, iv)

    output = [0] * 15
    for i in range(114):
        output[int(i / 8)] |= cipher.next_bit() << (7 - (i & 7))
    if output == test_keystream1:
        print('Test#1: OK')
        
    output = [0] * 15
    for i in range(114):
        output[int(i / 8)] |= cipher.next_bit() << (7 - (i & 7))
    if output == test_keystream2:
        print('Test#2: OK')

