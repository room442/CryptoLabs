import GOST.curves as crv
from sage.all import *
import GOST.params as prm
from random import randint

a = int(prm.a, 10)
b = int(prm.b, 10)
p = int(prm.p, 10)
r = int(prm.r, 10)
x = int(prm.x, 10)
y = int(prm.y, 10)

def mult():
    k = randint(1, r)
    E = EllipticCurve(GF(p), [a, b])
    P = E(x, y)
    print(F"my = {crv.point_mult(x, y, k, p, a)}")
    print(F"sage = {k*P}")

if __name__ == '__main__':
    mult()
