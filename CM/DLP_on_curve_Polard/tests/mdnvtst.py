from util import modinv
from sage.all import *

def million_tests():
    for i in range(100):
        p = random_prime(2**256)
        a = randint(1, p)
        assert modinv(a, p) == inverse_mod(a, p)

def test_million():
    for i in range(1):
        million_tests()

