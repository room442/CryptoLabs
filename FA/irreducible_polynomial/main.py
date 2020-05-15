from sage.all import *

def check_reduce(F, f):
    x = F.gen(0)
    q = F.characteristic()
    n = f.degree()
    g = pow(x, q, f)
    for i in range(1, n):
        if is_prime(n//i) and GCD(f, g-x) != 1:
            return False
        g = pow(g, q, f)
    if g != x:
        return False
    return True

def getNewPolynomial(F, f):
    # x = polygen(QuotientRing(F, f), 'x')
    # K = x.parent()
    K = QuotientRing(F, f, 'x')
    x = K.gen(0)
    q = F.characteristic()
    n = f.degree()
    while True:
        a = K.random_element()
        r = 1
        ph = K(x) - a
        g = pow(a, q)#%f
        while g != a:
            r = r+1
            ph = ph * (K(x) - g)#%f
            g = pow(g, q)#%f
        if r<n:
            continue
        return F(ph.list())+f



if __name__ == '__main__':
    q = 1511231
    x = polygen(GF(q), 'x')
    F = x.parent()
    f = F(
                  x ** 18 +
        1511126 * x ** 17 +
        5202    * x ** 16 +
        1349663 * x ** 15 +
        502658  * x ** 14 +
        55450   * x ** 13 +
        911133  * x ** 12 +
        396723  * x ** 11 +
        227138  * x ** 10 +
        1346399 * x **  9 +
        252634  * x **  8 +
        1486897 * x **  7 +
        21313   * x **  6 +
        466557  * x **  5 +
        1211991 * x **  4 +
        869175  * x **  3 +
        472027  * x **  2 +
        1265812 * x **  1 +
        793348
    )
    f2 = F(
                  x ** 18 +
        1219501 * x ** 17 +
        764805  * x ** 16 +
        454903  * x ** 15 +
        617833  * x ** 14 +
        211543  * x ** 13 +
        962797  * x ** 12 +
        816764  * x ** 11 +
        577726  * x ** 10 +
        1277309 * x **  9 +
        1032282 * x **  8 +
        1358786 * x **  7 +
        301404  * x **  6 +
        1200672 * x **  5 +
        743242  * x **  4 +
        1238281 * x **  3 +
        802749  * x **  2 +
        1014    * x **  1 +
        669215
    )
    ph = getNewPolynomial(F, f)
    print(F"f = {f} \nis irreducible: {check_reduce(F, f)}")
    print(F"f2 = {f2} \nis irreducible: {check_reduce(F, f2)}")
    print(F"New f = {ph} \nis irreducible: {check_reduce(F, ph)}")