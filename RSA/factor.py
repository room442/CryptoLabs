import argparse
from util import auto_int, modinv
from sympy import isprime
from random import randint
from math import gcd
from RSA.factor_vuln_params import n, e, d


def parse_args():
    parser = argparse.ArgumentParser(
        description='RSA factorisation tool, outputs p,q such as pq = n, and d such as bobkey*d = 1 mod(phi(n))')

    parser.add_argument("-n",
                        type=auto_int,
                        help="Big complex integer")

    parser.add_argument("-e",
                        type=auto_int,
                        help="Alice's open key")

    parser.add_argument("-d",
                        type=auto_int,
                        help="Alice's secret key")

    parser.add_argument("--file",
                        action="store_true",
                        help="Use file params.py")

    parser.add_argument("--bobkey",
                        type=auto_int,
                        default=0,
                        help="Bob's open key")

    return parser.parse_args()


def factorise(n, e, d, bobe):
    N = e * d - 1
    f = 0
    t = 0
    while N % 2 == 0:
        f = f + 1
        N = N // 2
    while True:
        a = randint(2, n - 1)
        l = 0
        b = pow(a, N, n)
        bb = pow(b, 2, n)
        while bb != 1:
            b = bb
            bb = pow(bb, 2, n)
        if b == -1:
            continue
        else:
            t = b
            p = gcd(t + 1, n)
            q = gcd(t - 1, n)
            if p == 1 or q == 1:
                continue
            break

    phi = (p - 1) * (q - 1)

    if bobe != 0:
        bobd = modinv(bobe, phi)
    else:
        bobd = 0

    return p, q, bobd


if __name__ == '__main__':
    args = parse_args()
    if args.file == True:
        p, q, bobd = factorise(int(n, 16), int(e[0],16), int(d[0], 16), int(e[1], 16))
    else:
        p, q, bobd = factorise(args.n, args.e, args.d, args.bobkey)

    print(F"p = {hex(p)[2:]},\nq = {hex(q)[2:]},\nbobd = {hex(bobd)[2:]}")
