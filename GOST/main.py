from GOST.asn import *
import GOST.params
from GOST.crypto import *
import argparse

A = int(GOST.params.a, 10)
B = int(GOST.params.b, 10)
p = int(GOST.params.p, 10)
q = int(GOST.params.r, 10)
x = int(GOST.params.x, 10)
y = int(GOST.params.y, 10)

def parse_args():
    parser = argparse.ArgumentParser(description='GOST digital signature generator')
    parser.add_argument("FILE",
                        help="Name of input file")


    parser.add_argument("-s", "--sign",
                        action="store_true",
                        help="Sign FILE")

    parser.add_argument("-c", "--check",
                        action="store_true",
                        help="Check FILE signaruture, given by --sfile")


    parser.add_argument("--sfile",
                        help="Name of signature file")

    return parser.parse_args()


def GOSTfileSign(filename):
    d, xq, yq = GOSTgenKeys(p, A, B, q, q, x, y)
    r, s = GOSTSignAdd(filename, d, p, A, B, q, q, x, y)
    with open(filename + ".sign", "wb") as file:
        file.write(
            GOSTencodeSign(xq, yq, p, A, B, x, y, q, r, s)
        )

def GOSTfileCheckSignature(filename, sig_filename):
    xq_decoded, yq_decoded, prime_decoded, A_decoded, B_decoded, xp_decoded, yp_decoded, q_decoded, r_decoded, s_decoded = GOSTdecodeSign(sig_filename)
    return GOSTSignCheck(filename, xq_decoded, yq_decoded, prime_decoded, A_decoded, B_decoded, q_decoded, q_decoded, xp_decoded, yp_decoded, r_decoded, s_decoded)

if __name__ == '__main__':
    args = parse_args()
    try:
        if args.sign:
            GOSTfileSign(args.FILE)
            print("Signing complete")

        if args.check:
            if args.sfile is None:
                print("You should give the signature file by --sfile command")
                exit(1)
            else:
                result = GOSTfileCheckSignature(args.FILE, args.sfile)
            print("Sign check: " + str(result))
    except NameError:
        print("Error with names of varaibles, please, check params.py or re-generete it with schemeinstall.py")
