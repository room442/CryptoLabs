import math


def auto_int(x):
    return int(x, 0)


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("modular inverse does not exist")
    else:
        return x % m


def contFrac(x, k=3):
    cf = []
    q = math.floor(x)
    cf.append(q)
    x = x - q
    i = 0
    while x != 0 and i < k:
        q = math.floor(1 / x)
        cf.append(q)
        x = 1 / x - q
        i = i + 1
    return cf
