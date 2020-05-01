from pygost import gost34112012
from random import randint
from util import modinv
from math import gcd
from GOST.curves import *


def GOSTSignAdd(filename, d, p, A, B, m, q, xp, yp):
    with open(filename, "rb") as file:
        data = file.read()

    e = int(gost34112012.GOST34112012(data).hexdigest(), 16) % q
    if e == 0:
        e = 1

    while True:
        k = randint(0, q)
        xc, yc = point_mult(xp, yp, k, p, A)
        r = xc % q
        if r == 0:
            continue
        s = (r * d + k * e) % q
        if s == 0:
            continue
        break

    return r, s


def GOSTSignCheck(filename, xq, yq, p, A, B, m, q, xp, yp, r, s):
    if r < q or r < 0 or s < q or s < 0:
        return False

    with open(filename, "rb") as file:
        data = file.read()

    e = int(gost34112012.GOST34112012(data).hexdigest(), 16) % q
    if e == 0:
        e = 1

    v = modinv(e, q)
    z1 = (s * v) % q
    z2 = (-1 * r * v) % q

    xz1p, yz1p = point_mult(xp, yp, z1, p, A)
    xz2q, yz2q = point_mult(xq, yq, z2, p, A)
    xc, yc = point_add(xz1p, yz1p, xz2q, yz2q, p, A)
    R = xc % q

    return r == R

def GOSTgenKeys(p, A, B, m, q, xp, yp):
    d = randint(1, q)
    xq, yq = point_mult(xp, yp, d, p, A)

    return d, xq, yq