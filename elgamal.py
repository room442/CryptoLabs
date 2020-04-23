import asn1
from hashlib import sha256
from random import randint
from math import gcd
from sympy import mod_inverse
import sys

from elg_params import *


def ELGSignAdd(filename, x, a, p, r):
    def gen_k(r):
        k = randint(2, r - 2)
        while gcd(k, r - 1) != 1:
            k = randint(2, r - 2)

        return k

    with open(filename, "rb") as file:
        data = file.read()

    m = int(sha256(data).hexdigest(), 16) % r
    k = gen_k(r)
    w = pow(a, k, p)
    s = ((m - (x * w) % r) * mod_inverse(k, r)) % r

    return w, s


def ELGSignCheck(filename, a, b, p, r, w, s):
    if w >= p:
        return False

    with open(filename, "rb") as file:
        data = file.read()

    m = int(sha256(data).hexdigest(), 16) % r

    return pow(a, m, p) == ((pow(b, w, p) * pow(w, s, p)) % p)

def parse(decoder, integers): # Функция разбора asn.1 файла, которая просто достает оттуда все числовые значения.
    while not decoder.eof():
        try:
            tag = decoder.peek()

            if tag.nr == asn1.Numbers.Null:
                break

            if tag.typ == asn1.Types.Primitive: #если тип примитивный
                tag, value = decoder.read()

                if tag.nr == asn1.Numbers.Integer: #если тип Integer
                    integers.append(value) #добавить к возвращаемому массиву

            else:
                decoder.enter() #если тип не примитивный, входим для разбора
                integers = parse(decoder, integers)
                decoder.leave()

        except asn1.Error:
            break

    return integers #возвращаем все целочисленные значения


def ELGencodeSign(
        prime,  # p
        r,  # r
        generator,  # a
        w,
        s,
        b
):
    encoder = asn1.Encoder()

    encoder.start()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.enter(asn1.Numbers.Set)
    encoder.enter(asn1.Numbers.Sequence)

    encoder.write(b'\x80\x06', asn1.Numbers.OctetString)
    # encoder.write(b'\x02\x00', asn1.Numbers.OctetString)
    encoder.write(b'ELG Sign', asn1.Numbers.UTF8String)

    encoder.enter(asn1.Numbers.Sequence)
    encoder.write(b, asn1.Numbers.Integer)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.write(prime, asn1.Numbers.Integer)
    encoder.write(r, asn1.Numbers.Integer)
    encoder.write(generator, asn1.Numbers.Integer)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.write(w, asn1.Numbers.Integer)
    encoder.write(s, asn1.Numbers.Integer)
    encoder.leave()

    encoder.leave()

    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.leave()

    encoder.leave()

    return encoder.output()


def ELGdecodeSign(filename):  # type: (filename) -> (b, p, r, a, w, s)
    integers = []  # list of integers in ASN.1 file
    with open(filename, "rb") as file:
        data = file.read()
        decoder = asn1.Decoder()
        decoder.start(data)
        integers = parse(decoder, integers)
    return integers



def ELGfileSign(filename):
    w, s = ELGSignAdd(
        filename,
        int(x, 16),
        int(a, 16),
        int(p, 16),
        int(r, 16)
    )
    with open(filename + ".sign", "wb") as file:
        file.write(
            ELGencodeSign(
                int(p, 16),
                int(r, 16),
                int(a, 16),
                w,
                s,
                int(b, 16)
            )
        )

def ELGfileCheckSignature(filename, sig_filename):
    b, p, r, a, w, s = ELGdecodeSign(sig_filename)

    return ELGSignCheck(
        filename,
        a,
        b,
        p,
        r,
        w,
        s
    )

if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("sign.py -[sc] filename [signfile]")
    if sys.argv[1] == "-s":
        ELGfileSign(sys.argv[2])
    elif sys.argv[1] == "-c":
        print(F"result = {ELGfileCheckSignature(sys.argv[2], sys.argv[3])}")