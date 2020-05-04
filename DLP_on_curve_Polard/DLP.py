import DLP_on_curve_Polard.params as prm
from random import randint
import curves_common as crv
from util import modinv

p = int(prm.p, 16)
A = int(prm.A, 16)
B = int(prm.B, 16)
Px = int(prm.Px, 16)
Py = int(prm.Py, 16)
q = int(prm.q, 16)
# d = int(prm.d, 16)  # only for check
Qx = int(prm.Qx, 16)
Qy = int(prm.Qy, 16)


def add_mult(_Px, _Py, _Qx, _Qy, _a, _b, _p, _A):
    aPx, aPy = crv.point_mult(_Px, _Py, _a, _p, _A)
    bQx, bQy = crv.point_mult(_Qx, _Qy, _b, _p, _A)
    return crv.point_add(aPx, aPy, bQx, bQy, _p, _A)


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
        Rs.append(add_mult(Px, Py, Qx, Qy, a, b, q, A))


    a_ = randint(1, q-1)
    b_ = randint(1, q-1)
    T_x, T_y = add_mult(Px, Py, Qx, Qy, a_, b_, p, A)
    T__x, T__y = T_x, T_y
    a__, b__ = a_, b_

    while True:

        # 5.1 -- one step
        j = T_x % L
        T_x, T_y = crv.point_add(T_x, T_y, Rs[j][0], Rs[j][1], q, A)
        a_ = (a_ + a_arr[j]) % q
        b_ = (b_ + b_arr[j]) % q

        # 5.2 -- two steps
        j = T__x % L
        T__x, T__y = crv.point_add(T__x, T__y, Rs[j][0], Rs[j][1], q, A)
        a__ = (a__ + a_arr[j]) % q
        b__ = (b__ + b_arr[j]) % q
        j = T__x % L
        T__x, T__y = crv.point_add(T__x, T__y, Rs[j][0], Rs[j][1], q, A)
        a__ = (a__ + a_arr[j]) % q
        b__ = (b__ + b_arr[j]) % q

        if T_x == T__x and T_y == T__y:
            break


    if a_ == a__ and b_ == b__:
        print("oooops")
    else:
        d = ((a_-a__) * modinv(b__ - b_, q))%q
        print(d)
