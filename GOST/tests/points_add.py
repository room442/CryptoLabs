import curves_common as crv
from sage.all import *
import GOST.params as prm

"""USING SAGE"""

a = int(prm.a, 10)
b = int(prm.b, 10)
p = int(prm.p, 10)
r = int(prm.r, 10)
x = int(prm.x, 10)
y = int(prm.y, 10)

def double():
    print("\n======*****======doubling======*****======\b")
    print(F"my: {crv.point_double(x, y, p, a)}")
    print(F"sage: {2*EllipticCurve(GF(p), [a, b])(x, y)}")

def add():
    print("\n======*****======add======*****======\n")
    E = EllipticCurve(GF(p), [a,b])
    P, Q = E.random_point(), E.random_point()
    print(F"my: {crv.point_add(int(P[0]), int(P[1]), int(Q[0]), int(Q[1]), p, a)}")
    print(F"sage: {P+Q}")

if __name__ == '__main__':
    double()
    add()
