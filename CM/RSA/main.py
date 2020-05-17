from CM.RSA.asn import RSAdecode, RSAdecodeSign, RSAencode, RSAencodeSign
from CM.RSA.crypto import RSAsignCheck, RSAsignAdd, RSAdecrypt, RSAencrypt
import aes_common
import argparse
from CM.RSA.params import *


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


def RSAfileEncrypt(filename):
    with open(filename, "rb") as file:
        data = file.read()
        encrypted, key = aes_common.AES256encrypt(data)

    print(F"AES key: {hex(int.from_bytes(key, 'big'))[2:]}")

    encrypted_key = RSAencrypt(
        int.from_bytes(key, "big"),
        int(e, 16),
        int(n, 16)
    )

    print("e = ", e)
    print("d = ", d)
    print("n = ", n)

    encoded = RSAencode(
        int(n, 16),
        int(e, 16),
        encrypted_key,
        len(encrypted),
        encrypted
    )

    with open(filename + ".enc", "wb") as file:
        file.write(encoded)


def RSAfileDecrypt(filename):
    n, e, encrypted_key, encrypted = RSAdecode(filename)

    print("e = ", e)
    print("d = ", d)
    print("n = ", n)

    key = RSAdecrypt(
        encrypted_key,
        int(d, 16),
        n
    )

    key = key.to_bytes(aes_common.AES.key_size[-1], "big")

    decrypted = aes_common.AES256decrypt(encrypted, key)

    with open(filename + ".dec", "wb") as file:
        file.write(decrypted)


def RSAfileSign(filename):
    with open(filename + ".sign", "wb") as file:
        file.write(
            RSAencodeSign(
                int(sign_n, 16),
                int(sign_d, 16),
                RSAsignAdd(filename,
                                      int(sign_d, 16),
                                      int(sign_n, 16)
                                      )
            )
        )


def RSAfileCheckSignature(filename, sig_filename):
    n, sign = RSAdecodeSign(sig_filename)
    return RSAsignCheck(
        filename,
        int(e, 16),
        n,
        sign
    )


if __name__ == '__main__':
    args = parse_args()
    try:
        if args.encrypt:
            RSAfileEncrypt(args.FILE)

        if args.decrypt:
            RSAfileDecrypt(args.FILE)
            print("Decryption complete")

        if args.sign:
            RSAfileSign(args.FILE)
            print("Signing complete")

        if args.check:
            if args.sfile is None:
                print("You should give the signature file by --sfile command")
                exit(1)
            result = RSAfileCheckSignature(args.FILE, args.sfile)
            print(F"Sign check result: {result}")
    except NameError:
        print("Error with names of varaibles, please, check params.py or re-generete it with schemeinstall.py")
