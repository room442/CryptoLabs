
from hashlib import sha256
from random import randint
from util import modinv
from math import gcd


def ELGSignAdd(filename, x, a, p, r):
    def gen_k(r):
        k = randint(2, r - 2)
        while gcd(k, r - 1) != 1:
            k = randint(2, r - 2)

        return k

    with open(filename, "rb") as file:
        data = file.read()

    m = int(sha256(data).hexdigest(), 16) % r
    k = gen_k(r)
    w = pow(a, k, p)
    s = ((m - (x * w) % r) * modinv(k, r)) % r

    return w, s


def ELGSignCheck(filename, a, b, p, r, w, s):
    if w >= p:
        return False

    with open(filename, "rb") as file:
        data = file.read()

    m = int(sha256(data).hexdigest(), 16) % r

    return pow(a, m, p) == ((pow(b, w, p) * pow(w, s, p)) % p)