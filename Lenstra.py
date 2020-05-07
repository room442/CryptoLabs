import time
from lenstra_params import n
import argparse
from random import randint
from math import log2
from sage.all import *

N = int(n, 16)


def parse_args():
    parser = argparse.ArgumentParser(description='factorization tool')
    parser.add_argument("-m",
                        type=int,
                        default=10000,
                        help="Number of primes for factorization (Default = 10000)")
    return parser.parse_args()


def get_primes(n):
    primes = [2]

    while len(primes) < n:
        primes.append(next_prime(n))

    return primes


def factor(n, primes):
    iter = 1
    while True:

        Qx, Qy = randint(1, n - 1), randint(1,n - 1)  # we can choose random curve, so there is no need for choosing curve
                                                      # and finding point, we can generate point and the curve
        A = randint(1, n - 1)
        B = (Qy * Qy - Qx * Qx * Qx - A * Qx) % n
        i = 0
        Qix, Qiy = Qx, Qy
        try:
            for p in primes:
                ai = int(0.5 * log2(n) // log2(p))
                for j in range(ai):
                    Qix, Qiy = crv.point_mult(Qix, Qiy, p, n, A)
        except Exception as e:
            _, g = e.args
            return g
        iter = iter + 1


if __name__ == '__main__':
    args = parse_args()
    start = time.time()
    p = factor(N, get_primes(args.m))
    end = time.time()
    print(F"\nFound p: {hex(p)}, q: {hex(N // p)}, time: {end - start}s")
