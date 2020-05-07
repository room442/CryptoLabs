import time
import lenstra_params as prm
import argparse
from random import randint
from math import log2
from sage.all import next_prime

N = int(prm.n, 16)


def modular_inv(a, b):
    if b == 0:
        return 1, 0, a
    q, r = divmod(a, b)
    x, y, g = modular_inv(b, r)
    return y, x - q * y, g


def parse_args():
    parser = argparse.ArgumentParser(description='factorization tool')
    parser.add_argument("-m",
                        type=int,
                        default=250,
                        help="Number of primes for factorization (Default = 250)")
    return parser.parse_args()


def get_primes(n):
    primes = [2]

    while len(primes) < n:
        primes.append(next_prime(primes[-1]))

    return primes


def dbl(P, p, A):
    if P == [0, 1]:
        return 0, 1

    num = (3 * P[0] ** 2 + A) % p
    denum = (2 * P[1]) % p
    inv, _, g = modular_inv(denum, p)
    if g > 1:
        raise Exception(g)
    k = (num * inv) % p
    x3 = (k ** 2 - 2 * P[0]) % p
    y3 = (k * (P[0] - x3) - P[1]) % p
    res = [x3, y3]

    return res


def add(P, Q, p, A):
    if P == [0, 1]:
        return Q
    if Q == [0, 1]:
        return P
    if P == Q:
        return dbl(P, p, A)
    if P[0] == Q[0]:
        return 0, 1

    num = (Q[1] - P[1]) % p
    denum = (Q[0] - P[0]) % p
    inv, _, g = modular_inv(denum, p)
    if g > 1:
        raise Exception(g)

    k = (num * inv) % p
    x3 = (k ** 2 - P[0] - Q[0]) % p
    y3 = (k * (P[0] - x3) - P[1]) % p

    res = [x3, y3]

    return res


def mult(P, k, p, A):
    if k == 0:
        return [0, 0]
    if k == 1:
        return P
    if k == 2:
        return dbl(P, p, A)

    Q = [0, 1]
    for bit in bin(k)[2:]:
        qx, qy = dbl(Q, p, A)
        if bit == "1":
            qx, qy = add(Q, P, p, A)

    res = [qx, qy]

    return res


def factor(n, primes):
    while True:

        Q = randint(1, n - 1), randint(1, n - 1)
        A = randint(1, n - 1)
        B = int(Q[1] * Q[1] - Q[0] * Q[0] * Q[0] - A * Q[0]) % int(n)
        i = 0
        Qi = Q
        for p in primes:
            ai = int(float(0.5) * int(log2(n) // log2(p)))
            for j in range(ai):
                try:
                    Qi = mult(Qi, p, n, A)
                except Exception as e:
                    return e.args[0]


if __name__ == '__main__':
    args = parse_args()
    start = time.time()
    p = factor(N, get_primes(args.m))
    end = time.time()
    print(F"Нашли p: {hex(p)}, q: {hex(N // p)}, time: {end - start}s")
