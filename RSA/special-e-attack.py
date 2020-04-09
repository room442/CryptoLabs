import argparse
from util import auto_int
from RSA.special_vuln_params import *
from RSA.crypto import RSAencrypt, RSAdecrypt
from sympy.ntheory.modular import crt
from decimal import Decimal

'''
Will use file special_vuln_params.py
'''


def get_args():
    parser = argparse.ArgumentParser(description='Attack on broadcast message with small e')

    return parser.parse_args()


def attack(ms):
    nn = [int(nnn, 16) for nnn in n]
    x = crt(nn, ms)

    xx = (Decimal(x[0]).__pow__(Decimal(1) / Decimal(e)))

    m = int(xx) + 1

    print(hex(m))


if __name__ == '__main__':
    # Вот тут можно добавить файл, хотя хз красиво ли это или лучше все выносить в мейн, но пока что мне лень

    ms = []
    for i, _ in enumerate(n):
        ms.append(RSAencrypt(0x123456789, e, int(n[i], 16)))

    attack(ms)
