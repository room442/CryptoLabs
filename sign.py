from params import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import sys
import asn1
from hashlib import sha256

def parse(decoder, integers): # такой же парсер, как и в шифровании
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


def rsa_encr(m, e, n):
    return pow(m, e, n)


def rsa_decrypt(c, d, n):
    return pow(c, d, n)


def rsa_add_sign(filename, d, n): # тут смысл в том, что мы шифруем хеш-значение от данных в файле -- это и будет подписи.
    with open(filename, "rb") as file:
        data = file.read()

    r = sha256(data).hexdigest()

    return rsa_encr(int(r, 16), d, n)


def rsa_check_sign(filename, e, n, sign): # соответственно расшифровываем то, что нам передали и сверяем хеш-значение.
    s = rsa_decrypt(sign, e, n)

    with open(filename, "rb") as file:
        data = file.read()

    r = sha256(data).hexdigest()

    if int(r, 16) == s:
        return True

    return False


def sign_to_asn(
        n,
        e,
        sign
): # тут принцип такой же, как в шифровании, просто немного другой формат
    encoder = asn1.Encoder()

    encoder.start()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.enter(asn1.Numbers.Set)
    encoder.enter(asn1.Numbers.Sequence)

    encoder.write(b'\x00\x40', asn1.Numbers.OctetString) # идентификатор подписи
    encoder.write(b'\x0C\x00', asn1.Numbers.UTF8String)

    encoder.enter(asn1.Numbers.Sequence)
    encoder.write(n, asn1.Numbers.Integer)
    encoder.write(e, asn1.Numbers.Integer)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.write(sign, asn1.Numbers.Integer) #сама подпись в качестве шифротекста
    encoder.leave()

    encoder.leave()

    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)
    encoder.leave()

    encoder.leave() # на этот раз зашифрованных данных нет.

    return encoder.output()


def sign_from_asn(filename):  # type: (filename) -> (n, sign)
    integers = []  # list of integers in ASN.1 file
    with open(filename, "rb") as file:
        data = file.read()
        decoder = asn1.Decoder()
        decoder.start(data)
        integers = parse(decoder, integers)
    return integers[0], integers[2]


def rsa_sign_file(filename):
    with open(filename + ".sign", "wb") as file:
        file.write(
            sign_to_asn(
                int(sign_n, 16),
                int(sign_d, 16),
                rsa_add_sign(filename,
                             int(sign_d, 16),
                             int(sign_n, 16)
                             )
            )
        )


def rsa_file_check_sign(filename, sig_filename):
    n, sign = sign_from_asn(sig_filename)
    return rsa_check_sign(
        filename,
        int(e, 16),
        n,
        sign
    )



if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("sign.py -[sc] filename [signfile]")
    if sys.argv[1] == "-s":
        rsa_sign_file(sys.argv[2])
    elif sys.argv[1] == "-c":
        print(F"result = {rsa_file_check_sign(sys.argv[2], sys.argv[3])}")