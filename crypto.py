from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


iv = b'\x00' * AES.block_size


def RSAencrypt(m, e, n):
    return pow(m, e, n)


def RSAdecrypt(c, d, n):
    return pow(c, d, n)


def AES256encrypt(data):
    key = get_random_bytes(AES.key_size[-1])
    cipher = AES.new(key, AES.MODE_CBC, iv)

    ciphertext = cipher.encrypt(pad(data, AES.block_size))

    return ciphertext, key


def AES256decrypt(data, key):
    decipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted = unpad(decipher.decrypt(data), AES.block_size)

    return decrypted
