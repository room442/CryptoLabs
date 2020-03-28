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

def getPQ(frac):

    P = [frac[0],   frac[0]*frac[1]+1]
    Q = [1,         frac[1]]

    for k in range(2, len(frac)):
        P.append(P[k-1] * frac[k] + P[k-2])
        Q.append(Q[k-1] * frac[k] + Q[k-2])

    return P, Q