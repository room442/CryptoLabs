import math
from decimal import getcontext, Decimal


def contFrac(a, b, k=3):

    eps = 300
    getcontext().prec = eps

    x = Decimal(a)/Decimal(b)
    cf = [int(x)]
    x = x - int(x)

    for i in range(k):
        a_i = int(Decimal(1)/x)
        x = (Decimal(1)/x) - a_i

        cf.append(a_i)

        if x < Decimal(1)/Decimal(10 ** (eps / 2)):
            break

    return cf

def getPQ(i, frac):

    P = [1, 0]
    Q = [0, 1]

    for j in range(2, i+2):
        P_j = frac[j-1]