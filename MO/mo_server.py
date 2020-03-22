from MO.asn import MOdecodeParams, MOencodeResponse, MOdecodeFinish
from MO.crypto import MOencrypt, MOdecrypt, MOgetKeys
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


def server():
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

        try:
            os.mkdir("received")
        except:
            pass
        with open(F"MO/received/MOreceived {address}.dec", "wb") as file:
            file.write(opentext)
            print(F"get new opentext: {opentext}")
            file.close()

        # time.sleep(1)


