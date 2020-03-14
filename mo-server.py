import asyncio
from random import randint
from asn import MOdecodeParams, MOencodeResponse, MOdecodeFinish
from crypto import MOencrypt, MOdecrypt, AES256decrypt, AES

import socket

ip = "127.0.0.1"
port = 8888

# Настраиваем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ip, port))
server_socket.listen(10)

# Слушаем запросы
while True:
    connection, address = server_socket.accept()

    p, r, t_a = MOdecodeParams(connection.recv(1024))
    b = randint(2, r - 1)
    connection.send(MOencodeResponse(MOencrypt(t_a, b, p)))
    t_b, len, encrypted = MOdecodeFinish(connection.recv(1024))
    if len > 1024:
        rcv = 1024
        while rcv < len:
            encrypted = encrypted + connection.recv(1024)
            rcv = rcv + 1024

    t = MOdecrypt(t_b, b, p)  # fixme: t != key
    opentext = AES256decrypt(encrypted, t.to_bytes(AES.key_size[-1], "big"))
    print(opentext)
    connection.close()
