from hashlib import sha256

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