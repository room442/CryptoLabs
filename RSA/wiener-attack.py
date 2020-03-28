import math
from util import auto_int
from frac import contFrac, getPQ
import argparse
from RSA.crypto import RSAencrypt
from RSA.wiener_vuln import *


def get_args():
    parser = argparse.ArgumentParser(description='Wiener attack')

    parser.add_argument("-n",
                        type=auto_int,
                        help="Big number, such as n = pq, where p,q is primes")

    parser.add_argument("-e",
                        type=auto_int,
                        help="Open key")

    parser.add_argument("--file",
                        action="store_true",
                        help="Use wiener_vuln.py for params")

    return parser.parse_args()


def attack(n, e, m):
    frac = contFrac(e, n, int(math.log(n, 2)))
    P, Q = getPQ(frac)
    for i, d in enumerate(Q):
        if RSAencrypt(m, (e * d), n) == m % n: # Encrypt m with e*d, where d is known. M can be already encrypted, it doesnt metter
            print(F"i = {i}")
            return d


if __name__ == '__main__':
    args = get_args()
    if args.file:
        attack(n, e, 0x111111)
    else:
        print(attack(args.n, args.e, 0x111111))
