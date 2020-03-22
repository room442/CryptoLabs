import asn1
from asn_common import parse

def MOencodeParams(  # A --(params, t_a)-> B
        p,
        r,  # r = p-1???
        t_a
):
    encoder = asn1.Encoder()
    encoder.start()

    encoder.enter(asn1.Numbers.Sequence)  # 1 -- sequence of all
    encoder.enter(asn1.Numbers.Set)  # 2 -- set of keys
    encoder.enter(asn1.Numbers.Sequence)  # 3 -- sequence of first key

    encoder.write(b'\x08\x07\x02\x00', asn1.Numbers.OctetString)
    encoder.write(b'MO params and t^a', asn1.Numbers.UTF8String)

    encoder.enter(asn1.Numbers.Sequence)  # 4 -- sequence of open key
    encoder.leave()  # 4

    encoder.enter(asn1.Numbers.Sequence)  # 5 -- params
    encoder.write(p, asn1.Numbers.Integer)
    encoder.write(r, asn1.Numbers.Integer)
    encoder.leave()  # 5 -- leave first key

    encoder.enter(asn1.Numbers.Sequence)  # 6 -- cipher
    encoder.write(t_a, asn1.Numbers.Integer)
    encoder.leave()  # 6

    encoder.leave()  # 3
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)  # 7
    encoder.leave()  # 7

    encoder.leave()  # 1

    return encoder.output()


def MOencodeResponse(  # A <--(t_ab)-- B
        t_ab
):
    encoder = asn1.Encoder()
    encoder.start()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.enter(asn1.Numbers.Set)
    encoder.enter(asn1.Numbers.Sequence)

    encoder.write(b'\x08\x07\x02\x00', asn1.Numbers.OctetString)
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
    encoder.start()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.enter(asn1.Numbers.Set)
    encoder.enter(asn1.Numbers.Sequence)

    encoder.write(b'\x08\x07\x02\x00', asn1.Numbers.OctetString)
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

    return encoder.output()


def MOencodeMessage(  # after A and B get secret key t
        len,
        encrypted
):
    encoder = asn1.Encoder()
    encoder.start()

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