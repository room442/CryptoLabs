# -*- coding: UTF-8 -*-

import asn1


def encode(
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


def decode(filename): # type: (filename) -> (n, e, c, ciphertext)
    integers = []  # list of integers in ASN.1 file
    cipher = bytearray()
    with open(filename, "rb") as file:
        data = file.read()
        decoder = asn1.Decoder()
        decoder.start(data)
        integers = parse(decoder, integers)
        cipher = data[-integers[-1]:] #get last integrs[last] symbols, this is ciphertext
    return integers[0], integers[1], integers[2], cipher


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
