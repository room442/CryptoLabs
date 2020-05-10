from random import randint
from util import modinv

def MOencrypt(m, k, p):
    if pow(m, k, p) == 1:
        raise Exception("Cant encrypt")
    return pow(m, k, p) % p


def MOdecrypt(c, k, p):
    return MOencrypt(c, k, p)


def MOgetKeys(p):
    while True:
        try:
            e = randint(2, p - 1)
            d = modinv(e, p - 1)
        except:
            continue
        break
    return e, d