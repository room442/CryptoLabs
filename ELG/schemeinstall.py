import argparse
from sympy import randprime,  isprime
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
        while True:
            p1 = randprime(2**(bits-1), 2**(bits))
            p1 = (339386177002760482600239301413093740958616760302151848390552942930762297295213572171311950930933593543236070519889888679092428618587002337882482460717637418118082916909433900556103056132121618886707585999925527839883535073562715771894677877009039941024040993197552060215414950720782088758245094436639165829439-1)//2
            if isprime(p1*2+1):
                return p1*2+1, p1

    def gen_a(p, r):
        a = randint(1, p)
        while pow(a, 2, p-1) == 1:
            a = randint(1, p)
        return a

    def gen_x(r):
        return randprime(1, r)

    def gen_b(a, x, p):
        return pow(a, x, p)

    p, r = gen_p()
    a = gen_a(p, r)
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
