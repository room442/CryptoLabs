import gost_params
import argparse
from pygost import gost34112012
from random import randint
import asn1
from sage.all import *


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


def GOSTencodeSign(xq, yq, prime, A, B, xp, yp, q, r, s):
    encoder = asn1.Encoder()

    encoder.start()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.enter(asn1.Numbers.Set)
    encoder.enter(asn1.Numbers.Sequence)

    encoder.write(b'\x80\x06\x07\x00', asn1.Numbers.OctetString)
    encoder.write(b'gostSignKey', asn1.Numbers.UTF8String)

    encoder.enter(asn1.Numbers.Sequence)  # Open key
    encoder.write(xq, asn1.Numbers.Integer)
    encoder.write(yq, asn1.Numbers.Integer)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)  # cryptosystem params

    encoder.enter(asn1.Numbers.Sequence)  # field params
    encoder.write(prime, asn1.Numbers.Integer)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)  # curve params
    encoder.write(A, asn1.Numbers.Integer)
    encoder.write(B, asn1.Numbers.Integer)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)  # points generator
    encoder.write(xp, asn1.Numbers.Integer)
    encoder.write(yp, asn1.Numbers.Integer)
    encoder.leave()

    encoder.write(q, asn1.Numbers.Integer)

    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)  # sign
    encoder.write(r, asn1.Numbers.Integer)
    encoder.write(s, asn1.Numbers.Integer)
    encoder.leave()

    encoder.leave()

    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)  # file params
    encoder.leave()

    encoder.leave()

    return encoder.output()


def GOSTdecodeSign(filename):  # type: (filename) -> (xq, yq, prime, A, B, xp, yp, q, r, s)
    integers = []  # list of integers in ASN.1 file
    with open(filename, "rb") as file:
        data = file.read()
        decoder = asn1.Decoder()
        decoder.start(data)
        integers = parse(decoder, integers)
    return integers


def GOSTSignAdd(filename, d, p, A, B, m, q, xp, yp):
    with open(filename, "rb") as file:
        data = file.read()

    e = int(gost34112012.GOST34112012(data).hexdigest(), 16) % q
    if e == 0:
        e = 1

    while True:
        k = randint(0, q)
        xc, yc = point_mult(xp, yp, k, p, A)
        r = xc % q
        if r == 0:
            continue
        s = (r * d + k * e) % q
        if s == 0:
            continue
        break

    return r, s


def GOSTSignCheck(filename, xq, yq, p, A, B, m, q, xp, yp, r, s):
    if r > q or r < 0 or s > q or s < 0:
        return False

    with open(filename, "rb") as file:
        data = file.read()

    e = int(gost34112012.GOST34112012(data).hexdigest(), 16) % q
    if e == 0:
        e = 1

    v = inverse_mod(e, q)
    z1 = (s * v) % q
    z2 = (-1 * r * v) % q

    xz1p, yz1p = point_mult(xp, yp, z1, p, A)
    xz2q, yz2q = point_mult(xq, yq, z2, p, A)
    xc, yc = point_add(xz1p, yz1p, xz2q, yz2q, p, A)
    R = xc % q

    return r == R


def GOSTgenKeys(p, A, B, m, q, xp, yp):
    d = randint(1, q)
    xq, yq = point_mult(xp, yp, d, p, A)

    return d, xq, yq


A = int(gost_params.a, 10)
B = int(gost_params.b, 10)
p = int(gost_params.p, 10)
q = int(gost_params.r, 10)
x = int(gost_params.x, 10)
y = int(gost_params.y, 10)


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
    d, xq, yq = GOSTgenKeys(p, A, B, q, q, x, y)
    r, s = GOSTSignAdd(filename, d, p, A, B, q, q, x, y)
    with open(filename + ".sign", "wb") as file:
        file.write(
            GOSTencodeSign(xq, yq, p, A, B, x, y, q, r, s)
        )


def GOSTfileCheckSignature(filename, sig_filename):
    xq_decoded, yq_decoded, prime_decoded, A_decoded, B_decoded, xp_decoded, yp_decoded, q_decoded, r_decoded, s_decoded = GOSTdecodeSign(
        sig_filename)
    return GOSTSignCheck(filename, xq_decoded, yq_decoded, prime_decoded, A_decoded, B_decoded, q_decoded, q_decoded,
                         xp_decoded, yp_decoded, r_decoded, s_decoded)


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
    except NameError:
        print("Какая-то ошибка, скорее всего в параметрах.")
