import asn_common
import aes_common
import argparse
from ELG.params import *

def parse_args():
    parser = argparse.ArgumentParser(description='ELG digital signature generator')
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


def ELGfileSign(filename):
    w, s = aes_common.ELGSignAdd(
        filename,
        int(x, 16),
        int(a, 16),
        int(p, 16),
        int(r, 16)
    )
    with open(filename + ".sign", "wb") as file:
        file.write(
            asn_common.ELGencodeSign(
                int(p, 16),
                int(r, 16),
                int(a, 16),
                w,
                s,
                int(b, 16)
            )
        )

def ELGfileCheckSignature(filename, sig_filename):
    b, p, r, a, w, s = asn_common.ELGdecodeSign(sig_filename)

    return aes_common.ELGSignCheck(
        filename,
        a,
        b,
        p,
        r,
        w,
        s
    )


if __name__ == '__main__':
    args = parse_args()
    try:
        if args.sign:
            ELGfileSign(args.FILE)
            print("Signing complete")

        if args.check:
            if args.sfile is None:
                print("You should give the signature file by --sfile command")
                exit(1)
            else:
                result = ELGfileCheckSignature(args.FILE, args.sfile)
            print("Sign check: " + str(result))
    except NameError:
        print("Error with names of varaibles, please, check params.py or re-generete it with schemeinstall.py")
