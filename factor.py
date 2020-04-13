from sympy import mod_inverse
from random import randint
from math import gcd
from factor_vuln_params import n, e, d


def auto_int(x):
    return int(x, 0)


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
        bobd = mod_inverse(bobe, phi)
    else:
        bobd = 0

    return p, q, bobd


if __name__ == '__main__':
    p, q, bobd = factorise(int(n, 16), int(e[0], 16), int(d[0], 16), int(e[1], 16))

    print(F"p = {hex(p)[2:]},\nq = {hex(q)[2:]},\nbobd = {hex(bobd)[2:]}")
