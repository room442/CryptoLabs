from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib

iv = b'\x00' * AES.block_size


def RSAencrypt(m, e, n):
    return pow(m, e, n)


def RSAdecrypt(c, d, n):
    return pow(c, d, n)


def encryptAES256(data):
    # key = get_random_bytes(32)
    key = b'12341234123412341234123412341234'
    cipher = AES.new(key, AES.MODE_CBC, iv)

    ciphertext = cipher.encrypt(data)

    return ciphertext, key


def decryptAES256(data, key):
    decipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted = decipher.decrypt(data)

    return decrypted
