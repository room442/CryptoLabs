import argparse
import rsa  # for keys
from util import auto_int


def get_args():
    parser = argparse.ArgumentParser(description='RSA encoder and digital signature generator')

    parser.add_argument("BITS",
                        nargs="?",
                        type=auto_int,
                        default=1024,
                        help="Number of bits, default = 1024")

    parser.add_argument("-f",
                        help="file to save")

    return parser.parse_args()


def gen_rsa(filename, bits):
    exp = 0x10001

    pubkey, privkey = rsa.newkeys(bits, exponent=exp)
    signpubkey, signprivkey = rsa.newkeys(1024, exponent=exp)

    try:
        mystr = F"exp = \"{hex(exp)[2:]}\"\n" \
                F"n = \"{hex(pubkey.n)[2:]}\"\n"\
                F"d = \"{hex(privkey.d)[2:]}\"\n"\
                F"p = \"{hex(privkey.p)[2:]}\"\n"\
                F"q = \"{hex(privkey.q)[2:]}\"\n"\
                F"sign_n = \"{hex(signpubkey.n)[2:]}\"\n"\
                F"sign_d = \"{hex(signprivkey.d)[2:]} \""
        with open(filename, "w") as file:
            file.write(mystr)
    except:
        print(F"exp = \"{hex(exp)[2:]}\"")
        print(F"n = \"{hex(pubkey.n)[2:]}\"")
        print(F"d = \"{hex(privkey.d)[2:]}\"")
        print(F"p = \"{hex(privkey.p)[2:]}\"")
        print(F"q = \"{hex(privkey.q)[2:]}\"")


if __name__ == '__main__':
    args = get_args()
    gen_rsa(args.f, args.BITS)
