from Crypto.Util.number import*
from secret import flag


class LCG:
    def __init__(self):
        self.a = getRandomNBitInteger(32)
        self.b = getRandomNBitInteger(32)
        self.m = getPrime(32)
        self.seed = getRandomNBitInteger(32)

    def next(self):
        self.seed = (self.a*self.seed+self.b) % self.m
        return self.seed >> 16

    def output(self):
        print("a = {}\nb = {}\nm = {}".format(self.a, self.b, self.m))
        print("state1 = {}".format(self.next()))
        print("state2 = {}".format(self.next()))


class DH:
    def __init__(self):
        self.lcg = LCG()
        self.lcg.output()
        self.g = getRandomNBitInteger(128)
        self.m = getPrime(256)
        self.A, self.a = self.gen_AB()
        self.B, self.b = self.gen_AB()
        self.key = pow(self.A, self.b, self.m)

    def gen_AB(self):
        x = ''
        for _ in range(64):
            x += '1' if self.lcg.next() % 2 else '0'
        return pow(self.g, int(x, 2), self.m), int(x, 2)


DH = DH()
flag = bytes_to_long(flag)
print("g = {}\nA = {}\nB = {}\nM = {}".format(DH.g, DH.A, DH.B, DH.m))
print("Cipher = {}".format(flag ^ DH.key))

'''
a = 3844066521
b = 3316005024
m = 2249804527
state1 = 16269
state2 = 4249
g = 183096451267674849541594370111199688704
A = 102248652770540219619953045171664636108622486775480799200725530949685509093530
B = 74913924633988481450801262607456437193056607965094613549273335198280176291445
M = 102752586316294557951738800745394456033378966059875498971396396583576430992701
Cipher = 13040004482819935755130996285494678592830702618071750116744173145400949521388647864913527703
'''