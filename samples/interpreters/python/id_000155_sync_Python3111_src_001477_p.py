

import unittest
from test import support

import os

class BoolTest(unittest.TestCase):

    def test_subclass(self):
        try:
            class C(bool):
                pass
        except TypeError:
            pass
        else:
            self.fail("bool should not be subclassable")

        self.assertRaises(TypeError, int.__new__, bool, 0)

    def test_print(self):
        try:
            fo = open(support.TESTFN, "w")
            print(False, True, file=fo)
            fo.close()
            fo = open(support.TESTFN, "r")
            self.assertEqual(fo.read(), 'False True\n')
        finally:
            fo.close()
            os.remove(support.TESTFN)

    def test_repr(self):
        self.assertEqual(repr(False), 'False')
        self.assertEqual(repr(True), 'True')
        self.assertEqual(eval(repr(False)), False)
        self.assertEqual(eval(repr(True)), True)

    def test_str(self):
        self.assertEqual(str(False), 'False')
        self.assertEqual(str(True), 'True')

    def test_int(self):
        self.assertEqual(int(False), 0)
        self.assertIsNot(int(False), False)
        self.assertEqual(int(True), 1)
        self.assertIsNot(int(True), True)

    def test_float(self):
        self.assertEqual(float(False), 0.0)
        self.assertIsNot(float(False), False)
        self.assertEqual(float(True), 1.0)
        self.assertIsNot(float(True), True)

    def test_math(self):
        self.assertEqual(+False, 0)
        self.assertIsNot(+False, False)
        self.assertEqual(-False, 0)
        self.assertIsNot(-False, False)
        self.assertEqual(abs(False), 0)
        self.assertIsNot(abs(False), False)
        self.assertEqual(+True, 1)
        self.assertIsNot(+True, True)
        self.assertEqual(-True, -1)
        self.assertEqual(abs(True), 1)
        self.assertIsNot(abs(True), True)
        self.assertEqual(~False, -1)
        self.assertEqual(~True, -2)

        self.assertEqual(False+2, 2)
        self.assertEqual(True+2, 3)
        self.assertEqual(2+False, 2)
        self.assertEqual(2+True, 3)

        self.assertEqual(False+False, 0)
        self.assertIsNot(False+False, False)
        self.assertEqual(False+True, 1)
        self.assertIsNot(False+True, True)
        self.assertEqual(True+False, 1)
        self.assertIsNot(True+False, True)
        self.assertEqual(True+True, 2)

        self.assertEqual(True-True, 0)
        self.assertIsNot(True-True, False)
        self.assertEqual(False-False, 0)
        self.assertIsNot(False-False, False)
        self.assertEqual(True-False, 1)
        self.assertIsNot(True-False, True)
        self.assertEqual(False-True, -1)

        self.assertEqual(True*1, 1)
        self.assertEqual(False*1, 0)
        self.assertIsNot(False*1, False)

        self.assertEqual(True/1, 1)
        self.assertIsNot(True/1, True)
        self.assertEqual(False/1, 0)
        self.assertIsNot(False/1, False)

        for b in False, True:
            for i in 0, 1, 2:
                self.assertEqual(b**i, int(b)**i)
                self.assertIsNot(b**i, bool(int(b)**i))

        for a in False, True:
            for b in False, True:
                self.assertIs(a&b, bool(int(a)&int(b)))
                self.assertIs(a|b, bool(int(a)|int(b)))
                self.assertIs(a^b, bool(int(a)^int(b)))
                self.assertEqual(a&int(b), int(a)&int(b))
                self.assertIsNot(a&int(b), bool(int(a)&int(b)))
                self.assertEqual(a|int(b), int(a)|int(b))
                self.assertIsNot(a|int(b), bool(int(a)|int(b)))
                self.assertEqual(a^int(b), int(a)^int(b))
                self.assertIsNot(a^int(b), bool(int(a)^int(b)))
                self.assertEqual(int(a)&b, int(a)&int(b))
                self.assertIsNot(int(a)&b, bool(int(a)&int(b)))
                self.assertEqual(int(a)|b, int(a)|int(b))
                self.assertIsNot(int(a)|b, bool(int(a)|int(b)))
                self.assertEqual(int(a)^b, int(a)^int(b))
                self.assertIsNot(int(a)^b, bool(int(a)^int(b)))

        self.assertIs(1==1, True)
        self.assertIs(1==0, False)
        self.assertIs(0<1, True)
        self.assertIs(1<0, False)
        self.assertIs(0<=0, True)
        self.assertIs(1<=0, False)
        self.assertIs(1>0, True)
        self.assertIs(1>1, False)
        self.assertIs(1>=1, True)
        self.assertIs(0>=1, False)
        self.assertIs(0!=1, True)
        self.assertIs(0!=0, False)

        x = [1]
        self.assertIs(x is x, True)
        self.assertIs(x is not x, False)

        self.assertIs(1 in x, True)
        self.assertIs(0 in x, False)
        self.assertIs(1 not in x, False)
        self.assertIs(0 not in x, True)

        x = {1: 2}
        self.assertIs(x is x, True)
        self.assertIs(x is not x, False)

        self.assertIs(1 in x, True)
        self.assertIs(0 in x, False)
        self.assertIs(1 not in x, False)
        self.assertIs(0 not in x, True)

        self.assertIs(not True, False)
        self.assertIs(not False, True)

    def test_convert(self):
        self.assertRaises(TypeError, bool, 42, 42)
        self.assertIs(bool(10), True)
        self.assertIs(bool(1), True)
        self.assertIs(bool(-1), True)
        self.assertIs(bool(0), False)
        self.assertIs(bool("hello"), True)
        self.assertIs(bool(""), False)
        self.assertIs(bool(), False)

    def test_format(self):
        self.assertEqual("%d" % False, "0")
        self.assertEqual("%d" % True, "1")
        self.assertEqual("%x" % False, "0")
        self.assertEqual("%x" % True, "1")

    def test_hasattr(self):
        self.assertIs(hasattr([], "append"), True)
        self.assertIs(hasattr([], "wobble"), False)

    def test_callable(self):
        self.assertIs(callable(len), True)
        self.assertIs(callable(1), False)

    def test_isinstance(self):
        self.assertIs(isinstance(True, bool), True)
        self.assertIs(isinstance(False, bool), True)
        self.assertIs(isinstance(True, int), True)
        self.assertIs(isinstance(False, int), True)
        self.assertIs(isinstance(1, bool), False)
        self.assertIs(isinstance(0, bool), False)

    def test_issubclass(self):
        self.assertIs(issubclass(bool, int), True)
        self.assertIs(issubclass(int, bool), False)

    def test_contains(self):
        self.assertIs(1 in {}, False)
        self.assertIs(1 in {1:1}, True)

    def test_string(self):
        self.assertIs("xyz".endswith("z"), True)
        self.assertIs("xyz".endswith("x"), False)
        self.assertIs("xyz0123".isalnum(), True)
        self.assertIs("@".isalnum(), False)
        self.assertIs("xyz".isalpha(), True)
        self.assertIs("@".isalpha(), False)
        self.assertIs("0123".isdigit(), True)
        self.assertIs("xyz".isdigit(), False)
        self.assertIs("xyz".islower(), True)
        self.assertIs("XYZ".islower(), False)
        self.assertIs("0123".isdecimal(), True)
        self.assertIs("xyz".isdecimal(), False)
        self.assertIs("0123".isnumeric(), True)
        self.assertIs("xyz".isnumeric(), False)
        self.assertIs(" ".isspace(), True)
        self.assertIs("\xa0".isspace(), True)
        self.assertIs("\u3000".isspace(), True)
        self.assertIs("XYZ".isspace(), False)
        self.assertIs("X".istitle(), True)
        self.assertIs("x".istitle(), False)
        self.assertIs("XYZ".isupper(), True)
        self.assertIs("xyz".isupper(), False)
        self.assertIs("xyz".startswith("x"), True)
        self.assertIs("xyz".startswith("z"), False)

    def test_boolean(self):
        self.assertEqual(True & 1, 1)
        self.assertNotIsInstance(True & 1, bool)
        self.assertIs(True & True, True)

        self.assertEqual(True | 1, 1)
        self.assertNotIsInstance(True | 1, bool)
        self.assertIs(True | True, True)

        self.assertEqual(True ^ 1, 0)
        self.assertNotIsInstance(True ^ 1, bool)
        self.assertIs(True ^ True, False)

    def test_fileclosed(self):
        try:
            f = open(support.TESTFN, "w")
            self.assertIs(f.closed, False)
            f.close()
            self.assertIs(f.closed, True)
        finally:
            os.remove(support.TESTFN)

    def test_types(self):
        
        for t in [bool, complex, dict, float, int, list, object,
                  set, str, tuple, type]:
            self.assertIs(bool(t), True)

    def test_operator(self):
        import operator
        self.assertIs(operator.truth(0), False)
        self.assertIs(operator.truth(1), True)
        self.assertIs(operator.not_(1), False)
        self.assertIs(operator.not_(0), True)
        self.assertIs(operator.contains([], 1), False)
        self.assertIs(operator.contains([1], 1), True)
        self.assertIs(operator.lt(0, 0), False)
        self.assertIs(operator.lt(0, 1), True)
        self.assertIs(operator.is_(True, True), True)
        self.assertIs(operator.is_(True, False), False)
        self.assertIs(operator.is_not(True, True), False)
        self.assertIs(operator.is_not(True, False), True)

    def test_marshal(self):
        import marshal
        self.assertIs(marshal.loads(marshal.dumps(True)), True)
        self.assertIs(marshal.loads(marshal.dumps(False)), False)

    def test_pickle(self):
        import pickle
        for proto in range(pickle.HIGHEST_PROTOCOL + 1):
            self.assertIs(pickle.loads(pickle.dumps(True, proto)), True)
            self.assertIs(pickle.loads(pickle.dumps(False, proto)), False)

    def test_picklevalues(self):
        
        import pickle
        self.assertEqual(pickle.dumps(True, protocol=0), b"I01\n.")
        self.assertEqual(pickle.dumps(False, protocol=0), b"I00\n.")
        self.assertEqual(pickle.dumps(True, protocol=1), b"I01\n.")
        self.assertEqual(pickle.dumps(False, protocol=1), b"I00\n.")
        self.assertEqual(pickle.dumps(True, protocol=2), b'\x80\x02\x88.')
        self.assertEqual(pickle.dumps(False, protocol=2), b'\x80\x02\x89.')

    def test_convert_to_bool(self):
        
        
        
        check = lambda o: self.assertRaises(TypeError, bool, o)
        class Foo(object):
            def __bool__(self):
                return self
        check(Foo())

        class Bar(object):
            def __bool__(self):
                return "Yes"
        check(Bar())

        class Baz(int):
            def __bool__(self):
                return self
        check(Baz())

        
        class Spam(int):
            def __bool__(self):
                return 1
        check(Spam())

        class Eggs:
            def __len__(self):
                return -1
        self.assertRaises(ValueError, bool, Eggs())

    def test_sane_len(self):
        
        
        for badval in ['illegal', -1, 1 << 32]:
            class A:
                def __len__(self):
                    return badval
            try:
                bool(A())
            except (Exception) as e_bool:
                try:
                    len(A())
                except (Exception) as e_len:
                    self.assertEqual(str(e_bool), str(e_len))

    def test_real_and_imag(self):
        self.assertEqual(True.real, 1)
        self.assertEqual(True.imag, 0)
        self.assertIs(type(True.real), int)
        self.assertIs(type(True.imag), int)
        self.assertEqual(False.real, 0)
        self.assertEqual(False.imag, 0)
        self.assertIs(type(False.real), int)
        self.assertIs(type(False.imag), int)

def test_main():
    support.run_unittest(BoolTest)

if __name__ == "__main__":
    test_main()
