p = 115792089237316193816632940749697632410663669518650351611559539913753142201939
A = 105628356504476664242964797754114282327459123882280107825013854231750340487961
B = 70418904336317776161976531836076188218306082588186738550009236154500226991974
G = [1, 52563562842658272751844618990493989989838273496765630840028383544556360996525]

# find 2g, 7007G + 777000000000000000777G
# method: doubling in Chudnovskiy coord, addition in Chudnovskiy-Jacobian coord

# Chudnovskiy coord same as Jacobian, but with z^2 z^3: (X : Y : Z : Z^2: Z^3)
# Jacobian coord is projective coord, but with c = 2, d = 3.
# Affinian curve: y^2 = x^3 + Ax + B
# Projective (y = Y/Z, x = X/Z): ZY^2 = X^3 + AXZ^2 + BZ^3
# Chudnovskiy (and Jacobian) (y = Y/Z^3, x = X/Z^2): Y^2 = X^3 + AXZ^4 + BZ^6
# 0 in Jacobian is (1 : 1 : 0), in Chudnovsky, resp (1 : 1 : 0 : 0 : 0)


# Elliptic curve is [A, B, K.char)

from util import modinv
import random
from math import sqrt

from sage.all import EllipticCurve, GF


def affine_to_jacobian(x, y):
    if x == 0 and y == 1:
        return 1, 1, 0
    return x, y, 1


def affine_from_jacobian(x, y, z, K):
    if z == 0:
        return 0, 1, 0
    return K((x * K(z ** (-2)))), K(y * K(z ** (-3))), K(z * K(z ** (-1)))


def affine_to_chudanovskiy(x, y):
    if x == 0 and y == 1:
        return 1, 1, 0, 0, 0
    return x, y, 1, 1, 1


def affine_from_chudanovskiy(x, y, z, z2, z3, K):
    if z == 0:
        return 0, 1, 0
    return K((x / z2)), K(y / z3), 1


def jacobian_to_chudanovskiy(x, y, z, K):
    return x, y, z, K(pow(z, 2)), K(pow(z, 3))


def jacobian_from_chudanovskiy(x, y, z, zz, zzz, K=None):
    return x, y, z


def chudanovskiy_to_jacobian(x, y, z, zz, zzz, K=None):
    return jacobian_from_chudanovskiy(x, y, z, zz, zzz, K)


def chudanovskiy_from_jacobian(x, y, z, K):
    return jacobian_to_chudanovskiy(x, y, z, K)


def is_inf(P):  # without sage
    return P == (1, 1, 0, 0, 0) or P == (1, 1, 0)


def is_on_curve(x, y, z, A, B, p, zz=None, zzz=None):  # without sage
    left = (y * y) % p

    if zz is None or zzz is None or (
            (zz == 0 and zzz == 0) or (zz == 1 and zzz == 1)):  # zz and zzz can not be 0 same time
        zz = pow(z, 2, p)
        zzz = pow(z, 3, p)
    z6 = (z * zz * zzz) % p
    # z6 = pow(z, 6, p)
    right = (pow(x, 3, p) + (A * x * pow(zz, 2, p)) % p + (B * z6) % p) % p
    return left == right


def point_double_chu(x, y, z, zz, zzz, A, B, p):  # get and return point in chudnovskiy coord
    if z == 0:
        return x, y, z, zz, zzz
    if not is_on_curve(x, y, z, A, B, p, zz=zz, zzz=zzz): raise ValueError(
        F"point {[x, y, z, zz, zzz]} is not on curve A={A}, B={B} over field of size {p})")

    T1 = pow(x, 2, p)
    T2 = pow(y, 2, p)
    T3 = pow(T2, 2, p)
    C = zz
    # C = pow(z, 2, p)
    S = (2 * (pow((x + T2), 2, p) - T1 - T3)) % p
    M = (3 * T1 + A * pow(C, 2, p)) % p
    F = (pow(M, 2, p) - 2 * S) % p
    x2 = F
    y2 = (M * (S - F) - 8 * T3) % p
    z2 = (pow((y + z), 2, p) - T2 - C) % p

    if not is_on_curve(x2, y2, z2, A, B, p): raise ValueError(
        F"DOUBLING ERROR: point {[x2, y2, z2]} is not on curve A={A}, B={B} over field of size {p}")

    return x2, y2, z2, pow(z2, 2, p), pow(z2, 3, p)


def point_add_jac_chu(px, py, pz, qx, qy, qz, qzz, qzzz, A, B, p):
    if pz == 0:
        return qx, qy, qz
    if qz == 0:
        return px, py, pz
    if px == qx and py == qy and pz == qz:
        return point_double_chu(qx, qy, qz, qzz, qzzz, A, B, p)
    if not is_on_curve(qx, qy, qz, A, B, p): raise ValueError(
        F"point {[qx, qy, qz, qzz, qzzz]} is not on curve A={A}, B={B} over field of size {p}")
    if not is_on_curve(px, py, pz, A, B, p): raise ValueError(
        F"point {[px, py, pz]} is not on curve A={A}, B={B} over field of size {p})")

    T1 = pow(pz, 2, p)
    T2 = qzz
    U1 = (px * T2) % p
    U2 = (qx * T1) % p

    S1 = (py * qz * T2) % p
    S2 = (qy * pz * T1) % p
    H = (U2 - U1) % p
    I = pow(2 * H, 2, p)

    J = (H * I) % p
    r = (2 * (S2 - S1)) % p
    V = (U1 * I) % p

    x = (pow(r, 2, p) - J - 2 * V) % p
    y = ((r * (V - x)) - 2 * S1 * J) % p
    z = ((pow(pz + qz, 2, p) - T1 - T2) * H) % p

    return x, y, z


def point_mult_chu(x, y, z, k, A, B, p):
    qx, qy, qz, qzz, qzzz = 1, 1, 0, 0, 0
    for bit in bin(k)[2:]:
        qx, qy, qz, qzz, qzzz = point_double_chu(qx, qy, qz, qzz, qzzz, A, B, p)
        if bit == "1":
            qx, qy, qz = point_add_jac_chu(x, y, z, qx, qy, qz, qzz, qzzz, A, B, p)
            # add returns Jacobian coord, so we need to find z^2, z^3
            qzz = pow(qz, 2, p)
            qzzz = pow(qz, 3, p)

    return qx, qy, qz


def point_double(PP, E):  # get Sage point, return 2*Sage point
    x, y, z, zz, zzz = affine_to_chudanovskiy(PP[0], PP[1])
    x, y, z, zz, zzz = point_double_chu(x, y, z, zz, zzz, E.a4(), E.a6(), E.base_field().characteristic())
    x, y, z = affine_from_chudanovskiy(x, y, z, zz, zzz, E.base_field())
    return E(x, y, z)


def point_add(PP, QQ, E):
    px, py, pz = affine_to_jacobian(PP[0], PP[1])
    qx, qy, qz, qzz, qzzz = affine_to_chudanovskiy(QQ[0], QQ[1])

    x, y, z = point_add_jac_chu(px, py, pz, qx, qy, qz, qzz, qzzz, E.a4(), E.a6(), E.base_field().characteristic())

    x, y, z = affine_from_jacobian(x, y, z, E.base_field())

    return E(x, y, z)


def point_mult(PP, k, E):
    if k == 0:
        return E(0, 1, 0)
    if k == 1:
        return PP
    if k == 2:
        return point_double(PP, E)

    x, y, z = affine_to_jacobian(PP[0], PP[1])
    x, y, z = point_mult_chu(x, y, z, k, E.a4(), E.a6(), E.base_field().characteristic())
    x, y, z = affine_from_jacobian(x, y, z, E.base_field())

    return E(x, y, z)


def point_mult_cool_algo(PP, k, w, E):
    t = len(bin(k)[2:])
    d = int(t/w)+1
    bk = ("0" * (d*w-t)) + bin(k)[2:]
    windows = []
    Pi = [PP]
    for i in range(d):
        Ki = int(bk[i*w:(i+1)*w], 2)
        windows.append(Ki)
    windows.reverse()
    for i in range(1, d):
        P = Pi[-1]
        for ww in range(w):
            P = point_double(P, E)
        Pi.append(P)

    A = (0, 1, 0)
    B = (0, 1, 0)

    for j in range((2**w)-1, 2, -1):
        for i, win in enumerate(windows):
            if win == j:
                B = point_add(B, Pi[i], E)
        A = point_add(A, B, E)

    return A


def get_random_point(E, P=None):
    if P is None:
        P = (56294930529307888037266989938554520078909974976727867290405186147804672857970,
             40227799284408618946039395270241596338545732655219360714266457471089156305972, 1)
    k = random.randint(0, E[0])

    P = point_mult(P, k, E)

    return P


if __name__ == '__main__':
    E = EllipticCurve(GF(p), [A, B])
    P = E(G[0], G[1])

    rand_P = E.random_point()

    # newR = get_random_point(E)

    print(is_inf(P))
    print(is_on_curve(P, E))
    print(point_double(P, E))
    print(point_add(P, rand_P, E))
    print(point_mult(P, 11, E))
    print(F"New random point {newR} is on curve: {is_on_curve(newR, E)}")




    print(F"old: {point_mult(rand_P, 46237, E)}")
    print(F"new: {point_mult_cool_algo(rand_P, 46237, 4, E)}")