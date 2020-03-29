#!/usr/lib/python3
# -*- coding: utf-8 -*-


class Cipher:
    def __init__(self, key: int):
        self.regs = [[0] * 23, [0] * 29, [0] * 31, [0] * 37]
        self.b0 = [22, 21, 19, 17, 16, 12, 10, 9, 8, 7, 3, 2, 1, 0]
        self.b1 = [28, 27, 26, 24, 23, 22, 21, 20, 17, 16, 12, 10, 9, 5, 4, 2, 1, 0]
        self.b2 = [30, 29, 26, 24, 23, 22, 21, 20, 19, 15, 14, 12, 11, 10, 9, 8, 7, 3, 2, 0]
        self.b3 = [36, 33, 32, 31, 29, 28, 25, 23, 19, 18, 17, 16, 15, 12, 10, 7, 6, 5, 3, 1, 0]
        self.f = 0x6B

        key = int_to_list(key, 120)[:120]
        self.regs[0] = key[:23]
        self.regs[1] = key[23:23+29]
        self.regs[2] = key[23+29:23+29+31]
        self.regs[3] = key[23+29+31:]

    @staticmethod
    def r_shift(reg, n):
        assert len(reg) > n
        if n == 0:
            return list_to_int(reg)
        return list_to_int(reg[:-n])

    @staticmethod
    def bitwise_and(reg, n):
        return list_to_int(reg) & n

    def clock_r(self, reg: list, branches: list) -> tuple:
        ret = reg[len(reg) - 1]
        new = 0
        for i in branches:
            new ^= reg[i]
        reg = [new] + reg[:-1]

        return reg, ret

    def next_bit(self) -> int:
        s = self.bitwise_and(self.regs[0], 3) + 1
        for i in range(s):
            self.regs[0], _ = self.clock_r(self.regs[0], self.b0)

        x0 = self.bitwise_and(self.regs[0], 1)

        t = self.r_shift(self.regs[0], 3) & 0x7
        self.f = self.f ^ self.r_shift(self.regs[0], t) & 0xFF

        self.regs[1], x1 = self.clock_r(self.regs[1], self.b1)
        self.regs[2], x2 = self.clock_r(self.regs[2], self.b2)
        self.regs[3], x3 = self.clock_r(self.regs[3], self.b3)

        idx = x1 + (x2 << 1) + (x3 << 2)
        f = int_to_list(self.f, 8)[::-1]
        o = x0 ^ f[idx]

        return o


def int_to_list(n, fill):
    tmp = list(map(int, list(bin(n)[2:])))
    assert fill >= len(tmp)
    return [0] * (fill - len(tmp)) + tmp


def list_to_int(l):
    tmp = ''.join(list(map(str, l)))
    return int(tmp, 2)


if __name__ == '__main__':
    key = 0xABCDEF0123456789ABCDEF01234567
    test_keystream1 = [1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 
                       0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 
                       0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 
                       1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 
                       0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 
                       1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 
                       1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 
                       0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1]
    
    cipher = Cipher(key)

    output = []
    for _ in range(128):
        output.append(cipher.next_bit())

    if output == test_keystream1:
        print('Test: OK')