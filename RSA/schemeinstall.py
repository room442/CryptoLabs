import argparse
import rsa  # for keys
from util import auto_int, modinv
from sympy import randprime
from random import randint
from math import sqrt


def get_args():
    parser = argparse.ArgumentParser(description='RSA encoder and digital signature generator')

    parser.add_argument("BITS",
                        nargs="?",
                        type=auto_int,
                        default=1024,
                        help="Number of bits, default = 1024")

    parser.add_argument("-f",
                        help="file to save")

    parser.add_argument("--self",
                        action="store_true",
                        help="Use key-generation algorithm insted of rsa lib. Can use params")

    parser.add_argument("--wienner",
                        action="store_true",
                        help="Generate wienner-attack immune params")

    return parser.parse_args()


def gen_rsa(filename, bits):
    exp = 0x10001

    pubkey, privkey = rsa.newkeys(bits, exponent=exp)
    signpubkey, signprivkey = rsa.newkeys(1024, exponent=exp)

    try:
        mystr = F"e = \"{hex(exp)[2:]} \"\n" \
                F"n = \"{hex(pubkey.n)[2:]}\"\n" \
                F"d = \"{hex(privkey.d)[2:]}\"\n" \
                F"p = \"{hex(privkey.p)[2:]}\"\n" \
                F"q = \"{hex(privkey.q)[2:]}\"\n" \
                F"sign_n = \"{hex(signpubkey.n)[2:]}\"\n" \
                F"sign_d = \"{hex(signprivkey.d)[2:]} \""
        with open(filename, "w") as file:
            file.write(mystr)
    except:
        print(F"e = \"{hex(exp)[2:]}\"")
        print(F"n = \"{hex(pubkey.n)[2:]}\"")
        print(F"d = \"{hex(privkey.d)[2:]}\"")
        print(F"p = \"{hex(privkey.p)[2:]}\"")
        print(F"q = \"{hex(privkey.q)[2:]}\"")


def gen_rsa_wiener_vuln(filename, bits):
    p = randprime(2 ** (bits - 1), 2 ** bits)
    q = randprime(2 ** (bits - 1), 2 ** bits)
    n = p * q
    d = randint(0x10001, (1 / 3) * pow(n, 0.25))
    e = modinv(d, (p - 1) * (q - 1))
    try:
        mystr = F"e = \"{hex(e)[2:]} \"\n" \
                F"n = \"{hex(n)[2:]}\"\n" \
                F"d = \"{hex(d)[2:]}\"\n" \
                F"p = \"{hex(p)[2:]}\"\n" \
                F"q = \"{hex(q)[2:]}\"\n" \
                F"sign_n = \"{hex(n)[2:]}\"\n" \
                F"sign_d = \"{hex(d)[2:]} \""
        with open(filename, "w") as file:
            file.write(mystr)
    except:
        print(F"e = \"{hex(e)[2:]}\"")
        print(F"n = \"{hex(n)[2:]}\"")
        print(F"d = \"{hex(d)[2:]}\"")
        print(F"p = \"{hex(p)[2:]}\"")
        print(F"q = \"{hex(q)[2:]}\"")


if __name__ == '__main__':
    args = get_args()
    gen_rsa(args.f, args.BITS)
