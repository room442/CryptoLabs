from CM.MO.asn import MOdecodeParams, MOencodeResponse, MOdecodeFinish
from CM.MO.crypto import MOencrypt, MOdecrypt, MOgetKeys
from aes_common import AES256decrypt, AES
import socket
import os

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


def server(verbose=False):
    # Настраиваем сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(10)

    while True:
        connection, address = server_socket.accept()
        print(f"Connected: {address}")

        msg = get_data(connection)
        p, r, t_a = MOdecodeParams(msg)

        e, d = MOgetKeys(p)

        if verbose:
            print(F"SERVER 1st msg: {msg}")
            print(F"SERVER p = {p}")
            print(F"SERVER t_a = {t_a}")
            print(F"SERVER e = {e}")
            print(F"SERVER d = {d}")

        while True:
            try:
                t_ab = MOencrypt(t_a, e, p)
            except:
                e, d = MOgetKeys(p)
                continue
            break
        connection.send(MOencodeResponse(t_ab))

        msg = get_data(connection)
        t_b, len, encrypted = MOdecodeFinish(msg)

        t = MOdecrypt(t_b, d, p)

        opentext = AES256decrypt(encrypted, int.to_bytes(t, AES.key_size[-1], "big"))
        connection.close()

        if verbose:
            print(F"SERVER t_ab = {t_ab}")
            print(F"SERVER 2nd msg: {MOencodeResponse(t_ab)}")
            print(F"SERVER 3rd msg: {msg}")
            print(F"SERVER t_b = {t_b}")
            print(F"SERVER len = {len}")
            print(F"SERVER encrypted[:100] = {bytes(encrypted)[:100]}")
            print(F"SERVER t = {t}")
            print(F"SERVER opentext[:100] = {bytes(opentext)[:100]}")



        try:
            os.mkdir("received")
        except:
            pass
        with open(F"received/{address}.dec", "wb") as file:
            file.write(opentext)

        # time.sleep(1)


