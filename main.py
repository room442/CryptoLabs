from asn import *
from crypto import *
import argparse
from params import *


def parse_args():
    parser = argparse.ArgumentParser(description='RSA encoder and idgital signature generator')
    parser.add_argument("--file",
                        help="Name of input file")

    parser.add_argument("-e", "--encrypt",
                        action="store_true",
                        help="Name of file with scheme settings in asn.1 representation. Only e and n are required.")

    parser.add_argument('-d', "--decrypt",
                        action="store_true",
                        help='Name of output file (encrypted text or digital sign file)')

    return parser.parse_args()


def encrypt(filename):
    with open(filename, "rb") as file:
        data = file.read()
        encrypted, key = AES256encrypt(data)

    encrypted_key = RSAencrypt(
        int.from_bytes(key, "big"),
        int(exp, 16),
        int(n, 16)
    )

    print("e = ", exp)
    print("d = ", d)
    print("n = ", n)

    encoded = encode(
        int(n, 16),
        int(exp, 16),
        encrypted_key,
        len(encrypted),
        encrypted
    )

    with open(filename + ".enc", "wb") as file:
        file.write(encoded)

def decrypt(filename):
    n, e, encrypted_key, encrypted = decode(filename)

    print("e = ", e)
    print("d = ", d)
    print("n = ", n)

    key = RSAdecrypt(
        encrypted_key,
        int(d, 16),
        n
    )

    key = key.to_bytes(AES.key_size[-1], "big")

    decrypted = AES256decrypt(encrypted, key)

    with open(filename + ".dec", "wb") as file:
        file.write(decrypted)

if __name__ == '__main__':
    args = parse_args()

    if args.encrypt:
        encrypt(args.file)

    if args.decrypt:
        decrypt(args.file)
