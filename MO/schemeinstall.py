from util import auto_int
from sympy import randprime
import argparse


def get_args():
    parser = argparse.ArgumentParser(description='MO encoder and digital signature generator')

    parser.add_argument("BITS",
                        nargs="?",
                        type=auto_int,
                        default=1024,
                        help="Number of bits, default = 1024")

    parser.add_argument("-f",
                        help="file to save")

    return parser.parse_args()


def gen_mo(filename, bits):
    r = randprime(2 ** bits, 2 ** (bits + 1))
    try:
        mystr = "r = \"" + str(hex(r)[2:]) + "\""
        with open(filename, "w") as file:
            file.write(mystr)
    except:
        print("r = \"" + str(hex(r)[2:]) + "\"")


if __name__ == '__main__':
    args = get_args()
    gen_elg(args.f, args.BITS)
