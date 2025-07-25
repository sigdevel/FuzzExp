

import sys
import unittest
import struct
import itertools
import functools
import contextlib
import hashlib
import binascii
import base64
try:
    from math import gcd
except ImportError:
    from fractions import gcd

from eccref import *
from testcrypt import *
from ssh import *

assert sys.version_info[:2] >= (3,0), "This is Python 3 code"

try:
    base64decode = base64.decodebytes
except AttributeError:
    base64decode = base64.decodestring

def unhex(s):
    return binascii.unhexlify(s.replace(" ", "").replace("\n", ""))

def rsa_bare(e, n):
    rsa = rsa_new()
    get_rsa_ssh1_pub(ssh_uint32(nbits(n)) + ssh1_mpint(e) + ssh1_mpint(n),
                     rsa, 'exponent_first')
    return rsa

def find_non_square_mod(p):
    
    
    return next(z for z in itertools.count(2) if jacobi(z, p) == -1)

def fibonacci_scattered(n=10):
    
    
    
    yield 0
    a, b, c = 0, 1, 1
    while True:
        yield b
        n -= 1
        if n <= 0:
            break
        a, b, c = (a**2+b**2, b*(a+c), b**2+c**2)

def fibonacci(n=10):
    
    a, b = 0, 1
    while True:
        yield a
        n -= 1
        if n <= 0:
            break
        a, b = b, a+b

def mp_mask(mp):
    
    
    
    
    
    return ((1 << mp_max_bits(mp))-1)

def adjtuples(iterable, n):
    
    
    
    it = iter(iterable)
    toret = [next(it) for _ in range(n-1)]
    for element in it:
        toret.append(element)
        yield tuple(toret)
        toret[:1] = []

def last(iterable):
    
    it = iter(iterable)
    toret = None
    for toret in it:
        pass
    return toret

@contextlib.contextmanager
def queued_random_data(nbytes, seed):
    hashsize = 512 // 8
    data = b''.join(
        hashlib.sha512("preimage:{:d}:{}".format(i, seed).encode('ascii'))
        .digest() for i in range((nbytes + hashsize - 1) // hashsize))
    data = data[:nbytes]
    random_queue(data)
    yield None
    random_clear()

@contextlib.contextmanager
def queued_specific_random_data(data):
    random_queue(data)
    yield None
    random_clear()

@contextlib.contextmanager
def random_prng(seed):
    random_make_prng('sha256', seed)
    yield None
    random_clear()

def hash_str(alg, message):
    h = ssh_hash_new(alg)
    ssh_hash_update(h, message)
    return ssh_hash_final(h)

def hash_str_iter(alg, message_iter):
    h = ssh_hash_new(alg)
    for string in message_iter:
        ssh_hash_update(h, string)
    return ssh_hash_final(h)

def mac_str(alg, key, message, cipher=None):
    m = ssh2_mac_new(alg, cipher)
    ssh2_mac_setkey(m, key)
    ssh2_mac_start(m)
    ssh2_mac_update(m, "dummy")
    
    ssh2_mac_start(m)
    ssh2_mac_update(m, message)
    return ssh2_mac_genresult(m)

def lcm(a, b):
    return a * b // gcd(a, b)

class MyTestBase(unittest.TestCase):
    "Intermediate class that adds useful helper methods."
    def assertEqualBin(self, x, y):
        
        
        self.assertEqual(binascii.hexlify(x), binascii.hexlify(y))

class mpint(MyTestBase):
    def testCreation(self):
        self.assertEqual(int(mp_new(128)), 0)
        self.assertEqual(int(mp_from_bytes_be(b'ABCDEFGHIJKLMNOP')),
                         0x4142434445464748494a4b4c4d4e4f50)
        self.assertEqual(int(mp_from_bytes_le(b'ABCDEFGHIJKLMNOP')),
                         0x504f4e4d4c4b4a494847464544434241)
        self.assertEqual(int(mp_from_integer(12345)), 12345)
        decstr = '91596559417721901505460351493238411077414937428167'
        self.assertEqual(int(mp_from_decimal_pl(decstr)), int(decstr, 10))
        self.assertEqual(int(mp_from_decimal(decstr)), int(decstr, 10))
        self.assertEqual(int(mp_from_decimal("")), 0)
        
        hexstr = 'ea7cb89f409ae845215822e37D32D0C63EC43E1381C2FF8094'
        self.assertEqual(int(mp_from_hex_pl(hexstr)), int(hexstr, 16))
        self.assertEqual(int(mp_from_hex(hexstr)), int(hexstr, 16))
        self.assertEqual(int(mp_from_hex("")), 0)
        p2 = mp_power_2(123)
        self.assertEqual(int(p2), 1 << 123)
        p2c = mp_copy(p2)
        self.assertEqual(int(p2c), 1 << 123)
        
        
        
        mp_set_bit(p2c, 120, 1)
        self.assertEqual(int(p2c), (1 << 123) + (1 << 120))
        self.assertEqual(int(p2), 1 << 123)

    def testBytesAndBits(self):
        x = mp_new(128)
        self.assertEqual(mp_get_byte(x, 2), 0)
        mp_set_bit(x, 2*8+3, 1)
        self.assertEqual(mp_get_byte(x, 2), 1<<3)
        self.assertEqual(mp_get_bit(x, 2*8+3), 1)
        mp_set_bit(x, 2*8+3, 0)
        self.assertEqual(mp_get_byte(x, 2), 0)
        self.assertEqual(mp_get_bit(x, 2*8+3), 0)
        
        
        
        self.assertEqual(mp_max_bytes(x), 128/8)
        self.assertEqual(mp_max_bits(x), 128)

        nb = lambda hexstr: mp_get_nbits(mp_from_hex(hexstr))
        self.assertEqual(nb('00000000000000000000000000000000'), 0)
        self.assertEqual(nb('00000000000000000000000000000001'), 1)
        self.assertEqual(nb('00000000000000000000000000000002'), 2)
        self.assertEqual(nb('00000000000000000000000000000003'), 2)
        self.assertEqual(nb('00000000000000000000000000000004'), 3)
        self.assertEqual(nb('000003ffffffffffffffffffffffffff'), 106)
        self.assertEqual(nb('000003ffffffffff0000000000000000'), 106)
        self.assertEqual(nb('80000000000000000000000000000000'), 128)
        self.assertEqual(nb('ffffffffffffffffffffffffffffffff'), 128)

    def testDecAndHex(self):
        def checkHex(hexstr):
            n = mp_from_hex(hexstr)
            i = int(hexstr, 16)
            self.assertEqual(mp_get_hex(n),
                             "{:x}".format(i).encode('ascii'))
            self.assertEqual(mp_get_hex_uppercase(n),
                             "{:X}".format(i).encode('ascii'))
        checkHex("0")
        checkHex("f")
        checkHex("00000000000000000000000000000000000000000000000000")
        checkHex("d5aa1acd5a9a1f6b126ed416015390b8dc5fceee4c86afc8c2")
        checkHex("ffffffffffffffffffffffffffffffffffffffffffffffffff")

        def checkDec(hexstr):
            n = mp_from_hex(hexstr)
            i = int(hexstr, 16)
            self.assertEqual(mp_get_decimal(n),
                             "{:d}".format(i).encode('ascii'))
        checkDec("0")
        checkDec("f")
        checkDec("00000000000000000000000000000000000000000000000000")
        checkDec("d5aa1acd5a9a1f6b126ed416015390b8dc5fceee4c86afc8c2")
        checkDec("ffffffffffffffffffffffffffffffffffffffffffffffffff")
        checkDec("f" * 512)

    def testComparison(self):
        inputs = [
            "0", "1", "2", "10", "314159265358979", "FFFFFFFFFFFFFFFF",

            
            
            "0000000000000000000000000000000000000000000000000000000000000000"
            "0000000000000000000000000000000000000000000000000000000000000000",

            "0000000000000000000000000000000000000000000000000000000000000000"
            "0000000000000000000000000000000000000000000000000000000000000001",

            "0000000000000000000000000000000000000000000000000000000000000000"
            "0000000000000000000000000000000000000000000000000000000000000002",

            "0000000000000000000000000000000000000000000000000000000000000000"
            "000000000000000000000000000000000000000000000000FFFFFFFFFFFFFFFF",

            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
            "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        ]
        values = [(mp_from_hex(s), int(s, 16)) for s in inputs]
        for am, ai in values:
            for bm, bi in values:
                self.assertEqual(mp_cmp_eq(am, bm) == 1, ai == bi)
                self.assertEqual(mp_cmp_hs(am, bm) == 1, ai >= bi)
                if (bi >> 64) == 0:
                    self.assertEqual(mp_eq_integer(am, bi) == 1, ai == bi)
                    self.assertEqual(mp_hs_integer(am, bi) == 1, ai >= bi)

                
                
                self.assertEqual(int(mp_min(am, bm)), min(ai, bi))
                self.assertEqual(int(mp_max(am, bm)), max(ai, bi))
                am_small = mp_copy(am if ai<bi else bm)
                mp_min_into(am_small, am, bm)
                self.assertEqual(int(am_small), min(ai, bi))
                am_big = mp_copy(am if ai>bi else bm)
                mp_max_into(am_big, am, bm)
                self.assertEqual(int(am_big), max(ai, bi))

        
        
        
        mp10 = mp_new(4)
        mp_copy_integer_into(mp10, 10)
        highbit = 1 << 63
        self.assertEqual(mp_hs_integer(mp10, highbit | 9), 0)
        self.assertEqual(mp_hs_integer(mp10, highbit | 10), 0)
        self.assertEqual(mp_hs_integer(mp10, highbit | 11), 0)
        self.assertEqual(mp_eq_integer(mp10, highbit | 9), 0)
        self.assertEqual(mp_eq_integer(mp10, highbit | 10), 0)
        self.assertEqual(mp_eq_integer(mp10, highbit | 11), 0)

    def testConditionals(self):
        testnumbers = [(mp_copy(n),n) for n in fibonacci_scattered()]
        for am, ai in testnumbers:
            for bm, bi in testnumbers:
                cm = mp_copy(am)
                mp_select_into(cm, am, bm, 0)
                self.assertEqual(int(cm), ai & mp_mask(am))
                mp_select_into(cm, am, bm, 1)
                self.assertEqual(int(cm), bi & mp_mask(am))

                mp_cond_add_into(cm, am, bm, 0)
                self.assertEqual(int(cm), ai & mp_mask(am))
                mp_cond_add_into(cm, am, bm, 1)
                self.assertEqual(int(cm), (ai+bi) & mp_mask(am))

                mp_cond_sub_into(cm, am, bm, 0)
                self.assertEqual(int(cm), ai & mp_mask(am))
                mp_cond_sub_into(cm, am, bm, 1)
                self.assertEqual(int(cm), (ai-bi) & mp_mask(am))

                maxbits = max(mp_max_bits(am), mp_max_bits(bm))
                cm = mp_new(maxbits)
                dm = mp_new(maxbits)
                mp_copy_into(cm, am)
                mp_copy_into(dm, bm)

                self.assertEqual(int(cm), ai)
                self.assertEqual(int(dm), bi)
                mp_cond_swap(cm, dm, 0)
                self.assertEqual(int(cm), ai)
                self.assertEqual(int(dm), bi)
                mp_cond_swap(cm, dm, 1)
                self.assertEqual(int(cm), bi)
                self.assertEqual(int(dm), ai)

                if bi != 0:
                    mp_cond_clear(cm, 0)
                    self.assertEqual(int(cm), bi)
                    mp_cond_clear(cm, 1)
                    self.assertEqual(int(cm), 0)

    def testBasicArithmetic(self):
        testnumbers = list(fibonacci_scattered(5))
        testnumbers.extend([1 << (1 << i) for i in range(3,10)])
        testnumbers.extend([(1 << (1 << i)) - 1 for i in range(3,10)])

        testnumbers = [(mp_copy(n),n) for n in testnumbers]

        for am, ai in testnumbers:
            for bm, bi in testnumbers:
                self.assertEqual(int(mp_add(am, bm)), ai + bi)
                self.assertEqual(int(mp_mul(am, bm)), ai * bi)
                
                diff = mp_sub(am, bm)
                self.assertEqual(int(diff), (ai - bi) & mp_mask(diff))

                for bits in range(64, 512, 64):
                    cm = mp_new(bits)
                    mp_add_into(cm, am, bm)
                    self.assertEqual(int(cm), (ai + bi) & mp_mask(cm))
                    mp_mul_into(cm, am, bm)
                    self.assertEqual(int(cm), (ai * bi) & mp_mask(cm))
                    mp_sub_into(cm, am, bm)
                    self.assertEqual(int(cm), (ai - bi) & mp_mask(cm))

        
        
        
        
        
        ai, bi = 0xb4ff6ed2c633847562087ed9354c5c17be212ac83b59c10c316250f50b7889e5b058bf6bfafd12825225ba225ede0cba583ffbd0882de88c9e62677385a6dbdedaf81959a273eb7909ebde21ae5d12e2a584501a6756fe50ccb93b93f0d6ee721b6052a0d88431e62f410d608532868cdf3a6de26886559e94cc2677eea9bd797918b70e2717e95b45918bd1f86530cb9989e68b632c496becff848aa1956cd57ed46676a65ce6dd9783f230c8796909eef5583fcfe4acbf9c8b4ea33a08ec3fd417cf7175f434025d032567a00fc329aee154ca20f799b961fbab8f841cb7351f561a44aea45746ceaf56874dad99b63a7d7af2769d2f185e2d1c656cc6630b5aba98399fa57, 0xb50a77c03ac195225021dc18d930a352f27c0404742f961ca828c972737bad3ada74b1144657ab1d15fe1b8aefde8784ad61783f3c8d4584aa5f22a4eeca619f90563ae351b5da46770df182cf348d8e23b25fda07670c6609118e916a57ce4043608752c91515708327e36f5bb5ebd92cd4cfb39424167a679870202b23593aa524bac541a3ad322c38102a01e9659b06a4335c78d50739a51027954ac2bf03e500f975c2fa4d0ab5dd84cc9334f219d2ae933946583e384ed5dbf6498f214480ca66987b867df0f69d92e4e14071e4b8545212dd5e29ff0248ed751e168d78934da7930bcbe10e9a212128a68de5d749c61f5e424cf8cf6aa329674de0cf49c6f9b4c8b8cc3
        am = mp_copy(ai)
        bm = mp_copy(bi)
        self.assertEqual(int(mp_mul(am, bm)), ai * bi)

        
        
        
        ai, bi = (2**8512 * 2 // 3), (2**4224 * 11 // 15)
        am = mp_copy(ai)
        bm = mp_copy(bi)
        self.assertEqual(int(mp_mul(am, bm)), ai * bi)

    def testAddInteger(self):
        initial = mp_copy(4444444444444444444444444)

        x = mp_new(mp_max_bits(initial) + 64)

        
        
        mp_add_integer_into(x, initial, 123123123123123)
        self.assertEqual(int(x), 4444444444567567567567567)
        mp_sub_integer_into(x, initial, 123123123123123)
        self.assertEqual(int(x), 4444444444321321321321321)
        mp_copy_integer_into(x, 123123123123123)
        self.assertEqual(int(x), 123123123123123)

        
        mp_mul_integer_into(x, initial, 10001)
        self.assertEqual(int(x), 44448888888888888888888884444)

    def testDivision(self):
        divisors = [1, 2, 3, 2**16+1, 2**32-1, 2**32+1, 2**128-159,
                    141421356237309504880168872420969807856967187537694807]
        quotients = [0, 1, 2, 2**64-1, 2**64, 2**64+1, 17320508075688772935]
        for d in divisors:
            for q in quotients:
                remainders = {0, 1, d-1, 2*d//3}
                for r in sorted(remainders):
                    if r >= d:
                        continue 
                    n = q*d + r
                    mq = mp_new(max(nbits(q), 1))
                    mr = mp_new(max(nbits(r), 1))
                    mp_divmod_into(n, d, mq, mr)
                    self.assertEqual(int(mq), q)
                    self.assertEqual(int(mr), r)
                    self.assertEqual(int(mp_div(n, d)), q)
                    self.assertEqual(int(mp_mod(n, d)), r)

                    
                    
                    mp_clear(mq)
                    mp_divmod_into(n, d, mq, None)
                    self.assertEqual(int(mq), q)
                    mp_clear(mr)
                    mp_divmod_into(n, d, None, mr)
                    self.assertEqual(int(mr), r)
                    mp_divmod_into(n, d, None, None)
                    
                    

    def testNthRoot(self):
        roots = [1, 13, 1234567654321,
                 57721566490153286060651209008240243104215933593992]
        tests = []
        tests.append((0, 2, 0, 0))
        tests.append((0, 3, 0, 0))
        for r in roots:
            for n in 2, 3, 5:
                tests.append((r**n, n, r, 0))
                tests.append((r**n+1, n, r, 1))
                tests.append((r**n-1, n, r-1, r**n - (r-1)**n - 1))
        for x, n, eroot, eremainder in tests:
            with self.subTest(x=x):
                mx = mp_copy(x)
                remainder = mp_copy(mx)
                root = mp_nthroot(x, n, remainder)
                self.assertEqual(int(root), eroot)
                self.assertEqual(int(remainder), eremainder)
        self.assertEqual(int(mp_nthroot(2*10**100, 2, None)),
                         141421356237309504880168872420969807856967187537694)
        self.assertEqual(int(mp_nthroot(3*10**150, 3, None)),
                         144224957030740838232163831078010958839186925349935)

    def testBitwise(self):
        p = 0x3243f6a8885a308d313198a2e03707344a4093822299f31d0082efa98ec4e
        e = 0x2b7e151628aed2a6abf7158809cf4f3c762e7160f38b4da56a784d9045190
        x = mp_new(nbits(p))

        mp_and_into(x, p, e)
        self.assertEqual(int(x), p & e)

        mp_or_into(x, p, e)
        self.assertEqual(int(x), p | e)

        mp_xor_into(x, p, e)
        self.assertEqual(int(x), p ^ e)

        mp_bic_into(x, p, e)
        self.assertEqual(int(x), p & ~e)

    def testInversion(self):
        
        testnumbers = [(mp_copy(n),n) for n in fibonacci_scattered()
                       if n & 1]
        for power2 in [1, 2, 3, 5, 13, 32, 64, 127, 128, 129]:
            for am, ai in testnumbers:
                bm = mp_invert_mod_2to(am, power2)
                bi = int(bm)
                self.assertEqual(((ai * bi) & ((1 << power2) - 1)), 1)

                
                
                rm = mp_copy(am)
                mp_reduce_mod_2to(rm, power2)
                self.assertEqual(int(rm), ai & ((1 << power2) - 1))

        
        moduli = [2, 3, 2**16+1, 2**32-1, 2**32+1, 2**128-159,
                  141421356237309504880168872420969807856967187537694807,
                  2**128-1]
        for m in moduli:
            
            
            mc = monty_new(m) if m & 1 else None

            to_invert = {1, 2, 3, 7, 19, m-1, 5*m//17, (m-1)//2, (m+1)//2}
            for x in sorted(to_invert):
                if gcd(x, m) != 1:
                    continue 
                inv = int(mp_invert(x, m))
                assert x * inv % m == 1

                
                if mc is not None:
                    self.assertEqual(
                        int(monty_invert(mc, monty_import(mc, x))),
                        int(monty_import(mc, inv)))

    def testGCD(self):
        powerpairs = [(0,0), (1,0), (1,1), (2,1), (2,2), (75,3), (17,23)]
        for a2, b2 in powerpairs:
            for a3, b3 in powerpairs:
                for a5, b5 in powerpairs:
                    a = 2**a2 * 3**a3 * 5**a5 * 17 * 19 * 23
                    b = 2**b2 * 3**b3 * 5**b5 * 65423
                    d = 2**min(a2, b2) * 3**min(a3, b3) * 5**min(a5, b5)

                    ma = mp_copy(a)
                    mb = mp_copy(b)

                    self.assertEqual(int(mp_gcd(ma, mb)), d)

                    md = mp_new(nbits(d))
                    mA = mp_new(nbits(b))
                    mB = mp_new(nbits(a))
                    mp_gcd_into(ma, mb, md, mA, mB)
                    self.assertEqual(int(md), d)
                    A = int(mA)
                    B = int(mB)
                    self.assertEqual(a*A - b*B, d)
                    self.assertTrue(0 <= A < b//d)
                    self.assertTrue(0 <= B < a//d)

                    self.assertEqual(mp_coprime(ma, mb), 1 if d==1 else 0)

                    
                    
                    mp_clear(md)
                    mp_gcd_into(ma, mb, md, None, None)
                    self.assertEqual(int(md), d)
                    mp_clear(mA)
                    mp_gcd_into(ma, mb, None, mA, None)
                    self.assertEqual(int(mA), A)
                    mp_clear(mB)
                    mp_gcd_into(ma, mb, None, None, mB)
                    self.assertEqual(int(mB), B)
                    mp_gcd_into(ma, mb, None, None, None)
                    
                    

    def testMonty(self):
        moduli = [5, 19, 2**16+1, 2**31-1, 2**128-159, 2**255-19,
                  293828847201107461142630006802421204703,
                  113064788724832491560079164581712332614996441637880086878209969852674997069759]

        for m in moduli:
            mc = monty_new(m)

            
            inputs = [(monty_import(mc, n), n)
                      for n in sorted({0, 1, 2, 3, 2*m//3, m-1})]

            
            self.assertEqual(int(monty_modulus(mc)), m)
            self.assertEqual(int(monty_identity(mc)), int(inputs[1][0]))

            
            for mn, n in inputs:
                self.assertEqual(int(monty_export(mc, mn)), n)

            for ma, a in inputs:
                for mb, b in inputs:
                    xprod = int(monty_export(mc, monty_mul(mc, ma, mb)))
                    self.assertEqual(xprod, a*b % m)

                    xsum = int(monty_export(mc, monty_add(mc, ma, mb)))
                    self.assertEqual(xsum, (a+b) % m)

                    xdiff = int(monty_export(mc, monty_sub(mc, ma, mb)))
                    self.assertEqual(xdiff, (a-b) % m)

                    
                    
                    

                    xprod = int(mp_modmul(a, b, m))
                    self.assertEqual(xprod, a*b % m)

                    xsum = int(mp_modadd(a, b, m))
                    self.assertEqual(xsum, (a+b) % m)

                    xdiff = int(mp_modsub(a, b, m))
                    self.assertEqual(xdiff, (a-b) % m)

            for ma, a in inputs:
                
                indices = list(fibonacci())
                powers = [int(monty_export(mc, monty_pow(mc, ma, power)))
                          for power in indices]
                
                self.assertEqual(powers[0], 1)
                self.assertEqual(powers[1], a)
                
                
                for p0, p1, p2 in adjtuples(powers, 3):
                    self.assertEqual(p2, p0 * p1 % m)

                
                
                for index, power in zip(indices, powers):
                    self.assertEqual(int(mp_modpow(a, index, m)), power)

        
        
        
        b, e, m = 0x2B5B93812F253FF91F56B3B4DAD01CA2884B6A80719B0DA4E2159A230C6009EDA97C5C8FD4636B324F9594706EE3AD444831571BA5E17B1B2DFA92DEA8B7E, 0x25, 0xC8FCFD0FD7371F4FE8D0150EFC124E220581569587CCD8E50423FA8D41E0B2A0127E100E92501E5EE3228D12EA422A568C17E0AD2E5C5FCC2AE9159D2B7FB8CB
        assert(int(mp_modpow(b, e, m)) == pow(b, e, m))

        
        
        assert(int(mp_modpow(1<<877, 907, 999979)) == pow(2, 877*907, 999979))

    def testModsqrt(self):
        moduli = [
            5, 19, 2**16+1, 2**31-1, 2**128-159, 2**255-19,
            293828847201107461142630006802421204703,
            113064788724832491560079164581712332614996441637880086878209969852674997069759,
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF6FFFFFFFF00000001]
        for p in moduli:
            
            
            factors_of_2 = nbits((p-1) & (1-p)) - 1
            assert (p & ((2 << factors_of_2)-1)) == ((1 << factors_of_2)+1)

            z = find_non_square_mod(p)

            sc = modsqrt_new(p, z)

            def ptest(x):
                root, success = mp_modsqrt(sc, x)
                r = int(root)
                self.assertTrue(success)
                self.assertEqual((r * r - x) % p, 0)

            def ntest(x):
                root, success = mp_modsqrt(sc, x)
                self.assertFalse(success)

            
            v1 = pow(3, nbits(p), p)
            v2 = pow(5, v1, p)
            test_roots = [0, 1, 2, 3, 4, 3*p//4, v1, v2, v1+1, 12873*v1, v1*v2]
            known_squares = {r*r % p for r in test_roots}
            for s in known_squares:
                ptest(s)
                if s != 0:
                    ntest(z*s % p)

            
            
            
            
            
            
            
            
            vbase = z
            for k in range(factors_of_2):
                
                
                
                vbase = vbase * pow(z, (vbase + v1 + v2) | 1, p) % p

                
                
                vbase = pow(vbase, 2, p)

                ptest(vbase)

    def testShifts(self):
        x = ((1<<900) // 9949) | 1
        for i in range(2049):
            mp = mp_copy(x)

            mp_lshift_fixed_into(mp, mp, i)
            self.assertEqual(int(mp), (x << i) & mp_mask(mp))

            mp_copy_into(mp, x)
            mp_lshift_safe_into(mp, mp, i)
            self.assertEqual(int(mp), (x << i) & mp_mask(mp))

            mp_copy_into(mp, x)
            mp_rshift_fixed_into(mp, mp, i)
            self.assertEqual(int(mp), x >> i)

            mp_copy_into(mp, x)
            mp_rshift_safe_into(mp, mp, i)
            self.assertEqual(int(mp), x >> i)

            self.assertEqual(int(mp_rshift_fixed(x, i)), x >> i)

            self.assertEqual(int(mp_rshift_safe(x, i)), x >> i)

    def testRandom(self):
        
        
        
        for bits in range(512):
            bytes_needed = (bits + 7) // 8
            with queued_random_data(bytes_needed, "random_bits test"):
                mp = mp_random_bits(bits)
                self.assertTrue(int(mp) < (1 << bits))
                self.assertEqual(random_queue_len(), 0)

        
        
        for rangesize in [2, 3, 19, 35]:
            for lo in [0, 1, 0x10001, 1<<512]:
                hi = lo + rangesize
                bytes_needed = mp_max_bytes(hi) + 16
                for trial in range(rangesize*3):
                    with queued_random_data(
                            bytes_needed,
                            "random_in_range {:d}".format(trial)):
                        v = int(mp_random_in_range(lo, hi))
                        self.assertTrue(lo <= v < hi)

class ecc(MyTestBase):
    def testWeierstrassSimple(self):
        
        
        
        

        p = 3141592661
        a, b = -3 % p, 12345
        rc = WeierstrassCurve(p, a, b)
        wc = ecc_weierstrass_curve(p, a, b, None)

        def check_point(wp, rp):
            self.assertTrue(ecc_weierstrass_point_valid(wp))
            is_id = ecc_weierstrass_is_identity(wp)
            x, y = ecc_weierstrass_get_affine(wp)
            if rp.infinite:
                self.assertEqual(is_id, 1)
            else:
                self.assertEqual(is_id, 0)
                self.assertEqual(int(x), int(rp.x))
                self.assertEqual(int(y), int(rp.y))

        def make_point(x, y):
            wp = ecc_weierstrass_point_new(wc, x, y)
            rp = rc.point(x, y)
            check_point(wp, rp)
            return wp, rp

        
        
        wI, rI = ecc_weierstrass_point_new_identity(wc), rc.point()
        wP, rP = make_point(102, 387427089)
        wQ, rQ = make_point(1000, 546126574)
        wmP, rmP = make_point(102, p - 387427089)

        
        check_point(ecc_weierstrass_add(wP, wQ), rP + rQ)
        check_point(ecc_weierstrass_add(wQ, wP), rP + rQ)
        check_point(ecc_weierstrass_double(wP), rP + rP)
        check_point(ecc_weierstrass_double(wQ), rQ + rQ)

        
        
        check_point(ecc_weierstrass_add_general(wP, wQ), rP + rQ)
        
        check_point(ecc_weierstrass_add_general(wP, wP), rP + rP)
        check_point(ecc_weierstrass_add_general(wQ, wQ), rQ + rQ)
        
        check_point(ecc_weierstrass_add_general(wI, wP), rP)
        check_point(ecc_weierstrass_add_general(wI, wQ), rQ)
        check_point(ecc_weierstrass_add_general(wP, wI), rP)
        check_point(ecc_weierstrass_add_general(wQ, wI), rQ)
        
        check_point(ecc_weierstrass_add_general(wI, wI), rI)
        
        check_point(ecc_weierstrass_add_general(wmP, wP), rI)
        check_point(ecc_weierstrass_add_general(wP, wmP), rI)

        
        bogus = ecc_weierstrass_point_new(wc, int(rP.x), int(rP.y * 3))
        self.assertFalse(ecc_weierstrass_point_valid(bogus))

        
        
        
        wc = ecc_weierstrass_curve(p, a, b, find_non_square_mod(p))

        x, yp = int(rP.x), (int(rP.y) & 1)
        check_point(ecc_weierstrass_point_new_from_x(wc, x, yp), rP)
        check_point(ecc_weierstrass_point_new_from_x(wc, x, yp ^ 1), rmP)
        x, yp = int(rQ.x), (int(rQ.y) & 1)
        check_point(ecc_weierstrass_point_new_from_x(wc, x, yp), rQ)

    def testMontgomerySimple(self):
        p, a, b = 3141592661, 0xabc, 0xde

        rc = MontgomeryCurve(p, a, b)
        mc = ecc_montgomery_curve(p, a, b)

        rP = rc.cpoint(0x1001)
        rQ = rc.cpoint(0x20001)
        rdiff = rP - rQ
        rsum = rP + rQ

        def make_mpoint(rp):
            return ecc_montgomery_point_new(mc, int(rp.x))

        mP = make_mpoint(rP)
        mQ = make_mpoint(rQ)
        mdiff = make_mpoint(rdiff)
        msum = make_mpoint(rsum)

        def check_point(mp, rp):
            x = ecc_montgomery_get_affine(mp)
            self.assertEqual(int(x), int(rp.x))

        check_point(ecc_montgomery_diff_add(mP, mQ, mdiff), rsum)
        check_point(ecc_montgomery_diff_add(mQ, mP, mdiff), rsum)
        check_point(ecc_montgomery_diff_add(mP, mQ, msum), rdiff)
        check_point(ecc_montgomery_diff_add(mQ, mP, msum), rdiff)
        check_point(ecc_montgomery_double(mP), rP + rP)
        check_point(ecc_montgomery_double(mQ), rQ + rQ)

        zero = ecc_montgomery_point_new(mc, 0)
        self.assertEqual(ecc_montgomery_is_identity(zero), False)
        identity = ecc_montgomery_double(zero)
        ecc_montgomery_get_affine(identity)
        self.assertEqual(ecc_montgomery_is_identity(identity), True)

    def testEdwardsSimple(self):
        p, d, a = 3141592661, 2688750488, 367934288

        rc = TwistedEdwardsCurve(p, d, a)
        ec = ecc_edwards_curve(p, d, a, None)

        def check_point(ep, rp):
            x, y = ecc_edwards_get_affine(ep)
            self.assertEqual(int(x), int(rp.x))
            self.assertEqual(int(y), int(rp.y))

        def make_point(x, y):
            ep = ecc_edwards_point_new(ec, x, y)
            rp = rc.point(x, y)
            check_point(ep, rp)
            return ep, rp

        
        
        eI, rI = make_point(0, 1)
        eP, rP = make_point(196270812, 1576162644)
        eQ, rQ = make_point(1777630975, 2717453445)
        emP, rmP = make_point(p - 196270812, 1576162644)

        
        

        
        check_point(ecc_edwards_add(eP, eQ), rP + rQ)
        check_point(ecc_edwards_add(eQ, eP), rP + rQ)
        
        check_point(ecc_edwards_add(eP, eP), rP + rP)
        check_point(ecc_edwards_add(eQ, eQ), rQ + rQ)
        
        check_point(ecc_edwards_add(eI, eP), rP)
        check_point(ecc_edwards_add(eI, eQ), rQ)
        check_point(ecc_edwards_add(eP, eI), rP)
        check_point(ecc_edwards_add(eQ, eI), rQ)
        
        check_point(ecc_edwards_add(eI, eI), rI)
        
        check_point(ecc_edwards_add(emP, eP), rI)
        check_point(ecc_edwards_add(eP, emP), rI)

        
        
        
        ec = ecc_edwards_curve(p, d, a, find_non_square_mod(p))

        y, xp = int(rP.y), (int(rP.x) & 1)
        check_point(ecc_edwards_point_new_from_y(ec, y, xp), rP)
        check_point(ecc_edwards_point_new_from_y(ec, y, xp ^ 1), rmP)
        y, xp = int(rQ.y), (int(rQ.x) & 1)
        check_point(ecc_edwards_point_new_from_y(ec, y, xp), rQ)

    
    

    def testWeierstrassMultiply(self):
        wc = ecc_weierstrass_curve(p256.p, int(p256.a), int(p256.b), None)
        wG = ecc_weierstrass_point_new(wc, int(p256.G.x), int(p256.G.y))
        self.assertTrue(ecc_weierstrass_point_valid(wG))

        ints = set(i % p256.p for i in fibonacci_scattered(10))
        ints.remove(0) 
        for i in sorted(ints):
            wGi = ecc_weierstrass_multiply(wG, i)
            x, y = ecc_weierstrass_get_affine(wGi)
            rGi = p256.G * i
            self.assertEqual(int(x), int(rGi.x))
            self.assertEqual(int(y), int(rGi.y))

    def testMontgomeryMultiply(self):
        mc = ecc_montgomery_curve(
            curve25519.p, int(curve25519.a), int(curve25519.b))
        mG = ecc_montgomery_point_new(mc, int(curve25519.G.x))

        ints = set(i % p256.p for i in fibonacci_scattered(10))
        ints.remove(0) 
        for i in sorted(ints):
            mGi = ecc_montgomery_multiply(mG, i)
            x = ecc_montgomery_get_affine(mGi)
            rGi = curve25519.G * i
            self.assertEqual(int(x), int(rGi.x))

    def testEdwardsMultiply(self):
        ec = ecc_edwards_curve(ed25519.p, int(ed25519.d), int(ed25519.a), None)
        eG = ecc_edwards_point_new(ec, int(ed25519.G.x), int(ed25519.G.y))

        ints = set(i % ed25519.p for i in fibonacci_scattered(10))
        ints.remove(0) 
        for i in sorted(ints):
            eGi = ecc_edwards_multiply(eG, i)
            x, y = ecc_edwards_get_affine(eGi)
            rGi = ed25519.G * i
            self.assertEqual(int(x), int(rGi.x))
            self.assertEqual(int(y), int(rGi.y))

class keygen(MyTestBase):
    def testPrimeCandidateSource(self):
        def inspect(pcs):
            
            return tuple(map(int, pcs_inspect(pcs)))

        
        
        
        
        
        
        
        
        
        

        def check(pcs, lo, hi, mod_res_pairs):
            limit, factor, addend = inspect(pcs)

            for mod, res in mod_res_pairs:
                self.assertEqual(addend % mod, res % mod)

            self.assertEqual(factor, functools.reduce(
                lcm, [mod for mod, res in mod_res_pairs]))

            self.assertFalse(lo <= addend +      (-1) * factor < hi)
            self.assertTrue (lo <= addend                      < hi)
            self.assertTrue (lo <= addend + (limit-1) * factor < hi)
            self.assertFalse(lo <= addend +  limit    * factor < hi)

        pcs = pcs_new(64)
        check(pcs, 2**63, 2**64, [(2, 1)])
        pcs_require_residue(pcs, 3, 2)
        check(pcs, 2**63, 2**64, [(2, 1), (3, 2)])
        pcs_require_residue_1(pcs, 7)
        check(pcs, 2**63, 2**64, [(2, 1), (3, 2), (7, 1)])
        pcs_require_residue(pcs, 16, 7)
        check(pcs, 2**63, 2**64, [(2, 1), (3, 2), (7, 1), (16, 7)])
        pcs_require_residue(pcs, 49, 8)
        check(pcs, 2**63, 2**64, [(2, 1), (3, 2), (7, 1), (16, 7), (49, 8)])

        
        
        
        pcs = pcs_new_with_firstbits(64, 0xAB, 8)
        pcs_require_residue(pcs, 0x100, 0xCD)
        pcs_require_residue_1(pcs, 65537)
        pcs_avoid_residue_small(pcs, 5, 3)
        pcs_ready(pcs)
        with random_prng("test seed"):
            for i in range(100):
                n = int(pcs_generate(pcs))
                self.assertTrue((0xAB<<56) < n < (0xAC<<56))
                self.assertEqual(n % 0x100, 0xCD)
                self.assertEqual(n % 65537, 1)
                self.assertNotEqual(n % 5, 3)

                
                
                
                
                
                
                
                
                
                

                for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61]:
                    self.assertNotEqual(n % p, 0)

    def testPocklePositive(self):
        def add_small(po, *ps):
            for p in ps:
                self.assertEqual(pockle_add_small_prime(po, p), 'POCKLE_OK')
        def add(po, *args):
            self.assertEqual(pockle_add_prime(po, *args), 'POCKLE_OK')

        
        
        po = pockle_new()
        p1 = (2**130 - 6) // 1517314646
        p2 = (p1 - 1) // 222890620702
        add_small(po, 37003, 221101)
        add(po, p2, [37003, 221101], 2)
        add(po, p1, [p2], 2)
        add(po, 2**130 - 5, [p1], 2)

        
        po = pockle_new()
        p1 = 8574133
        p2 = 1919519569386763
        p3 = 75445702479781427272750846543864801
        p4 = (2**255 - 20) // (65147*12)
        p = 2**255 - 19
        add_small(po, p1)
        add(po, p2, [p1], 2)
        add(po, p3, [p2], 2)
        add(po, p4, [p3], 2)
        add(po, p, [p4], 2)

        
        po = pockle_new()
        p1 = 379979
        p2 = 1764234391
        p3 = 97859369123353
        p4 = 34741861125639557
        p5 = 36131535570665139281
        p6 = 167773885276849215533569
        p7 = 596242599987116128415063
        p = 2**448 - 2**224 - 1
        add_small(po, p1, p2)
        add(po, p3, [p1], 2)
        add(po, p4, [p2], 2)
        add(po, p5, [p4], 2)
        add(po, p6, [p3], 3)
        add(po, p7, [p5], 3)
        add(po, p, [p6, p7], 2)

        p = 4095744004479977
        factors = [2, 79999] 
        po = pockle_new()
        for q in factors:
            add_small(po, q)
        add(po, p, factors, 3)

        
        po = pockle_new()
        p1a, p1b = 132667, 137849
        p2 = 3044861653679985063343
        p3 = 198211423230930754013084525763697
        p = 2**252 + 0x14def9dea2f79cd65812631a5cf5d3ed
        add_small(po, p1a, p1b)
        add(po, p2, [p1a, p1b], 2)
        add(po, p3, [p2], 2)
        add(po, p, [p3], 2)

        
        po = pockle_new()
        p1 = 766223
        p2 = 3009341
        p3 = 7156907
        p4 = 671065561
        p5 = 342682509629
        p6 = 6730519843040614479184435237013
        p = 2**446 - 0x8335dc163bb124b65129c96fde933d8d723a70aadc873d6d54a7bb0d
        add_small(po, p1, p2, p3, p4)
        add(po, p5, [p1], 2)
        add(po, p6, [p3,p4], 2)
        add(po, p, [p2,p5,p6], 2)

    def testPockleNegative(self):
        def add_small(po, p):
            self.assertEqual(pockle_add_small_prime(po, p), 'POCKLE_OK')

        po = pockle_new()
        self.assertEqual(pockle_add_small_prime(po, 0),
                         'POCKLE_PRIME_SMALLER_THAN_2')
        self.assertEqual(pockle_add_small_prime(po, 1),
                         'POCKLE_PRIME_SMALLER_THAN_2')
        self.assertEqual(pockle_add_small_prime(po, 2**61 - 1),
                         'POCKLE_SMALL_PRIME_NOT_SMALL')
        self.assertEqual(pockle_add_small_prime(po, 4),
                         'POCKLE_SMALL_PRIME_NOT_PRIME')

        po = pockle_new()
        self.assertEqual(pockle_add_prime(po, 1919519569386763, [8574133], 2),
                         'POCKLE_FACTOR_NOT_KNOWN_PRIME')

        po = pockle_new()
        add_small(po, 8574133)
        self.assertEqual(pockle_add_prime(po, 1919519569386765, [8574133], 2),
                         'POCKLE_FACTOR_NOT_A_FACTOR')

        p = 4095744004479977
        factors = [2, 79997] 
        po = pockle_new()
        for q in factors:
            add_small(po, q)
        self.assertEqual(pockle_add_prime(po, p, factors, 3),
                         'POCKLE_PRODUCT_OF_FACTORS_TOO_SMALL')

        p = 1999527 * 3999053
        factors = [999763]
        po = pockle_new()
        for q in factors:
            add_small(po, q)
        self.assertEqual(pockle_add_prime(po, p, factors, 3),
                         'POCKLE_DISCRIMINANT_IS_SQUARE')

        p = 9999929 * 9999931
        factors = [257, 2593]
        po = pockle_new()
        for q in factors:
            add_small(po, q)
        self.assertEqual(pockle_add_prime(po, p, factors, 3),
                         'POCKLE_FERMAT_TEST_FAILED')

        p = 1713000920401 
        po = pockle_new()
        add_small(po, 561787)
        self.assertEqual(pockle_add_prime(po, p, [561787], 2),
                         'POCKLE_WITNESS_POWER_IS_1')

        p = 4294971121
        factors = [3, 5, 11, 17]
        po = pockle_new()
        for q in factors:
            add_small(po, q)
        self.assertEqual(pockle_add_prime(po, p, factors, 17),
                         'POCKLE_WITNESS_POWER_NOT_COPRIME')

        po = pockle_new()
        add_small(po, 2)
        self.assertEqual(pockle_add_prime(po, 1, [2], 1),
                         'POCKLE_PRIME_SMALLER_THAN_2')

class crypt(MyTestBase):
    def testSSH1Fingerprint(self):
        
        
        rsa = rsa_bare(65537, 984185866443261798625575612408956568591522723900235822424492423996716524817102482330189709310179009158443944785704183009867662230534501187034891091310377917105259938712348098594526746211645472854839799025154390701673823298369051411)
        fp = rsa_ssh1_fingerprint(rsa)
        self.assertEqual(
            fp, b"768 96:12:c8:bc:e6:03:75:86:e8:c7:b9:af:d8:0c:15:75")

    def testAES(self):
        
        
        

        def vector(cipher, key, iv, plaintext, ciphertext):
            for suffix in "hw", "sw":
                c = ssh_cipher_new("{}_{}".format(cipher, suffix))
                if c is None: return 
                ssh_cipher_setkey(c, key)
                ssh_cipher_setiv(c, iv)
                self.assertEqualBin(
                    ssh_cipher_encrypt(c, plaintext), ciphertext)
                ssh_cipher_setiv(c, iv)
                self.assertEqualBin(
                    ssh_cipher_decrypt(c, ciphertext), plaintext)

        

        key = unhex(
            '98483c6eb40b6c31a448c22a66ded3b5e5e8d5119cac8327b655c8b5c4836489')
        iv = unhex('38f87b0b9b736160bfc0cbd8447af6ee')
        plaintext = unhex('''
        ee16271827b12d828f61d56fddccc38ccaa69601da2b36d3af1a34c51947b71a
        362f05e07bf5e7766c24599799b252ad2d5954353c0c6ca668c46779c2659c94
        8df04e4179666e335470ff042e213c8bcff57f54842237fbf9f3c7e6111620ac
        1c007180edd25f0e337c2a49d890a7173f6b52d61e3d2a21ddc8e41513a0e825
        afd5932172270940b01014b5b7fb8495946151520a126518946b44ea32f9b2a9
        ''')

        vector('aes128_cbc', key[:16], iv, plaintext, unhex('''
        547ee90514cb6406d5bb00855c8092892c58299646edda0b4e7c044247795c8d
        3c3eb3d91332e401215d4d528b94a691969d27b7890d1ae42fe3421b91c989d5
        113fefa908921a573526259c6b4f8e4d90ea888e1d8b7747457ba3a43b5b79b9
        34873ebf21102d14b51836709ee85ed590b7ca618a1e884f5c57c8ea73fe3d0d
        6bf8c082dd602732bde28131159ed0b6e9cf67c353ffdd010a5a634815aaa963'''))

        vector('aes192_cbc', key[:24], iv, plaintext, unhex('''
        e3dee5122edd3fec5fab95e7db8c784c0cb617103e2a406fba4ae3b4508dd608
        4ff5723a670316cc91ed86e413c11b35557c56a6f5a7a2c660fc6ee603d73814
        73a287645be0f297cdda97aef6c51faeb2392fec9d33adb65138d60f954babd9
        8ee0daab0d1decaa8d1e07007c4a3c7b726948025f9fb72dd7de41f74f2f36b4
        23ac6a5b4b6b39682ec74f57d9d300e547f3c3e467b77f5e4009923b2f94c903'''))

        vector('aes256_cbc', key[:32], iv, plaintext, unhex('''
        088c6d4d41997bea79c408925255266f6c32c03ea465a5f607c2f076ec98e725
        7e0beed79609b3577c16ebdf17d7a63f8865278e72e859e2367de81b3b1fe9ab
        8f045e1d008388a3cfc4ff87daffedbb47807260489ad48566dbe73256ce9dd4
        ae1689770a883b29695928f5983f33e8d7aec4668f64722e943b0b671c365709
        dfa86c648d5fb00544ff11bd29121baf822d867e32da942ba3a0d26299bcee13'''))

        
        
        

        sdctrIVs = [
            unhex('38f87b0b9b736160bfc0cbd8447af6ee'),
            unhex('fffffffffffffffffffffffffffffffe'),
        ]

        vector('aes128_ctr', key[:16], sdctrIVs[0], plaintext[:64], unhex('''
        d0061d7b6e8c4ef4fe5614b95683383f46cdd2766e66b6fb0b0f0b3a24520b2d
        15d869b06cbf685ede064bcf8fb5fb6726cfd68de7016696a126e9e84420af38'''))
        vector('aes128_ctr', key[:16], sdctrIVs[1], plaintext[:64], unhex('''
        49ac67164fd9ce8701caddbbc9a2b06ac6524d4aa0fdac95253971974b8f3bc2
        bb8d7c970f6bcd79b25218cc95582edf7711aae2384f6cf91d8d07c9d9b370bc'''))

        vector('aes192_ctr', key[:24], sdctrIVs[0], plaintext[:64], unhex('''
        0baa86acbe8580845f0671b7ebad4856ca11b74e5108f515e34e54fa90f87a9a
        c6eee26686253c19156f9be64957f0dbc4f8ecd7cabb1f4e0afefe33888faeec'''))
        vector('aes192_ctr', key[:24], sdctrIVs[1], plaintext[:64], unhex('''
        2da1791250100dc0d1461afe1bbfad8fa0320253ba5d7905d837386ba0a3a41f
        01965c770fcfe01cf307b5316afb3981e0e4aa59a6e755f0a5784d9accdc52be'''))

        vector('aes256_ctr', key[:32], sdctrIVs[0], plaintext[:64], unhex('''
        49c7b284222d408544c770137b6ef17ef770c47e24f61fa66e7e46cae4888882
        f980a0f2446956bf47d2aed55ebd2e0694bfc46527ed1fd33efe708fec2f8b1f'''))
        vector('aes256_ctr', key[:32], sdctrIVs[1], plaintext[:64], unhex('''
        f1d013c3913ccb4fc0091e25d165804480fb0a1d5c741bf012bba144afda6db2
        c512f3942018574bd7a8fdd88285a73d25ef81e621aebffb6e9b8ecc8e2549d4'''))

    def testAESSDCTR(self):
        
        
        
        
        
        
        

        def increment(keylen, suffix, iv):
            key = b'\xab' * (keylen//8)
            sdctr = ssh_cipher_new("aes{}_ctr_{}".format(keylen, suffix))
            if sdctr is None: return 
            ssh_cipher_setkey(sdctr, key)
            cbc = ssh_cipher_new("aes{}_cbc_{}".format(keylen, suffix))
            ssh_cipher_setkey(cbc, key)

            ssh_cipher_setiv(sdctr, iv)
            ec0 = ssh_cipher_encrypt(sdctr, b'\x00' * 16)
            ec1 = ssh_cipher_encrypt(sdctr, b'\x00' * 16)
            ssh_cipher_setiv(cbc, b'\x00' * 16)
            dc0 = ssh_cipher_decrypt(cbc, ec0)
            ssh_cipher_setiv(cbc, b'\x00' * 16)
            dc1 = ssh_cipher_decrypt(cbc, ec1)
            self.assertEqualBin(iv, dc0)
            return dc1

        def test(keylen, suffix, ivInteger):
            mask = (1 << 128) - 1
            ivInteger &= mask
            ivBinary = unhex("{:032x}".format(ivInteger))
            ivIntegerInc = (ivInteger + 1) & mask
            ivBinaryInc = unhex("{:032x}".format((ivIntegerInc)))
            actualResult = increment(keylen, suffix, ivBinary)
            if actualResult is not None:
                self.assertEqualBin(actualResult, ivBinaryInc)

        
        
        
        
        
        
        

        for suffix in "hw", "sw":
            for keylen in [128, 192, 256]:
                hexTestValues = ["00000000", "00000001", "ffffffff"]
                for ivHexBytes in itertools.product(*([hexTestValues] * 4)):
                    ivInteger = int("".join(ivHexBytes), 16)
                    test(keylen, suffix, ivInteger)

    def testAESParallelism(self):
        
        
        

        
        test_ciphertext = ssh2_mpint(last(fibonacci_scattered(14)))
        test_ciphertext += b"x" * (15 & -len(test_ciphertext)) 

        
        test_key = b"foobarbazquxquuxFooBarBazQuxQuux"
        test_iv = b"FOOBARBAZQUXQUUX"

        for keylen in [128, 192, 256]:
            decryptions = []

            for suffix in "hw", "sw":
                c = ssh_cipher_new("aes{:d}_cbc_{}".format(keylen, suffix))
                if c is None: continue
                ssh_cipher_setkey(c, test_key[:keylen//8])
                for chunklen in range(16, 16*12, 16):
                    ssh_cipher_setiv(c, test_iv)
                    decryption = b""
                    for pos in range(0, len(test_ciphertext), chunklen):
                        chunk = test_ciphertext[pos:pos+chunklen]
                        decryption += ssh_cipher_decrypt(c, chunk)
                    decryptions.append(decryption)

            for d in decryptions:
                self.assertEqualBin(d, decryptions[0])

    def testCRC32(self):
        
        
        
        
        
        
        

        
        
        
        
        shift1 = lambda x, dummy=None: (x >> 1) ^ (0xEDB88320 * (x & 1))
        shift8 = lambda x: functools.reduce(shift1, [None]*8, x)

        
        
        test_prior_values = [0, 0xFFFFFFFF, 0x45CC1F6A, 0xA0C4ADCF, 0xD482CDF1]

        for prior in test_prior_values:
            prior_shifted = shift8(prior)
            for i in range(256):
                exp = shift8(i) ^ prior_shifted
                self.assertEqual(crc32_update(prior, struct.pack("B", i)), exp)

                
                
                self.assertEqual(shift8(i ^ prior), exp)

    def testCRCDA(self):
        def pattern(badblk, otherblks, pat):
            
            
            retstr = b""
            while pat != 0:
                retstr += (badblk if pat & 1 else next(otherblks))
                pat >>= 1
            return retstr

        def testCases(pat):
            badblock = b'muhahaha' 

            
            
            
            for otherblocks in [
                    itertools.repeat(b'GoodData'),
                    (struct.pack('>Q', i) for i in itertools.count()),
                    (struct.pack('<Q', i) for i in itertools.count())]:
                yield pattern(badblock, otherblocks, pat)

        def positiveTest(pat):
            for data in testCases(pat):
                self.assertTrue(crcda_detect(data, ""))
                self.assertTrue(crcda_detect(data[8:], data[:8]))

        def negativeTest(pat):
            for data in testCases(pat):
                self.assertFalse(crcda_detect(data, ""))
                self.assertFalse(crcda_detect(data[8:], data[:8]))

        
        
        
        
        
        
        
        
        
        
        
        
        positiveTest(0x1db710641) 
        positiveTest(0x26d930ac3) 
        positiveTest(0xbdbdf21cf) 
        positiveTest(0x3a66a39b653f6889d)
        positiveTest(0x170db3167dd9f782b9765214c03e71a18f685b7f3)
        positiveTest(0x1751997d000000000000000000000000000000001)
        positiveTest(0x800000000000000000000000000000000f128a2d1)

        
        negativeTest(0x1db711a41)
        negativeTest(0x3a66a39b453f6889d)
        negativeTest(0x170db3167dd9f782b9765214c03e71b18f685b7f3)
        negativeTest(0x1751997d000000000000000000000001000000001)
        negativeTest(0x800000000000002000000000000000000f128a2d1)

    def testAuxEncryptFns(self):
        
        
        
        
        
        
        

        p = b'three AES blocks, or six DES, of arbitrary input'

        k = b'thirty-two-byte aes-256 test key'
        c = unhex('7b112d00c0fc95bc13fcdacfd43281bf'
                  'de9389db1bbcfde79d59a303d41fd2eb'
                  '0955c9477ae4ee3a4d6c1fbe474c0ef6')
        self.assertEqualBin(aes256_encrypt_pubkey(k, p), c)
        self.assertEqualBin(aes256_decrypt_pubkey(k, c), p)

        k = b'3des with keys distinct.'
        iv = b'randomIV'
        c = unhex('be81ff840d885869a54d63b03d7cd8db'
                  'd39ab875e5f7b9da1081f8434cb33c47'
                  'dee5bcd530a3f6c13a9fc73e321a843a')
        self.assertEqualBin(des3_encrypt_pubkey_ossh(k, iv, p), c)
        self.assertEqualBin(des3_decrypt_pubkey_ossh(k, iv, c), p)

        k = b'3des, 2keys only'
        c = unhex('0b845650d73f615cf16ee3ed20535b5c'
                  'd2a8866ee628547bbdad916e2b4b9f19'
                  '67c15bde33c5b03ff7f403b4f8cf2364')
        self.assertEqualBin(des3_encrypt_pubkey(k, p), c)
        self.assertEqualBin(des3_decrypt_pubkey(k, c), p)

        k = b'7 bytes'
        c = unhex('5cac9999cffc980a1d1184d84b71c8cb'
                  '313d12a1d25a7831179aeb11edaca5ad'
                  '9482b224105a61c27137587620edcba8')
        self.assertEqualBin(des_encrypt_xdmauth(k, p), c)
        self.assertEqualBin(des_decrypt_xdmauth(k, c), p)

    def testSSHCiphers(self):
        
        
        

        p = b'64 bytes of test input data, enough to check any cipher mode xyz'
        k = b'sixty-four bytes of test key data, enough to key any cipher pqrs'
        iv = b'16 bytes of IV w'

        ciphers = [
            ("3des_ctr",      24,    8, False, unhex('83c17a29250d3d4fa81250fc0362c54e40456936445b77709a30fccf8b983d57129a969c59070d7c2977f3d25dd7d71163687c7b3cd2edb0d07514e6c77479f5')),
            ("3des_ssh2",     24,    8, True,  unhex('d5f1cc25b8fbc62decc74b432344de674f7249b2e38871f764411eaae17a1097396bd97b66a1e4d49f08c219acaef2a483198ce837f75cc1ef67b37c2432da3e')),
            ("3des_ssh1",     24,    8, False, unhex('d5f1cc25b8fbc62de63590b9b92344adf6dd72753273ff0fb32d4dbc6af858529129f34242f3d557eed3a5c84204eb4f868474294964cf70df5d8f45dfccfc45')),
            ("des_cbc",        8,    8, True,  unhex('051524e77fb40e109d9fffeceacf0f28c940e2f8415ddccc117020bdd2612af5036490b12085d0e46129919b8e499f51cb82a4b341d7a1a1ea3e65201ef248f6')),
            ("aes256_ctr",    32,   16, False, unhex('b87b35e819f60f0f398a37b05d7bcf0b04ad4ebe570bd08e8bfa8606bafb0db2cfcd82baf2ccceae5de1a3c1ae08a8b8fdd884fdc5092031ea8ce53333e62976')),
            ("aes256_ctr_hw", 32,   16, False, unhex('b87b35e819f60f0f398a37b05d7bcf0b04ad4ebe570bd08e8bfa8606bafb0db2cfcd82baf2ccceae5de1a3c1ae08a8b8fdd884fdc5092031ea8ce53333e62976')),
            ("aes256_ctr_sw", 32,   16, False, unhex('b87b35e819f60f0f398a37b05d7bcf0b04ad4ebe570bd08e8bfa8606bafb0db2cfcd82baf2ccceae5de1a3c1ae08a8b8fdd884fdc5092031ea8ce53333e62976')),
            ("aes256_cbc",    32,   16, True,  unhex('381cbb2fbcc48118d0094540242bd990dd6af5b9a9890edd013d5cad2d904f34b9261c623a452f32ea60e5402919a77165df12862742f1059f8c4a862f0827c5')),
            ("aes256_cbc_hw", 32,   16, True,  unhex('381cbb2fbcc48118d0094540242bd990dd6af5b9a9890edd013d5cad2d904f34b9261c623a452f32ea60e5402919a77165df12862742f1059f8c4a862f0827c5')),
            ("aes256_cbc_sw", 32,   16, True,  unhex('381cbb2fbcc48118d0094540242bd990dd6af5b9a9890edd013d5cad2d904f34b9261c623a452f32ea60e5402919a77165df12862742f1059f8c4a862f0827c5')),
            ("aes192_ctr",    24,   16, False, unhex('06bcfa7ccf075d723e12b724695a571a0fad67c56287ea609c410ac12749c51bb96e27fa7e1c7ea3b14792bbbb8856efb0617ebec24a8e4a87340d820cf347b8')),
            ("aes192_ctr_hw", 24,   16, False, unhex('06bcfa7ccf075d723e12b724695a571a0fad67c56287ea609c410ac12749c51bb96e27fa7e1c7ea3b14792bbbb8856efb0617ebec24a8e4a87340d820cf347b8')),
            ("aes192_ctr_sw", 24,   16, False, unhex('06bcfa7ccf075d723e12b724695a571a0fad67c56287ea609c410ac12749c51bb96e27fa7e1c7ea3b14792bbbb8856efb0617ebec24a8e4a87340d820cf347b8')),
            ("aes192_cbc",    24,   16, True,  unhex('ac97f8698170f9c05341214bd7624d5d2efef8311596163dc597d9fe6c868971bd7557389974612cbf49ea4e7cc6cc302d4cc90519478dd88a4f09b530c141f3')),
            ("aes192_cbc_hw", 24,   16, True,  unhex('ac97f8698170f9c05341214bd7624d5d2efef8311596163dc597d9fe6c868971bd7557389974612cbf49ea4e7cc6cc302d4cc90519478dd88a4f09b530c141f3')),
            ("aes192_cbc_sw", 24,   16, True,  unhex('ac97f8698170f9c05341214bd7624d5d2efef8311596163dc597d9fe6c868971bd7557389974612cbf49ea4e7cc6cc302d4cc90519478dd88a4f09b530c141f3')),
            ("aes128_ctr",    16,   16, False, unhex('0ad4ddfd2360ec59d77dcb9a981f92109437c68c5e7f02f92017d9f424f89ab7850473ac0e19274125e740f252c84ad1f6ad138b6020a03bdaba2f3a7378ce1e')),
            ("aes128_ctr_hw", 16,   16, False, unhex('0ad4ddfd2360ec59d77dcb9a981f92109437c68c5e7f02f92017d9f424f89ab7850473ac0e19274125e740f252c84ad1f6ad138b6020a03bdaba2f3a7378ce1e')),
            ("aes128_ctr_sw", 16,   16, False, unhex('0ad4ddfd2360ec59d77dcb9a981f92109437c68c5e7f02f92017d9f424f89ab7850473ac0e19274125e740f252c84ad1f6ad138b6020a03bdaba2f3a7378ce1e')),
            ("aes128_cbc",    16,   16, True,  unhex('36de36917fb7955a711c8b0bf149b29120a77524f393ae3490f4ce5b1d5ca2a0d7064ce3c38e267807438d12c0e40cd0d84134647f9f4a5b11804a0cc5070e62')),
            ("aes128_cbc_hw", 16,   16, True,  unhex('36de36917fb7955a711c8b0bf149b29120a77524f393ae3490f4ce5b1d5ca2a0d7064ce3c38e267807438d12c0e40cd0d84134647f9f4a5b11804a0cc5070e62')),
            ("aes128_cbc_sw", 16,   16, True,  unhex('36de36917fb7955a711c8b0bf149b29120a77524f393ae3490f4ce5b1d5ca2a0d7064ce3c38e267807438d12c0e40cd0d84134647f9f4a5b11804a0cc5070e62')),
            ("blowfish_ctr",  32,    8, False, unhex('079daf0f859363ccf72e975764d709232ec48adc74f88ccd1f342683f0bfa89ca0e8dbfccc8d4d99005d6b61e9cc4e6eaa2fd2a8163271b94bf08ef212129f01')),
            ("blowfish_ssh2", 16,    8, True,  unhex('e986b7b01f17dfe80ee34cac81fa029b771ec0f859ae21ae3ec3df1674bc4ceb54a184c6c56c17dd2863c3e9c068e76fd9aef5673465995f0d648b0bb848017f')),
            ("blowfish_ssh1", 32,    8, True,  unhex('d44092a9035d895acf564ba0365d19570fbb4f125d5a4fd2a1812ee6c8a1911a51bb181fbf7d1a261253cab71ee19346eb477b3e7ecf1d95dd941e635c1a4fbf')),
            ("arcfour256",    32, None, False, unhex('db68db4cd9bbc1d302cce5919ff3181659272f5d38753e464b3122fc69518793fe15dd0fbdd9cd742bd86c5e8a3ae126c17ecc420bd2d5204f1a24874d00fda3')),
            ("arcfour128",    16, None, False, unhex('fd4af54c5642cb29629e50a15d22e4944e21ffba77d0543b27590eafffe3886686d1aefae0484afc9e67edc0e67eb176bbb5340af1919ea39adfe866d066dd05')),
        ]

        for alg, keylen, ivlen, simple_cbc, c in ciphers:
            cipher = ssh_cipher_new(alg)
            if cipher is None:
                continue 

            ssh_cipher_setkey(cipher, k[:keylen])
            if ivlen is not None:
                ssh_cipher_setiv(cipher, iv[:ivlen])
            self.assertEqualBin(ssh_cipher_encrypt(cipher, p), c)

            ssh_cipher_setkey(cipher, k[:keylen])
            if ivlen is not None:
                ssh_cipher_setiv(cipher, iv[:ivlen])
            self.assertEqualBin(ssh_cipher_decrypt(cipher, c), p)

            if simple_cbc:
                
                
                
                
                
                
                
                
                
                
                ssh_cipher_setkey(cipher, k[:keylen])
                ssh_cipher_decrypt(cipher, iv[:ivlen])
                self.assertEqualBin(ssh_cipher_decrypt(cipher, c), p)

    def testRSAKex(self):
        
        
        
        def blobs(n, e, d, p, q, iqmp):
            
            
            
            
            
            
            pubblob = ssh_string(b"ssh-rsa") + ssh2_mpint(e) + ssh2_mpint(n)
            privblob = (ssh_uint32(nbits(n)) + ssh1_mpint(n) + ssh1_mpint(e) +
                        ssh1_mpint(d) + ssh1_mpint(iqmp) +
                        ssh1_mpint(q) + ssh1_mpint(p))
            return pubblob, privblob

        
        p = 0xf49e4d21c1ec3d1c20dc8656cc29aadb2644a12c98ed6c81a6161839d20d398d
        q = 0xa5f0bc464bf23c4c83cf17a2f396b15136fbe205c07cb3bb3bdb7ed357d1cd13
        n = p*q
        e = 37
        d = int(mp_invert(e, (p-1)*(q-1)))
        iqmp = int(mp_invert(q, p))
        assert iqmp * q % p == 1
        assert d * e % (p-1) == 1
        assert d * e % (q-1) == 1

        pubblob, privblob = blobs(n, e, d, p, q, iqmp)

        pubkey = ssh_rsakex_newkey(pubblob)
        privkey = get_rsa_ssh1_priv_agent(privblob)

        plain = 0x123456789abcdef
        hashalg = 'md5'
        with queued_random_data(64, "rsakex encrypt test"):
            cipher = ssh_rsakex_encrypt(pubkey, hashalg, ssh2_mpint(plain))
        decoded = ssh_rsakex_decrypt(privkey, hashalg, cipher)
        self.assertEqual(int(decoded), plain)
        self.assertEqualBin(cipher, unhex(
            '34277d1060dc0a434d98b4239de9cec59902a4a7d17a763587cdf8c25d57f51a'
            '7964541892e7511798e61dd78429358f4d6a887a50d2c5ebccf0e04f48fc665c'
        ))

    def testMontgomeryKexLowOrderPoints(self):
        
        
        
        
        
        
        bad_keys_25519 = [
            "0000000000000000000000000000000000000000000000000000000000000000",
            "0100000000000000000000000000000000000000000000000000000000000000",
            "5f9c95bca3508c24b1d0b1559c83ef5b04445cc4581c8e86d8224eddd09f1157",
            "e0eb7a7c3b41b8ae1656e3faf19fc46ada098deb9c32b1fd866205165f49b800",
            "ecffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f",

            
            
            
            "edffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f",
            "eeffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f",

            
            
            
            
            
            "0000000000000000000000000000000000000000000000000000000000000080",
            "0100000000000000000000000000000000000000000000000000000000000080",
            "5f9c95bca3508c24b1d0b1559c83ef5b04445cc4581c8e86d8224eddd09f11d7",
            "e0eb7a7c3b41b8ae1656e3faf19fc46ada098deb9c32b1fd866205165f49b880",
            "ecffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            "edffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
            "eeffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        ]

        
        
        bad_keys_448 = [
            
            
            '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
            '0100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
            'fefffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffffffffffffffffffffffffffffffffffffffffffffffffff',

            
            
            
            'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffffffffffffffffffffffffffffffffffffffffffffffffff',
            '00000000000000000000000000000000000000000000000000000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffff'

            
            
            
        ]

        with random_prng("doesn't matter"):
            ecdh25519 = ssh_ecdhkex_newkey('curve25519')
            ecdh448 = ssh_ecdhkex_newkey('curve448')
        for pub in bad_keys_25519:
            key = ssh_ecdhkex_getkey(ecdh25519, unhex(pub))
            self.assertEqual(key, None)
        for pub in bad_keys_448:
            key = ssh_ecdhkex_getkey(ecdh448, unhex(pub))
            self.assertEqual(key, None)

    def testPRNG(self):
        hashalg = 'sha256'
        seed = b"hello, world"
        entropy = b'1234567890' * 100

        
        
        pr = prng_new(hashalg)
        prng_seed_begin(pr)
        prng_seed_update(pr, seed)
        prng_seed_finish(pr)
        data1 = prng_read(pr, 128)
        data2 = prng_read(pr, 127) 
        prng_add_entropy(pr, 0, entropy) 
        data3 = prng_read(pr, 128)

        key1 = hash_str(hashalg, b'R' + seed)
        expected_data1 = b''.join(
            hash_str(hashalg, key1 + b'G' + ssh2_mpint(counter))
            for counter in range(4))
        
        
        
        key2 = hash_str(hashalg, key1 + b'R')
        expected_data2 = b''.join(
            hash_str(hashalg, key2 + b'G' + ssh2_mpint(counter))
            for counter in range(4,8))
        
        
        key3 = hash_str(hashalg, key2 + b'R')
        key4 = hash_str(hashalg, key3 + b'R' + hash_str(hashalg, entropy))
        expected_data3 = b''.join(
            hash_str(hashalg, key4 + b'G' + ssh2_mpint(counter))
            for counter in range(8,12))

        self.assertEqualBin(data1, expected_data1)
        self.assertEqualBin(data2, expected_data2[:127])
        self.assertEqualBin(data3, expected_data3)

    def testHashPadding(self):
        
        
        
        
        

        
        
        
        
        
        
        

        text = """
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
minim veniam, quis nostrud exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.
        """.replace('\n', ' ').strip()

        def test(hashname, maxlen, expected):
            assert len(text) >= maxlen
            buf = b''.join(hash_str(hashname, text[:i])
                           for i in range(maxlen))
            self.assertEqualBin(hash_str(hashname, buf), unhex(expected))

        test('md5', 128, '8169d766cc3b8df182b3ce756ae19a15')
        test('sha1', 128, '3691759577deb3b70f427763a9c15acb9dfc0259')
        test('sha256', 128, 'ec539c4d678412c86c13ee4eb9452232'
             '35d4eed3368d876fdf10c9df27396640')
        test('sha512', 256,
             'cb725b4b4ec0ac1174d69427b4d97848b7db4fc01181f99a8049a4d721862578'
             'f91e026778bb2d389a9dd88153405189e6ba438b213c5387284103d2267fd055'
        )

    def testDSA(self):
        p = 0xe93618c54716992ffd54e79df6e1b0edd517f7bbe4a49d64631eb3efe8105f676e8146248cfb4f05720862533210f0c2ab0f9dd61dbc0e5195200c4ebd95364b
        q = 0xf3533bcece2e164ca7c5ce64bc1e395e9a15bbdd
        g = 0x5ac9d0401c27d7abfbc5c17cdc1dc43323cd0ef18b79e1909bdace6d17af675a10d37dde8bd8b70e72a8666592216ccb00614629c27e870e4fbf393b812a9f05
        y = 0xac3ddeb22d65a5a2ded4a28418b2a748d8e5e544ba5e818c137d7b042ef356b0ef6d66cfca0b3ab5affa2969522e7b07bee60562fa4869829a5afce0ad0c4cd0
        x = 0x664f8250b7f1a5093047fe0c7fe4b58e46b73295
        pubblob = ssh_string(b"ssh-dss") + b"".join(map(ssh2_mpint, [p,q,g,y]))
        privblob = ssh2_mpint(x)
        pubkey = ssh_key_new_pub('dsa', pubblob)
        privkey = ssh_key_new_priv('dsa', pubblob, privblob)

        sig = ssh_key_sign(privkey, b"hello, world", 0)
        self.assertTrue(ssh_key_verify(pubkey, sig, b"hello, world"))
        self.assertFalse(ssh_key_verify(pubkey, sig, b"hello, again"))

        badsig0 = unhex('{:040x}{:040x}'.format(1, 0))
        badsigq = unhex('{:040x}{:040x}'.format(1, q))
        self.assertFalse(ssh_key_verify(pubkey, badsig0, "hello, world"))
        self.assertFalse(ssh_key_verify(pubkey, badsigq, "hello, world"))
        self.assertFalse(ssh_key_verify(pubkey, badsig0, "hello, again"))
        self.assertFalse(ssh_key_verify(pubkey, badsigq, "hello, again"))

    def testRSAVerify(self):
        def blobs(n, e, d, p, q, iqmp):
            pubblob = ssh_string(b"ssh-rsa") + ssh2_mpint(e) + ssh2_mpint(n)
            privblob = (ssh2_mpint(d) + ssh2_mpint(p) +
                        ssh2_mpint(q) + ssh2_mpint(iqmp))
            return pubblob, privblob

        def failure_test(*args):
            pubblob, privblob = blobs(*args)
            key = ssh_key_new_priv('rsa', pubblob, privblob)
            self.assertEqual(key, None)

        def success_test(*args):
            pubblob, privblob = blobs(*args)
            key = ssh_key_new_priv('rsa', pubblob, privblob)
            self.assertNotEqual(key, None)

        
        n = 0xb5d545a2f6423eabd55ffede53e21628d5d4491541482e10676d9d6f2783b9a5
        e = 0x25
        d = 0x6733db6a546ac99fcc21ba2b28b0c077156e8a705976205a955c6d9cef98f419
        p = 0xe30ebd7348bf10dca72b36f2724dafa7
        q = 0xcd02c87a7f7c08c4e9dc80c9b9bad5d3
        iqmp = 0x60a129b30db9227910efe1608976c513

        
        success_test(n, e, d, p, q, iqmp)

        
        
        
        failure_test(n+1, e, d, p, q, iqmp)
        failure_test(n, e+1, d, p, q, iqmp)
        failure_test(n, e, d+1, p, q, iqmp)
        failure_test(n, e, d, p+1, q, iqmp)
        failure_test(n, e, d, p, q+1, iqmp)
        success_test(n, e, d, p, q, iqmp+1)

        
        
        success_test(n, e, d, q, p, iqmp)

        
        
        
        
        failure_test(n, e, d, 0, q, iqmp)
        failure_test(n, e, d, p, 0, iqmp)
        failure_test(n, e, d, 1, q, iqmp)
        failure_test(n, e, d, p, 1, iqmp)

    def testKeyMethods(self):
        
        
        
        
        
        
        
        
        
        
        
        

        test_message = b"Message to be signed by crypt.testKeyMethods\n"

        test_keys = [
            ('ed25519', 'AAAAC3NzaC1lZDI1NTE5AAAAIM7jupzef6CD0ps2JYxJp9IlwY49oorOseV5z5JFDFKn', 'AAAAIAf4/WRtypofgdNF2vbZOUFE1h4hvjw4tkGJZyOzI7c3', 255, b'0xf4d6e7f6f4479c23f0764ef43cea1711dbfe02aa2b5a32ff925c7c1fbf0f0db,0x27520c4592cf79e5b1ce8aa23d8ec125d2a7498c25369bd283a07fde9cbae3ce', [(0, 'AAAAC3NzaC1lZDI1NTE5AAAAQN73EqfyA4WneqDhgZ98TlRj9V5Wg8zCrMxTLJN1UtyfAnPUJDtfG/U0vOsP8PrnQxd41DDDnxrAXuqJz8rOagc=')]),
            ('ed448', 'AAAACXNzaC1lZDQ0OAAAADnRI0CQDym5IqUidLNDcSdHe54bYEwqjpjBlab8uKGoe6FRqqejha7+5U/VAHy7BmE23+ju26O9XgA=', 'AAAAObP9klqyiJSJsdFJf+xwZQdkbZGUqXE07K6e5plfRTGjYYkyWJFUNFH4jzIn9xH1TX9z9EGycPaXAA==', 448, b'0x4bf4a2b6586c60d8cdb52c2b45b897f6d2224bc37987489c0d70febb449e8c82964ed5785827be808e44d31dd31e6ff7c99f43e49f419928,0x5ebda3dbeee8df366106bb7c00d54fe5feae85a3a7aa51a17ba8a1b8fca695c1988e2a4c601b9e7b47277143b37422a522b9290f904023d1', [(0, 'AAAACXNzaC1lZDQ0OAAAAHLkSVioGMvLesZp3Tn+Z/sSK0Hl7RHsHP4q9flLzTpZG5h6JDH3VmZBEjTJ6iOLaa0v4FoNt0ng4wAB53WrlQC4h3iAusoGXnPMAKJLmqzplKOCi8HKXk8Xl8fsXbaoyhatv1OZpwJcffmh1x+x+LSgNQA=')]),
            ('p256', 'AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBHkYQ0sQoq5LbJI1VMWhw3bV43TSYi3WVpqIgKcBKK91TcFFlAMZgceOHQ0xAFYcSczIttLvFu+xkcLXrRd4N7Q=', 'AAAAIQCV/1VqiCsHZm/n+bq7lHEHlyy7KFgZBEbzqYaWtbx48Q==', 256, b'nistp256,0x7918434b10a2ae4b6c923554c5a1c376d5e374d2622dd6569a8880a70128af75,0x4dc14594031981c78e1d0d3100561c49ccc8b6d2ef16efb191c2d7ad177837b4', [(0, 'AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAABIAAAAIAryzHDGi/TcCnbdxZkIYR5EGR6SNYXr/HlQRF8le+/IAAAAIERfzn6eHuBbqWIop2qL8S7DWRB3lenN1iyL10xYQPKw')]),
            ('p384', 'AAAAE2VjZHNhLXNoYTItbmlzdHAzODQAAAAIbmlzdHAzODQAAABhBMYK8PUtfAlJwKaBTIGEuCzH0vqOMa4UbcjrBbTbkGVSUnfo+nuC80NCdj9JJMs1jvfF8GzKLc5z8H3nZyM741/BUFjV7rEHsQFDek4KyWvKkEgKiTlZid19VukNo1q2Hg==', 'AAAAMGsfTmdB4zHdbiQ2euTSdzM6UKEOnrVjMAWwHEYvmG5qUOcBnn62fJDRJy67L+QGdg==', 384, b'nistp384,0xc60af0f52d7c0949c0a6814c8184b82cc7d2fa8e31ae146dc8eb05b4db9065525277e8fa7b82f34342763f4924cb358e,0xf7c5f06cca2dce73f07de767233be35fc15058d5eeb107b101437a4e0ac96bca90480a89395989dd7d56e90da35ab61e', [(0, 'AAAAE2VjZHNhLXNoYTItbmlzdHAzODQAAABpAAAAMDmHrtXCADzLvkkWG/duBAHlf6B1mVvdt6F0uzXfsf8Yub8WXNUNVnYq6ovrWPzLggAAADEA9izzwoUuFcXYRJeKcRLZEGMmSDDPzUZb7oZR0UgD1jsMQXs8UfpO31Qur/FDSCRK')]),
            ('p521', 'AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAFrGthlKM152vu2Ghk+R7iO9/M6e+hTehNZ6+FBwof4HPkPB2/HHXj5+w5ynWyUrWiX5TI2riuJEIrJErcRH5LglADnJDX2w4yrKZ+wDHSz9lwh9p2F+B5R952es6gX3RJRkGA+qhKpKup8gKx78RMbleX8wgRtIu+4YMUnKb1edREiRg==', 'AAAAQgFh7VNJFUljWhhyAEiL0z+UPs/QggcMTd3Vv2aKDeBdCRl5di8r+BMm39L7bRzxRMEtW5NSKlDtE8MFEGdIE9khsw==', 521, b'nistp521,0x16b1ad86528cd79dafbb61a193e47b88ef7f33a7be8537a1359ebe141c287f81cf90f076fc71d78f9fb0e729d6c94ad6897e53236ae2b89108ac912b7111f92e094,0xe72435f6c38cab299fb00c74b3f65c21f69d85f81e51f79d9eb3a817dd125190603eaa12a92aea7c80ac7bf1131b95e5fcc2046d22efb860c52729bd5e75112246', [(0, 'AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAACMAAAAQgCLgvftvwM3CUaigrW0yzmCHoYjC6GLtO+6S91itqpgMEtWPNlaTZH6QQqkgscijWdXx98dDkQao/gcAKVmOZKPXgAAAEIB1PIrsDF1y6poJ/czqujB7NSUWt31v+c2t6UA8m2gTA1ARuVJ9XBGLMdceOTB00Hi9psC2RYFLpaWREOGCeDa6ow=')]),
            ('dsa', 'AAAAB3NzaC1kc3MAAABhAJyWZzjVddGdyc5JPu/WPrC07vKRAmlqO6TUi49ah96iRcM7/D1aRMVAdYBepQ2mf1fsQTmvoC9KgQa79nN3kHhz0voQBKOuKI1ZAodfVOgpP4xmcXgjaA73Vjz22n4newAAABUA6l7/vIveaiA33YYv+SKcKLQaA8cAAABgbErc8QLw/WDz7mhVRZrU+9x3Tfs68j3eW+B/d7Rz1ZCqMYDk7r/F8dlBdQlYhpQvhuSBgzoFa0+qPvSSxPmutgb94wNqhHlVIUb9ZOJNloNr2lXiPP//Wu51TxXAEvAAAAAAYQCcQ9mufXtZa5RyfwT4NuLivdsidP4HRoLXdlnppfFAbNdbhxE0Us8WZt+a/443bwKnYxgif8dgxv5UROnWTngWu0jbJHpaDcTc9lRyTeSUiZZK312s/Sl7qDk3/Du7RUI=', 'AAAAFGx3ft7G8AQzFsjhle7PWardUXh3', 768, b'0x9c966738d575d19dc9ce493eefd63eb0b4eef29102696a3ba4d48b8f5a87dea245c33bfc3d5a44c54075805ea50da67f57ec4139afa02f4a8106bbf67377907873d2fa1004a3ae288d5902875f54e8293f8c66717823680ef7563cf6da7e277b,0xea5effbc8bde6a2037dd862ff9229c28b41a03c7,0x6c4adcf102f0fd60f3ee6855459ad4fbdc774dfb3af23dde5be07f77b473d590aa3180e4eebfc5f1d94175095886942f86e481833a056b4faa3ef492c4f9aeb606fde3036a8479552146fd64e24d96836bda55e23cffff5aee754f15c012f000,0x9c43d9ae7d7b596b94727f04f836e2e2bddb2274fe074682d77659e9a5f1406cd75b87113452cf1666df9aff8e376f02a76318227fc760c6fe5444e9d64e7816bb48db247a5a0dc4dcf654724de49489964adf5dacfd297ba83937fc3bbb4542', [(0, 'AAAAB3NzaC1kc3MAAAAo0T2t6dr8Qr5DK2B0ETwUa3BhxMLPjLY0ZtlOACmP/kUt3JgByLv+3g==')]),
            ('rsa', 'AAAAB3NzaC1yc2EAAAABJQAAAGEA2ChX9+mQD/NULFkBrxLDI8d1PHgrInC2u11U4Grqu4oVzKvnFROo6DZeCu6sKhFJE5CnIL7evAthQ9hkXVHDhQ7xGVauzqyHGdIU4/pHRScAYWBv/PZOlNMrSoP/PP91', 'AAAAYCMNdgyGvWpez2EjMLSbQj0nQ3GW8jzvru3zdYwtA3hblNUU9QpWNxDmOMOApkwCzUgsdIPsBxctIeWT2h+v8sVOH+d66LCaNmNR0lp+dQ+iXM67hcGNuxJwRdMupD9ZbQAAADEA7XMrMAb4WuHaFafoTfGrf6Jhdy9Ozjqi1fStuld7Nj9JkoZluiL2dCwIrxqOjwU5AAAAMQDpC1gYiGVSPeDRILr2oxREtXWOsW+/ZZTfZNX7lvoufnp+qvwZPqvZnXQFHyZ8qB0AAAAwQE0wx8TPgcvRVEVv8Wt+o1NFlkJZayWD5hqpe/8AqUMZbqfg/aiso5mvecDLFgfV', 768, b'0x25,0xd82857f7e9900ff3542c5901af12c323c7753c782b2270b6bb5d54e06aeabb8a15ccabe71513a8e8365e0aeeac2a11491390a720bedebc0b6143d8645d51c3850ef11956aeceac8719d214e3fa4745270061606ffcf64e94d32b4a83ff3cff75', [(0, 'AAAAB3NzaC1yc2EAAABgrLSC4635RCsH1b3en58NqLsrH7PKRZyb3YmRasOyr8xIZMSlKZyxNg+kkn9OgBzbH9vChafzarfHyVwtJE2IMt3uwxTIWjwgwH19tc16k8YmNfDzujmB6OFOArmzKJgJ'), (2, 'AAAADHJzYS1zaGEyLTI1NgAAAGAJszr04BZlVBEdRLGOv1rTJwPiid/0I6/MycSH+noahvUH2wjrRhqDuv51F4nKYF5J9vBsEotTSrSF/cnLsliCdvVkEfmvhdcn/jx2LWF2OfjqETiYSc69Dde9UFmAPds='), (4, 'AAAADHJzYS1zaGEyLTUxMgAAAGBxfZ2m+WjvZ5YV5RFm0+w84CgHQ95EPndoAha0PCMc93AUHBmoHnezsJvEGuLovUm35w/0POmUNHI7HzM9PECwXrV0rO6N/HL/oFxJuDYmeqCpjMVmN8QXka+yxs2GEtA=')]),
        ]

        for alg, pubb64, privb64, bits, cachestr, siglist in test_keys:
            
            pubblob = base64decode(pubb64.encode('ASCII'))
            privblob = base64decode(privb64.encode('ASCII'))

            
            
            self.assertEqual(ssh_key_public_bits(alg, pubblob), bits)

            
            pubkey = ssh_key_new_pub(alg, pubblob)
            privkey = ssh_key_new_priv(alg, pubblob, privblob)

            
            
            self.assertEqual(ssh_key_public_blob(pubkey), pubblob)
            self.assertEqual(ssh_key_public_blob(privkey), pubblob)
            self.assertEqual(ssh_key_private_blob(privkey), privblob)

            
            
            
            osshblob = ssh_key_openssh_blob(privkey)
            privkey2 = ssh_key_new_priv_openssh(alg, osshblob)
            self.assertEqual(ssh_key_public_blob(privkey2), pubblob)
            self.assertEqual(ssh_key_private_blob(privkey2), privblob)
            self.assertEqual(ssh_key_openssh_blob(privkey2), osshblob)

            
            
            for key in [pubkey, privkey, privkey2]:
                self.assertEqual(ssh_key_cache_str(key), cachestr)

            
            
            for flags, sigb64 in siglist:
                
                sigblob = base64decode(sigb64.encode('ASCII'))

                
                
                
                
                
                
                
                
                for key in [privkey, privkey2]:
                    self.assertEqual(ssh_key_sign(
                        key, test_message, flags), sigblob)

                if flags != 0:
                    
                    
                    continue

                
                
                for key in [pubkey, privkey, privkey2]:
                    self.assertTrue(ssh_key_verify(key, sigblob, test_message))

                
                
                
                
                
                
                
                
                
                for n, d in [(1,3),(2,3)]:
                    sigbytes = list(sigblob)
                    bit = 8 * len(sigbytes) * n // d
                    sigbytes[bit // 8] ^= 1 << (bit % 8)
                    badsig = bytes(sigbytes)
                    for key in [pubkey, privkey, privkey2]:
                        self.assertFalse(ssh_key_verify(
                            key, badsig, test_message))

    def testPPKLoadSave(self):
        
        input_clear_key = b"""\
PuTTY-User-Key-File-2: ssh-ed25519
Encryption: none
Comment: ed25519-key-20200105
Public-Lines: 2
AAAAC3NzaC1lZDI1NTE5AAAAIHJCszOHaI9X/yGLtjn22f0hO6VPMQDVtctkym6F
JH1W
Private-Lines: 1
AAAAIGvvIpl8jyqn8Xufkw6v3FnEGtXF3KWw55AP3/AGEBpY
Private-MAC: 2a629acfcfbe28488a1ba9b6948c36406bc28422
"""
        input_encrypted_key = b"""\
PuTTY-User-Key-File-2: ssh-ed25519
Encryption: aes256-cbc
Comment: ed25519-key-20200105
Public-Lines: 2
AAAAC3NzaC1lZDI1NTE5AAAAIHJCszOHaI9X/yGLtjn22f0hO6VPMQDVtctkym6F
JH1W
Private-Lines: 1
4/jKlTgC652oa9HLVGrMjHZw7tj0sKRuZaJPOuLhGTvb25Jzpcqpbi+Uf+y+uo+Z
Private-MAC: 5b1f6f4cc43eb0060d2c3e181bc0129343adba2b
"""
        algorithm = b'ssh-ed25519'
        comment = b'ed25519-key-20200105'
        pp = b'test-passphrase'
        public_blob = unhex(
            '0000000b7373682d65643235353139000000207242b33387688f57ff218bb639'
            'f6d9fd213ba54f3100d5b5cb64ca6e85247d56')

        self.assertEqual(ppk_encrypted_s(input_clear_key), (False, comment))
        self.assertEqual(ppk_encrypted_s(input_encrypted_key), (True, comment))
        self.assertEqual(ppk_encrypted_s("not a key file"), (False, None))

        self.assertEqual(ppk_loadpub_s(input_clear_key),
                         (True, algorithm, public_blob, comment, None))
        self.assertEqual(ppk_loadpub_s(input_encrypted_key),
                         (True, algorithm, public_blob, comment, None))
        self.assertEqual(ppk_loadpub_s("not a key file"),
                         (False, None, b'', None,
                          b'not a PuTTY SSH-2 private key'))

        k1, c, e = ppk_load_s(input_clear_key, None)
        self.assertEqual((c, e), (comment, None))
        k2, c, e = ppk_load_s(input_encrypted_key, pp)
        self.assertEqual((c, e), (comment, None))

        self.assertEqual(ppk_save_sb(k1, comment, None), input_clear_key)
        self.assertEqual(ppk_save_sb(k2, comment, None), input_clear_key)

        self.assertEqual(ppk_save_sb(k1, comment, pp), input_encrypted_key)
        self.assertEqual(ppk_save_sb(k2, comment, pp), input_encrypted_key)

    def testRSA1LoadSave(self):
        
        input_clear_key = unhex(
            "5353482050524956415445204B45592046494C4520464F524D415420312E310A"
            "000000000000000002000200BB115A85B741E84E3D940E690DF96A0CBFDC07CA"
            "70E51DA8234D211DE77341CEF40C214CAA5DCF68BE2127447FD6C84CCB17D057"
            "A74F2365B9D84A78906AEB51000625000000107273612D6B65792D3230323030"
            "313036208E208E0200929EE615C6FC4E4B29585E52570F984F2E97B3144AA5BD"
            "4C6EB2130999BB339305A21FFFA79442462A8397AF8CAC395A3A3827DE10457A"
            "1F1B277ABFB8C069C100FF55B1CAD69B3BD9E42456CF28B1A4B98130AFCE08B2"
            "8BCFFF5FFFED76C5D51E9F0100C5DE76889C62B1090A770AE68F087A19AB5126"
            "E60DF87710093A2AD57B3380FB0100F2068AC47ECB33BF8F13DF402BABF35EE7"
            "26BD32F7564E51502DF5C8F4888B2300000000")
        input_encrypted_key = unhex(
            "5353482050524956415445204b45592046494c4520464f524d415420312e310a"
            "000300000000000002000200bb115a85b741e84e3d940e690df96a0cbfdc07ca"
            "70e51da8234d211de77341cef40c214caa5dcf68be2127447fd6c84ccb17d057"
            "a74f2365b9d84a78906aeb51000625000000107273612d6b65792d3230323030"
            "3130363377f926e811a5f044c52714801ecdcf9dd572ee0a193c4f67e87ab2ce"
            "4569d0c5776fd6028909ed8b6d663bef15d207d3ef6307e7e21dbec56e8d8b4e"
            "894ded34df891bb29bae6b2b74805ac80f7304926abf01ae314dd69c64240761"
            "34f15d50c99f7573252993530ec9c4d5016dd1f5191730cda31a5d95d362628b"
            "2a26f4bb21840d01c8360e4a6ce216c4686d25b8699d45cf361663bb185e2c5e"
            "652012a1e0f9d6d19afbb28506f7775bfd8129")

        comment = b'rsa-key-20200106'
        pp = b'test-passphrase'
        public_blob = unhex(
            "000002000006250200bb115a85b741e84e3d940e690df96a0cbfdc07ca70e51d"
            "a8234d211de77341cef40c214caa5dcf68be2127447fd6c84ccb17d057a74f23"
            "65b9d84a78906aeb51")

        self.assertEqual(rsa1_encrypted_s(input_clear_key), (False, comment))
        self.assertEqual(rsa1_encrypted_s(input_encrypted_key),
                         (True, comment))
        self.assertEqual(rsa1_encrypted_s("not a key file"), (False, None))

        self.assertEqual(rsa1_loadpub_s(input_clear_key),
                         (1, public_blob, comment, None))
        self.assertEqual(rsa1_loadpub_s(input_encrypted_key),
                         (1, public_blob, comment, None))

        k1 = rsa_new()
        status, c, e = rsa1_load_s(input_clear_key, k1, None)
        self.assertEqual((status, c, e), (1, comment, None))
        k2 = rsa_new()
        status, c, e = rsa1_load_s(input_clear_key, k2, None)
        self.assertEqual((status, c, e), (1, comment, None))

        with queued_specific_random_data(unhex("208e")):
            self.assertEqual(rsa1_save_sb(k1, comment, None), input_clear_key)
        with queued_specific_random_data(unhex("208e")):
            self.assertEqual(rsa1_save_sb(k2, comment, None), input_clear_key)

        with queued_specific_random_data(unhex("99f3")):
            self.assertEqual(rsa1_save_sb(k1, comment, pp),
                             input_encrypted_key)
        with queued_specific_random_data(unhex("99f3")):
            self.assertEqual(rsa1_save_sb(k2, comment, pp),
                             input_encrypted_key)

class standard_test_vectors(MyTestBase):
    def testAES(self):
        def vector(cipher, key, plaintext, ciphertext):
            for suffix in "hw", "sw":
                c = ssh_cipher_new("{}_{}".format(cipher, suffix))
                if c is None: return 
                ssh_cipher_setkey(c, key)

                
                
                
                
                

                ssh_cipher_setiv(c, b'\x00' * 16)
                self.assertEqualBin(
                    ssh_cipher_encrypt(c, plaintext), ciphertext)

                ssh_cipher_setiv(c, b'\x00' * 16)
                self.assertEqualBin(
                    ssh_cipher_decrypt(c, ciphertext), plaintext)

        
        
        
        vector('aes128_cbc',
               unhex('2b7e151628aed2a6abf7158809cf4f3c'),
               unhex('3243f6a8885a308d313198a2e0370734'),
               unhex('3925841d02dc09fbdc118597196a0b32'))

        
        
        
        fullkey = struct.pack("B"*32, *range(32))
        plaintext = struct.pack("B"*16, *[0x11*i for i in range(16)])
        vector('aes128_cbc', fullkey[:16], plaintext,
               unhex('69c4e0d86a7b0430d8cdb78070b4c55a'))
        vector('aes192_cbc', fullkey[:24], plaintext,
               unhex('dda97ca4864cdfe06eaf70a0ec0d7191'))
        vector('aes256_cbc', fullkey[:32], plaintext,
               unhex('8ea2b7ca516745bfeafc49904b496089'))

    def testDES(self):
        c = ssh_cipher_new("des_cbc")
        def vector(key, plaintext, ciphertext):
            key = unhex(key)
            plaintext = unhex(plaintext)
            ciphertext = unhex(ciphertext)

            
            
            ssh_cipher_setkey(c, key)
            ssh_cipher_setiv(c, b'\x00' * 8)
            self.assertEqualBin(ssh_cipher_encrypt(c, plaintext), ciphertext)
            ssh_cipher_setiv(c, b'\x00' * 8)
            self.assertEqualBin(ssh_cipher_decrypt(c, ciphertext), plaintext)

        

        
        
        
        
        
        ipe_key = '01' * 8
        ipe_plaintexts = [
'166B40B44ABA4BD6', '06E7EA22CE92708F', 'D2FD8867D50D2DFE', 'CC083F1E6D9E85F6',
'5B711BC4CEEBF2EE', '0953E2258E8E90A1', 'E07C30D7E4E26E12', '2FBC291A570DB5C4',
'DD7C0BBD61FAFD54', '48221B9937748A23', 'E643D78090CA4207', '8405D1ABE24FB942',
'CE332329248F3228', '1D1CA853AE7C0C5F', '5D86CB23639DBEA9', '1029D55E880EC2D0',
'8DD45A2DDF90796C', 'CAFFC6AC4542DE31', 'EA51D3975595B86B', '8B54536F2F3E64A8',
'866ECEDD8072BB0E', '79E90DBC98F92CCA', 'AB6A20C0620D1C6F', '25EB5FC3F8CF0621',
'4D49DB1532919C9F', '814EEB3B91D90726', '5E0905517BB59BCF', 'CA3A2B036DBC8502',
'FA0752B07D9C4AB8', 'B160E4680F6C696F', 'DF98C8276F54B04B', 'E943D7568AEC0C5C',
'AEB5F5EDE22D1A36', 'E428581186EC8F46', 'E1652C6B138C64A5', 'D106FF0BED5255D7',
'9D64555A9A10B852', 'F02B263B328E2B60', '64FEED9C724C2FAF', '750D079407521363',
'FBE00A8A1EF8AD72', 'A484C3AD38DC9C19', '12A9F5817FF2D65D', 'E7FCE22557D23C97',
'329A8ED523D71AEC', 'E19E275D846A1298', '889DE068A16F0BE6', '2B9F982F20037FA9',
'F356834379D165CD', 'ECBFE3BD3F591A5E', 'E6D5F82752AD63D1', 'ADD0CC8D6E5DEBA1',
'F15D0F286B65BD28', 'B8061B7ECD9A21E5', '424250B37C3DD951', 'D9031B0271BD5A0A',
'0D9F279BA5D87260', '6CC5DEFAAF04512F', '55579380D77138EF', '20B9E767B2FB1456',
'4BD388FF6CD81D4F', '2E8653104F3834EA', 'DD7F121CA5015619', '95F8A5E5DD31D900',
        ]
        ipe_ciphertexts = [
'166B40B44ABA4BD6', '06E7EA22CE92708F', 'D2FD8867D50D2DFE', 'CC083F1E6D9E85F6',
'5B711BC4CEEBF2EE', '0953E2258E8E90A1', 'E07C30D7E4E26E12', '2FBC291A570DB5C4',
'DD7C0BBD61FAFD54', '48221B9937748A23', 'E643D78090CA4207', '8405D1ABE24FB942',
'CE332329248F3228', '1D1CA853AE7C0C5F', '5D86CB23639DBEA9', '1029D55E880EC2D0',
'8DD45A2DDF90796C', 'CAFFC6AC4542DE31', 'EA51D3975595B86B', '8B54536F2F3E64A8',
'866ECEDD8072BB0E', '79E90DBC98F92CCA', 'AB6A20C0620D1C6F', '25EB5FC3F8CF0621',
'4D49DB1532919C9F', '814EEB3B91D90726', '5E0905517BB59BCF', 'CA3A2B036DBC8502',
'FA0752B07D9C4AB8', 'B160E4680F6C696F', 'DF98C8276F54B04B', 'E943D7568AEC0C5C',
'AEB5F5EDE22D1A36', 'E428581186EC8F46', 'E1652C6B138C64A5', 'D106FF0BED5255D7',
'9D64555A9A10B852', 'F02B263B328E2B60', '64FEED9C724C2FAF', '750D079407521363',
'FBE00A8A1EF8AD72', 'A484C3AD38DC9C19', '12A9F5817FF2D65D', 'E7FCE22557D23C97',
'329A8ED523D71AEC', 'E19E275D846A1298', '889DE068A16F0BE6', '2B9F982F20037FA9',
'F356834379D165CD', 'ECBFE3BD3F591A5E', 'E6D5F82752AD63D1', 'ADD0CC8D6E5DEBA1',
'F15D0F286B65BD28', 'B8061B7ECD9A21E5', '424250B37C3DD951', 'D9031B0271BD5A0A',
'0D9F279BA5D87260', '6CC5DEFAAF04512F', '55579380D77138EF', '20B9E767B2FB1456',
'4BD388FF6CD81D4F', '2E8653104F3834EA', 'DD7F121CA5015619', '95F8A5E5DD31D900',
        ]
        ipe_single_bits = ["{:016x}".format(1 << bit) for bit in range(64)]
        for plaintext, ciphertext in zip(ipe_plaintexts, ipe_single_bits):
            vector(ipe_key, plaintext, ciphertext)
        for plaintext, ciphertext in zip(ipe_single_bits, ipe_ciphertexts):
            vector(ipe_key, plaintext, ciphertext)

        
        
        
        
        
        kp_ciphertexts = [
'95A8D72813DAA94D', '0EEC1487DD8C26D5', '7AD16FFB79C45926', 'D3746294CA6A6CF3',
'809F5F873C1FD761', 'C02FAFFEC989D1FC', '4615AA1D33E72F10', '2055123350C00858',
'DF3B99D6577397C8', '31FE17369B5288C9', 'DFDD3CC64DAE1642', '178C83CE2B399D94',
'50F636324A9B7F80', 'A8468EE3BC18F06D', 'A2DC9E92FD3CDE92', 'CAC09F797D031287',
'90BA680B22AEB525', 'CE7A24F350E280B6', '882BFF0AA01A0B87', '25610288924511C2',
'C71516C29C75D170', '5199C29A52C9F059', 'C22F0A294A71F29F', 'EE371483714C02EA',
'A81FBD448F9E522F', '4F644C92E192DFED', '1AFA9A66A6DF92AE', 'B3C1CC715CB879D8',
'19D032E64AB0BD8B', '3CFAA7A7DC8720DC', 'B7265F7F447AC6F3', '9DB73B3C0D163F54',
'8181B65BABF4A975', '93C9B64042EAA240', '5570530829705592', '8638809E878787A0',
'41B9A79AF79AC208', '7A9BE42F2009A892', '29038D56BA6D2745', '5495C6ABF1E5DF51',
'AE13DBD561488933', '024D1FFA8904E389', 'D1399712F99BF02E', '14C1D7C1CFFEC79E',
'1DE5279DAE3BED6F', 'E941A33F85501303', 'DA99DBBC9A03F379', 'B7FC92F91D8E92E9',
'AE8E5CAA3CA04E85', '9CC62DF43B6EED74', 'D863DBB5C59A91A0', 'A1AB2190545B91D7',
'0875041E64C570F7', '5A594528BEBEF1CC', 'FCDB3291DE21F0C0', '869EFD7F9F265A09',
        ]
        kp_key_repl_bytes = ["{:02x}".format(0x80>>i) for i in range(7)]
        kp_keys = ['01'*j + b + '01'*(7-j)
                   for j in range(8) for b in kp_key_repl_bytes]
        kp_plaintext = '0' * 16
        for key, ciphertext in zip(kp_keys, kp_ciphertexts):
            vector(key, kp_plaintext, ciphertext)

        
        
        dp_keys_and_ciphertexts = [
'1046913489980131:88D55E54F54C97B4', '1007103489988020:0C0CC00C83EA48FD',
'10071034C8980120:83BC8EF3A6570183', '1046103489988020:DF725DCAD94EA2E9',
'1086911519190101:E652B53B550BE8B0', '1086911519580101:AF527120C485CBB0',
'5107B01519580101:0F04CE393DB926D5', '1007B01519190101:C9F00FFC74079067',
'3107915498080101:7CFD82A593252B4E', '3107919498080101:CB49A2F9E91363E3',
'10079115B9080140:00B588BE70D23F56', '3107911598080140:406A9A6AB43399AE',
'1007D01589980101:6CB773611DCA9ADA', '9107911589980101:67FD21C17DBB5D70',
'9107D01589190101:9592CB4110430787', '1007D01598980120:A6B7FF68A318DDD3',
'1007940498190101:4D102196C914CA16', '0107910491190401:2DFA9F4573594965',
'0107910491190101:B46604816C0E0774', '0107940491190401:6E7E6221A4F34E87',
'19079210981A0101:AA85E74643233199', '1007911998190801:2E5A19DB4D1962D6',
'10079119981A0801:23A866A809D30894', '1007921098190101:D812D961F017D320',
'100791159819010B:055605816E58608F', '1004801598190101:ABD88E8B1B7716F1',
'1004801598190102:537AC95BE69DA1E1', '1004801598190108:AED0F6AE3C25CDD8',
'1002911498100104:B3E35A5EE53E7B8D', '1002911598190104:61C79C71921A2EF8',
'1002911598100201:E2F5728F0995013C', '1002911698100101:1AEAC39A61F0A464',
        ]
        dp_plaintext = '0' * 16
        for key_and_ciphertext in dp_keys_and_ciphertexts:
            key, ciphertext = key_and_ciphertext.split(":")
            vector(key, dp_plaintext, ciphertext)

        
        
        sb_complete_tests = [
            '7CA110454A1A6E57:01A1D6D039776742:690F5B0D9A26939B',
            '0131D9619DC1376E:5CD54CA83DEF57DA:7A389D10354BD271',
            '07A1133E4A0B2686:0248D43806F67172:868EBB51CAB4599A',
            '3849674C2602319E:51454B582DDF440A:7178876E01F19B2A',
            '04B915BA43FEB5B6:42FD443059577FA2:AF37FB421F8C4095',
            '0113B970FD34F2CE:059B5E0851CF143A:86A560F10EC6D85B',
            '0170F175468FB5E6:0756D8E0774761D2:0CD3DA020021DC09',
            '43297FAD38E373FE:762514B829BF486A:EA676B2CB7DB2B7A',
            '07A7137045DA2A16:3BDD119049372802:DFD64A815CAF1A0F',
            '04689104C2FD3B2F:26955F6835AF609A:5C513C9C4886C088',
            '37D06BB516CB7546:164D5E404F275232:0A2AEEAE3FF4AB77',
            '1F08260D1AC2465E:6B056E18759F5CCA:EF1BF03E5DFA575A',
            '584023641ABA6176:004BD6EF09176062:88BF0DB6D70DEE56',
            '025816164629B007:480D39006EE762F2:A1F9915541020B56',
            '49793EBC79B3258F:437540C8698F3CFA:6FBF1CAFCFFD0556',
            '4FB05E1515AB73A7:072D43A077075292:2F22E49BAB7CA1AC',
            '49E95D6D4CA229BF:02FE55778117F12A:5A6B612CC26CCE4A',
            '018310DC409B26D6:1D9D5C5018F728C2:5F4C038ED12B2E41',
            '1C587F1C13924FEF:305532286D6F295A:63FAC0D034D9F793',
        ]
        for test in sb_complete_tests:
            key, plaintext, ciphertext = test.split(":")
            vector(key, plaintext, ciphertext)

    def testMD5(self):
        MD5 = lambda s: hash_str('md5', s)

        
        self.assertEqualBin(MD5(""),
                            unhex('d41d8cd98f00b204e9800998ecf8427e'))
        self.assertEqualBin(MD5("a"),
                            unhex('0cc175b9c0f1b6a831c399e269772661'))
        self.assertEqualBin(MD5("abc"),
                            unhex('900150983cd24fb0d6963f7d28e17f72'))
        self.assertEqualBin(MD5("message digest"),
                            unhex('f96b697d7cb7938d525a2f31aaf161d0'))
        self.assertEqualBin(MD5("abcdefghijklmnopqrstuvwxyz"),
                            unhex('c3fcd3d76192e4007dfb496cca67e13b'))
        self.assertEqualBin(MD5("ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                                "abcdefghijklmnopqrstuvwxyz0123456789"),
                            unhex('d174ab98d277d9f5a5611c2c9f419d9f'))
        self.assertEqualBin(MD5("1234567890123456789012345678901234567890"
                                "1234567890123456789012345678901234567890"),
                            unhex('57edf4a22be3c955ac49da2e2107b67a'))

    def testHmacMD5(self):
        
        self.assertEqualBin(mac_str('hmac_md5', unhex('0b'*16), "Hi There"),
                         unhex('9294727a3638bb1c13f48ef8158bfc9d'))
        self.assertEqualBin(mac_str('hmac_md5', "Jefe",
                                 "what do ya want for nothing?"),
                         unhex('750c783e6ab0b503eaa86e310a5db738'))
        self.assertEqualBin(mac_str('hmac_md5', unhex('aa'*16), unhex('dd'*50)),
                         unhex('56be34521d144c88dbb8c733f0e8b3f6'))

    def testSHA1(self):
        for hashname in ['sha1_sw', 'sha1_hw']:
            if ssh_hash_new(hashname) is None:
                continue 

            
            
            self.assertEqualBin(hash_str(hashname, "abc"), unhex(
                "a9993e364706816aba3e25717850c26c9cd0d89d"))
            self.assertEqualBin(hash_str(hashname,
                "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"),
                unhex("84983e441c3bd26ebaae4aa1f95129e5e54670f1"))
            self.assertEqualBin(hash_str_iter(hashname,
                ("a" * 1000 for _ in range(1000))), unhex(
                "34aa973cd4c4daa4f61eeb2bdbad27316534016f"))
            self.assertEqualBin(hash_str(hashname,
                "01234567012345670123456701234567" * 20), unhex(
                "dea356a2cddd90c7a7ecedc5ebb563934f460452"))
            self.assertEqualBin(hash_str(hashname, b"\x5e"), unhex(
                "5e6f80a34a9798cafc6a5db96cc57ba4c4db59c2"))
            self.assertEqualBin(hash_str(hashname,
                unhex("9a7dfdf1ecead06ed646aa55fe757146")), unhex(
                "82abff6605dbe1c17def12a394fa22a82b544a35"))
            self.assertEqualBin(hash_str(hashname, unhex(
                "f78f92141bcd170ae89b4fba15a1d59f"
                "3fd84d223c9251bdacbbae61d05ed115"
                "a06a7ce117b7beead24421ded9c32592"
                "bd57edeae39c39fa1fe8946a84d0cf1f"
                "7beead1713e2e0959897347f67c80b04"
                "00c209815d6b10a683836fd5562a56ca"
                "b1a28e81b6576654631cf16566b86e3b"
                "33a108b05307c00aff14a768ed735060"
                "6a0f85e6a91d396f5b5cbe577f9b3880"
                "7c7d523d6d792f6ebc24a4ecf2b3a427"
                "cdbbfb")), unhex(
                "cb0082c8f197d260991ba6a460e76e202bad27b3"))

    def testSHA256(self):
        for hashname in ['sha256_sw', 'sha256_hw']:
            if ssh_hash_new(hashname) is None:
                continue 

            
            
            self.assertEqualBin(hash_str(hashname, "abc"),
                                unhex("ba7816bf8f01cfea414140de5dae2223"
                                      "b00361a396177a9cb410ff61f20015ad"))
            self.assertEqualBin(hash_str(hashname,
                "abcdbcdecdefdefgefghfghighijhijk""ijkljklmklmnlmnomnopnopq"),
                                unhex("248d6a61d20638b8e5c026930c3e6039"
                                      "a33ce45964ff2167f6ecedd419db06c1"))
            self.assertEqualBin(
                hash_str_iter(hashname, ("a" * 1000 for _ in range(1000))),
                unhex("cdc76e5c9914fb9281a1c7e284d73e67"
                      "f1809a48a497200e046d39ccc7112cd0"))
            self.assertEqualBin(
                hash_str(hashname, "01234567012345670123456701234567" * 20),
                unhex("594847328451bdfa85056225462cc1d8"
                      "67d877fb388df0ce35f25ab5562bfbb5"))
            self.assertEqualBin(hash_str(hashname, b"\x19"),
                                unhex("68aa2e2ee5dff96e3355e6c7ee373e3d"
                                      "6a4e17f75f9518d843709c0c9bc3e3d4"))
            self.assertEqualBin(
                hash_str(hashname, unhex("e3d72570dcdd787ce3887ab2cd684652")),
                unhex("175ee69b02ba9b58e2b0a5fd13819cea"
                      "573f3940a94f825128cf4209beabb4e8"))
            self.assertEqualBin(hash_str(hashname, unhex(
                "8326754e2277372f4fc12b20527afef0"
                "4d8a056971b11ad57123a7c137760000"
                "d7bef6f3c1f7a9083aa39d810db31077"
                "7dab8b1e7f02b84a26c773325f8b2374"
                "de7a4b5a58cb5c5cf35bcee6fb946e5b"
                "d694fa593a8beb3f9d6592ecedaa66ca"
                "82a29d0c51bcf9336230e5d784e4c0a4"
                "3f8d79a30a165cbabe452b774b9c7109"
                "a97d138f129228966f6c0adc106aad5a"
                "9fdd30825769b2c671af6759df28eb39"
                "3d54d6")), unhex(
                    "97dbca7df46d62c8a422c941dd7e835b"
                    "8ad3361763f7e9b2d95f4f0da6e1ccbc"))

    def testSHA384(self):
        
        
        self.assertEqualBin(hash_str('sha384', "abc"), unhex(
            'cb00753f45a35e8bb5a03d699ac65007272c32ab0eded163'
            '1a8b605a43ff5bed8086072ba1e7cc2358baeca134c825a7'))
        self.assertEqualBin(hash_str('sha384',
            "abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmn"
            "hijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu"), unhex(
            '09330c33f71147e83d192fc782cd1b4753111b173b3b05d2'
            '2fa08086e3b0f712fcc7c71a557e2db966c3e9fa91746039'))
        self.assertEqualBin(hash_str_iter('sha384',
            ("a" * 1000 for _ in range(1000))), unhex(
            '9d0e1809716474cb086e834e310a4a1ced149e9c00f24852'
            '7972cec5704c2a5b07b8b3dc38ecc4ebae97ddd87f3d8985'))
        self.assertEqualBin(hash_str('sha384',
            "01234567012345670123456701234567" * 20), unhex(
            '2fc64a4f500ddb6828f6a3430b8dd72a368eb7f3a8322a70'
            'bc84275b9c0b3ab00d27a5cc3c2d224aa6b61a0d79fb4596'))
        self.assertEqualBin(hash_str('sha384', b"\xB9"), unhex(
            'bc8089a19007c0b14195f4ecc74094fec64f01f90929282c'
            '2fb392881578208ad466828b1c6c283d2722cf0ad1ab6938'))
        self.assertEqualBin(hash_str('sha384',
            unhex("a41c497779c0375ff10a7f4e08591739")), unhex(
            'c9a68443a005812256b8ec76b00516f0dbb74fab26d66591'
            '3f194b6ffb0e91ea9967566b58109cbc675cc208e4c823f7'))
        self.assertEqualBin(hash_str('sha384', unhex(
            "399669e28f6b9c6dbcbb6912ec10ffcf74790349b7dc8fbe4a8e7b3b5621db0f"
            "3e7dc87f823264bbe40d1811c9ea2061e1c84ad10a23fac1727e7202fc3f5042"
            "e6bf58cba8a2746e1f64f9b9ea352c711507053cf4e5339d52865f25cc22b5e8"
            "7784a12fc961d66cb6e89573199a2ce6565cbdf13dca403832cfcb0e8b7211e8"
            "3af32a11ac17929ff1c073a51cc027aaedeff85aad7c2b7c5a803e2404d96d2a"
            "77357bda1a6daeed17151cb9bc5125a422e941de0ca0fc5011c23ecffefdd096"
            "76711cf3db0a3440720e1615c1f22fbc3c721de521e1b99ba1bd557740864214"
            "7ed096")), unhex(
            '4f440db1e6edd2899fa335f09515aa025ee177a79f4b4aaf'
            '38e42b5c4de660f5de8fb2a5b2fbd2a3cbffd20cff1288c0'))

    def testSHA512(self):
        
        
        self.assertEqualBin(hash_str('sha512', "abc"), unhex(
            'ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a'
            '2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f'))
        self.assertEqualBin(hash_str('sha512',
            "abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmn"
            "hijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu"), unhex(
            '8e959b75dae313da8cf4f72814fc143f8f7779c6eb9f7fa17299aeadb6889018'
            '501d289e4900f7e4331b99dec4b5433ac7d329eeb6dd26545e96e55b874be909'))
        self.assertEqualBin(hash_str_iter('sha512',
            ("a" * 1000 for _ in range(1000))), unhex(
            'e718483d0ce769644e2e42c7bc15b4638e1f98b13b2044285632a803afa973eb'
            'de0ff244877ea60a4cb0432ce577c31beb009c5c2c49aa2e4eadb217ad8cc09b'))
        self.assertEqualBin(hash_str('sha512',
            "01234567012345670123456701234567" * 20), unhex(
            '89d05ba632c699c31231ded4ffc127d5a894dad412c0e024db872d1abd2ba814'
            '1a0f85072a9be1e2aa04cf33c765cb510813a39cd5a84c4acaa64d3f3fb7bae9'))
        self.assertEqualBin(hash_str('sha512', b"\xD0"), unhex(
            '9992202938e882e73e20f6b69e68a0a7149090423d93c81bab3f21678d4aceee'
            'e50e4e8cafada4c85a54ea8306826c4ad6e74cece9631bfa8a549b4ab3fbba15'))
        self.assertEqualBin(hash_str('sha512',
            unhex("8d4e3c0e3889191491816e9d98bff0a0")), unhex(
            'cb0b67a4b8712cd73c9aabc0b199e9269b20844afb75acbdd1c153c9828924c3'
            'ddedaafe669c5fdd0bc66f630f6773988213eb1b16f517ad0de4b2f0c95c90f8'))
        self.assertEqualBin(hash_str('sha512', unhex(
            "a55f20c411aad132807a502d65824e31a2305432aa3d06d3e282a8d84e0de1de"
            "6974bf495469fc7f338f8054d58c26c49360c3e87af56523acf6d89d03e56ff2"
            "f868002bc3e431edc44df2f0223d4bb3b243586e1a7d924936694fcbbaf88d95"
            "19e4eb50a644f8e4f95eb0ea95bc4465c8821aacd2fe15ab4981164bbb6dc32f"
            "969087a145b0d9cc9c67c22b763299419cc4128be9a077b3ace634064e6d9928"
            "3513dc06e7515d0d73132e9a0dc6d3b1f8b246f1a98a3fc72941b1e3bb2098e8"
            "bf16f268d64f0b0f4707fe1ea1a1791ba2f3c0c758e5f551863a96c949ad47d7"
            "fb40d2")), unhex(
            'c665befb36da189d78822d10528cbf3b12b3eef726039909c1a16a270d487193'
            '77966b957a878e720584779a62825c18da26415e49a7176a894e7510fd1451f5'))

    def testSHA3(self):
        
        
        

        self.assertEqualBin(hash_str('sha3_224', ''), unhex("6b4e03423667dbb73b6e15454f0eb1abd4597f9a1b078e3f5b5a6bc7"))
        self.assertEqualBin(hash_str('sha3_224', unhex('a3')*200), unhex("9376816aba503f72f96ce7eb65ac095deee3be4bf9bbc2a1cb7e11e0"))
        self.assertEqualBin(hash_str('sha3_256', ''), unhex("a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"))
        self.assertEqualBin(hash_str('sha3_256', unhex('a3')*200), unhex("79f38adec5c20307a98ef76e8324afbfd46cfd81b22e3973c65fa1bd9de31787"))
        self.assertEqualBin(hash_str('sha3_384', ''), unhex("0c63a75b845e4f7d01107d852e4c2485c51a50aaaa94fc61995e71bbee983a2ac3713831264adb47fb6bd1e058d5f004"))
        self.assertEqualBin(hash_str('sha3_384', unhex('a3')*200), unhex("1881de2ca7e41ef95dc4732b8f5f002b189cc1e42b74168ed1732649ce1dbcdd76197a31fd55ee989f2d7050dd473e8f"))
        self.assertEqualBin(hash_str('sha3_512', ''), unhex("a69f73cca23a9ac5c8b567dc185a756e97c982164fe25859e0d1dcc1475c80a615b2123af1f5f94c11e3e9402c3ac558f500199d95b6d3e301758586281dcd26"))
        self.assertEqualBin(hash_str('sha3_512', unhex('a3')*200), unhex("e76dfad22084a8b1467fcf2ffa58361bec7628edf5f3fdc0e4805dc48caeeca81b7c13c30adf52a3659584739a2df46be589c51ca1a4a8416df6545a1ce8ba00"))
        self.assertEqualBin(hash_str('shake256_114bytes', ''), unhex("46b9dd2b0ba88d13233b3feb743eeb243fcd52ea62b81b82b50c27646ed5762fd75dc4ddd8c0f200cb05019d67b592f6fc821c49479ab48640292eacb3b7c4be141e96616fb13957692cc7edd0b45ae3dc07223c8e92937bef84bc0eab862853349ec75546f58fb7c2775c38462c5010d846"))
        self.assertEqualBin(hash_str('shake256_114bytes', unhex('a3')*200), unhex("cd8a920ed141aa0407a22d59288652e9d9f1a7ee0c1e7c1ca699424da84a904d2d700caae7396ece96604440577da4f3aa22aeb8857f961c4cd8e06f0ae6610b1048a7f64e1074cd629e85ad7566048efc4fb500b486a3309a8f26724c0ed628001a1099422468de726f1061d99eb9e93604"))

    def testHmacSHA(self):
        
        def vector(key, message, s1=None, s256=None):
            if s1 is not None:
                self.assertEqualBin(
                    mac_str('hmac_sha1', key, message), unhex(s1))
            if s256 is not None:
                self.assertEqualBin(
                    mac_str('hmac_sha256', key, message), unhex(s256))
        vector(
            unhex("0b"*20), "Hi There",
            "b617318655057264e28bc0b6fb378c8ef146be00",
            "b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7")
        vector(
            "Jefe", "what do ya want for nothing?",
            "effcdf6ae5eb2fa2d27416d5f184df9c259a7c79",
            "5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843")
        vector(
            unhex("aa"*20), unhex('dd'*50),
            "125d7342b9ac11cd91a39af48aa17b4f63f175d3",
            "773ea91e36800e46854db8ebd09181a72959098b3ef8c122d9635514ced565FE")
        vector(
            unhex("0102030405060708090a0b0c0d0e0f10111213141516171819"),
            unhex("cd"*50),
            "4c9007f4026250c6bc8414f9bf50c86c2d7235da",
            "82558a389a443c0ea4cc819899f2083a85f0faa3e578f8077a2e3ff46729665b")
        vector(
            unhex("aa"*80),
            "Test Using Larger Than Block-Size Key - Hash Key First",
            s1="aa4ae5e15272d00e95705637ce8a3b55ed402112")
        vector(
            unhex("aa"*131),
            "Test Using Larger Than Block-Size Key - Hash Key First",
            s256="60e431591ee0b67f0d8a26aacbf5b77f"
            "8e0bc6213728c5140546040f0ee37f54")
        vector(
            unhex("aa"*80),
            "Test Using Larger Than Block-Size Key and "
            "Larger Than One Block-Size Data",
            s1="e8e99d0f45237d786d6bbaa7965c7808bbff1a91")
        vector(
            unhex("aa"*131),
            "This is a test using a larger than block-size key and a "
            "larger than block-size data. The key needs to be hashed "
            "before being used by the HMAC algorithm.",
            s256="9B09FFA71B942FCB27635FBCD5B0E944BFDC63644F0713938A7F51535C3A35E2")

    def testEd25519(self):
        def vector(privkey, pubkey, message, signature):
            x, y = ecc_edwards_get_affine(eddsa_public(
                mp_from_bytes_le(privkey), 'ed25519'))
            self.assertEqual(int(y) | ((int(x) & 1) << 255),
                             int(mp_from_bytes_le(pubkey)))
            pubblob = ssh_string(b"ssh-ed25519") + ssh_string(pubkey)
            privblob = ssh_string(privkey)
            sigblob = ssh_string(b"ssh-ed25519") + ssh_string(signature)
            pubkey = ssh_key_new_pub('ed25519', pubblob)
            self.assertTrue(ssh_key_verify(pubkey, sigblob, message))
            privkey = ssh_key_new_priv('ed25519', pubblob, privblob)
            
            
            
            
            
            
            
            self.assertEqualBin(ssh_key_sign(privkey, message, 0), sigblob)

        
        
        
        privkey = unhex(
            'c89955e0f7741d905df0730b3dc2b0ce1a13134e44fef3d40d60c020ef19df77')
        pubkey = unhex(
            'fdb30673402faf1c8033714f3517e47cc0f91fe70cf3836d6c23636e3fd2287c')
        message = unhex(
            '507c94c8820d2a5793cbf3442b3d71936f35fe3afef316')
        signature = unhex(
            '7ef66e5e86f2360848e0014e94880ae2920ad8a3185a46b35d1e07dea8fa8ae4'
            'f6b843ba174d99fa7986654a0891c12a794455669375bf92af4cc2770b579e0c')
        vector(privkey, pubkey, message, signature)

        
        
        
        
        ed25519_test_vector_path = None
        if ed25519_test_vector_path is not None:
            with open(ed25519_test_vector_path) as f:
                for line in iter(f.readline, ""):
                    words = line.split(":")
                    
                    
                    
                    
                    privkey = unhex(words[0])[:32]
                    pubkey = unhex(words[1])
                    message = unhex(words[2])
                    signature = unhex(words[3])[:64]
                    vector(privkey, pubkey, message, signature)

    def testEd448(self):
        def vector(privkey, pubkey, message, signature):
            x, y = ecc_edwards_get_affine(eddsa_public(
                mp_from_bytes_le(privkey), 'ed448'))
            self.assertEqual(int(y) | ((int(x) & 1) << 455),
                             int(mp_from_bytes_le(pubkey)))
            pubblob = ssh_string(b"ssh-ed448") + ssh_string(pubkey)
            privblob = ssh_string(privkey)
            sigblob = ssh_string(b"ssh-ed448") + ssh_string(signature)
            pubkey = ssh_key_new_pub('ed448', pubblob)
            self.assertTrue(ssh_key_verify(pubkey, sigblob, message))
            privkey = ssh_key_new_priv('ed448', pubblob, privblob)
            
            self.assertEqualBin(ssh_key_sign(privkey, message, 0), sigblob)

        

        privkey = unhex('6c82a562cb808d10d632be89c8513ebf6c929f34ddfa8c9f63c9960ef6e348a3528c8a3fcc2f044e39a3fc5b94492f8f032e7549a20098f95b')
        pubkey = unhex('5fd7449b59b461fd2ce787ec616ad46a1da1342485a70e1f8a0ea75d80e96778edf124769b46c7061bd6783df1e50f6cd1fa1abeafe8256180')
        message = b''
        signature = unhex('533a37f6bbe457251f023c0d88f976ae2dfb504a843e34d2074fd823d41a591f2b233f034f628281f2fd7a22ddd47d7828c59bd0a21bfd3980ff0d2028d4b18a9df63e006c5d1c2d345b925d8dc00b4104852db99ac5c7cdda8530a113a0f4dbb61149f05a7363268c71d95808ff2e652600')
        vector(privkey, pubkey, message, signature)

        privkey = unhex('c4eab05d357007c632f3dbb48489924d552b08fe0c353a0d4a1f00acda2c463afbea67c5e8d2877c5e3bc397a659949ef8021e954e0a12274e')
        pubkey = unhex('43ba28f430cdff456ae531545f7ecd0ac834a55d9358c0372bfa0c6c6798c0866aea01eb00742802b8438ea4cb82169c235160627b4c3a9480')
        message = unhex('03')
        signature = unhex('26b8f91727bd62897af15e41eb43c377efb9c610d48f2335cb0bd0087810f4352541b143c4b981b7e18f62de8ccdf633fc1bf037ab7cd779805e0dbcc0aae1cbcee1afb2e027df36bc04dcecbf154336c19f0af7e0a6472905e799f1953d2a0ff3348ab21aa4adafd1d234441cf807c03a00')
        vector(privkey, pubkey, message, signature)

        privkey = unhex('cd23d24f714274e744343237b93290f511f6425f98e64459ff203e8985083ffdf60500553abc0e05cd02184bdb89c4ccd67e187951267eb328')
        pubkey = unhex('dcea9e78f35a1bf3499a831b10b86c90aac01cd84b67a0109b55a36e9328b1e365fce161d71ce7131a543ea4cb5f7e9f1d8b00696447001400')
        message = unhex('0c3e544074ec63b0265e0c')
        signature = unhex('1f0a8888ce25e8d458a21130879b840a9089d999aaba039eaf3e3afa090a09d389dba82c4ff2ae8ac5cdfb7c55e94d5d961a29fe0109941e00b8dbdeea6d3b051068df7254c0cdc129cbe62db2dc957dbb47b51fd3f213fb8698f064774250a5028961c9bf8ffd973fe5d5c206492b140e00')
        vector(privkey, pubkey, message, signature)

        privkey = unhex('258cdd4ada32ed9c9ff54e63756ae582fb8fab2ac721f2c8e676a72768513d939f63dddb55609133f29adf86ec9929dccb52c1c5fd2ff7e21b')
        pubkey = unhex('3ba16da0c6f2cc1f30187740756f5e798d6bc5fc015d7c63cc9510ee3fd44adc24d8e968b6e46e6f94d19b945361726bd75e149ef09817f580')
        message = unhex('64a65f3cdedcdd66811e2915')
        signature = unhex('7eeeab7c4e50fb799b418ee5e3197ff6bf15d43a14c34389b59dd1a7b1b85b4ae90438aca634bea45e3a2695f1270f07fdcdf7c62b8efeaf00b45c2c96ba457eb1a8bf075a3db28e5c24f6b923ed4ad747c3c9e03c7079efb87cb110d3a99861e72003cbae6d6b8b827e4e6c143064ff3c00')
        vector(privkey, pubkey, message, signature)

        privkey = unhex('d65df341ad13e008567688baedda8e9dcdc17dc024974ea5b4227b6530e339bff21f99e68ca6968f3cca6dfe0fb9f4fab4fa135d5542ea3f01')
        pubkey = unhex('df9705f58edbab802c7f8363cfe5560ab1c6132c20a9f1dd163483a26f8ac53a39d6808bf4a1dfbd261b099bb03b3fb50906cb28bd8a081f00')
        message = unhex('bd0f6a3747cd561bdddf4640a332461a4a30a12a434cd0bf40d766d9c6d458e5512204a30c17d1f50b5079631f64eb3112182da3005835461113718d1a5ef944')
        signature = unhex('554bc2480860b49eab8532d2a533b7d578ef473eeb58c98bb2d0e1ce488a98b18dfde9b9b90775e67f47d4a1c3482058efc9f40d2ca033a0801b63d45b3b722ef552bad3b4ccb667da350192b61c508cf7b6b5adadc2c8d9a446ef003fb05cba5f30e88e36ec2703b349ca229c2670833900')
        vector(privkey, pubkey, message, signature)

        privkey = unhex('2ec5fe3c17045abdb136a5e6a913e32ab75ae68b53d2fc149b77e504132d37569b7e766ba74a19bd6162343a21c8590aa9cebca9014c636df5')
        pubkey = unhex('79756f014dcfe2079f5dd9e718be4171e2ef2486a08f25186f6bff43a9936b9bfe12402b08ae65798a3d81e22e9ec80e7690862ef3d4ed3a00')
        message = unhex('15777532b0bdd0d1389f636c5f6b9ba734c90af572877e2d272dd078aa1e567cfa80e12928bb542330e8409f3174504107ecd5efac61ae7504dabe2a602ede89e5cca6257a7c77e27a702b3ae39fc769fc54f2395ae6a1178cab4738e543072fc1c177fe71e92e25bf03e4ecb72f47b64d0465aaea4c7fad372536c8ba516a6039c3c2a39f0e4d832be432dfa9a706a6e5c7e19f397964ca4258002f7c0541b590316dbc5622b6b2a6fe7a4abffd96105eca76ea7b98816af0748c10df048ce012d901015a51f189f3888145c03650aa23ce894c3bd889e030d565071c59f409a9981b51878fd6fc110624dcbcde0bf7a69ccce38fabdf86f3bef6044819de11')
        signature = unhex('c650ddbb0601c19ca11439e1640dd931f43c518ea5bea70d3dcde5f4191fe53f00cf966546b72bcc7d58be2b9badef28743954e3a44a23f880e8d4f1cfce2d7a61452d26da05896f0a50da66a239a8a188b6d825b3305ad77b73fbac0836ecc60987fd08527c1a8e80d5823e65cafe2a3d00')
        vector(privkey, pubkey, message, signature)

        privkey = unhex('872d093780f5d3730df7c212664b37b8a0f24f56810daa8382cd4fa3f77634ec44dc54f1c2ed9bea86fafb7632d8be199ea165f5ad55dd9ce8')
        pubkey = unhex('a81b2e8a70a5ac94ffdbcc9badfc3feb0801f258578bb114ad44ece1ec0e799da08effb81c5d685c0c56f64eecaef8cdf11cc38737838cf400')
        message = unhex('6ddf802e1aae4986935f7f981ba3f0351d6273c0a0c22c9c0e8339168e675412a3debfaf435ed651558007db4384b650fcc07e3b586a27a4f7a00ac8a6fec2cd86ae4bf1570c41e6a40c931db27b2faa15a8cedd52cff7362c4e6e23daec0fbc3a79b6806e316efcc7b68119bf46bc76a26067a53f296dafdbdc11c77f7777e972660cf4b6a9b369a6665f02e0cc9b6edfad136b4fabe723d2813db3136cfde9b6d044322fee2947952e031b73ab5c603349b307bdc27bc6cb8b8bbd7bd323219b8033a581b59eadebb09b3c4f3d2277d4f0343624acc817804728b25ab797172b4c5c21a22f9c7839d64300232eb66e53f31c723fa37fe387c7d3e50bdf9813a30e5bb12cf4cd930c40cfb4e1fc622592a49588794494d56d24ea4b40c89fc0596cc9ebb961c8cb10adde976a5d602b1c3f85b9b9a001ed3c6a4d3b1437f52096cd1956d042a597d561a596ecd3d1735a8d570ea0ec27225a2c4aaff26306d1526c1af3ca6d9cf5a2c98f47e1c46db9a33234cfd4d81f2c98538a09ebe76998d0d8fd25997c7d255c6d66ece6fa56f11144950f027795e653008f4bd7ca2dee85d8e90f3dc315130ce2a00375a318c7c3d97be2c8ce5b6db41a6254ff264fa6155baee3b0773c0f497c573f19bb4f4240281f0b1f4f7be857a4e59d416c06b4c50fa09e1810ddc6b1467baeac5a3668d11b6ecaa901440016f389f80acc4db977025e7f5924388c7e340a732e554440e76570f8dd71b7d640b3450d1fd5f0410a18f9a3494f707c717b79b4bf75c98400b096b21653b5d217cf3565c9597456f70703497a078763829bc01bb1cbc8fa04eadc9a6e3f6699587a9e75c94e5bab0036e0b2e711392cff0047d0d6b05bd2a588bc109718954259f1d86678a579a3120f19cfb2963f177aeb70f2d4844826262e51b80271272068ef5b3856fa8535aa2a88b2d41f2a0e2fda7624c2850272ac4a2f561f8f2f7a318bfd5caf9696149e4ac824ad3460538fdc25421beec2cc6818162d06bbed0c40a387192349db67a118bada6cd5ab0140ee273204f628aad1c135f770279a651e24d8c14d75a6059d76b96a6fd857def5e0b354b27ab937a5815d16b5fae407ff18222c6d1ed263be68c95f32d908bd895cd76207ae726487567f9a67dad79abec316f683b17f2d02bf07e0ac8b5bc6162cf94697b3c27cd1fea49b27f23ba2901871962506520c392da8b6ad0d99f7013fbc06c2c17a569500c8a7696481c1cd33e9b14e40b82e79a5f5db82571ba97bae3ad3e0479515bb0e2b0f3bfcd1fd33034efc6245eddd7ee2086ddae2600d8ca73e214e8c2b0bdb2b047c6a464a562ed77b73d2d841c4b34973551257713b753632efba348169abc90a68f42611a40126d7cb21b58695568186f7e569d2ff0f9e745d0487dd2eb997cafc5abf9dd102e62ff66cba87')
        signature = unhex('e301345a41a39a4d72fff8df69c98075a0cc082b802fc9b2b6bc503f926b65bddf7f4c8f1cb49f6396afc8a70abe6d8aef0db478d4c6b2970076c6a0484fe76d76b3a97625d79f1ce240e7c576750d295528286f719b413de9ada3e8eb78ed573603ce30d8bb761785dc30dbc320869e1a00')
        vector(privkey, pubkey, message, signature)

    def testMontgomeryKex(self):
        
        
        
        rfc7748s5_2 = [
            ('curve25519',
             'a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4',
             'e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c',
             0xc3da55379de9c6908e94ea4df28d084f32eccf03491c71f754b4075577a28552),
            ('curve25519',
             '4b66e9d4d1b4673c5ad22691957d6af5c11b6421e0ea01d42ca4169e7918ba0d',
             'e5210f12786811d3f4b7959d0538ae2c31dbe7106fc03c3efc4cd549c715a493',
             0x95cbde9476e8907d7aade45cb4b873f88b595a68799fa152e6f8f7647aac7957),
            ('curve448',
             '3d262fddf9ec8e88495266fea19a34d28882acef045104d0d1aae121700a779c984c24f8cdd78fbff44943eba368f54b29259a4f1c600ad3',
             '06fce640fa3487bfda5f6cf2d5263f8aad88334cbd07437f020f08f9814dc031ddbdc38c19c6da2583fa5429db94ada18aa7a7fb4ef8a086',
             0xce3e4ff95a60dc6697da1db1d85e6afbdf79b50a2412d7546d5f239fe14fbaadeb445fc66a01b0779d98223961111e21766282f73dd96b6f),
            ('curve448',
             '203d494428b8399352665ddca42f9de8fef600908e0d461cb021f8c538345dd77c3e4806e25f46d3315c44e0a5b4371282dd2c8d5be3095f',
             '0fbcc2f993cd56d3305b0b7d9e55d4c1a8fb5dbb52f8e9a1e9b6201b165d015894e56c4d3570bee52fe205e28a78b91cdfbde71ce8d157db',
             0x884a02576239ff7a2f2f63b2db6a9ff37047ac13568e1e30fe63c4a7ad1b3ee3a5700df34321d62077e63633c575c1c954514e99da7c179d),
        ]

        for method, priv, pub, expected in rfc7748s5_2:
            with queued_specific_random_data(unhex(priv)):
                ecdh = ssh_ecdhkex_newkey(method)
            key = ssh_ecdhkex_getkey(ecdh, unhex(pub))
            self.assertEqual(int(key), expected)

        
        
        
        rfc7748s6 = [
            ('curve25519', 
             '77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a',
             '8520f0098930a754748b7ddcb43ef75a0dbf3a0d26381af4eba4a98eaa9b4e6a',
             '5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb',
             'de9edb7d7b7dc1b4d35b61c2ece435373f8343c85b78674dadfc7e146f882b4f',
             0x4a5d9d5ba4ce2de1728e3bf480350f25e07e21c947d19e3376f09b3c1e161742),
            ('curve448', 
             '9a8f4925d1519f5775cf46b04b5800d4ee9ee8bae8bc5565d498c28dd9c9baf574a9419744897391006382a6f127ab1d9ac2d8c0a598726b',
             '9b08f7cc31b7e3e67d22d5aea121074a273bd2b83de09c63faa73d2c22c5d9bbc836647241d953d40c5b12da88120d53177f80e532c41fa0',
             '1c306a7ac2a0e2e0990b294470cba339e6453772b075811d8fad0d1d6927c120bb5ee8972b0d3e21374c9c921b09d1b0366f10b65173992d',
             '3eb7a829b0cd20f5bcfc0b599b6feccf6da4627107bdb0d4f345b43027d8b972fc3e34fb4232a13ca706dcb57aec3dae07bdc1c67bf33609',
             0x07fff4181ac6cc95ec1c16a94a0f74d12da232ce40a77552281d282bb60c0b56fd2464c335543936521c24403085d59a449a5037514a879d),
        ]

        for method, apriv, apub, bpriv, bpub, expected in rfc7748s6:
            with queued_specific_random_data(unhex(apriv)):
                alice = ssh_ecdhkex_newkey(method)
            with queued_specific_random_data(unhex(bpriv)):
                bob = ssh_ecdhkex_newkey(method)
            self.assertEqualBin(ssh_ecdhkex_getpublic(alice), unhex(apub))
            self.assertEqualBin(ssh_ecdhkex_getpublic(bob), unhex(bpub))
            akey = ssh_ecdhkex_getkey(alice, unhex(bpub))
            bkey = ssh_ecdhkex_getkey(bob, unhex(apub))
            self.assertEqual(int(akey), expected)
            self.assertEqual(int(bkey), expected)

    def testCRC32(self):
        self.assertEqual(crc32_rfc1662("123456789"), 0xCBF43926)
        self.assertEqual(crc32_ssh1("123456789"), 0x2DFD2D88)

        
        
        
        reveng_tests = [
            '000000001CDF4421',
            'F20183779DAB24',
            '0FAA005587B2C9B6',
            '00FF55111262A032',
            '332255AABBCCDDEEFF3D86AEB0',
            '926B559BA2DE9C',
            'FFFFFFFFFFFFFFFF',
            'C008300028CFE9521D3B08EA449900E808EA449900E8300102007E649416',
            '6173640ACEDE2D15',
        ]
        for vec in map(unhex, reveng_tests):
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            expected = struct.unpack("<L", vec[-4:])[0]
            self.assertEqual(crc32_rfc1662(vec[:-4]), expected)
            self.assertEqual(crc32_rfc1662(vec), 0x2144DF1C)

if __name__ == "__main__":
    
    
    testprogram = unittest.main(exit=False)

    
    if not testprogram.result.wasSuccessful():
        childprocess.wait_for_exit()
        sys.exit(1)

    
    
    
    
    childprocess.check_return_status()
