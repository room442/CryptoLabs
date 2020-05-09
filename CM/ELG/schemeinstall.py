import argparse
from sympy import randprime
from random import randint
from util import auto_int


def get_args():
    parser = argparse.ArgumentParser(description='ELG encoder and digital signature generator')

    parser.add_argument("BITS",
                        nargs="?",
                        type=auto_int,
                        default=1024,
                        help="Number of bits, default = 1024")

    parser.add_argument("-f",
                        help="file to save")

    return parser.parse_args()


def gen_elg(filename, bits):
    def gen_p():
        return randprime(2 ** bits, 2 ** (bits + 1))

    def gen_a(p):
        def gen_primitive_root(r):
            a = randint(1, r)
            phi_r = r - 1  # r is prime
            while pow(a, phi_r, r) != 1:  # aways true, as r is prime
                a = randint(1, r)

            return a

        r = randprime(2 ** (bits - 1), p)
        return r, gen_primitive_root(r)

    def gen_x(r):
        return randprime(1, r)  # Maybe x should be big?

    def gen_b(a, x, p):
        return pow(a, x, p)

    p = gen_p()
    r, a = gen_a(p)
    x = gen_x(r)
    b = gen_b(a, x, p)

    try:
        mystr = F"p = \"{hex(p)[2:]}\"\n" \
                F"a = \"{hex(a)[2:]}\"\n" \
                F"x = \"{hex(x)[2:]}\"\n" \
                F"b = \"{hex(b)[2:]}\"\n" \
                F"r = \"{hex(r)[2:]}\"\n"
        with open(filename, "w") as file:
            file.write(mystr)
    except:
        print(F"p = \"{hex(p)[2:]}\"")
        print(F"a = \"{hex(a)[2:]}\"")
        print(F"x = \"{hex(x)[2:]}\"")
        print(F"b = \"{hex(b)[2:]}\"")
        print(F"r = \"{hex(r)[2:]}\"")


if __name__ == '__main__':
    args = get_args()
    gen_elg(args.f, args.BITS)
