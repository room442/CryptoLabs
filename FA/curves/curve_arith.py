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


# Elliptic curve is [q, A, B]

from util import modinv
import random
from math import sqrt

from sage.all import EllipticCurve, GF



def affine_to_jacobian(x, y, E):
    if x == 0 and y == 1:
        return 1, 1, 0
    return x, y, 1


def affine_from_jacobian(x, y, z, E):
    if z == 0:
        return 0, 1
    z_inv = modinv(z, E[0])
    zz_inv = modinv(pow(z, 2, E[0]), E[0])
    zzz_inv = modinv(pow(z, 3, E[0]), E[0])
    return (x * zz_inv) % E[0], (y * zzz_inv) % E[0], (z * z_inv) % E[0]


def affine_to_chudanovskiy(x, y, E):
    if x == 0 and y == 1:
        return 1, 1, 0, 0, 0
    return x, y, 1, 1, 1


def affine_from_chudanovskiy(x, y, z, z2, z3, E):
    if z == 0:
        return 0, 1
    z_inv = modinv(z, E[0])
    zz_inv = modinv(z2, E[0])
    zzz_inv = modinv(z3, E[0])
    return (x * zz_inv) % E[0], (y * zzz_inv) % E[0], (z * z_inv) % E[0]


def jacobian_to_chudanovskuy(x, y, z, E):
    return x, y, z, pow(z, 2, E[0]), pow(z, 3, E[0])


def jacobian_from_chudanovskiy(x, y, z, zz, zzz, E):
    return x, y, z


def chudanovskiy_to_jacobian(x, y, z, zz, zzz, E):
    return jacobian_from_chudanovskiy(x, y, z, zz, zzz, E)


def chudanovskiy_from_jacobian(x, y, z, E):
    return jacobian_from_chudanovskiy(x, y, z, E)


def is_inf(P):
    return P == (1, 1, 0, 0, 0) or P == (1, 1, 0)


def is_on_curve(P, E):
    left = (P[1] * P[1]) % E[0]
    if len(P) == 3:
        right = ((pow(P[0], 3, E[0])) + (E[1] * P[0] * pow(P[2], 4, E[0])) + (E[2] * pow(P[2], 6, E[0]))) % E[0]
    else:
        right = ((pow(P[0], 3, E[0])) + (E[1] * P[0] * pow(P[3], 2, E[0])) + (E[2] * P[3] * P[4])) % E[0]

    return left == right


def point_double_chu(PP, E):  # get and retruern point in chudnovskiy coord
    if is_inf(PP): return PP
    if not is_on_curve(PP, E): raise ValueError(F"point {PP} is not on curve {E}")

    T1 = (P[0] * P[0]) % E[0]
    T2 = (P[1] * P[1]) % E[0]
    T3 = (T2 * T2) % E[0]
    C = P[2]
    S = (2 * (pow((P[0] + T2), 2, E[0]) - T1 - T3)) % E[0]
    M = (3 * T1 + E[1] * pow(C, 2, E[0])) % E[0]
    F = (pow(M, 2, E[0]) - 2 * S) % E[0]
    x = F
    y = (M * (S - F) - 8 * T3) % E[0]
    z = (pow((P[1] + P[2]), 2, E[0]) - T2 - C) % E[0]

    return x, y, z, pow(z, 2, E[0]), pow(z, 3, E[0])


def point_add_jac_chu(P, Q, E):
    if is_inf(P):
        if len(Q) == 3:
            return Q
        else:
            return jacobian_from_chudanovskiy(Q[0], Q[1], Q[2], Q[3], Q[4], E)
    if is_inf(Q):
        if len(P) == 3:
            return P
        else:
            return jacobian_from_chudanovskiy(P[0], P[1], P[2], P[3], P[4], E)
    if not is_on_curve(Q, E): raise ValueError(F"point {Q} is not on curve {E}")
    if not is_on_curve(P, E): raise ValueError(F"point {P} is not on curve {E}")

    T1 = pow(P[2], 2, E[0])
    T2 = Q[3]
    U1 = (P[0] * T2) % E[0]
    U2 = (Q[0] * T1) % E[0]

    S1 = (P[1] * Q[2] * T2) % E[0]
    S2 = (Q[1] * P[2] * T1) % E[0]
    H = (U2 - U1) % E[0]
    I = pow(2 * H, 2, E[0])

    J = (H * I) % E[0]
    r = (2 * (S2 - S1)) % E[0]
    V = (U1 * I) % E[0]

    x = (pow(r, 2, E[0]) - J - 2 * V) % E[0]
    y = ((r * (V - x)) - 2 * S1 * J) % E[0]
    z = ((pow(P[2] + Q[2], 2, E[0]) - T1 - T2) * H) % E[0]

    return x, y, z


def point_double(PP, E):  # only Chudnovskiy
    P = affine_to_chudanovskiy(PP[0], PP[1], E)
    Q = point_double_chu(P, E)
    return affine_from_chudanovskiy(Q[0], Q[1], Q[2], Q[3], Q[4], E)


# TODO: point add, point mult on digit

def point_add(PP, QQ, E):
    if PP == QQ:
        return point_double(PP, E)
    P = affine_to_jacobian(PP[0], PP[1], E)
    Q = affine_to_chudanovskiy(QQ[0], QQ[1], E)

    res = point_add_jac_chu(P, Q, E)

    return affine_from_jacobian(res[0], res[1], res[2], E)


def point_mult(PP, k, E):
    if k == 0:
        return 0, 1
    if k == 1:
        return PP
    if k == 2:
        return point_double(PP, E)

    P = affine_to_jacobian(PP[0], PP[1], E)
    Q = affine_to_chudanovskiy(PP[0], PP[1], E)
    Q = [0, 1, 0]  # point at inf
    for bit in bin(k)[2:]:
        Q = point_double(Q, E)
        if bit == "1":
            Q = point_add(Q, PP, E)

    return Q

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