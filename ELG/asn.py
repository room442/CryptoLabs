import asn1
from asn_common import parse


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