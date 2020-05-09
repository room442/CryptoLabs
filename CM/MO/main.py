import argparse
from CM.MO.params import *
from CM.MO import mo_server, mo_client
from multiprocessing import Process
import time


def parse_args():
    parser = argparse.ArgumentParser(description='MO client-server for secure sending files')
    parser.add_argument("FILE",
                        help="Name of input file")

    parser.add_argument("--server",
                        action="store_true",
                        help="Run as a server in MO scheme")

    parser.add_argument("--client",
                        action="store_true",
                        help="Run as a client in MO scheme")

    parser.add_argument("--verbose",
                        action="store_true",
                        default=False,
                        help="Run with verbose mode")

    return parser.parse_args()


def MO_three_pass(filename, verbose=False):
    server = Process(target=mo_server.server, args=verbose)
    server.start()
    time.sleep(0.1)
    client = Process(target=mo_client.client, args=(filename, int(r, 16), verbose))

    client.start()
    server.join()
    client.join()


def MO_server(verbose=False):
    mo_server.server(verbose)


def MO_client(filename, verbose=False):
    mo_client.client(filename, int(r, 16), verbose)


if __name__ == '__main__':
    args = parse_args()
    try:
        if args.server == True:
            MO_server(args.verbose)
        elif args.client == True:
            MO_client(args.FILE, args.verbose)
        else:
            MO_three_pass(args.FILE)


    except NameError:
        print("Error with names of varaibles, please, check params.py or re-generete it with schemeinstall.py")
