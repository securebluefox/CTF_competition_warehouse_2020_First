from base64 import b16encode

Zx.<x> = ZZ[]
n = 109 
q = 2048
p = 3
Df = 9
Dg = 10
Dr = 11

def mul(f,g):
    return (f * g) % (x^n-1)

def bal_mod(f,q):
    g = list(((f[i] + q//2) % q) - q//2 for i in range(n))
    return Zx(g)

def random_poly(d):
    assert d <= n
    result = n*[0]
    for j in range(d):
        while True:
            r = randrange(n)
            if not result[r]: break
        result[r] = 1-2*randrange(2)
    return Zx(result)

def inv_mod_prime(f,p):
    T = Zx.change_ring(Integers(p)).quotient(x^n-1)
    return Zx(lift(1 / T(f)))

def inv_mod_powerof2(f,q):
    assert q.is_power_of(2)
    g = inv_mod_prime(f,2)
    while True:
        r = bal_mod(mul(g,f),q)
        if r == 1: return g
        g = bal_mod(mul(g,2 - r),q)

def keygen():
    f = random_poly(Df)
    while True:
        try:
            fp = inv_mod_prime(f,p)
            fq = inv_mod_powerof2(f,q)
            break
        except:
            f = random_poly(Df)
    g = random_poly(Dg)
    h = bal_mod(p * mul(fq,g),q)
    pub_key = h
    pri_key = [f,fp]
    return pub_key,pri_key

def encrypt(m,h):
    r = random_poly(Dr)
    e = bal_mod(mul(h,r) + m,q)
    return e

if __name__ == '__main__':
    pub_key,pri_key = keygen()
    flag=b'SCTF{***********}'[5:-1]
    m = Zx(list(bin(int(b16encode(flag), 16))[2:]))
    print(m)
    e = encrypt(m,pub_key)
    print('pub_key=')
    print(pub_key)
    print('e=')
    print(e)
#pub_key=
#510*x^108 - 840*x^107 - 926*x^106 - 717*x^105 - 374*x^104 - 986*x^103 + 488*x^102 + 119*x^101 - 247*x^100 + 34*x^99 + 751*x^98 - 44*x^97 - 257*x^96 - 749*x^95 + 648*x^94 - 280*x^93 - 585*x^92 - 347*x^91 + 357*x^90 - 451*x^89 - 15*x^88 + 638*x^87 - 624*x^86 - 458*x^85 + 216*x^84 + 36*x^83 - 199*x^82 - 655*x^81 + 258*x^80 + 845*x^79 + 490*x^78 - 272*x^77 + 279*x^76 + 101*x^75 - 580*x^74 - 461*x^73 - 614*x^72 - 171*x^71 - 1012*x^70 + 71*x^69 - 579*x^68 + 290*x^67 + 597*x^66 + 841*x^65 + 35*x^64 - 545*x^63 + 575*x^62 - 665*x^61 + 304*x^60 - 900*x^59 + 428*x^58 - 992*x^57 - 241*x^56 + 953*x^55 - 784*x^54 - 730*x^53 - 317*x^52 + 108*x^51 + 180*x^50 - 881*x^49 - 943*x^48 + 413*x^47 - 898*x^46 + 453*x^45 - 407*x^44 + 153*x^43 - 932*x^42 + 262*x^41 + 874*x^40 - 7*x^39 - 364*x^38 + 98*x^37 - 130*x^36 + 942*x^35 - 845*x^34 - 890*x^33 + 558*x^32 - 791*x^31 - 654*x^30 - 733*x^29 - 171*x^28 - 182*x^27 + 644*x^26 - 18*x^25 + 776*x^24 + 845*x^23 - 675*x^22 - 741*x^21 - 352*x^20 - 143*x^19 - 351*x^18 - 158*x^17 + 671*x^16 + 609*x^15 - 34*x^14 + 811*x^13 - 674*x^12 + 595*x^11 - 1005*x^10 + 855*x^9 + 831*x^8 + 768*x^7 + 133*x^6 - 436*x^5 + 1016*x^4 + 403*x^3 + 904*x^2 + 874*x + 248
#e=
#-453*x^108 - 304*x^107 - 380*x^106 - 7*x^105 - 657*x^104 - 988*x^103 + 219*x^102 - 167*x^101 - 473*x^100 + 63*x^99 - 60*x^98 + 1014*x^97 - 874*x^96 - 846*x^95 + 604*x^94 - 649*x^93 + 18*x^92 - 458*x^91 + 689*x^90 + 80*x^89 - 439*x^88 + 968*x^87 - 834*x^86 - 967*x^85 - 784*x^84 + 496*x^83 - 883*x^82 + 971*x^81 - 242*x^80 + 956*x^79 - 832*x^78 - 587*x^77 + 525*x^76 + 87*x^75 + 464*x^74 + 661*x^73 - 36*x^72 - 14*x^71 + 940*x^70 - 16*x^69 - 277*x^68 + 899*x^67 - 390*x^66 + 441*x^65 + 246*x^64 + 267*x^63 - 395*x^62 + 185*x^61 + 221*x^60 + 466*x^59 + 249*x^58 + 813*x^57 + 116*x^56 - 100*x^55 + 109*x^54 + 579*x^53 + 151*x^52 + 194*x^51 + 364*x^50 - 413*x^49 + 614*x^48 + 367*x^47 + 758*x^46 + 460*x^45 + 162*x^44 + 837*x^43 + 903*x^42 + 896*x^41 - 747*x^40 + 410*x^39 - 928*x^38 - 230*x^37 + 465*x^36 - 496*x^35 - 568*x^34 + 30*x^33 - 158*x^32 + 687*x^31 - 284*x^30 + 794*x^29 - 606*x^28 + 705*x^27 - 37*x^26 + 926*x^25 - 602*x^24 - 442*x^23 - 523*x^22 - 260*x^21 + 530*x^20 - 796*x^19 + 443*x^18 + 902*x^17 - 210*x^16 + 926*x^15 + 785*x^14 + 440*x^13 - 572*x^12 - 268*x^11 - 217*x^10 + 26*x^9 + 866*x^8 + 19*x^7 + 778*x^6 + 923*x^5 - 197*x^4 - 446*x^3 - 202*x^2 - 353*x - 852