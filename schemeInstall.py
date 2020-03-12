import argparse
import rsa  # for keys



def auto_int(x):
    return int(x, 0)


parser = argparse.ArgumentParser(description='RSA encoder and digital signature generator')

parser.add_argument("BITS",
                    nargs="?",
                    type=auto_int,
                    default=1024,
                    help="Number of bits, default = 1024")

parser.add_argument("-f",
                    help="file to save")

args = parser.parse_args()

exp = 0x10001

pubkey, privkey = rsa.newkeys(args.BITS, exponent=exp)
signpubkey, signprivkey = rsa.newkeys(1024, exponent=exp)

try:
    mystr = "exp = \"" + str(hex(exp)[2:]) + "\"" + "\n"\
            "n = \"" + str(hex(pubkey.n))[2:] + "\"" + "\n"\
            "d = \"" + str(hex(privkey.d))[2:] + "\"" + "\n"\
            "p = \"" + str(hex(privkey.p))[2:] + "\"" + "\n"\
            "q = \"" + str(hex(privkey.q))[2:] + "\"" + "\n"\
            "sign_n = \"" + str(hex(signpubkey.n))[2:] + "\"" + "\n"\
            "sign_d = \"" + str(hex(signprivkey.d))[2:] + "\""
    with open(args.f, "w") as file:
        file.write(mystr)
except:
    print("exp = \"" + str(hex(exp)[2:]) + "\"")
    print("n = \"" + str(hex(pubkey.n))[2:] + "\"")
    print("d = \"" + str(hex(privkey.d))[2:] + "\"")
    print("p = \"" + str(hex(privkey.p))[2:] + "\"")
    print("q = \"" + str(hex(privkey.q))[2:] + "\"")


