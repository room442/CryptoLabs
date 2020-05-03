from util import modinv
from random import randint
from math import sqrt


def point_double(x, y, p, A):
    if x == 0 and y == 1:
        return 0, 1

    k = ((3 * x ** 2 + A) * modinv(2 * y, p)) % p
    x3 = (k ** 2 - 2 * x) % p
    y3 = (k * (x - x3) - y) % p

    return x3, y3


def point_add(x1, y1, x2, y2, p, A):
    if x1 == 0 and y1 == 1:
        return x2, y2
    if x2 == 0 and y2 == 1:
        return x1, y1
    if x1 == x2 and y1 == y2:
        return point_double(x1, y1, p, A)
    k = 1
    k = (((y2 - y1) % p) * modinv(((x2 - x1) % p), p)) % p
    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p

    return x3, y3


def point_mult(x, y, k, p, A):
    if k == 0:
        return 0, 0
    if k == 1:
        return x, y
    if k == 2:
        return point_double(x, y, p, A)

    qx, qy = 0, 1  # point at inf
    for bit in bin(k)[2:]:
        qx, qy = point_double(qx, qy, p, A)
        if bit == "1":
            qx, qy = point_add(qx, qy, x, y, p, A)

    return qx, qy

def get_random_point(p, A, B):
    while True:
        x = randint(0, p)
        y = sqrt(pow(x, 3, p) + (A*x)%p + B)
        if y == int(y):
            break

    return x, int(y)
