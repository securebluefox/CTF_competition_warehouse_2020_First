#!/usr/bin/env sage
from sage.all import *
from threshold import set_threshold
import random

FLAG = open("/flag", "r").read()


def launch_attack(P, Q, p):
    E = P.curve()
    Eqp = EllipticCurve(Qp(p, 8), [ZZ(t) for t in E.a_invariants()])

    P_Qps = Eqp.lift_x(ZZ(P.xy()[0]), all=True)
    for P_Qp in P_Qps:
        if GF(p)(P_Qp.xy()[1]) == P.xy()[1]:
            break

    Q_Qps = Eqp.lift_x(ZZ(Q.xy()[0]), all=True)
    for Q_Qp in Q_Qps:
        if GF(p)(Q_Qp.xy()[1]) == Q.xy()[1]:
            break

    p_times_P = p * P_Qp
    p_times_Q = p * Q_Qp

    x_P, y_P = p_times_P.xy()
    x_Q, y_Q = p_times_Q.xy()

    phi_P = -(x_P / y_P)
    phi_Q = -(x_Q / y_Q)
    k = phi_Q / phi_P

    return ZZ(k) % p


def attack(E, P, Q):
    private_key = launch_attack(P, Q, E.order())
    return private_key * P == Q


def input_int(msg):
    s = input(msg)
    return int(s)


def curve_agreement(threshold):
    print("Give me the coefficients of your curve in the form of y^2 = x^3 + ax + b mod p with p greater than %d:" % threshold)
    a = input_int("\ta = ")
    b = input_int("\tb = ")
    p = input_int("\tp = ")
    try:
        E = EllipticCurve(GF(p), [a, b])
        if p >= threshold and E.order() == p:
            P = random.choice(E.gens())
            print("Deal! Here is the generator: (%s, %s)" % (P.xy()[0], P.xy()[1]))
            return E, P
        else:
            raise ValueError
    except Exception:
        print("I don't like your curve. See you next time!")
        exit()


def receive_publickey(E):
    print("Send me your public key in the form of (x, y):")
    x = input_int("\tx = ")
    y = input_int("\ty = ")
    try:
        Q = E(x, y)
        return Q
    except TypeError:
        print("Your public key is invalid.")
        exit()


def banner():
    with open("/banner", "r") as f:
        print(f.read())


def main():
    banner()
    threshold = set_threshold()
    E, P = curve_agreement(threshold)
    Q = receive_publickey(E)
    if attack(E, P, Q):
        print("I know your private key. It's not safe. No answer :-)")
    else:
        print("Here is the answer: %s" % FLAG)


if __name__ == "__main__":
    main()
