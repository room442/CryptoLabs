from params import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import sys
import asn1


def parse(decoder, integers): # Функция разбора asn.1 файла, которая просто достает оттуда все числовые значения.
    while not decoder.eof():
        try:
            tag = decoder.peek()

            if tag.nr == asn1.Numbers.Null:
                break

            if tag.typ == asn1.Types.Primitive: #если тип примитивный
                tag, value = decoder.read()

                if tag.nr == asn1.Numbers.Integer: #если тип Integer
                    integers.append(value) #добавить к возвращаемому массиву

            else:
                decoder.enter() #если тип не примитивный, входим для разбора
                integers = parse(decoder, integers)
                decoder.leave()

        except asn1.Error:
            break

    return integers #возвращаем все целочисленные значения


def RSAencrypt(m, e, n):
    return pow(m, e, n)


def RSAdecrypt(c, d, n):
    return pow(c, d, n)


# iv = get_random_bytes(AES.block_size)
iv = b'\x00' * AES.block_size #синхропосылка нулевая, чтобы не хранить ее


def aes_encrypt(data):
    key = get_random_bytes(AES.key_size[-1]) #ключ рандомный
    cipher = AES.new(key, AES.MODE_CBC, iv)

    ciphertext = cipher.encrypt(pad(data, AES.block_size)) #зашифровали. Pad -- дополнение до полного блока.

    return ciphertext, key


def aes_decrypt(data, key):
    decipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted = unpad(decipher.decrypt(data), AES.block_size) #расшифровали и отбросили дополнение

    return decrypted


def to_asn(
        n,
        e,
        c,  # encrypted aes256 key
        len,
        encrypted
):
    encoder = asn1.Encoder()
    encoder.start()

    encoder.enter(asn1.Numbers.Sequence)  # Основная последовательность
    encoder.enter(asn1.Numbers.Set)  # Набор ключей RSA
    encoder.enter(asn1.Numbers.Sequence)  # Последовательность -- первый ключ RSA

    encoder.write(b'\x00\x01', asn1.Numbers.OctetString)  # идентификатор RSA
    encoder.write(b'\x0C\x00', asn1.Numbers.UTF8String)  # Необзяталеьный идентификатор ключа

    encoder.enter(asn1.Numbers.Sequence)  # последовательность, содержащая n, e -- открытый ключ
    encoder.write(n, asn1.Numbers.Integer)
    encoder.write(e, asn1.Numbers.Integer)
    encoder.leave()  # Вышли из последовательности открытого ключа

    encoder.enter(asn1.Numbers.Sequence)  # Параметры криптосистемы, в RSA не используются
    encoder.leave()

    encoder.enter(asn1.Numbers.Sequence)  # Зашифрованные данные RSA
    encoder.write(c, asn1.Numbers.Integer)
    encoder.leave() # Вышли из зашифрованных данных RSA

    encoder.leave()  # Вышли из множества первого ключа RSA
    encoder.leave()  # Вышли из набора ключей

    encoder.enter(asn1.Numbers.Sequence)  # Последовательность дополнительных данных
    encoder.write(b'\x10\x82', asn1.Numbers.OctetString)  # идентификатор алгоритма шифрования AES CBC
    encoder.write(len, asn1.Numbers.Integer)  # Длина шифровтекста
    encoder.leave()

    encoder.leave()  # Вышли из основной последовательности.

    encoder.write(encrypted) # Записали зашифрованные данные (зашифрованы при помощи AES CBC)

    return encoder.output() # вывод


def from_asn(filename):  # type: (filename) -> (n, e, c, ciphertext)
    integers = []
    with open(filename, "rb") as file:
        data = file.read()
        decoder = asn1.Decoder()
        decoder.start(data)
        integers = parse(decoder, integers) # получаем все целочисленные значения
        cipher = data[-integers[-1]:]  # мы знаем длину шифротекста и он в самом конце данных, так что можем просто взять последние байты
    return integers[0], integers[1], integers[2], cipher


def encr_file(filename):
    with open(filename, "rb") as file:
        data = file.read()
        encrypted, key = aes_encrypt(data)

    print(F"AES key: {hex(int.from_bytes(key, 'big'))[2:]}")

    encrypted_key = RSAencrypt(
        int.from_bytes(key, "big"),
        int(e, 16),
        int(n, 16)
    )

    print("e = ", e)
    print("d = ", d)
    print("n = ", n)

    encoded = to_asn(
        int(n, 16),
        int(e, 16),
        encrypted_key,
        len(encrypted),
        encrypted
    )

    with open(filename + ".enc", "wb") as file:
        file.write(encoded)


def decr_file(filename):
    n, e, encrypted_key, encrypted = from_asn(filename)

    print("e = ", e)
    print("d = ", d)
    print("n = ", n)

    key = RSAdecrypt(
        encrypted_key,
        int(d, 16),
        n
    )

    key = key.to_bytes(AES.key_size[-1], "big")

    decrypted = aes_decrypt(encrypted, key)

    with open(filename + ".dec", "wb") as file:
        file.write(decrypted)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("cipher.py -[ed] filename")
    if sys.argv[1] == "-e":
        encr_file(sys.argv[2])
    elif sys.argv[1] == "-d":
        decr_file(sys.argv[2])