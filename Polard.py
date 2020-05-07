import polard_params as prm
from random import randint
from util import modinv
from sage.all import *

p = int(prm.p, 16)
A = int(prm.A, 16)
B = int(prm.B, 16)
Px = int(prm.Px, 16)
Py = int(prm.Py, 16)
q = int(prm.q, 16)
# d = int(prm.d, 16)  # only for check
Qx = int(prm.Qx, 16)
Qy = int(prm.Qy, 16)

E = EllipticCurve(GF(p), [A, B])
P = E(Px, Py)
Q = E(Qx, Qy)



if __name__ == '__main__':
    L = 32
    Rs = []
    a_arr = []
    b_arr = []
    for j in range(L):
        a = randint(1, q-1)
        b = randint(1, q-1)
        a_arr.append(a)
        b_arr.append(b)
        Rs.append(a*P + b*Q)


    a_ = randint(1, q-1)
    b_ = randint(1, q-1)
    T_ = a_*P + b_*Q
    T__ = T_
    a__, b__ = a_, b_

    while True:

        # 5.1
        j = int(T_[0]) % L
        T_ = T_ + Rs[j]
        a_ = (a_ + a_arr[j]) % q
        b_ = (b_ + b_arr[j]) % q

        # 5.2
        j = int(T__[0]) % L
        T__ = T__ + Rs[j]
        a__ = (a__ + a_arr[j]) % q
        b__ = (b__ + b_arr[j]) % q
        j = int(T__[0]) % L
        T__ = T__ + Rs[j]
        a__ = (a__ + a_arr[j]) % q
        b__ = (b__ + b_arr[j]) % q

        if T_ == T__:
            break

    if a_ == a__ and b_ == b__:
        print("Не удалось разложить число, попробуйте заново")
        exit(-1)
    else:
        d = ((a_-a__) * modinv((b__ - b_)%q, q))%q
    print(hex(d))
