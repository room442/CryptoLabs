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

def leinstra_point_double(x, y, p, A):
    # as usial, but also returns lambda -- denom in k
    if x == 0 and y == 1:
        return 0, 1, 1

    k = ((3 * x ** 2 + A) * modinv(2 * y, p)) % p
    x3 = (k ** 2 - 2 * x) % p
    y3 = (k * (x - x3) - y) % p

    return x3, y3, (2 * y)%p


def leinstra_point_add(x1, y1, x2, y2, p, A):
    # as usial, but also returns lambda -- denom in k
    if x1 == 0 and y1 == 1:
        return x2, y2, 1
    if x2 == 0 and y2 == 1:
        return x1, y1, 1
    if x1 == x2 and y1 == y2:
        return leinstra_point_double(x1, y1, p, A)
    if x1 == x2:
        return 0, 1, 1
    k = 1
    k = (((y2 - y1) % p) * modinv(((x2 - x1) % p), p)) % p
    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p

    return x3, y3, (x2 - x1) % p

def leinstra_point_mult(x, y, k, p, A):
    # as usual, but using leinstra_point_add, leinstra_point_double, and returns gcd of denom in k and p
    d = 1
    if k == 0:
        return 0, 0, 1
    if k == 1:
        return x, y, 1
    if k == 2:
        tmp = leinstra_point_double(x, y, p, A)
        return tmp[0], tmp[1], gcd(tmp[2], p)

    qx, qy = 0, 1  # point at inf
    for bit in bin(k)[2:]:
        qx, qy, d = leinstra_point_double(qx, qy, p, A)
        if d != 1:
            return qx, qy, gcd(d, p)
        if bit == "1":
            qx, qy, d = leinstra_point_add(qx, qy, x, y, p, A)
            if d != 1:
                return qx, qy, gcd(d, p)


    return qx, qy, d


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
                    Qix, Qiy, d = leinstra_point_mult(Qix, Qiy, p, n, A)
                    if d != 1:
                        print(F"found d: {hex(d)}")
                        exit(0)
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

