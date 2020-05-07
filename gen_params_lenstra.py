import argparse
from util import auto_int
from sage.all import random_prime


def get_args():
    parser = argparse.ArgumentParser(description='Генерация параметров для алгоритма Леинстры')

    parser.add_argument("BITS",
                        nargs="?",
                        type=auto_int,
                        default=32,
                        help="Биты, по умолчанию 32")

    parser.add_argument("-f",
                        default="lenstra_params.py",
                        help="Файл для сохранения, по умолчанию lenstra_params.py")

    return parser.parse_args()

def gen_factor(filename, bits):

    p = random_prime(2**(bits//2 - 1), 2**(bits//2))
    q = random_prime(2**(bits//2 - 1), 2**(bits//2))
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