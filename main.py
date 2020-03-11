import asn1
from Crypto.Cipher import AES
import hashlib
import sys
import argparse

parser = argparse.ArgumentParser(description='RSA encoder and idgital signature generator')
parser.add_argument('INPUT',
                    nargs='?',
                    default='opentext.txt',
                    # type=open,
                    help='Name of input file (open text)')

parser.add_argument('SCHEME',
                    nargs='?',
                    default='scheme.bin',
                    # type=open,
                    help='Name of file with scheme settings in asn.1 representation. Only e and n are required.')

parser.add_argument('OUTPUT',
                    # nargs='?',
                    # default='encrypted.bin',
                    # type = open,
                    help='Name of output file (encrypted text or digital sign file)')


args = parser.parse_args()
# print(args.accumulate(args.integers))
print(args.INPUT)
print(args.SCHEME)
print(args.OUTPUT)



#
#
#
# password = b"ibks"
# key = hashlib.sha256(password).digest()
# print("bytes key: ", key)
# intkey = int.from_bytes(key, "big")
# print("intkey: ", intkey)
# intkey_str = ''.join('%02X '%i for i in key)
# print("key as a string: ", intkey_str + "\n")
#
# encoder = asn1.Encoder()
# encoder.start()
# encoder.enter(asn1.Numbers.Sequence)
# encoder.write(intkey)
# encoder.write(3)
# encoder.leave()
# encoded_bytes = encoder.output()
# encoded_bytes_str = ''.join('%02X '%i for i in encoded_bytes)
# print("encoded asn.1:", encoded_bytes_str)



# decoder.start(encoded_bytes)
# while True:
#     if decoder.peek() is None:
#         break
#     if decoder.peek()[0] == asn1.Numbers.Sequence:
#         decoder.enter()
#         continue
#     if decoder.peek()[0] == asn1.Numbers.Integer:
#         print("New value: ", decoder.read())



# test_val = 0x303F31323030040200010C04746573743015021011317E789C45CCCC7436C384D43549450201033000300B02090A0B0C0A0B0C0A0B0C3009040201210203133870
# print(str(format(test_val, "X")))
# bytestring = test_val.to_bytes(((len(bin(test_val)) - 2)//8 + 1), 'big')
# print(bytestring)




# print()
# test_val = bytes(0x303F31323030040200010C04746573743015021011317E789C45CCCC7436C384D43549450201033000300B02090A0B0C0A0B0C0A0B0C3009040201210203133870)
# decoder = asn1.Decoder()
# decoder.start(bytestring)
# tab_c = 0
# while True:
#     if decoder.peek() is None:
#         try:
#             decoder.leave()
#             print("\t" * tab_c + "<-- step back")
#             tab_c = tab_c-1
#             continue
#         except asn1.Error:
#             break
#     try:
#         if decoder.peek()[0] == asn1.Numbers.Sequence or decoder.peek()[0] == asn1.Numbers.Set:
#             print("\t" * tab_c + "Get sequence or set: ", decoder.peek())
#             tab_c = tab_c+1
#             decoder.enter()
#             continue
#     except:
#         continue
#
#     print("\t"*tab_c + "New value: ", decoder.read())



# answ = decoder.read()

# print("readed asn.1:", answ[1])

