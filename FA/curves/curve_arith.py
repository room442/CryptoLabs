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


def affine_to_jacobian(x, y, E):
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
    return P == [1, 1, 0, 0, 0] or P == [1, 1, 0]


def is_on_curve(P, E):
    left = (P[1] * P[1]) % E[0]
    if len(P) == 3:
        right = ((pow(P[0], 3, E[0])) + (E[1] * P[0] * pow(P[2], 4, E[0])) + (E[2] * pow(P[2], 6, E[0]))) % E[0]
    else:
        right = ((pow(P[0], 3, E[0])) + (E[1] * P[0] * pow(P[3], 2, E[0])) + (E[2] * P[3] * P[4])) % E[0]

    return left == right


def point_double(PP, E):  # only Chudnovskiy
    if is_inf(PP): return PP
    if not is_on_curve(PP, E): raise ValueError(F"point {PP} is not on curve {E}")

    P = affine_to_chudanovskiy(PP[0], PP[1], E)

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

    return affine_from_chudanovskiy(x, y, z, pow(z, 2, E[0]), pow(z, 3, E[0]), E)


# TODO: point add, point mult on digit

def point_add(PP, QQ, E):
    if is_inf(PP): return QQ
    if is_inf(QQ): return PP
    if not is_on_curve(QQ, E): raise ValueError(F"point {QQ} is not on curve {E}")
    if not is_on_curve(PP, E): raise ValueError(F"point {PP} is not on curve {E}")
    # P shuld be in Jacobian coord, and Q in Chudnovskiy

    P = affine_to_jacobian(PP[0], PP[1], E)
    Q = affine_to_chudanovskiy(QQ[0], QQ[1], E)

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

    return affine_from_jacobian(x, y, z, E)


if __name__ == '__main__':
    E = [p, A, B]
    P = [G[0], G[1], 1]

    rand_P = [56294930529307888037266989938554520078909974976727867290405186147804672857970, 40227799284408618946039395270241596338545732655219360714266457471089156305972, 1]

    print(is_inf(P))
    print(is_on_curve(P, E))
    print(point_double(P, E))
    print(point_add(P, rand_P, E))
