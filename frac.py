import math


def contFrac(x, k=3):
    cf = []
    q = math.floor(x)
    cf.append(q)
    x = x - q
    i = 0
    while x != 0 and i < k:
        q = math.floor(1 / x)
        cf.append(q)
        x = 1 / x - q
        i = i + 1
    return cf

def getPQ(i, frac):

    P = [1, 0]
    Q = [0, 1]

    for j in range(2, i+2):
        P_j = frac[j-1]