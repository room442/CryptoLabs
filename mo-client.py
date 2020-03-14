import asyncio
from crypto import MOencrypt, MOdecrypt, AES256encrypt
from random import randint
from asn import MOencodeFinish, MOdecodeFinish, MOencodeMessage, MOdecodeMessage, MOencodeParams, MOdecodeParams, MOencodeResponse, MOdecodeResponse


async def tcp_client(ip, port, p, encrypted, key, a, loop, len):
    reader, writer = await asyncio.open_connection(ip, port,
                                                   loop=loop)

    writer.write(MOencodeParams(p, p-1, MOencrypt(int.from_bytes(key, "big"), a, p)))

    # t_ab = MOdecodeResponse(await reader.read(100))

    # writer.write(MOencodeFinish(MOdecrypt(t_ab, a, p), len, encrypted)

    writer.close()


def sendfile(filename, p, ip, port):
    a = randint(2, p-1)
    with open(filename, "rb") as file:
        data = file.read()

    datalen = len(data)
    encrypted, key = AES256encrypt(data)

    loop = asyncio.get_event_loop()

    loop.run_until_complete(tcp_client(ip, port, p, encrypted, key, a, loop, datalen))
    loop.close()


if __name__ == '__main__':
    from params import *
    sendfile("opentext.txt", int(r, 16), "127.0.0.1", 8888)
