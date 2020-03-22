import argparse
from MO.params import *
from MO import mo_client, mo_server
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

    return parser.parse_args()


def MO_three_pass(filename):
    server = Process(target=mo_server.server, args=())
    server.start()
    time.sleep(0.1)
    client = Process(target=mo_client.client, args=(filename, int(r, 16)))

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
        if args.server == True:
            MO_server()
        elif args.client == True:
            MO_client(args.FILE)
        else:
            MO_three_pass(args.FILE)


    except NameError:
        print("Error with names of varaibles, please, check params.py or re-generete it with schemeinstall.py")
