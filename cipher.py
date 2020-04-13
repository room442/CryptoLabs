from params import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import sys
import asn1


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


def RSAencrypt(m, e, n):
    return pow(m, e, n)


def RSAdecrypt(c, d, n):
    return pow(c, d, n)


# iv = get_random_bytes(AES.block_size)
iv = b'\x00' * AES.block_size


def aes_encrypt(data):
    key = get_random_bytes(AES.key_size[-1])
    cipher = AES.new(key, AES.MODE_CBC, iv)

    ciphertext = cipher.encrypt(pad(data, AES.block_size))

    return ciphertext, key


def aes_decrypt(data, key):
    decipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted = unpad(decipher.decrypt(data), AES.block_size)

    return decrypted


def to_asn(
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


def from_asn(filename):  # type: (filename) -> (n, e, c, ciphertext)
    integers = []  # list of integers in ASN.1 file
    with open(filename, "rb") as file:
        data = file.read()
        decoder = asn1.Decoder()
        decoder.start(data)
        integers = parse(decoder, integers)
        cipher = data[-integers[-1]:]  # get last integrs[last] symbols, this is ciphertext
    return integers[0], integers[1], integers[2], cipher


def encr_file(filename):
    with open(filename, "rb") as file:
        data = file.read()
        encrypted, key = aes_encrypt(data)

    print(F"AES key: {hex(int.from_bytes(key, 'big'))[2:]}")

    encrypted_key = RSAencrypt(
        int.from_bytes(key, "big"),
        int(e, 16),
        int(n, 16)
    )

    print("e = ", e)
    print("d = ", d)
    print("n = ", n)

    encoded = to_asn(
        int(n, 16),
        int(e, 16),
        encrypted_key,
        len(encrypted),
        encrypted
    )

    with open(filename + ".enc", "wb") as file:
        file.write(encoded)


def decr_file(filename):
    n, e, encrypted_key, encrypted = from_asn(filename)

    print("e = ", e)
    print("d = ", d)
    print("n = ", n)

    key = RSAdecrypt(
        encrypted_key,
        int(d, 16),
        n
    )

    key = key.to_bytes(AES.key_size[-1], "big")

    decrypted = aes_decrypt(encrypted, key)

    with open(filename + ".dec", "wb") as file:
        file.write(decrypted)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("cipher.py -[ed] filename")
    if sys.argv[1] == "-e":
        encr_file(sys.argv[2])
    elif sys.argv[1] == "-d":
        decr_file(sys.argv[2])