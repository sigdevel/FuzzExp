import unittest
from test import support

import collections, random, string
import collections.abc
import gc, weakref
import pickle


class DictTest(unittest.TestCase):

    def test_invalid_keyword_arguments(self):
        class Custom(dict):
            pass
        for invalid in {1 : 2}, Custom({1 : 2}):
            with self.assertRaises(TypeError):
                dict(**invalid)
            with self.assertRaises(TypeError):
                {}.update(**invalid)

    def test_constructor(self):
        
        self.assertEqual(dict(), {})
        self.assertIsNot(dict(), {})

    def test_literal_constructor(self):
        
        
        for n in (0, 1, 6, 256, 400):
            items = [(''.join(random.sample(string.ascii_letters, 8)), i)
                     for i in range(n)]
            random.shuffle(items)
            formatted_items = ('{!r}: {:d}'.format(k, v) for k, v in items)
            dictliteral = '{' + ', '.join(formatted_items) + '}'
            self.assertEqual(eval(dictliteral), dict(items))

    def test_bool(self):
        self.assertIs(not {}, True)
        self.assertTrue({1: 2})
        self.assertIs(bool({}), False)
        self.assertIs(bool({1: 2}), True)

    def test_keys(self):
        d = {}
        self.assertEqual(set(d.keys()), set())
        d = {'a': 1, 'b': 2}
        k = d.keys()
        self.assertEqual(set(k), {'a', 'b'})
        self.assertIn('a', k)
        self.assertIn('b', k)
        self.assertIn('a', d)
        self.assertIn('b', d)
        self.assertRaises(TypeError, d.keys, None)
        self.assertEqual(repr(dict(a=1).keys()), "dict_keys(['a'])")

    def test_values(self):
        d = {}
        self.assertEqual(set(d.values()), set())
        d = {1:2}
        self.assertEqual(set(d.values()), {2})
        self.assertRaises(TypeError, d.values, None)
        self.assertEqual(repr(dict(a=1).values()), "dict_values([1])")

    def test_items(self):
        d = {}
        self.assertEqual(set(d.items()), set())

        d = {1:2}
        self.assertEqual(set(d.items()), {(1, 2)})
        self.assertRaises(TypeError, d.items, None)
        self.assertEqual(repr(dict(a=1).items()), "dict_items([('a', 1)])")

    def test_contains(self):
        d = {}
        self.assertNotIn('a', d)
        self.assertFalse('a' in d)
        self.assertTrue('a' not in d)
        d = {'a': 1, 'b': 2}
        self.assertIn('a', d)
        self.assertIn('b', d)
        self.assertNotIn('c', d)

        self.assertRaises(TypeError, d.__contains__)

    def test_len(self):
        d = {}
        self.assertEqual(len(d), 0)
        d = {'a': 1, 'b': 2}
        self.assertEqual(len(d), 2)

    def test_getitem(self):
        d = {'a': 1, 'b': 2}
        self.assertEqual(d['a'], 1)
        self.assertEqual(d['b'], 2)
        d['c'] = 3
        d['a'] = 4
        self.assertEqual(d['c'], 3)
        self.assertEqual(d['a'], 4)
        del d['b']
        self.assertEqual(d, {'a': 4, 'c': 3})

        self.assertRaises(TypeError, d.__getitem__)

        class BadEq(object):
            def __eq__(self, other):
                raise Exc()
            def __hash__(self):
                return 24

        d = {}
        d[BadEq()] = 42
        self.assertRaises(KeyError, d.__getitem__, 23)

        class Exc(Exception): pass

        class BadHash(object):
            fail = False
            def __hash__(self):
                if self.fail:
                    raise Exc()
                else:
                    return 42

        x = BadHash()
        d[x] = 42
        x.fail = True
        self.assertRaises(Exc, d.__getitem__, x)

    def test_clear(self):
        d = {1:1, 2:2, 3:3}
        d.clear()
        self.assertEqual(d, {})

        self.assertRaises(TypeError, d.clear, None)

    def test_update(self):
        d = {}
        d.update({1:100})
        d.update({2:20})
        d.update({1:1, 2:2, 3:3})
        self.assertEqual(d, {1:1, 2:2, 3:3})

        d.update()
        self.assertEqual(d, {1:1, 2:2, 3:3})

        self.assertRaises((TypeError, AttributeError), d.update, None)

        class SimpleUserDict:
            def __init__(self):
                self.d = {1:1, 2:2, 3:3}
            def keys(self):
                return self.d.keys()
            def __getitem__(self, i):
                return self.d[i]
        d.clear()
        d.update(SimpleUserDict())
        self.assertEqual(d, {1:1, 2:2, 3:3})

        class Exc(Exception): pass

        d.clear()
        class FailingUserDict:
            def keys(self):
                raise Exc
        self.assertRaises(Exc, d.update, FailingUserDict())

        class FailingUserDict:
            def keys(self):
                class BogonIter:
                    def __init__(self):
                        self.i = 1
                    def __iter__(self):
                        return self
                    def __next__(self):
                        if self.i:
                            self.i = 0
                            return 'a'
                        raise Exc
                return BogonIter()
            def __getitem__(self, key):
                return key
        self.assertRaises(Exc, d.update, FailingUserDict())

        class FailingUserDict:
            def keys(self):
                class BogonIter:
                    def __init__(self):
                        self.i = ord('a')
                    def __iter__(self):
                        return self
                    def __next__(self):
                        if self.i <= ord('z'):
                            rtn = chr(self.i)
                            self.i += 1
                            return rtn
                        raise StopIteration
                return BogonIter()
            def __getitem__(self, key):
                raise Exc
        self.assertRaises(Exc, d.update, FailingUserDict())

        class badseq(object):
            def __iter__(self):
                return self
            def __next__(self):
                raise Exc()

        self.assertRaises(Exc, {}.update, badseq())

        self.assertRaises(ValueError, {}.update, [(1, 2, 3)])

    def test_fromkeys(self):
        self.assertEqual(dict.fromkeys('abc'), {'a':None, 'b':None, 'c':None})
        d = {}
        self.assertIsNot(d.fromkeys('abc'), d)
        self.assertEqual(d.fromkeys('abc'), {'a':None, 'b':None, 'c':None})
        self.assertEqual(d.fromkeys((4,5),0), {4:0, 5:0})
        self.assertEqual(d.fromkeys([]), {})
        def g():
            yield 1
        self.assertEqual(d.fromkeys(g()), {1:None})
        self.assertRaises(TypeError, {}.fromkeys, 3)
        class dictlike(dict): pass
        self.assertEqual(dictlike.fromkeys('a'), {'a':None})
        self.assertEqual(dictlike().fromkeys('a'), {'a':None})
        self.assertIsInstance(dictlike.fromkeys('a'), dictlike)
        self.assertIsInstance(dictlike().fromkeys('a'), dictlike)
        class mydict(dict):
            def __new__(cls):
                return collections.UserDict()
        ud = mydict.fromkeys('ab')
        self.assertEqual(ud, {'a':None, 'b':None})
        self.assertIsInstance(ud, collections.UserDict)
        self.assertRaises(TypeError, dict.fromkeys)

        class Exc(Exception): pass

        class baddict1(dict):
            def __init__(self):
                raise Exc()

        self.assertRaises(Exc, baddict1.fromkeys, [1])

        class BadSeq(object):
            def __iter__(self):
                return self
            def __next__(self):
                raise Exc()

        self.assertRaises(Exc, dict.fromkeys, BadSeq())

        class baddict2(dict):
            def __setitem__(self, key, value):
                raise Exc()

        self.assertRaises(Exc, baddict2.fromkeys, [1])

        
        d = dict(zip(range(6), range(6)))
        self.assertEqual(dict.fromkeys(d, 0), dict(zip(range(6), [0]*6)))

        class baddict3(dict):
            def __new__(cls):
                return d
        d = {i : i for i in range(10)}
        res = d.copy()
        res.update(a=None, b=None, c=None)
        self.assertEqual(baddict3.fromkeys({"a", "b", "c"}), res)

    def test_copy(self):
        d = {1:1, 2:2, 3:3}
        self.assertEqual(d.copy(), {1:1, 2:2, 3:3})
        self.assertEqual({}.copy(), {})
        self.assertRaises(TypeError, d.copy, None)

    def test_get(self):
        d = {}
        self.assertIs(d.get('c'), None)
        self.assertEqual(d.get('c', 3), 3)
        d = {'a': 1, 'b': 2}
        self.assertIs(d.get('c'), None)
        self.assertEqual(d.get('c', 3), 3)
        self.assertEqual(d.get('a'), 1)
        self.assertEqual(d.get('a', 3), 1)
        self.assertRaises(TypeError, d.get)
        self.assertRaises(TypeError, d.get, None, None, None)

    def test_setdefault(self):
        
        d = {}
        self.assertIs(d.setdefault('key0'), None)
        d.setdefault('key0', [])
        self.assertIs(d.setdefault('key0'), None)
        d.setdefault('key', []).append(3)
        self.assertEqual(d['key'][0], 3)
        d.setdefault('key', []).append(4)
        self.assertEqual(len(d['key']), 2)
        self.assertRaises(TypeError, d.setdefault)

        class Exc(Exception): pass

        class BadHash(object):
            fail = False
            def __hash__(self):
                if self.fail:
                    raise Exc()
                else:
                    return 42

        x = BadHash()
        d[x] = 42
        x.fail = True
        self.assertRaises(Exc, d.setdefault, x, [])

    def test_setdefault_atomic(self):
        
        class Hashed(object):
            def __init__(self):
                self.hash_count = 0
                self.eq_count = 0
            def __hash__(self):
                self.hash_count += 1
                return 42
            def __eq__(self, other):
                self.eq_count += 1
                return id(self) == id(other)
        hashed1 = Hashed()
        y = {hashed1: 5}
        hashed2 = Hashed()
        y.setdefault(hashed2, [])
        self.assertEqual(hashed1.hash_count, 1)
        self.assertEqual(hashed2.hash_count, 1)
        self.assertEqual(hashed1.eq_count + hashed2.eq_count, 1)

    def test_setitem_atomic_at_resize(self):
        class Hashed(object):
            def __init__(self):
                self.hash_count = 0
                self.eq_count = 0
            def __hash__(self):
                self.hash_count += 1
                return 42
            def __eq__(self, other):
                self.eq_count += 1
                return id(self) == id(other)
        hashed1 = Hashed()
        
        y = {hashed1: 5, 0: 0, 1: 1, 2: 2, 3: 3}
        hashed2 = Hashed()
        
        y[hashed2] = []
        self.assertEqual(hashed1.hash_count, 1)
        self.assertEqual(hashed2.hash_count, 1)
        self.assertEqual(hashed1.eq_count + hashed2.eq_count, 1)

    def test_popitem(self):
        
        for copymode in -1, +1:
            
            
            for log2size in range(12):
                size = 2**log2size
                a = {}
                b = {}
                for i in range(size):
                    a[repr(i)] = i
                    if copymode < 0:
                        b[repr(i)] = i
                if copymode > 0:
                    b = a.copy()
                for i in range(size):
                    ka, va = ta = a.popitem()
                    self.assertEqual(va, int(ka))
                    kb, vb = tb = b.popitem()
                    self.assertEqual(vb, int(kb))
                    self.assertFalse(copymode < 0 and ta != tb)
                self.assertFalse(a)
                self.assertFalse(b)

        d = {}
        self.assertRaises(KeyError, d.popitem)

    def test_pop(self):
        
        d = {}
        k, v = 'abc', 'def'
        d[k] = v
        self.assertRaises(KeyError, d.pop, 'ghi')

        self.assertEqual(d.pop(k), v)
        self.assertEqual(len(d), 0)

        self.assertRaises(KeyError, d.pop, k)

        self.assertEqual(d.pop(k, v), v)
        d[k] = v
        self.assertEqual(d.pop(k, 1), v)

        self.assertRaises(TypeError, d.pop)

        class Exc(Exception): pass

        class BadHash(object):
            fail = False
            def __hash__(self):
                if self.fail:
                    raise Exc()
                else:
                    return 42

        x = BadHash()
        d[x] = 42
        x.fail = True
        self.assertRaises(Exc, d.pop, x)

    def test_mutating_iteration(self):
        
        d = {}
        d[1] = 1
        with self.assertRaises(RuntimeError):
            for i in d:
                d[i+1] = 1

    def test_mutating_lookup(self):
        
        class NastyKey:
            mutate_dict = None

            def __init__(self, value):
                self.value = value

            def __hash__(self):
                
                return 1

            def __eq__(self, other):
                if NastyKey.mutate_dict:
                    mydict, key = NastyKey.mutate_dict
                    NastyKey.mutate_dict = None
                    del mydict[key]
                return self.value == other.value

        key1 = NastyKey(1)
        key2 = NastyKey(2)
        d = {key1: 1}
        NastyKey.mutate_dict = (d, key1)
        d[key2] = 2
        self.assertEqual(d, {key2: 2})

    def test_repr(self):
        d = {}
        self.assertEqual(repr(d), '{}')
        d[1] = 2
        self.assertEqual(repr(d), '{1: 2}')
        d = {}
        d[1] = d
        self.assertEqual(repr(d), '{1: {...}}')

        class Exc(Exception): pass

        class BadRepr(object):
            def __repr__(self):
                raise Exc()

        d = {1: BadRepr()}
        self.assertRaises(Exc, repr, d)

    def test_eq(self):
        self.assertEqual({}, {})
        self.assertEqual({1: 2}, {1: 2})

        class Exc(Exception): pass

        class BadCmp(object):
            def __eq__(self, other):
                raise Exc()
            def __hash__(self):
                return 1

        d1 = {BadCmp(): 1}
        d2 = {1: 1}

        with self.assertRaises(Exc):
            d1 == d2

    def test_keys_contained(self):
        self.helper_keys_contained(lambda x: x.keys())
        self.helper_keys_contained(lambda x: x.items())

    def helper_keys_contained(self, fn):
        
        
        empty = fn(dict())
        empty2 = fn(dict())
        smaller = fn({1:1, 2:2})
        larger = fn({1:1, 2:2, 3:3})
        larger2 = fn({1:1, 2:2, 3:3})
        larger3 = fn({4:1, 2:2, 3:3})

        self.assertTrue(smaller <  larger)
        self.assertTrue(smaller <= larger)
        self.assertTrue(larger >  smaller)
        self.assertTrue(larger >= smaller)

        self.assertFalse(smaller >= larger)
        self.assertFalse(smaller >  larger)
        self.assertFalse(larger  <= smaller)
        self.assertFalse(larger  <  smaller)

        self.assertFalse(smaller <  larger3)
        self.assertFalse(smaller <= larger3)
        self.assertFalse(larger3 >  smaller)
        self.assertFalse(larger3 >= smaller)

        
        self.assertTrue(larger2 >= larger)
        self.assertTrue(larger2 <= larger)
        self.assertFalse(larger2 > larger)
        self.assertFalse(larger2 < larger)

        self.assertTrue(larger == larger2)
        self.assertTrue(smaller != larger)

        
        self.assertTrue(empty == empty2)
        self.assertFalse(empty != empty2)
        self.assertFalse(empty == smaller)
        self.assertTrue(empty != smaller)

        
        self.assertTrue(larger != larger3)
        self.assertFalse(larger == larger3)

    def test_errors_in_view_containment_check(self):
        class C:
            def __eq__(self, other):
                raise RuntimeError

        d1 = {1: C()}
        d2 = {1: C()}
        with self.assertRaises(RuntimeError):
            d1.items() == d2.items()
        with self.assertRaises(RuntimeError):
            d1.items() != d2.items()
        with self.assertRaises(RuntimeError):
            d1.items() <= d2.items()
        with self.assertRaises(RuntimeError):
            d1.items() >= d2.items()

        d3 = {1: C(), 2: C()}
        with self.assertRaises(RuntimeError):
            d2.items() < d3.items()
        with self.assertRaises(RuntimeError):
            d3.items() > d2.items()

    def test_dictview_set_operations_on_keys(self):
        k1 = {1:1, 2:2}.keys()
        k2 = {1:1, 2:2, 3:3}.keys()
        k3 = {4:4}.keys()

        self.assertEqual(k1 - k2, set())
        self.assertEqual(k1 - k3, {1,2})
        self.assertEqual(k2 - k1, {3})
        self.assertEqual(k3 - k1, {4})
        self.assertEqual(k1 & k2, {1,2})
        self.assertEqual(k1 & k3, set())
        self.assertEqual(k1 | k2, {1,2,3})
        self.assertEqual(k1 ^ k2, {3})
        self.assertEqual(k1 ^ k3, {1,2,4})

    def test_dictview_set_operations_on_items(self):
        k1 = {1:1, 2:2}.items()
        k2 = {1:1, 2:2, 3:3}.items()
        k3 = {4:4}.items()

        self.assertEqual(k1 - k2, set())
        self.assertEqual(k1 - k3, {(1,1), (2,2)})
        self.assertEqual(k2 - k1, {(3,3)})
        self.assertEqual(k3 - k1, {(4,4)})
        self.assertEqual(k1 & k2, {(1,1), (2,2)})
        self.assertEqual(k1 & k3, set())
        self.assertEqual(k1 | k2, {(1,1), (2,2), (3,3)})
        self.assertEqual(k1 ^ k2, {(3,3)})
        self.assertEqual(k1 ^ k3, {(1,1), (2,2), (4,4)})

    def test_dictview_mixed_set_operations(self):
        
        self.assertTrue({1:1}.keys() == {1})
        self.assertTrue({1} == {1:1}.keys())
        self.assertEqual({1:1}.keys() | {2}, {1, 2})
        self.assertEqual({2} | {1:1}.keys(), {1, 2})
        
        self.assertTrue({1:1}.items() == {(1,1)})
        self.assertTrue({(1,1)} == {1:1}.items())
        self.assertEqual({1:1}.items() | {2}, {(1,1), 2})
        self.assertEqual({2} | {1:1}.items(), {(1,1), 2})

    def test_missing(self):
        
        self.assertFalse(hasattr(dict, "__missing__"))
        self.assertFalse(hasattr({}, "__missing__"))
        
        
        
        
        
        class D(dict):
            def __missing__(self, key):
                return 42
        d = D({1: 2, 3: 4})
        self.assertEqual(d[1], 2)
        self.assertEqual(d[3], 4)
        self.assertNotIn(2, d)
        self.assertNotIn(2, d.keys())
        self.assertEqual(d[2], 42)

        class E(dict):
            def __missing__(self, key):
                raise RuntimeError(key)
        e = E()
        with self.assertRaises(RuntimeError) as c:
            e[42]
        self.assertEqual(c.exception.args, (42,))

        class F(dict):
            def __init__(self):
                
                self.__missing__ = lambda key: None
        f = F()
        with self.assertRaises(KeyError) as c:
            f[42]
        self.assertEqual(c.exception.args, (42,))

        class G(dict):
            pass
        g = G()
        with self.assertRaises(KeyError) as c:
            g[42]
        self.assertEqual(c.exception.args, (42,))

    def test_tuple_keyerror(self):
        
        d = {}
        with self.assertRaises(KeyError) as c:
            d[(1,)]
        self.assertEqual(c.exception.args, ((1,),))

    def test_bad_key(self):
        
        class CustomException(Exception):
            pass

        class BadDictKey:
            def __hash__(self):
                return hash(self.__class__)

            def __eq__(self, other):
                if isinstance(other, self.__class__):
                    raise CustomException
                return other

        d = {}
        x1 = BadDictKey()
        x2 = BadDictKey()
        d[x1] = 1
        for stmt in ['d[x2] = 2',
                     'z = d[x2]',
                     'x2 in d',
                     'd.get(x2)',
                     'd.setdefault(x2, 42)',
                     'd.pop(x2)',
                     'd.update({x2: 2})']:
            with self.assertRaises(CustomException):
                exec(stmt, locals())

    def test_resize1(self):
        
        
        
        
        
        

        d = {}
        for i in range(5):
            d[i] = i
        for i in range(5):
            del d[i]
        for i in range(5, 9):  
            d[i] = i

    def test_resize2(self):
        
        

        class X(object):
            def __hash__(self):
                return 5
            def __eq__(self, other):
                if resizing:
                    d.clear()
                return False
        d = {}
        resizing = False
        d[X()] = 1
        d[X()] = 2
        d[X()] = 3
        d[X()] = 4
        d[X()] = 5
        
        resizing = True
        d[9] = 6

    def test_empty_presized_dict_in_freelist(self):
        
        
        with self.assertRaises(ZeroDivisionError):
            d = {'a': 1 // 0, 'b': None, 'c': None, 'd': None, 'e': None,
                 'f': None, 'g': None, 'h': None}
        d = {}

    def test_container_iterator(self):
        
        
        class C(object):
            pass
        views = (dict.items, dict.values, dict.keys)
        for v in views:
            obj = C()
            ref = weakref.ref(obj)
            container = {obj: 1}
            obj.v = v(container)
            obj.x = iter(obj.v)
            del obj, container
            gc.collect()
            self.assertIs(ref(), None, "Cycle was not collected")

    def _not_tracked(self, t):
        
        gc.collect()
        gc.collect()
        self.assertFalse(gc.is_tracked(t), t)

    def _tracked(self, t):
        self.assertTrue(gc.is_tracked(t), t)
        gc.collect()
        gc.collect()
        self.assertTrue(gc.is_tracked(t), t)

    @support.cpython_only
    def test_track_literals(self):
        
        x, y, z, w = 1.5, "a", (1, None), []

        self._not_tracked({})
        self._not_tracked({x:(), y:x, z:1})
        self._not_tracked({1: "a", "b": 2})
        self._not_tracked({1: 2, (None, True, False, ()): int})
        self._not_tracked({1: object()})

        
        
        self._tracked({1: []})
        self._tracked({1: ([],)})
        self._tracked({1: {}})
        self._tracked({1: set()})

    @support.cpython_only
    def test_track_dynamic(self):
        
        class MyObject(object):
            pass
        x, y, z, w, o = 1.5, "a", (1, object()), [], MyObject()

        d = dict()
        self._not_tracked(d)
        d[1] = "a"
        self._not_tracked(d)
        d[y] = 2
        self._not_tracked(d)
        d[z] = 3
        self._not_tracked(d)
        self._not_tracked(d.copy())
        d[4] = w
        self._tracked(d)
        self._tracked(d.copy())
        d[4] = None
        self._not_tracked(d)
        self._not_tracked(d.copy())

        
        
        d = dict()
        dd = dict()
        d[1] = dd
        self._not_tracked(dd)
        self._tracked(d)
        dd[1] = d
        self._tracked(dd)

        d = dict.fromkeys([x, y, z])
        self._not_tracked(d)
        dd = dict()
        dd.update(d)
        self._not_tracked(dd)
        d = dict.fromkeys([x, y, z, o])
        self._tracked(d)
        dd = dict()
        dd.update(d)
        self._tracked(dd)

        d = dict(x=x, y=y, z=z)
        self._not_tracked(d)
        d = dict(x=x, y=y, z=z, w=w)
        self._tracked(d)
        d = dict()
        d.update(x=x, y=y, z=z)
        self._not_tracked(d)
        d.update(w=w)
        self._tracked(d)

        d = dict([(x, y), (z, 1)])
        self._not_tracked(d)
        d = dict([(x, y), (z, w)])
        self._tracked(d)
        d = dict()
        d.update([(x, y), (z, 1)])
        self._not_tracked(d)
        d.update([(x, y), (z, w)])
        self._tracked(d)

    @support.cpython_only
    def test_track_subtypes(self):
        
        class MyDict(dict):
            pass
        self._tracked(MyDict())

    def test_iterator_pickling(self):
        for proto in range(pickle.HIGHEST_PROTOCOL + 1):
            data = {1:"a", 2:"b", 3:"c"}
            it = iter(data)
            d = pickle.dumps(it, proto)
            it = pickle.loads(d)
            self.assertEqual(sorted(it), sorted(data))

            it = pickle.loads(d)
            try:
                drop = next(it)
            except StopIteration:
                continue
            d = pickle.dumps(it, proto)
            it = pickle.loads(d)
            del data[drop]
            self.assertEqual(sorted(it), sorted(data))

    def test_itemiterator_pickling(self):
        for proto in range(pickle.HIGHEST_PROTOCOL + 1):
            data = {1:"a", 2:"b", 3:"c"}
            
            itorg = iter(data.items())
            d = pickle.dumps(itorg, proto)
            it = pickle.loads(d)
            
            
            
            
            
            self.assertIsInstance(it, collections.abc.Iterator)
            self.assertEqual(dict(it), data)

            it = pickle.loads(d)
            drop = next(it)
            d = pickle.dumps(it, proto)
            it = pickle.loads(d)
            del data[drop[0]]
            self.assertEqual(dict(it), data)

    def test_valuesiterator_pickling(self):
        for proto in range(pickle.HIGHEST_PROTOCOL):
            data = {1:"a", 2:"b", 3:"c"}
            
            it = iter(data.values())
            d = pickle.dumps(it, proto)
            it = pickle.loads(d)
            self.assertEqual(sorted(list(it)), sorted(list(data.values())))

            it = pickle.loads(d)
            drop = next(it)
            d = pickle.dumps(it, proto)
            it = pickle.loads(d)
            values = list(it) + [drop]
            self.assertEqual(sorted(values), sorted(list(data.values())))

    def test_instance_dict_getattr_str_subclass(self):
        class Foo:
            def __init__(self, msg):
                self.msg = msg
        f = Foo('123')
        class _str(str):
            pass
        self.assertEqual(f.msg, getattr(f, _str('msg')))
        self.assertEqual(f.msg, f.__dict__[_str('msg')])

    def test_object_set_item_single_instance_non_str_key(self):
        class Foo: pass
        f = Foo()
        f.__dict__[1] = 1
        f.a = 'a'
        self.assertEqual(f.__dict__, {1:1, 'a':'a'})

    def check_reentrant_insertion(self, mutate):
        
        
        
        class Mutating:
            def __del__(self):
                mutate(d)

        d = {k: Mutating() for k in 'abcdefghijklmnopqr'}
        for k in list(d):
            d[k] = k

    def test_reentrant_insertion(self):
        
        def mutate(d):
            d['b'] = 5
        self.check_reentrant_insertion(mutate)

        def mutate(d):
            d.update(self.__dict__)
            d.clear()
        self.check_reentrant_insertion(mutate)

        def mutate(d):
            while d:
                d.popitem()
        self.check_reentrant_insertion(mutate)

    def test_merge_and_mutate(self):
        class X:
            def __hash__(self):
                return 0

            def __eq__(self, o):
                other.clear()
                return False

        l = [(i,0) for i in range(1, 1337)]
        other = dict(l)
        other[X()] = 0
        d = {X(): 0, 1: 1}
        self.assertRaises(RuntimeError, d.update, other)

from test import mapping_tests

class GeneralMappingTests(mapping_tests.BasicTestMappingProtocol):
    type2test = dict

class Dict(dict):
    pass

class SubclassMappingTests(mapping_tests.BasicTestMappingProtocol):
    type2test = Dict

def test_main():
    support.run_unittest(
        DictTest,
        GeneralMappingTests,
        SubclassMappingTests,
    )

if __name__ == "__main__":
    test_main()
