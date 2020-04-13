import argparse
from wiener_params import *
import math
from decimal import getcontext, Decimal


def RSAencrypt(m, e, n):
    return pow(m, e, n)


def RSAdecrypt(c, d, n):
    return pow(c, d, n)


def contFrac(a, b, k=3):
    eps = 300
    getcontext().prec = eps

    x = Decimal(a) / Decimal(b)
    cf = [int(x)]
    x = x - int(x)

    for i in range(k):
        a_i = int(Decimal(1) / x)
        x = (Decimal(1) / x) - a_i

        cf.append(a_i)

        if x < Decimal(1) / Decimal(10 ** (eps / 2)):
            break

    return cf


def getPQ(frac):
    P = [frac[0], frac[0] * frac[1] + 1]
    Q = [1, frac[1]]

    for k in range(2, len(frac)):
        P.append(P[k - 1] * frac[k] + P[k - 2])
        Q.append(Q[k - 1] * frac[k] + Q[k - 2])

    return P, Q


def attack(n, e, m):
    frac = contFrac(e, n, int(math.log(n, 2)))
    P, Q = getPQ(frac)
    for i, d in enumerate(Q):
        if RSAencrypt(m, (e * d),
                      n) == m % n:  # Encrypt m with e*d, where d is known. M can be already encrypted, it doesnt metter
            print(F"i = {i}")
            return d
    return None


if __name__ == '__main__':
    print(F"Find d: {hex(attack(int(n, 16), int(e, 16), 0x111111))}")
