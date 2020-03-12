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


if __name__ == '__main__':
    args = parse_args()

