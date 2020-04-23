import argparse
import rsa  # for keys
from sympy import randprime, mod_inverse, isprime
from random import randint
from math import sqrt
from decimal import Decimal


def _print_params(filename, e, n, d, p, q, nn, dd, openmode="w", num=0):
    try:
        if num == 0:
            mystr = F"e = \"{hex(e)[2:]}\"\n" \
                    F"n = \"{hex(n)[2:]}\"\n" \
                    F"d = \"{hex(d)[2:]}\"\n" \
                    F"p = \"{hex(p)[2:]}\"\n" \
                    F"q = \"{hex(q)[2:]}\"\n" \
                    F"sign_n = \"{hex(nn)[2:]}\"\n" \
                    F"sign_d = \"{hex(dd)[2:]} \""
        else:
            mystr = F"e_{num} = \"{hex(e)[2:]}\"\n" \
                    F"n_{num} = \"{hex(n)[2:]}\"\n" \
                    F"d_{num} = \"{hex(d)[2:]}\"\n" \
                    F"p_{num} = \"{hex(p)[2:]}\"\n" \
                    F"q_{num} = \"{hex(q)[2:]}\"\n" \
                    F"sign_n_{num} = \"{hex(nn)[2:]}\"\n" \
                    F"sign_d_{num} = \"{hex(dd)[2:]}\""
        with open(filename, openmode) as file:
            file.write("#This file should always be in place\n")
            file.write(mystr)
    except:
        print(F"e_{num} = \"{hex(e)[2:]}\"")
        print(F"n_{num} = \"{hex(n)[2:]}\"")
        print(F"d_{num} = \"{hex(d)[2:]}\"")
        print(F"p_{num} = \"{hex(p)[2:]}\"")
        print(F"q_{num} = \"{hex(q)[2:]}\"")


def _print_arr(filename, name, arr):
    with open(filename, "a") as file:
        file.write(F"{name} = [")
        for elem in arr:
            file.write(F"\"{hex(elem)[2:]}\", ")
        file.write("]\n")


def _getNPQ(bits):
    p = randprime(2 ** ((bits // 2) - 1), 2 ** (bits // 2))
    q = randprime(2 ** ((bits // 2) - 1), 2 ** (bits // 2))
    p, q = max(p, q), min(p, q)
    n = p * q
    return n, p, q


def get_args():
    parser = argparse.ArgumentParser(description='Генерация параметров криптосистем')

    parser.add_argument("BITS",
                        nargs="?",
                        type=int,
                        default=1024,
                        help="Битность числа n=pq, по-умолчанию 1024")

    parser.add_argument("-f",
                        help="Куда сохранять параметры")

    parser.add_argument("--self",
                        action="store_true",
                        help="Генерация при помощи своего алгоритма. Иначе будет использоваться библиотека")

    parser.add_argument("--wiener",
                        action="store_true",
                        help="Параметры, пригодные для атаки Винера")

    parser.add_argument("--special",
                        action="store_true",
                        help="Параметры с маленьким e")

    parser.add_argument("--factor",
                        action="store_true",
                        help="Два набора ключей на одном n")

    parser.add_argument("--elg",
                        action="store_true",
                        help="Параметры для криптосистемы эль-гамаля")

    parser.add_argument("-c", "--clients",
                        type=int,
                        default=3,
                        help="Количество клиентов для атаки на широковещательное сообщение")

    return parser.parse_args()


def gen_rsa(filename, bits):
    exp = 0x10001

    pubkey, privkey = rsa.newkeys(bits, exponent=exp)
    signpubkey, signprivkey = rsa.newkeys(1024, exponent=exp)

    _print_params(filename,
                  exp,
                  pubkey.n,
                  privkey.d,
                  privkey.p,
                  privkey.q,
                  signpubkey.n,
                  signprivkey.d)


def gen_rsa_wiener_vuln(filename, bits):
    n, p, q = _getNPQ(bits)
    n = Decimal(n)
    d = randint(0x10001, int((Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()))
    while True:
        try:
            e = mod_inverse(d, (p - 1) * (q - 1))
        except:
            d = randint(0x10001, int((Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()))
            continue
        break
    n = int(n)
    _print_params(filename,
                  e, n, d, p, q, n, d
                  )


def gen_rsa_self(filename, bits):
    n, p, q = _getNPQ(bits)
    n = Decimal(n)
    d = randint(int((Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()),
                int(n - (Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()))
    while True:
        try:
            e = mod_inverse(d, (p - 1) * (q - 1))
        except:
            d = randint(int((Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()),
                        int(n - (Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()))
            continue
        break
    n = int(n)

    _print_params(filename,
                  e, n, d, p, q, n, d
                  )


def gen_rsa_special_vuln(filename, bits, clientnum):
    n, p, q, d = [], [], [], []
    e = 3

    for _ in range(clientnum):
        while True:
            try:
                nn, pp, qq = _getNPQ(bits)
                dd = mod_inverse(e, (pp - 1) * (qq - 1))
                n.append(nn)
                p.append(pp)
                q.append(qq)
                d.append(dd)
            except:
                continue
            break

    with open(filename, "w") as file:
        file.write(F"e ={e}\n")
    _print_arr(filename, "n", n)
    _print_arr(filename, "d", d)
    _print_arr(filename, "p", p)
    _print_arr(filename, "q", q)
    _print_arr(filename, "sign_n", n)
    _print_arr(filename, "sign_d", d)


def gen_rsa_one_n(filename, bits):
    n, p, q = _getNPQ(bits)
    n = Decimal(n)
    d = randint(int((Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()),
                int(n - (Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()))
    while True:
        try:
            e = mod_inverse(d, (p - 1) * (q - 1))
        except:
            d = randint(int((Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()),
                        int(n - (Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()))
            continue
        break
    dd = randint(int((Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()),
                 int(n - (Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()))
    while True:
        try:
            ee = mod_inverse(dd, (p - 1) * (q - 1))
        except:
            dd = randint(int((Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()),
                         int(n - (Decimal(1) / Decimal(3)) * Decimal(n).sqrt().sqrt()))
            continue
        break
    n = int(n)

    with open(filename, "w") as file:
        pass
    _print_arr(filename, "e", [e, ee])
    with open(filename, "a") as file:
        file.write(F"n = \"{hex(n)[2:]}\"\n")
    _print_arr(filename, "d", [d, dd])
    with open(filename, "a") as file:
        file.write(F"p = \"{hex(p)[2:]}\"\n")
        file.write(F"q = \"{hex(q)[2:]}\"\n")

def gen_elg(filename, bits):
    def gen_p():
        while True:
            p1 = randprime(2**(bits-1), 2**(bits))
            p1 = (339386177002760482600239301413093740958616760302151848390552942930762297295213572171311950930933593543236070519889888679092428618587002337882482460717637418118082916909433900556103056132121618886707585999925527839883535073562715771894677877009039941024040993197552060215414950720782088758245094436639165829439-1)//2
            if isprime(p1*2+1):
                return p1*2+1, p1

    def gen_a(p, r):
        a = randint(1, p)
        while pow(a, 2, p-1) == 1:
            a = randint(1, p)
        return a

    def gen_x(r):
        return randprime(1, r)

    def gen_b(a, x, p):
        return pow(a, x, p)

    p, r = gen_p()
    a = gen_a(p, r)
    x = gen_x(r)
    b = gen_b(a, x, p)

    try:
        mystr = F"p = \"{hex(p)[2:]}\"\n" \
                F"a = \"{hex(a)[2:]}\"\n" \
                F"x = \"{hex(x)[2:]}\"\n" \
                F"b = \"{hex(b)[2:]}\"\n" \
                F"r = \"{hex(r)[2:]}\"\n"
        with open(filename, "w") as file:
            file.write(mystr)
    except:
        print(F"p = \"{hex(p)[2:]}\"")
        print(F"a = \"{hex(a)[2:]}\"")
        print(F"x = \"{hex(x)[2:]}\"")
        print(F"b = \"{hex(b)[2:]}\"")
        print(F"r = \"{hex(r)[2:]}\"")

if __name__ == '__main__':
    args = get_args()
    if args.wiener:
        gen_rsa_wiener_vuln(args.f, args.BITS)
    elif args.special:
        gen_rsa_special_vuln(args.f, args.BITS, args.clients)
    elif args.factor:
        gen_rsa_one_n(args.f, args.BITS)
    elif args.self:
        gen_rsa_self(args.f, args.BITS)
    elif args.elg:
        gen_elg(args.f, args.BITS)
    else:
        gen_rsa(args.f, args.BITS)
