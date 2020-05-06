import time
from sympy import nextprime, gcd # you can implement this function by yours hand and miller-rabin algo
from params import n
import argparse
from random import randint
from math import log2
import curves_common as crv
from util import modinv

N = int(n, 16)

def parse_args():
    parser = argparse.ArgumentParser(description='factorization tool')
    parser.add_argument("-m",
                        type=int,
                        default=10000,
                        help="Number of primes for factorization (Default = 10000)")
    return parser.parse_args()

def get_primes(n):
    primes = []
    print(F"Generating {n} primes")
    with open("primes.txt", "r") as f:
        print("Open file, reading")
        start = time.time()
        p = 0
        for line in f:
            primes.append(int(line))
            p = p+1
            if p >= n:
                break
        print(F"Close file, time = {time.time()-start}")

    while len(primes) < n:
        primes.append(nextprime(primes[-1]))

    return primes


def factor(n, primes):
    iter = 1
    while True:
        print(".", end="")
        if iter%100 == 0:
            print()
        Qx, Qy = randint(1, n-1), randint(1, n-1) # we can choose random curve, so there is no need for choosing curve
                                                  # and finding point, we can generate point and the curve
        A = randint(1, n-1)
        B = (Qy*Qy - Qx * Qx * Qx - A * Qx) % n
        i = 0
        Qix, Qiy = Qx, Qy
        try:
            for p in primes:
                ai = int(0.5 * log2(n)//log2(p))
                for j in range(ai):
                    Qix, Qiy = crv.point_mult(Qix, Qiy, p, n, A)
        except Exception as e:
            _, g = e.args
            return g
        iter = iter+1





if __name__ == '__main__':
    args = parse_args()
    start = time.time()
    p = factor(N, get_primes(args.m))
    end = time.time()
    print(F"\nFound p: {hex(p)}, q: {hex(N//p)}, time: {end-start}s")

