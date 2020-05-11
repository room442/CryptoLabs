from CM.MO.crypto import MOencrypt, MOdecrypt, MOgetKeys
from aes_common import AES256encrypt
from CM.MO.asn import MOencodeFinish, MOencodeParams, MOdecodeResponse
import socket

ip = "127.0.0.1"
port = 8888


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


def sendfile(filename, p, ip, port, verbose=False):
    e, d = MOgetKeys(p)
    if verbose:
        print(F"CLIENT e = {e}")
        print(F"CLIENT d = {d}")

    with open(filename, "rb") as file:
        data = file.read()
        if verbose:
            print(F"CLIENT opendata[:100] = {bytes(data)[:100]}")

    encrypted, key = AES256encrypt(data)
    datalen = len(encrypted)
    if verbose:
        print(F"CLIENT encdata[:100] = {bytes(encrypted)[:100]}")
        print(F"CLIENT enckey = {key}")
        print(F"CLIENT datalen = {datalen}")


    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))

    integer_key = int.from_bytes(key, "big")
    while True:
        try:
            t_a = MOencrypt(integer_key, e, p)
        except:
            e, d = MOgetKeys(p)
            continue
        break
    client.send(MOencodeParams(p, p - 1, t_a))

    msg = get_data(client)
    t_ab = MOdecodeResponse(msg)
    t_b = MOdecrypt(t_ab, d, p)

    client.send(MOencodeFinish(t_b, datalen, encrypted))

    if verbose:
        print(F"CLIENT p = {p}")
        print(F"CLIENT t_a = {t_a}")
        print(F"CLIENT encoded 1st msg = {MOencodeParams(p, p - 1, t_a)}")
        print(F"CLIENT encoded 2nd msg = {msg}")
        print(F"CLIENT t_ab = {t_ab}")
        print(F"CLIENT t_b = {t_b}")
        print(F"CLIENT encoded 3rd msg = {MOencodeFinish(t_b, datalen, encrypted)}")


def client(filename, p, verbose=False):
    sendfile(filename, p, ip, port, verbose)
