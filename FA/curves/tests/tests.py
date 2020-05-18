from FA.curves.curve_arith import *
from sage.all import *
import pytest


class TestTransition:

    @pytest.fixture
    def curve(self):
        K = GF(random_prime(1<<64))
        char = K.characteristic()
        E = EllipticCurve(K, [randint(1, char), randint(1, char)])
        return E, K

    def test_affine_to_jacobian_and_back(self, curve):
        E, K = curve
        P = E.random_point()
        x, y = P[0], P[1]
        jx, jy, jz = affine_to_jacobian(x,y)
        nx, ny, _ = affine_from_jacobian(jx, jy, jz, K)
        assert [nx, ny] == [x, y]

    def test_affine_to_jacobian_and_back_inf(self, curve):
        E, K = curve
        P = E(0, 1, 0)
        x, y = P[0], P[1]
        jx, jy,jz = affine_to_jacobian(x,y)
        nx, ny, _ = affine_from_jacobian(jx, jy, jz, K)
        assert [nx, ny] == [x, y]

    def test_affine_to_chudnovskiy_and_back(self, curve):
        E, K = curve
        P = E.random_point()
        x, y = P[0], P[1]
        cx, cy, cz, czz, czzz = affine_to_chudanovskiy(x,y)
        nx, ny, _ = affine_from_chudanovskiy(cx, cy, cz, czz, czzz, K)
        assert [nx, ny] == [x, y]

    def test_affine_to_chudnovskiy_and_back_inf(self, curve):
        E, K = curve
        P = E(0, 1, 0)
        x, y = P[0], P[1]
        cx, cy, cz, czz, czzz = affine_to_chudanovskiy(x,y)
        nx, ny, _ = affine_from_chudanovskiy(cx, cy, cz, czz, czzz, K)
        assert [nx, ny] == [x, y]


