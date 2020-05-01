from util import modinv


def point_double(x, y, p, A):
    k = ((3 * x ** 2 + A) * modinv(2 * y, p)) % p
    x3 = (k ** 2 - 2 * x) % p
    y3 = (k * (x - x3) - y) % p

    return x3, y3


def point_add(x1, y1, x2, y2, p, A):
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

    xx, yy = x, y
    mask = bin(k)[2:]
    for i in range(len(mask)):
        xx, yy = point_double(xx, yy, p, A)
        if mask[i] == '1':
            xx, yy = point_add(xx, yy, x, y, p, A)

    return xx, yy

