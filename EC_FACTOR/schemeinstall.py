import curves_common as crv
import argparse
from util import auto_int
from sympy import randprime
from random import randint

# USES SAGE

def get_args():
    parser = argparse.ArgumentParser(description='Scheme install of factorization tool')

    parser.add_argument("BITS",
                        nargs="?",
                        type=auto_int,
                        default=32,
                        help="Number of bits, default = 32")

    parser.add_argument("-f",
                        help="file to save")

    return parser.parse_args()

def gen_factor(filename, bits):

    p = randprime(2**(bits-1), 2**(bits))
    q = randprime(2**(bits-1), 2**(bits))
    n = p*q


    mystr = F"n = \"{hex(n)[2:]}\"\n" \
            F"p = \"{hex(p)[2:]}\"\n" \
            F"q = \"{hex(q)[2:]}\"\n"
    try:
        with open(filename, "w") as file:
            file.write(mystr)
    except:
        print(mystr)


if __name__ == '__main__':
    args = get_args()
    gen_factor(args.f, args.BITS)