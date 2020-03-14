# -*- coding: UTF-8 -*-

import asn1


def RSAencode(
        n,
        e,
        c,  # encrypted aes256 key
        len,
        encrypted
):
    encoder = asn1.Encoder()
    encoder.start()

    encoder.enter(asn1.Numbers.Sequence)  # Start of sequence_1 -- main sequence of metadata
    encoder.enter(asn1.Numbers.Set)  # Start of set_1 -- set of RSA keys
    encoder.enter(asn1.Numbers.Sequence)  # Start of sequence_2 -- first RSA key

    encoder.write(b'\x00\x01', asn1.Numbers.OctetString)  # RSA identifier
    encoder.write(b'\x0C\x00', asn1.Numbers.UTF8String)  # ID of the key (empty)

    encoder.enter(asn1.Numbers.Sequence)  # Start of sequence_3 -- sequence of e and n of RSA
    encoder.write(n, asn1.Numbers.Integer)
    encoder.write(e, asn1.Numbers.Integer)
    encoder.leave()  # End of sequence_3

    encoder.enter(
        asn1.Numbers.Sequence)  # Cryptographic parameters, not used in RSA, because parameter n is a part of open key
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)  # Start of sequence_4 -- sequence of RSA encrypted data
    encoder.write(c, asn1.Numbers.Integer)
    encoder.leave()

    encoder.leave()  # End of sequence_2
    encoder.leave()  # End of set_1

    encoder.enter(asn1.Numbers.Sequence)  # Start of sequence_5 -- sequence of additional data
    encoder.write(b'\x10\x82', asn1.Numbers.OctetString)  # AES CBC identifier
    encoder.write(len, asn1.Numbers.Integer)  # len of the ciphertext
    encoder.leave()

    encoder.leave()  # End of sequence_1

    encoder.write(encrypted)

    return encoder.output()


def RSAdecode(filename):  # type: (filename) -> (n, e, c, ciphertext)
    integers = []  # list of integers in ASN.1 file
    with open(filename, "rb") as file:
        data = file.read()
        decoder = asn1.Decoder()
        decoder.start(data)
        integers = parse(decoder, integers)
        cipher = data[-integers[-1]:]  # get last integrs[last] symbols, this is ciphertext
    return integers[0], integers[1], integers[2], cipher


def RSAencodeSign(
        n,
        e,
        sign
):
    encoder = asn1.Encoder()

    encoder.start()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.enter(asn1.Numbers.Set)
    encoder.enter(asn1.Numbers.Sequence)

    encoder.write(b'\x00\x40', asn1.Numbers.OctetString)
    encoder.write(b'\x0C\x00', asn1.Numbers.UTF8String)

    encoder.enter(asn1.Numbers.Sequence)
    encoder.write(n, asn1.Numbers.Integer)
    encoder.write(e, asn1.Numbers.Integer)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.write(sign, asn1.Numbers.Integer)
    encoder.leave()

    encoder.leave()

    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.leave()

    encoder.leave()

    return encoder.output()


def RSAdecodeSign(filename):  # type: (filename) -> (n, sign)
    integers = []  # list of integers in ASN.1 file
    with open(filename, "rb") as file:
        data = file.read()
        decoder = asn1.Decoder()
        decoder.start(data)
        integers = parse(decoder, integers)
    return integers[0], integers[2]


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


def MOencodeParams(  # A --(params, t_a)-> B
        p,
        r,  # r = p-1???
        t_a
):
    encoder = asn1.Encoder()

    encoder.enter(asn1.Numbers.Sequence)  # 1
    encoder.enter(asn1.Numbers.Set)  # 2
    encoder.enter(asn1.Numbers.Sequence)  # 3

    encoder.write(b'\x08\x07\x02\x00', asn1.Numbers.OctetString)  # TODO: check if it works correctly
    encoder.write(b'MO params and t^a', asn1.Numbers.UTF8String)

    encoder.enter(asn1.Numbers.Sequence)  # 4
    encoder.leave()  # 4

    encoder.enter(asn1.Numbers.Sequence)  # 5
    encoder.write(p, asn1.Numbers.Integer)
    encoder.write(r, asn1.Numbers.Integer)
    encoder.leave()  # 5

    encoder.enter(asn1.Numbers.Sequence)  # 6
    encoder.write(t_a, asn1.Numbers.Integer)
    encoder.leave()  # 6

    encoder.leave()  # 3
    encoder.leave()  # 2

    encoder.enter(asn1.Numbers.Sequence)  # 7
    encoder.leave()  # 7

    encoder.leave()  # 1

    return encoder.output()


def MOencodeResponse(  # A <--(t_ab)-- B
        t_ab
):
    encoder = asn1.Encoder()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.enter(asn1.Numbers.Set)
    encoder.enter(asn1.Numbers.Sequence)

    encoder.write(b'\x08\x07\x02\x00', asn1.Numbers.OctetString)  # TODO: check if it works correctly
    encoder.write("MO t^(ab) response")

    encoder.enter(asn1.Numbers.Sequence)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.write(t_ab, asn1.Numbers.Integer)
    encoder.leave()
    encoder.leave()
    encoder.leave()
    encoder.enter(asn1.Numbers.Sequence)
    encoder.leave()
    encoder.leave()

    return encoder.output()


def MOencodeFinish(  # A --(t_b, cipher_params)-> B
        t_b,
        len,
        encrypted
):
    encoder = asn1.Encoder()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.enter(asn1.Numbers.Set)
    encoder.enter(asn1.Numbers.Sequence)

    encoder.write(b'\x08\x07\x02\x00', asn1.Numbers.OctetString)  # TODO: check if it works correctly
    encoder.write("MO t^b and first message")

    encoder.enter(asn1.Numbers.Sequence)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.write(t_b, asn1.Numbers.Integer)
    encoder.leave()
    encoder.leave()
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.write(b'\x10\x82', asn1.Numbers.OctetString)  # AES CBC
    encoder.write(len, asn1.Numbers.Integer)
    encoder.leave()

    encoder.leave()

    encoder.write(encrypted)


def MOencodeMessage(  # after A and B get secret key t
        len,
        encrypted
):
    encoder = asn1.Encoder()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.enter(asn1.Numbers.Set)
    encoder.enter(asn1.Numbers.Sequence)

    encoder.write(b'\x00\x00', asn1.Numbers.OctetString)
    encoder.write("message")

    encoder.enter(asn1.Numbers.Sequence)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.leave()
    encoder.leave()
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.write(b'\x10\x82', asn1.Numbers.OctetString)  # AES CBC
    encoder.write(len, asn1.Numbers.Integer)
    encoder.leave()

    encoder.leave()

    encoder.write(encrypted)


def MOdecodeParams(data):  # type: (data) -> (p, r, t_a)
    integers = []  # list of integers in ASN.1 file
    decoder = asn1.Decoder()
    decoder.start(data)
    integers = parse(decoder, integers)
    return integers[0], integers[1], integers[2]


def MOdecodeResponse(data):  # type: (data) -> t_ab
    integers = []  # list of integers in ASN.1 file
    decoder = asn1.Decoder()
    decoder.start(data)
    integers = parse(decoder, integers)
    return integers[0]


def MOdecodeFinish(data):  # type: (data) -> (t_b, len, encrypted)
    integers = []  # list of integers in ASN.1 file
    decoder = asn1.Decoder()
    decoder.start(data)
    integers = parse(decoder, integers)
    cipher = data[-integers[-1]:]  # get last integrs[last] symbols, this is ciphertext
    return integers[0], integers[1], cipher


def MOdecodeMessage(data): # type: (data) -> (len, encrypted)
    integers = []  # list of integers in ASN.1 file
    decoder = asn1.Decoder()
    decoder.start(data)
    integers = parse(decoder, integers)
    cipher = data[-integers[-1]:]  # get last integrs[last] symbols, this is ciphertext
    return integers[0],  cipher


def parse(decoder, integers):
    while not decoder.eof():
        try:
            tag = decoder.peek()

            if tag.nr == asn1.Numbers.Null:
                break

            if tag.typ == asn1.Types.Primitive:
                tag, value = decoder.read()

                if tag.nr == asn1.Numbers.Integer:
                    integers.append(value)

            else:
                decoder.enter()
                integers = parse(decoder, integers)
                decoder.leave()

        except asn1.Error:
            break

    return integers
