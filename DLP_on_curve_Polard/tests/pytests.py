from sage.all import *
import curves_common as crv

# USES SAGE


def test_add():
    p = random_prime(2**256)
    A = randint(1, p)
    B = randint(1, p)
    E = EllipticCurve(GF(p), [A, B])
    P = E.random_point()
    Q = E.random_point()

    assert crv.point_add(int(P[0]), int(P[1]), int(Q[0]), int(Q[1]), int(p), int(A)) == (int((P+Q)[0]), int((P+Q)[1]))

def test_mult():
    p = random_prime(2**256)
    A = randint(1, p)
    B = randint(1, p)
    k = randint(1, p)
    E = EllipticCurve(GF(p), [A, B])
    P = E.random_point()
    assert crv.point_mult(int(P[0]), int(P[1]), int(k), int(p), int(A)) == (int((k*P)[0]), int((k*P)[1]))
    assert crv.point_mult(int(P[0]), int(P[1]), int(2), int(p), int(A)) == (int((2*P)[0]), int((2*P)[1]))

def test_double():
    p = random_prime(2**256)
    A = randint(1, p)
    B = randint(1, p)
    E = EllipticCurve(GF(p), [A, B])
    P = E.random_point()
    assert crv.point_mult(int(P[0]), int(P[1]), int(2), int(p), int(A)) == (int((2*P)[0]), int((2*P)[1]))
    assert crv.point_add(int(P[0]), int(P[1]), int(P[0]), int(P[1]), int(p), int(A)) == (int((P+P)[0]), int((P+P)[1]))

def test_hand():
    p = 29
    A = 19
    B = 18
    Px, Py = 2, 8
    Qx, Qy = 7, 28
    E = EllipticCurve(GF(p), [A, B])
    P = E(Px, Py)
    Q = E(Qx, Qy)



    assert crv.point_add(int(P[0]), int(P[1]), int(Q[0]), int(Q[1]), int(p), int(A)) == (int((P+Q)[0]), int((P+Q)[1]))