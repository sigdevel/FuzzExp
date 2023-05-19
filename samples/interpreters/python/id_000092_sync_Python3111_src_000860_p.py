import unittest
import unittest.mock
import random
import time
import pickle
import warnings
from functools import partial
from math import log, exp, pi, fsum, sin
from test import support

class TestBasicOps:
    
    
    

    def randomlist(self, n):
        """Helper function to make a list of random numbers"""
        return [self.gen.random() for i in range(n)]

    def test_autoseed(self):
        self.gen.seed()
        state1 = self.gen.getstate()
        time.sleep(0.1)
        self.gen.seed()      
        state2 = self.gen.getstate()
        self.assertNotEqual(state1, state2)

    def test_saverestore(self):
        N = 1000
        self.gen.seed()
        state = self.gen.getstate()
        randseq = self.randomlist(N)
        self.gen.setstate(state)    
        self.assertEqual(randseq, self.randomlist(N))

    def test_seedargs(self):
        
        class MySeed(object):
            def __hash__(self):
                return -1729
        for arg in [None, 0, 0, 1, 1, -1, -1, 10**20, -(10**20),
                    3.14, 1+2j, 'a', tuple('abc'), MySeed()]:
            self.gen.seed(arg)
        for arg in [list(range(3)), dict(one=1)]:
            self.assertRaises(TypeError, self.gen.seed, arg)
        self.assertRaises(TypeError, self.gen.seed, 1, 2, 3, 4)
        self.assertRaises(TypeError, type(self.gen), [])

    @unittest.mock.patch('random._urandom') 
    def test_seed_when_randomness_source_not_found(self, urandom_mock):
        
        
        
        
        
        urandom_mock.side_effect = NotImplementedError
        self.test_seedargs()

    def test_shuffle(self):
        shuffle = self.gen.shuffle
        lst = []
        shuffle(lst)
        self.assertEqual(lst, [])
        lst = [37]
        shuffle(lst)
        self.assertEqual(lst, [37])
        seqs = [list(range(n)) for n in range(10)]
        shuffled_seqs = [list(range(n)) for n in range(10)]
        for shuffled_seq in shuffled_seqs:
            shuffle(shuffled_seq)
        for (seq, shuffled_seq) in zip(seqs, shuffled_seqs):
            self.assertEqual(len(seq), len(shuffled_seq))
            self.assertEqual(set(seq), set(shuffled_seq))
        
        
        
        
        
        
        
        
        
        
        lst = list(range(1000))
        shuffled_lst = list(range(1000))
        shuffle(shuffled_lst)
        self.assertTrue(lst != shuffled_lst)
        shuffle(lst)
        self.assertTrue(lst != shuffled_lst)

    def test_choice(self):
        choice = self.gen.choice
        with self.assertRaises(IndexError):
            choice([])
        self.assertEqual(choice([50]), 50)
        self.assertIn(choice([25, 75]), [25, 75])

    def test_sample(self):
        
        
        N = 100
        population = range(N)
        for k in range(N+1):
            s = self.gen.sample(population, k)
            self.assertEqual(len(s), k)
            uniq = set(s)
            self.assertEqual(len(uniq), k)
            self.assertTrue(uniq <= set(population))
        self.assertEqual(self.gen.sample([], 0), [])  
        
        self.assertRaises(ValueError, self.gen.sample, population, N+1)

    def test_sample_distribution(self):
        
        
        n = 5
        pop = range(n)
        trials = 10000  
        def factorial(n):
            if n == 0:
                return 1
            return n * factorial(n - 1)
        for k in range(n):
            expected = factorial(n) // factorial(n-k)
            perms = {}
            for i in range(trials):
                perms[tuple(self.gen.sample(pop, k))] = None
                if len(perms) == expected:
                    break
            else:
                self.fail()

    def test_sample_inputs(self):
        
        self.gen.sample(set(range(20)), 2)
        self.gen.sample(range(20), 2)
        self.gen.sample(range(20), 2)
        self.gen.sample(str('abcdefghijklmnopqrst'), 2)
        self.gen.sample(tuple('abcdefghijklmnopqrst'), 2)

    def test_sample_on_dicts(self):
        self.assertRaises(TypeError, self.gen.sample, dict.fromkeys('abcdef'), 2)

    def test_gauss(self):
        
        
        

        for seed in 1, 12, 123, 1234, 12345, 123456, 654321:
            self.gen.seed(seed)
            x1 = self.gen.random()
            y1 = self.gen.gauss(0, 1)

            self.gen.seed(seed)
            x2 = self.gen.random()
            y2 = self.gen.gauss(0, 1)

            self.assertEqual(x1, x2)
            self.assertEqual(y1, y2)

    def test_pickling(self):
        for proto in range(pickle.HIGHEST_PROTOCOL + 1):
            state = pickle.dumps(self.gen, proto)
            origseq = [self.gen.random() for i in range(10)]
            newgen = pickle.loads(state)
            restoredseq = [newgen.random() for i in range(10)]
            self.assertEqual(origseq, restoredseq)

    def test_bug_1727780(self):
        
        
        
        files = [("randv2_32.pck", 780),
                 ("randv2_64.pck", 866),
                 ("randv3.pck", 343)]
        for file, value in files:
            f = open(support.findfile(file),"rb")
            r = pickle.load(f)
            f.close()
            self.assertEqual(int(r.random()*1000), value)

    def test_bug_9025(self):
        
        
        n = 100000
        randrange = self.gen.randrange
        k = sum(randrange(6755399441055744) % 3 == 2 for i in range(n))
        self.assertTrue(0.30 < k/n < .37, (k/n))

try:
    random.SystemRandom().random()
except NotImplementedError:
    SystemRandom_available = False
else:
    SystemRandom_available = True

@unittest.skipUnless(SystemRandom_available, "random.SystemRandom not available")
class SystemRandom_TestBasicOps(TestBasicOps, unittest.TestCase):
    gen = random.SystemRandom()

    def test_autoseed(self):
        
        self.gen.seed()

    def test_saverestore(self):
        self.assertRaises(NotImplementedError, self.gen.getstate)
        self.assertRaises(NotImplementedError, self.gen.setstate, None)

    def test_seedargs(self):
        
        self.gen.seed(100)

    def test_gauss(self):
        self.gen.gauss_next = None
        self.gen.seed(100)
        self.assertEqual(self.gen.gauss_next, None)

    def test_pickling(self):
        for proto in range(pickle.HIGHEST_PROTOCOL + 1):
            self.assertRaises(NotImplementedError, pickle.dumps, self.gen, proto)

    def test_53_bits_per_float(self):
        
        span = 2 ** 53
        cum = 0
        for i in range(100):
            cum |= int(self.gen.random() * span)
        self.assertEqual(cum, span-1)

    def test_bigrand(self):
        
        
        span = 2 ** 500
        cum = 0
        for i in range(100):
            r = self.gen.randrange(span)
            self.assertTrue(0 <= r < span)
            cum |= r
        self.assertEqual(cum, span-1)

    def test_bigrand_ranges(self):
        for i in [40,80, 160, 200, 211, 250, 375, 512, 550]:
            start = self.gen.randrange(2 ** (i-2))
            stop = self.gen.randrange(2 ** i)
            if stop <= start:
                continue
            self.assertTrue(start <= self.gen.randrange(start, stop) < stop)

    def test_rangelimits(self):
        for start, stop in [(-2,0), (-(2**60)-2,-(2**60)), (2**60,2**60+2)]:
            self.assertEqual(set(range(start,stop)),
                set([self.gen.randrange(start,stop) for i in range(100)]))

    def test_randrange_nonunit_step(self):
        rint = self.gen.randrange(0, 10, 2)
        self.assertIn(rint, (0, 2, 4, 6, 8))
        rint = self.gen.randrange(0, 2, 2)
        self.assertEqual(rint, 0)

    def test_randrange_errors(self):
        raises = partial(self.assertRaises, ValueError, self.gen.randrange)
        
        raises(3, 3)
        raises(-721)
        raises(0, 100, -12)
        
        raises(3.14159)
        raises(0, 2.71828)
        
        raises(0, 42, 0)
        raises(0, 42, 3.14159)

    def test_genrandbits(self):
        
        for k in range(1, 1000):
            self.assertTrue(0 <= self.gen.getrandbits(k) < 2**k)

        
        getbits = self.gen.getrandbits
        for span in [1, 2, 3, 4, 31, 32, 32, 52, 53, 54, 119, 127, 128, 129]:
            cum = 0
            for i in range(100):
                cum |= getbits(span)
            self.assertEqual(cum, 2**span-1)

        
        self.assertRaises(TypeError, self.gen.getrandbits)
        self.assertRaises(TypeError, self.gen.getrandbits, 1, 2)
        self.assertRaises(ValueError, self.gen.getrandbits, 0)
        self.assertRaises(ValueError, self.gen.getrandbits, -1)
        self.assertRaises(TypeError, self.gen.getrandbits, 10.1)

    def test_randbelow_logic(self, _log=log, int=int):
        
        
        
        for i in range(1, 1000):
            n = 1 << i 
            numbits = i+1
            k = int(1.00001 + _log(n, 2))
            self.assertEqual(k, numbits)
            self.assertEqual(n, 2**(k-1))

            n += n - 1      
            k = int(1.00001 + _log(n, 2))
            self.assertIn(k, [numbits, numbits+1])
            self.assertTrue(2**k > n > 2**(k-2))

            n -= n >> 15     
            k = int(1.00001 + _log(n, 2))
            self.assertEqual(k, numbits)        
            self.assertTrue(2**k > n > 2**(k-1))   


class MersenneTwister_TestBasicOps(TestBasicOps, unittest.TestCase):
    gen = random.Random()

    def test_guaranteed_stable(self):
        
        self.gen.seed(3456147, version=1)
        self.assertEqual([self.gen.random().hex() for i in range(4)],
            ['0x1.ac362300d90d2p-1', '0x1.9d16f74365005p-1',
             '0x1.1ebb4352e4c4dp-1', '0x1.1a7422abf9c11p-1'])
        self.gen.seed("the quick brown fox", version=2)
        self.assertEqual([self.gen.random().hex() for i in range(4)],
            ['0x1.1239ddfb11b7cp-3', '0x1.b3cbb5c51b120p-4',
             '0x1.8c4f55116b60fp-1', '0x1.63eb525174a27p-1'])

    def test_setstate_first_arg(self):
        self.assertRaises(ValueError, self.gen.setstate, (1, None, None))

    def test_setstate_middle_arg(self):
        
        self.assertRaises(TypeError, self.gen.setstate, (2, None, None))
        
        self.assertRaises(ValueError, self.gen.setstate, (2, (1,2,3), None))
        
        self.assertRaises(TypeError, self.gen.setstate, (2, ('a',)*625, None))
        
        self.assertRaises(TypeError, self.gen.setstate, (2, (0,)*624+('a',), None))
        
        with self.assertRaises((ValueError, OverflowError)):
            self.gen.setstate((2, (1,)*624+(625,), None))
        with self.assertRaises((ValueError, OverflowError)):
            self.gen.setstate((2, (1,)*624+(-1,), None))

        "tuple(x % (2**32) for x in internalstate)"
        
        
        
        state_values = self.gen.getstate()[1]
        state_values = list(state_values)
        state_values[-1] = float('nan')
        state = (int(x) for x in state_values)
        self.assertRaises(TypeError, self.gen.setstate, (2, state, None))

    def test_referenceImplementation(self):
        
        
        
        
        
        
        
        
        
        
        "%.15f ", genrand_res53());
        "\n");
        
        
        expected = [0.45839803073713259,
                    0.86057815201978782,
                    0.92848331726782152,
                    0.35932681119782461,
                    0.081823493762449573,
                    0.14332226470169329,
                    0.084297823823520024,
                    0.53814864671831453,
                    0.089215024911993401,
                    0.78486196105372907]

        self.gen.seed(61731 + (24903<<32) + (614<<64) + (42143<<96))
        actual = self.randomlist(2000)[-10:]
        for a, e in zip(actual, expected):
            self.assertAlmostEqual(a,e,places=14)

    def test_strong_reference_implementation(self):
        
        
        
        
        from math import ldexp

        expected = [0x0eab3258d2231f,
                    0x1b89db315277a5,
                    0x1db622a5518016,
                    0x0b7f9af0d575bf,
                    0x029e4c4db82240,
                    0x04961892f5d673,
                    0x02b291598e4589,
                    0x11388382c15694,
                    0x02dad977c9e1fe,
                    0x191d96d4d334c6]
        self.gen.seed(61731 + (24903<<32) + (614<<64) + (42143<<96))
        actual = self.randomlist(2000)[-10:]
        for a, e in zip(actual, expected):
            self.assertEqual(int(ldexp(a, 53)), e)

    def test_long_seed(self):
        
        
        
        
        
        seed = (1 << (10000 * 8)) - 1  
        self.gen.seed(seed)

    def test_53_bits_per_float(self):
        
        span = 2 ** 53
        cum = 0
        for i in range(100):
            cum |= int(self.gen.random() * span)
        self.assertEqual(cum, span-1)

    def test_bigrand(self):
        
        
        span = 2 ** 500
        cum = 0
        for i in range(100):
            r = self.gen.randrange(span)
            self.assertTrue(0 <= r < span)
            cum |= r
        self.assertEqual(cum, span-1)

    def test_bigrand_ranges(self):
        for i in [40,80, 160, 200, 211, 250, 375, 512, 550]:
            start = self.gen.randrange(2 ** (i-2))
            stop = self.gen.randrange(2 ** i)
            if stop <= start:
                continue
            self.assertTrue(start <= self.gen.randrange(start, stop) < stop)

    def test_rangelimits(self):
        for start, stop in [(-2,0), (-(2**60)-2,-(2**60)), (2**60,2**60+2)]:
            self.assertEqual(set(range(start,stop)),
                set([self.gen.randrange(start,stop) for i in range(100)]))

    def test_genrandbits(self):
        
        self.gen.seed(1234567)
        self.assertEqual(self.gen.getrandbits(100),
                         97904845777343510404718956115)
        
        for k in range(1, 1000):
            self.assertTrue(0 <= self.gen.getrandbits(k) < 2**k)

        
        getbits = self.gen.getrandbits
        for span in [1, 2, 3, 4, 31, 32, 32, 52, 53, 54, 119, 127, 128, 129]:
            cum = 0
            for i in range(100):
                cum |= getbits(span)
            self.assertEqual(cum, 2**span-1)

        
        self.assertRaises(TypeError, self.gen.getrandbits)
        self.assertRaises(TypeError, self.gen.getrandbits, 'a')
        self.assertRaises(TypeError, self.gen.getrandbits, 1, 2)
        self.assertRaises(ValueError, self.gen.getrandbits, 0)
        self.assertRaises(ValueError, self.gen.getrandbits, -1)

    def test_randbelow_logic(self, _log=log, int=int):
        
        
        
        for i in range(1, 1000):
            n = 1 << i 
            numbits = i+1
            k = int(1.00001 + _log(n, 2))
            self.assertEqual(k, numbits)
            self.assertEqual(n, 2**(k-1))

            n += n - 1      
            k = int(1.00001 + _log(n, 2))
            self.assertIn(k, [numbits, numbits+1])
            self.assertTrue(2**k > n > 2**(k-2))

            n -= n >> 15     
            k = int(1.00001 + _log(n, 2))
            self.assertEqual(k, numbits)        
            self.assertTrue(2**k > n > 2**(k-1))   

    @unittest.mock.patch('random.Random.random')
    def test_randbelow_overriden_random(self, random_mock):
        
        
        random_mock.side_effect = random.SystemRandom().random
        maxsize = 1<<random.BPF
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            
            self.gen._randbelow(maxsize+1, maxsize = maxsize)
        self.gen._randbelow(5640, maxsize = maxsize)

        
        
        
        
        
        
        
        
        
        
        
        
        

        n = 42
        epsilon = 0.01
        limit = (maxsize - (maxsize % n)) / maxsize
        random_mock.side_effect = [limit + epsilon, limit - epsilon]
        self.gen._randbelow(n, maxsize = maxsize)

    def test_randrange_bug_1590891(self):
        start = 1000000000000
        stop = -100000000000000000000
        step = -200
        x = self.gen.randrange(start, stop, step)
        self.assertTrue(stop < x <= start)
        self.assertEqual((x+stop)%step, 0)

def gamma(z, sqrt2pi=(2.0*pi)**0.5):
    
    if z < 0.5:
        return pi / sin(pi*z) / gamma(1.0-z)
    
    az = z + (7.0 - 0.5)
    return az ** (z-0.5) / exp(az) * sqrt2pi * fsum([
        0.9999999999995183,
        676.5203681218835 / z,
        -1259.139216722289 / (z+1.0),
        771.3234287757674 / (z+2.0),
        -176.6150291498386 / (z+3.0),
        12.50734324009056 / (z+4.0),
        -0.1385710331296526 / (z+5.0),
        0.9934937113930748e-05 / (z+6.0),
        0.1659470187408462e-06 / (z+7.0),
    ])

class TestDistributions(unittest.TestCase):
    def test_zeroinputs(self):
        
        g = random.Random()
        x = [g.random() for i in range(50)] + [0.0]*5
        g.random = x[:].pop; g.uniform(1,10)
        g.random = x[:].pop; g.paretovariate(1.0)
        g.random = x[:].pop; g.expovariate(1.0)
        g.random = x[:].pop; g.weibullvariate(1.0, 1.0)
        g.random = x[:].pop; g.vonmisesvariate(1.0, 1.0)
        g.random = x[:].pop; g.normalvariate(0.0, 1.0)
        g.random = x[:].pop; g.gauss(0.0, 1.0)
        g.random = x[:].pop; g.lognormvariate(0.0, 1.0)
        g.random = x[:].pop; g.vonmisesvariate(0.0, 1.0)
        g.random = x[:].pop; g.gammavariate(0.01, 1.0)
        g.random = x[:].pop; g.gammavariate(1.0, 1.0)
        g.random = x[:].pop; g.gammavariate(200.0, 1.0)
        g.random = x[:].pop; g.betavariate(3.0, 3.0)
        g.random = x[:].pop; g.triangular(0.0, 1.0, 1.0/3.0)

    def test_avg_std(self):
        
        
        g = random.Random()
        N = 5000
        x = [i/float(N) for i in range(1,N)]
        for variate, args, mu, sigmasqrd in [
                (g.uniform, (1.0,10.0), (10.0+1.0)/2, (10.0-1.0)**2/12),
                (g.triangular, (0.0, 1.0, 1.0/3.0), 4.0/9.0, 7.0/9.0/18.0),
                (g.expovariate, (1.5,), 1/1.5, 1/1.5**2),
                (g.vonmisesvariate, (1.23, 0), pi, pi**2/3),
                (g.paretovariate, (5.0,), 5.0/(5.0-1),
                                  5.0/((5.0-1)**2*(5.0-2))),
                (g.weibullvariate, (1.0, 3.0), gamma(1+1/3.0),
                                  gamma(1+2/3.0)-gamma(1+1/3.0)**2) ]:
            g.random = x[:].pop
            y = []
            for i in range(len(x)):
                try:
                    y.append(variate(*args))
                except IndexError:
                    pass
            s1 = s2 = 0
            for e in y:
                s1 += e
                s2 += (e - mu) ** 2
            N = len(y)
            self.assertAlmostEqual(s1/N, mu, places=2,
                                   msg='%s%r' % (variate.__name__, args))
            self.assertAlmostEqual(s2/(N-1), sigmasqrd, places=2,
                                   msg='%s%r' % (variate.__name__, args))

    def test_constant(self):
        g = random.Random()
        N = 100
        for variate, args, expected in [
                (g.uniform, (10.0, 10.0), 10.0),
                (g.triangular, (10.0, 10.0), 10.0),
                (g.triangular, (10.0, 10.0, 10.0), 10.0),
                (g.expovariate, (float('inf'),), 0.0),
                (g.vonmisesvariate, (3.0, float('inf')), 3.0),
                (g.gauss, (10.0, 0.0), 10.0),
                (g.lognormvariate, (0.0, 0.0), 1.0),
                (g.lognormvariate, (-float('inf'), 0.0), 0.0),
                (g.normalvariate, (10.0, 0.0), 10.0),
                (g.paretovariate, (float('inf'),), 1.0),
                (g.weibullvariate, (10.0, float('inf')), 10.0),
                (g.weibullvariate, (0.0, 10.0), 0.0),
            ]:
            for i in range(N):
                self.assertEqual(variate(*args), expected)

    def test_von_mises_range(self):
        
        
        g = random.Random()
        N = 100
        for mu in 0.0, 0.1, 3.1, 6.2:
            for kappa in 0.0, 2.3, 500.0:
                for _ in range(N):
                    sample = g.vonmisesvariate(mu, kappa)
                    self.assertTrue(
                        0 <= sample <= random.TWOPI,
                        msg=("vonmisesvariate({}, {}) produced a result {} out"
                             " of range [0, 2*pi]").format(mu, kappa, sample))

    def test_von_mises_large_kappa(self):
        
        random.vonmisesvariate(0, 1e15)
        random.vonmisesvariate(0, 1e100)

    def test_gammavariate_errors(self):
        
        self.assertRaises(ValueError, random.gammavariate, -1, 3)
        self.assertRaises(ValueError, random.gammavariate, 0, 2)
        self.assertRaises(ValueError, random.gammavariate, 2, 0)
        self.assertRaises(ValueError, random.gammavariate, 1, -3)

    @unittest.mock.patch('random.Random.random')
    def test_gammavariate_full_code_coverage(self, random_mock):
        
        
        
        

        
        
        
        random_mock.side_effect = [1e-8, 0.5, 0.3]
        returned_value = random.gammavariate(1.1, 2.3)
        self.assertAlmostEqual(returned_value, 2.53)

        
        
        
        random_mock.side_effect = [1e-8, 0.45]
        returned_value = random.gammavariate(1.0, 3.14)
        self.assertAlmostEqual(returned_value, 2.507314166123803)

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        _e = random._e
        _exp = random._exp
        _log = random._log
        alpha = 0.35
        beta = 1.45
        b = (_e + alpha)/_e
        epsilon = 0.01

        r1 = 0.8859296441566 
        r2 = 0.3678794411714 

        "random" values result in the following trace:
        
        
        random_mock.side_effect = [r1, r2 + epsilon, r1, r2]
        returned_value = random.gammavariate(alpha, beta)
        self.assertAlmostEqual(returned_value, 1.4499999999997544)

        
        
        
        
        
        
        
        r1 = 0.8959296441566 
        r2 = 0.9445400408898141

        
        
        
        random_mock.side_effect = [r1, r2 + epsilon, r1, r2]
        returned_value = random.gammavariate(alpha, beta)
        self.assertAlmostEqual(returned_value, 1.5830349561760781)

    @unittest.mock.patch('random.Random.gammavariate')
    def test_betavariate_return_zero(self, gammavariate_mock):
        
        
        gammavariate_mock.return_value = 0.0
        self.assertEqual(0.0, random.betavariate(2.71828, 3.14159))

class TestModule(unittest.TestCase):
    def testMagicConstants(self):
        self.assertAlmostEqual(random.NV_MAGICCONST, 1.71552776992141)
        self.assertAlmostEqual(random.TWOPI, 6.28318530718)
        self.assertAlmostEqual(random.LOG4, 1.38629436111989)
        self.assertAlmostEqual(random.SG_MAGICCONST, 2.50407739677627)

    def test__all__(self):
        
        self.assertTrue(set(random.__all__) <= set(dir(random)))

    def test_random_subclass_with_kwargs(self):
        
        class Subclass(random.Random):
            def __init__(self, newarg=None):
                random.Random.__init__(self)
        Subclass(newarg=1)


if __name__ == "__main__":
    unittest.main()
