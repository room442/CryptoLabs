from broadcast_params import *
from sympy.ntheory.modular import crt
from decimal import Decimal
from aes_common import AES
from Crypto.Random import get_random_bytes


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
    #FIXME: не работает на больших числах (порядка 256 бит)


    # sec = get_random_bytes(AES.key_size[-1])
    # print(F"sec: {sec}")
    for i, _ in enumerate(n):
        # ms.append(RSAencrypt(int.from_bytes(sec, "big"), e, int(n[i], 16)))
        ms.append(RSAencrypt(0x123456789, e, int(n[i], 16)))

    attack(ms)
