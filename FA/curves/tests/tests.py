from FA.curves.curve_arith import *
from sage.all import *
import pytest


@pytest.fixture
def curve():
    K = GF(random_prime(1 << 64))
    char = K.characteristic()
    E = EllipticCurve(K, [randint(1, char), randint(1, char)])
    return E, K


class TestTransition:

    def test_affine_to_jacobian_and_back(self, curve):
        E, K = curve
        P = E.random_point()
        x, y = P[0], P[1]
        jx, jy, jz = affine_to_jacobian(x, y)
        nx, ny, _ = affine_from_jacobian(jx, jy, jz, K)
        assert [nx, ny] == [x, y]

    def test_affine_to_jacobian_and_back_inf(self, curve):
        E, K = curve
        P = E(0, 1, 0)
        x, y = P[0], P[1]
        jx, jy, jz = affine_to_jacobian(x, y)
        nx, ny, _ = affine_from_jacobian(jx, jy, jz, K)
        assert [nx, ny] == [x, y]

    def test_affine_to_chudnovskiy_and_back(self, curve):
        E, K = curve
        P = E.random_point()
        x, y = P[0], P[1]
        cx, cy, cz, czz, czzz = affine_to_chudanovskiy(x, y)
        nx, ny, _ = affine_from_chudanovskiy(cx, cy, cz, czz, czzz, K)
        assert [nx, ny] == [x, y]

    def test_affine_to_chudnovskiy_and_back_inf(self, curve):
        E, K = curve
        P = E(0, 1, 0)
        x, y = P[0], P[1]
        cx, cy, cz, czz, czzz = affine_to_chudanovskiy(x, y)
        nx, ny, _ = affine_from_chudanovskiy(cx, cy, cz, czz, czzz, K)
        assert [nx, ny] == [x, y]

    def test_jacobian_to_chudnovskiy_and_back(self, curve):
        E, K = curve
        P = E.random_point()
        x, y, z = P[0], P[1], P[2]
        cx, cy, cz, czz, czzz = jacobian_to_chudanovskiy(x, y, z, K)
        jx, jy, jz = jacobian_from_chudanovskiy(cx, cy, cz, czz, czz, K)
        assert [jx, jy, jz] == [x, y, z]

    def test_jacobian_to_chudnovskiy_and_back_inf(self, curve):
        E, K = curve
        P = E(0, 1, 0)
        x, y, z = P[0], P[1], P[2]
        cx, cy, cz, czz, czzz = jacobian_to_chudanovskiy(x, y, z, K)
        jx, jy, jz = jacobian_from_chudanovskiy(cx, cy, cz, czz, czz, K)
        assert [jx, jy, jz] == [x, y, z]


class TestArith:

    def test_addition(self, curve):
        E, K = curve
        P = E.random_point()
        Q = E.random_point()
        orig = P + Q
        result = point_add(P, Q, E)
        assert [result[0], result[1], result[2]] == [orig[0], orig[1], orig[2]]

    def test_little_doubling(self):
        E = EllipticCurve(GF(5), [1, 2])
        P = E.points()[1]
        orig = 2 * P
        result = point_double(P, E)
        assert [result[0], result[1], result[2]] == [orig[0], orig[1], orig[2]]

    def test_little_doubling_2(self):
        E = EllipticCurve(GF(5), [2, 4])
        P = E.points()[1]
        orig = 2 * P
        result = point_double(P, E)
        assert [result[0], result[1], result[2]] == [orig[0], orig[1], orig[2]]

    def test_doubling(self, curve):
        E, K = curve
        P = E.random_point()
        orig = 2 * P
        result = point_double(P, E)
        assert [result[0], result[1], result[2]] == [orig[0], orig[1], orig[2]]

    def test_multipling(self, curve):
        E, K = curve
        P = E.random_point()
        k = randint(1, K.characteristic())
        orig = k * P
        result = point_mult(P, k, E)
        assert [result[0], result[1], result[2]] == [orig[0], orig[1], orig[2]]

    def test_little_multipling_cool(self):
        E = EllipticCurve(GF(5), [2, 4])
        P = E.points()[1]
        k = randint(3, E.base_field().characteristic())
        orig = k * P
        result = point_mult_cool_algo(P, k, 4, E)
        assert [result[0], result[1], result[2]] == [orig[0], orig[1], orig[2]]

    def test_multipling_cool(self, curve):
        E, K = curve
        P = E.random_point()
        k = randint(3, K.characteristic())
        orig = k * P
        result = point_mult_cool_algo(P, k, 4, E)
        assert [result[0], result[1], result[2]] == [orig[0], orig[1], orig[2]]


def test_isOnCurve_true(curve):
    E, K = curve
    P = E.random_point()
    assert is_on_curve(P[0], P[1], P[2], E.a4(), E.a6(), K.characteristic()) == True


def test_isOnCurve_false(curve):
    E, K = curve
    while True:
        P = (randint(1, K.characteristic()), randint(1, K.characteristic()), 1)
        try:
            E(P[0], P[1], P[2])
        except TypeError:
            break
    assert is_on_curve(P[0], P[1], P[2], E.a4(), E.a6(), K.characteristic(), E) == False


def test_isOnCurve_random(curve):
    E, K = curve
    P = (randint(1, K.characteristic()), randint(1, K.characteristic()), 1)
    try:
        E(P[0], P[1], P[2])
        result = True
    except TypeError:
        result = False
    assert is_on_curve(P[0], P[1], P[2], E.a4(), E.a6(), K.characteristic(), E) == False
