import asn1
from asn_common import parse


def GOSTencodeSign(xq, yq, prime, A, B, xp, yp, q, r, s):
    encoder = asn1.Encoder()

    encoder.start()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.enter(asn1.Numbers.Set)
    encoder.enter(asn1.Numbers.Sequence)

    encoder.write(b'\x80\x06\x07\x00', asn1.Numbers.OctetString)
    encoder.write(b'gostSignKey', asn1.Numbers.UTF8String)

    encoder.enter(asn1.Numbers.Sequence) # Open key
    encoder.write(xq, asn1.Numbers.Integer)
    encoder.write(yq, asn1.Numbers.Integer)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence) # cryptosystem params

    encoder.enter(asn1.Numbers.Sequence) # field params
    encoder.write(prime, asn1.Numbers.Integer)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence) # curve params
    encoder.write(A, asn1.Numbers.Integer)
    encoder.write(B, asn1.Numbers.Integer)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence) # points generator
    encoder.write(xp, asn1.Numbers.Integer)
    encoder.write(yp, asn1.Numbers.Integer)
    encoder.leave()

    encoder.write(q, asn1.Numbers.Integer)

    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence) # sign
    encoder.write(r, asn1.Numbers.Integer)
    encoder.write(s, asn1.Numbers.Integer)
    encoder.leave()

    encoder.leave()

    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence) # file params
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