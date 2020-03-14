import argparse
import rsa  # for keys
from sympy import nextprime, gcd, randprime, is_primitive_root
from random import randint
from util import auto_int






def get_args():
    parser = argparse.ArgumentParser(description='RSA encoder and digital signature generator')

    parser.add_argument("BITS",
                        nargs="?",
                        type=auto_int,
                        default=1024,
                        help="Number of bits, default = 1024")

    parser.add_argument("SCH",
                        nargs="?",
                        default="RSA",
                        type=str,
                        help="Scheme for wich generete params, RSA|ELG|MO")

    parser.add_argument("-f",
                        help="file to save")

    return parser.parse_args()


def gen_rsa(filename, bits):
    exp = 0x10001

    pubkey, privkey = rsa.newkeys(bits, exponent=exp)
    signpubkey, signprivkey = rsa.newkeys(1024, exponent=exp)

    try:
        mystr = "exp = \"" + str(hex(exp)[2:]) + "\"" + "\n" \
                "n = \"" + str(hex(pubkey.n))[2:] + "\"" + "\n" \
                "d = \"" + str(hex(privkey.d))[2:] + "\"" + "\n" \
                "p = \"" + str(hex(privkey.p))[2:] + "\"" + "\n" \
                "q = \"" + str(hex(privkey.q))[2:] + "\"" + "\n" \
                "sign_n = \"" + str(hex(signpubkey.n))[2:] + "\"" + "\n" \
                "sign_d = \"" + str(hex(signprivkey.d))[2:] + "\""
        with open(filename, "w") as file:
            file.write(mystr)
    except:
        print("exp = \"" + str(hex(exp)[2:]) + "\"")
        print("n = \"" + str(hex(pubkey.n))[2:] + "\"")
        print("d = \"" + str(hex(privkey.d))[2:] + "\"")
        print("p = \"" + str(hex(privkey.p))[2:] + "\"")
        print("q = \"" + str(hex(privkey.q))[2:] + "\"")


def gen_elg(filename, bits):
    def gen_p():
        return randprime(2**bits, 2**(bits+1))

    def gen_a(p):
        def gen_primitive_root(r):
            a = randint(1, r)
            phi_r = r-1 #r is prime
            while pow(a, phi_r, r) != 1: #aways true, as r is prime
                a = randint(1, r)

            return a

        r = randprime(2**(bits-1), p)
        return r, gen_primitive_root(r)

    def gen_x(r):
        return randprime(1, r) #Maybe x should be big?

    def gen_b(a, x, p):
        return pow(a, x, p)


    p = gen_p()
    r, a = gen_a(p)
    x = gen_x(r)
    b = gen_b(a, x, p)

    try:
        mystr = "p = \"" + str(hex(p)[2:]) + "\"" + "\n" \
        "a = \"" + str(hex(a))[2:] + "\"" + "\n" \
        "x = \"" + str(hex(x))[2:] + "\"" + "\n" \
        "b = \"" + str(hex(b))[2:] + "\"" + "\n" \
        "r = \"" + str(hex(r))[2:] + "\"" + "\n"
        with open(filename, "w") as file:
            file.write(mystr)
    except:
        print("p= \"" + str(hex(p)[2:]) + "\"")
        print("a = \"" + str(hex(a))[2:] + "\"")
        print("x = \"" + str(hex(x))[2:] + "\"")
        print("b = \"" + str(hex(b))[2:] + "\"")
        print("r = \"" + str(hex(r))[2:] + "\"")


if __name__ == '__main__':
    args = get_args()

    if args.SCH == "RSA":
        gen_rsa(args.f, args.BITS)

    elif args.SCH == "ELG":
        gen_elg(args.f, args.BITS)
