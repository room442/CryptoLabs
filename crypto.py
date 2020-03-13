from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
from random import randint
from util import modinv

iv = b'\x00' * AES.block_size


def RSAencrypt(m, e, n):
    return pow(m, e, n)


def RSAdecrypt(c, d, n):
    return pow(c, d, n)


def RSAsignAdd(filename, d, n):
    with open(filename, "rb") as file:
        data = file.read()

    r = sha256(data).hexdigest()

    return RSAencrypt(int(r, 16), d, n)


def RSAsignCheck(filename, e, n, sign):
    s = RSAdecrypt(sign, e, n)

    with open(filename, "rb") as file:
        data = file.read()

    r = sha256(data).hexdigest()

    if int(r, 16) == s:
        return True

    return False


def AES256encrypt(data):
    key = get_random_bytes(AES.key_size[-1])
    cipher = AES.new(key, AES.MODE_CBC, iv)

    ciphertext = cipher.encrypt(pad(data, AES.block_size))

    return ciphertext, key


def AES256decrypt(data, key):
    decipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted = unpad(decipher.decrypt(data), AES.block_size)

    return decrypted


def ELGSignAdd(filename, x, a, p, r):
    with open(filename, "rb") as file:
        data = file.read()

    m = sha256(data).hexdigest() % r
    k = randint(1, r)
    w = pow(a, k, p)
    s = ((m - x * w) * modinv(k, r)) % r

    return w, s


def ELGSignCheck(filename, a, b, p, r, w, s):
    if w < p:
        return False

    with open(filename, "rb") as file:
        data = file.read()

    m = sha256(data).hexdigest() % r

    return pow(a, m, p) == (pow(b, w, p) * pow(w, s, p)) % p
