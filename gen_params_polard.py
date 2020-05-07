import curves_common as crv
import argparse
from util import auto_int
from sympy import randprime
from random import randint
from sage.all import *


def get_args():
    parser = argparse.ArgumentParser(description='Генерация параметров для алгоритма Поларда')

    parser.add_argument("BITS",
                        nargs="?",
                        type=auto_int,
                        default=32,
                        help="Биты, по умолчанию 32")

    parser.add_argument("-f",
                        default="polard_params.py",
                        help="Файл для сохранения параметров, по-умолчанию polad_params.py")

    return parser.parse_args()

def gen_polard(filename, bits):
    p = randprime(2**bits, 2**(bits+1))
    A = randint(1, p)
    B = randint(1, p)
    E = EllipticCurve(GF(p), [A, B])
    E_order = int(E.order())
    orders = factor(E_order)
    q = int(orders[-1][0])
    while True:
        P = (E_order//q)*E.random_point()
        if q*P == E(0, 1, 0) and (q-1)*P != E(0, 1, 0):
            break
    d = randint(1, q)
    Q = d*P


    mystr = F"p = \"{hex(p)[2:]}\"\n" \
            F"A = \"{hex(A)[2:]}\"\n" \
            F"B = \"{hex(B)[2:]}\"\n" \
            F"Px = \"{hex(P[0])[2:]}\"\n" \
            F"Py = \"{hex(P[1])[2:]}\"\n" \
            F"q = \"{hex(q)[2:]}\"\n" \
            F"d = \"{hex(d)[2:]}\"\n" \
            F"Qx = \"{hex(Q[0])[2:]}\"\n" \
            F"Qy = \"{hex(Q[1])[2:]}\"\n"
    try:
        with open(filename, "w") as file:
            file.write(mystr)
    except:
        print(mystr)


if __name__ == '__main__':
    args = get_args()
    gen_polard(args.f, args.BITS)