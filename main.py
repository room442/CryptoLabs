from asn import *
from crypto import *
import argparse
from params import *


def parse_args():
    parser = argparse.ArgumentParser(description='RSA encoder and idgital signature generator')
    parser.add_argument("FILE",
                        help="Name of input file")

    parser.add_argument("-e", "--encrypt",
                        action="store_true",
                        help="Encrypt FILE")

    parser.add_argument('-d', "--decrypt",
                        action="store_true",
                        help='Decrypt FILE')

    parser.add_argument("-s", "--sign",
                        action="store_true",
                        help="Sign FILE")

    parser.add_argument("-c", "--check",
                        action="store_true",
                        help="Check FILE signaruture, given by --sfile")

    parser.add_argument("--sfile",
                        help="Name of signature file")

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


def addSignature(filename):
    with open(filename + ".sign", "wb") as file:
        file.write(
            encodeSign(
                int(sign_n, 16),
                int(sign_d, 16),
                RSAsignAdd(filename,
                           int(sign_d, 16),
                           int(sign_n, 16)
                           )
            )
        )


def checkSignature(filename, sig_filename):
    n, sign = decodeSign(sig_filename)
    return RSAsignCheck(
        filename,
        int(exp, 16),
        n,
        sign
    )


if __name__ == '__main__':
    args = parse_args()

    if args.encrypt:
        encrypt(args.FILE)

    if args.decrypt:
        decrypt(args.FILE)

    if args.sign:
        addSignature(args.FILE)

    if args.check:
        if args.sfile is None:
            print("You should give the signature file by --sfile command")
            exit(1)
        print("Sign check: " + str(checkSignature(args.FILE, args.sfile)))
