import asyncio
from random import randint
from asn import MOdecodeParams, MOencodeResponse, MOdecodeFinish
from crypto import MOencrypt, MOdecrypt, AES256decrypt


async def handle_client(reader, writer):
    p, r, t_a = MOdecodeParams(await reader.read())
    b = randint(2, r - 1)
    writer.write(MOencodeResponse(MOencrypt(t_a, b, p)))
    t_b, len, encrypted = MOdecodeFinish(await reader.read())
    t = MOdecrypt(t_b, b, p)
    opentext = AES256decrypt(encrypted, t)
    print(opentext)

    writer.close()


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_client, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
