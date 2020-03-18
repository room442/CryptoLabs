import asyncio
from crypto import MOencrypt, MOdecrypt, AES256encrypt
from random import randint
from asn import MOencodeFinish, MOencodeParams, MOdecodeResponse
from sympy import randprime

import socket




def get_data(connection):
    data = b""
    while True:
        newpart = connection.recv(1024)
        if not newpart:
            break
        else:
            data = data + newpart
        if len(data) < 1024:
            break
    return data

def sendfile(filename, p, ip, port):
    a = randprime(2, p - 1)
    with open(filename, "rb") as file:
        data = file.read()

    datalen = len(data)
    encrypted, key = AES256encrypt(data)

    print(key)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))

    integer_key = int.from_bytes(key, "big")
    t_a = MOencrypt(integer_key, a, p)
    client.send(MOencodeParams(p, p-1, t_a))

    msg = get_data(client)
    t_ab = MOdecodeResponse(msg)
    t_b = MOdecrypt(t_ab, a, p)

    client.send(MOencodeFinish(t_b, datalen, encrypted))

    print("debug")


if __name__ == '__main__':
    from params import *

    sendfile("opentext.txt", int(r, 16), "127.0.0.1", 8888)
