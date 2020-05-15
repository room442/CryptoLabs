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

def is_inf(P):
    return P == [1, 1, 0, 0, 0] or P == [1, 1, 0]


def is_on_curve(P, E):
    left = (P[1] * P[1]) % E[0]
    if len(P) == 3:
        right = ((pow(P[0], 3, E[0])) + (E[1] * P[0] * pow(P[2], 4, E[0])) + (E[2] * pow(P[2], 6, E[0]))) % E[0]
    else:
        right = ((pow(P[0], 3, E[0])) + (E[1] * P[0] * pow(P[3], 2, E[0])) + (E[2] * P[3] * P[4])) % E[0]

    return left == right


def point_double(P, E):  # only Chudnovskiy
    if is_inf(P): return P

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

    return [x, y, z, pow(z, 2, E[0]), pow(z, 3, E[0])]

def point_add(P, Q, E):
    if len(P) != 5: # P in Chudnovsky, Q in 
        tmp = P
        P = Q
        Q = tmp
    if is_inf(P): return Q
    if is_inf(Q): return P
    if P == Q or

if __name__ == '__main__':
    E = [p, A, B]
    P = [G[0], G[1], 1]
    print(is_inf(P))
    print(is_on_curve(P, E))
