import asn
import crypto
import argparse
from params import *
import mo_client
import mo_server
from multiprocessing import Process
import time

def parse_args():
    parser = argparse.ArgumentParser(description='RSA encoder and idgital signature generator')
    parser.add_argument("FILE",
                        help="Name of input file")

    parser.add_argument("SCH",
                        type=str,
                        help="Scheme RSA|ELG, ELG supports only sign")

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

    parser.add_argument("--server",
                        action="store_true",
                        help="Run as a server in MO scheme")

    parser.add_argument("--client",
                        action="store_true",
                        help="Run as a client in MO scheme")

    parser.add_argument("--sfile",
                        help="Name of signature file")

    return parser.parse_args()


def RSAfileEncrypt(filename):
    with open(filename, "rb") as file:
        data = file.read()
        encrypted, key = crypto.AES256encrypt(data)

    encrypted_key = crypto.RSAencrypt(
        int.from_bytes(key, "big"),
        int(exp, 16),
        int(n, 16)
    )

    print("e = ", exp)
    print("d = ", d)
    print("n = ", n)

    encoded = asn.RSAencode(
        int(n, 16),
        int(exp, 16),
        encrypted_key,
        len(encrypted),
        encrypted
    )

    with open(filename + ".enc", "wb") as file:
        file.write(encoded)


def RSAfileDecrypt(filename):
    n, e, encrypted_key, encrypted = asn.RSAdecode(filename)

    print("e = ", e)
    print("d = ", d)
    print("n = ", n)

    key = crypto.RSAdecrypt(
        encrypted_key,
        int(d, 16),
        n
    )

    key = key.to_bytes(crypto.AES.key_size[-1], "big")

    decrypted = crypto.AES256decrypt(encrypted, key)

    with open(filename + ".dec", "wb") as file:
        file.write(decrypted)


def RSAfileSign(filename):
    with open(filename + ".sign", "wb") as file:
        file.write(
            asn.RSAencodeSign(
                int(sign_n, 16),
                int(sign_d, 16),
                crypto.RSAsignAdd(filename,
                                  int(sign_d, 16),
                                  int(sign_n, 16)
                                  )
            )
        )


def RSAfileCheckSignature(filename, sig_filename):
    n, sign = asn.RSAdecodeSign(sig_filename)
    return crypto.RSAsignCheck(
        filename,
        int(exp, 16),
        n,
        sign
    )

def ELGfileSign(filename):
    w, s = crypto.ELGSignAdd(
        filename,
        int(x, 16),
        int(a, 16),
        int(p, 16),
        int(r, 16)
    )
    with open(filename + ".sign", "wb") as file:
        file.write(
            asn.ELGencodeSign(
                int(p, 16),
                int(r, 16),
                int(a, 16),
                w,
                s,
                int(b, 16)
            )
        )

def ELGfileCheckSignature(filename, sig_filename):
    b, p, r, a, w, s = asn.ELGdecodeSign(sig_filename)

    return crypto.ELGSignCheck(
        filename,
        a,
        b,
        p,
        r,
        w,
        s
    )

def MO_three_pass(filename):
    server = Process(target=mo_server.server, args=())
    server.start()
    time.sleep(0.1)
    client = Process(target=mo_client.client, args=(filename, int(r,16)))

    client.start()
    server.join()
    client.join()

def MO_server():
    mo_server.server()

def MO_client(filename):
    mo_client.client(filename, int(r, 16))


if __name__ == '__main__':
    args = parse_args()
    try:
        if args.SCH == "MO":
            if args.server == True:
                MO_server()
            elif args.client == True:
                MO_client(args.FILE)
            else:
                MO_three_pass(args.FILE)
        if args.encrypt:
            if args.SCH == "RSA":
                RSAfileEncrypt(args.FILE)
                print("Ecryption complete")
            else:
                print("Wrong SCH")

        if args.decrypt:
            if args.SCH == "RSA":
                RSAfileDecrypt(args.FILE)
                print("Decryption complete")
            else:
                print("Wrong SCH")

        if args.sign:
            if args.SCH == "RSA":
                RSAfileSign(args.FILE)
            elif args.SCH == "ELG":
                ELGfileSign(args.FILE)
            print("Signing complete")

        if args.check:
            if args.sfile is None:
                print("You should give the signature file by --sfile command")
                exit(1)
            if args.SCH == "RSA":
                result = RSAfileCheckSignature(args.FILE, args.sfile)
            elif args.SCH == "ELG":
                result = ELGfileCheckSignature(args.FILE, args.sfile)
            print("Sign check: " + str(result))
    except NameError:
        print("Error with names of varaibles, please, check params.py or re-generete it with schemeinstall.py")
