import gost_params
import argparse
from pygost import gost34112012
from random import randint
import asn1
from sage.all import *


A = int(gost_params.a, 10)
B = int(gost_params.b, 10)
p = int(gost_params.p, 10)
q = int(gost_params.r, 10)
x = int(gost_params.x, 10)
y = int(gost_params.y, 10)


def parse(decoder, integers):  # Функция разбора asn.1 файла, которая просто достает оттуда все числовые значения.
    while not decoder.eof():
        try:
            tag = decoder.peek()

            if tag.nr == asn1.Numbers.Null:
                break

            if tag.typ == asn1.Types.Primitive:  # если тип примитивный
                tag, value = decoder.read()

                if tag.nr == asn1.Numbers.Integer:  # если тип Integer
                    integers.append(value)  # добавить к возвращаемому массиву

            else:
                decoder.enter()  # если тип не примитивный, входим для разбора
                integers = parse(decoder, integers)
                decoder.leave()

        except asn1.Error:
            break

    return integers  # возвращаем все целочисленные значения


def GOSTencodeSign(Q, prime, A, B, P, q, r, s):

    xq = int(Q[0])
    yq = int(Q[1])
    xp = int(P[0])
    yp = int(P[1])
    r = int(r)
    s = int(s)
    q = int(q)
    prime = int(prime)



    encoder = asn1.Encoder()

    encoder.start()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.enter(asn1.Numbers.Set)
    encoder.enter(asn1.Numbers.Sequence)

    encoder.write(b'\x80\x06\x07\x00', asn1.Numbers.OctetString)
    encoder.write(b'gostSignKey', asn1.Numbers.UTF8String)

    encoder.enter(asn1.Numbers.Sequence)  # Открытый ключ
    encoder.write(xq, asn1.Numbers.Integer)
    encoder.write(yq, asn1.Numbers.Integer)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)  # Параметры криптосистемы

    encoder.enter(asn1.Numbers.Sequence)  # Параметры поля
    encoder.write(prime, asn1.Numbers.Integer)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)  # Параметры кривой
    encoder.write(A, asn1.Numbers.Integer)
    encoder.write(B, asn1.Numbers.Integer)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)  # Образующая группы точек
    encoder.write(xp, asn1.Numbers.Integer)
    encoder.write(yp, asn1.Numbers.Integer)
    encoder.leave()

    encoder.write(q, asn1.Numbers.Integer) # Делитель порядка группы точек

    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)  # Подпись
    encoder.write(r, asn1.Numbers.Integer)
    encoder.write(s, asn1.Numbers.Integer)
    encoder.leave()

    encoder.leave()

    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)  # Параметры файла
    encoder.leave()

    encoder.leave()

    return encoder.output()


def GOSTdecodeSign(filename):  # type: (filename) -> (xq, yq, prime, A, B, xp, yp, q, r, s)
    integers = []  # Целочисленные
    with open(filename, "rb") as file:
        data = file.read()
        decoder = asn1.Decoder()
        decoder.start(data)
        integers = parse(decoder, integers)
    return integers


def GOSTSignAdd(filename, d, q, P):
    with open(filename, "rb") as file:
        data = file.read()

    e = int(gost34112012.GOST34112012(data).hexdigest(), 16) % q
    if e == 0:
        e = 1

    while True:
        k = randint(0, q)
        C = k * P
        r = C[0]
        if r == 0:
            continue
        s = (r * d + k * e)
        if s == 0:
            continue
        break

    return r, s


def GOSTSignCheck(filename, Q, E, q, P, r, s):
    if r > q or r < 0 or s > q or s < 0:
        return False

    with open(filename, "rb") as file:
        data = file.read()

    e = int(gost34112012.GOST34112012(data).hexdigest(), 16) % q
    if e == 0:
        e = 1

    v = inverse_mod(e, q)

    C = ((s * v) % q) * P + ((-1 * r * v) % q) * Q
    R = C[0]

    return r == R


def GOSTgenKeys(E, P):
    d = randint(1, q)
    Q = d * P

    return d, Q





def parse_args():
    parser = argparse.ArgumentParser(description='Цифровая подпись по алгоритму ГОСТ 34.11-2018')
    parser.add_argument("FILE",
                        help="Имя файла для подписи")

    parser.add_argument("-s", "--sign",
                        action="store_true",
                        help="Подписать FILE")

    parser.add_argument("-c", "--check",
                        action="store_true",
                        help="Проверить подписи FILE, подпись передается в параметр --sfile")

    parser.add_argument("--sfile",
                        help="Имя файла с подписью")

    return parser.parse_args()


def GOSTfileSign(filename):
    E = EllipticCurve(GF(p), [A, B])
    P = E(x, y)
    d, Q = GOSTgenKeys(E, P)
    r, s = GOSTSignAdd(filename, d, q, P)
    print(F"Информация о подписи:\n"
          F"E = {E}\n"
          F"P = {P}\n"
          F"d = {d}\n"
          F"Q = {Q}\n"
          F"dp = Q = {d*P}\n"
          F"r = {r}\n"
          F"s = {s}\n"
          F"A, B = {A}, {B}\n"
          F"p = {p}")
    with open(filename + ".sign", "wb") as file:
        file.write(
            GOSTencodeSign(Q, p, A, B, P, q, r, s)
        )


def GOSTfileCheckSignature(filename, sig_filename):
    xq_decoded, yq_decoded, prime_decoded, A_decoded, B_decoded, xp_decoded, yp_decoded, q_decoded, r_decoded, s_decoded = GOSTdecodeSign(
        sig_filename)
    E = EllipticCurve(GF(prime_decoded), [A_decoded, B_decoded])
    P = E(xp_decoded, yp_decoded)
    Q = E(xq_decoded, yq_decoded)

    print(F"Информация о подписи:\n"
          F"E = {E}\n"
          F"P = {P}\n"
          F"d -- неизвестно\n"
          F"Q = {Q}\n"
          F"dp -- неизвестно\n"
          F"r = {r_decoded}\n"
          F"s = {s_decoded}\n"
          F"A, B = {A_decoded}, {B_decoded}\n"
          F"p = {prime_decoded}")

    return GOSTSignCheck(filename, Q, E, q_decoded, P, r_decoded, s_decoded)


if __name__ == '__main__':
    args = parse_args()
    try:
        if args.sign:
            GOSTfileSign(args.FILE)
            print("Файл подписан")

        if args.check:
            if args.sfile is None:
                print("Передайте файл с подписью через команду --sfile")
                exit(1)
            else:
                result = GOSTfileCheckSignature(args.FILE, args.sfile)
            print("Sign check: " + str(result))
    except NameError as e:
        print(F"Какая-то ошибка, скорее всего в параметрах. Вот ошибка: {e}")
