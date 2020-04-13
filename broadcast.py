from broadcast_params import *
from sympy.ntheory.modular import crt
from decimal import Decimal


def RSAencrypt(m, e, n):
    return pow(m, e, n)


def RSAdecrypt(c, d, n):
    return pow(c, d, n)


def attack(ms):
    nn = [int(nnn, 16) for nnn in n]
    x = crt(nn, ms)

    xx = (Decimal(x[0]).__pow__(Decimal(1) / Decimal(e)))

    m = int(xx) + 1

    print(hex(m))


if __name__ == '__main__':

    ms = []
    for i, _ in enumerate(n):
        ms.append(RSAencrypt(0x123456789, e, int(n[i], 16)))

    attack(ms)
