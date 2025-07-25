import unittest, test.support
from test.script_helper import assert_python_ok, assert_python_failure
import sys, io, os
import struct
import subprocess
import textwrap
import warnings
import operator
import codecs
import gc
import sysconfig
import platform



numruns = 0

try:
    import threading
except ImportError:
    threading = None

class SysModuleTest(unittest.TestCase):

    def setUp(self):
        self.orig_stdout = sys.stdout
        self.orig_stderr = sys.stderr
        self.orig_displayhook = sys.displayhook

    def tearDown(self):
        sys.stdout = self.orig_stdout
        sys.stderr = self.orig_stderr
        sys.displayhook = self.orig_displayhook
        test.support.reap_children()

    def test_original_displayhook(self):
        import builtins
        out = io.StringIO()
        sys.stdout = out

        dh = sys.__displayhook__

        self.assertRaises(TypeError, dh)
        if hasattr(builtins, "_"):
            del builtins._

        dh(None)
        self.assertEqual(out.getvalue(), "")
        self.assertTrue(not hasattr(builtins, "_"))
        dh(42)
        self.assertEqual(out.getvalue(), "42\n")
        self.assertEqual(builtins._, 42)

        del sys.stdout
        self.assertRaises(RuntimeError, dh, 42)

    def test_lost_displayhook(self):
        del sys.displayhook
        code = compile("42", "<string>", "single")
        self.assertRaises(RuntimeError, eval, code)

    def test_custom_displayhook(self):
        def baddisplayhook(obj):
            raise ValueError
        sys.displayhook = baddisplayhook
        code = compile("42", "<string>", "single")
        self.assertRaises(ValueError, eval, code)

    def test_original_excepthook(self):
        err = io.StringIO()
        sys.stderr = err

        eh = sys.__excepthook__

        self.assertRaises(TypeError, eh)
        try:
            raise ValueError(42)
        except ValueError as exc:
            eh(*sys.exc_info())

        self.assertTrue(err.getvalue().endswith("ValueError: 42\n"))

    def test_excepthook(self):
        with test.support.captured_output("stderr") as stderr:
            sys.excepthook(1, '1', 1)
        self.assertTrue("TypeError: print_exception(): Exception expected for " \
                         "value, str found" in stderr.getvalue())

    
    

    def test_exit(self):
        
        self.assertRaises(TypeError, sys.exit, 42, 42)

        
        with self.assertRaises(SystemExit) as cm:
            sys.exit()
        self.assertIsNone(cm.exception.code)

        rc, out, err = assert_python_ok('-c', 'import sys; sys.exit()')
        self.assertEqual(rc, 0)
        self.assertEqual(out, b'')
        self.assertEqual(err, b'')

        
        with self.assertRaises(SystemExit) as cm:
            sys.exit(42)
        self.assertEqual(cm.exception.code, 42)

        
        
        with self.assertRaises(SystemExit) as cm:
            sys.exit((42,))
        self.assertEqual(cm.exception.code, 42)

        
        with self.assertRaises(SystemExit) as cm:
            sys.exit("exit")
        self.assertEqual(cm.exception.code, "exit")

        
        with self.assertRaises(SystemExit) as cm:
            sys.exit((17, 23))
        self.assertEqual(cm.exception.code, (17, 23))

        
        rc, out, err = assert_python_failure('-c', 'raise SystemExit(47)')
        self.assertEqual(rc, 47)
        self.assertEqual(out, b'')
        self.assertEqual(err, b'')

        def check_exit_message(code, expected, **env_vars):
            rc, out, err = assert_python_failure('-c', code, **env_vars)
            self.assertEqual(rc, 1)
            self.assertEqual(out, b'')
            self.assertTrue(err.startswith(expected),
                "%s doesn't start with %s" % (ascii(err), ascii(expected)))

        
        
        check_exit_message(
            r'import sys; sys.stderr.write("unflushed,"); sys.exit("message")',
            b"unflushed,message")

        
        
        check_exit_message(
            r'import sys; sys.exit("surrogates:\uDCFF")',
            b"surrogates:\\udcff")

        
        
        check_exit_message(
            r'import sys; sys.exit("h\xe9")',
            b"h\xe9", PYTHONIOENCODING='latin-1')

    def test_getdefaultencoding(self):
        self.assertRaises(TypeError, sys.getdefaultencoding, 42)
        
        self.assertIsInstance(sys.getdefaultencoding(), str)

    
    

    def test_setcheckinterval(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.assertRaises(TypeError, sys.setcheckinterval)
            orig = sys.getcheckinterval()
            for n in 0, 100, 120, orig: 
                sys.setcheckinterval(n)
                self.assertEqual(sys.getcheckinterval(), n)

    @unittest.skipUnless(threading, 'Threading required for this test.')
    def test_switchinterval(self):
        self.assertRaises(TypeError, sys.setswitchinterval)
        self.assertRaises(TypeError, sys.setswitchinterval, "a")
        self.assertRaises(ValueError, sys.setswitchinterval, -1.0)
        self.assertRaises(ValueError, sys.setswitchinterval, 0.0)
        orig = sys.getswitchinterval()
        
        self.assertTrue(orig < 0.5, orig)
        try:
            for n in 0.00001, 0.05, 3.0, orig:
                sys.setswitchinterval(n)
                self.assertAlmostEqual(sys.getswitchinterval(), n)
        finally:
            sys.setswitchinterval(orig)

    def test_recursionlimit(self):
        self.assertRaises(TypeError, sys.getrecursionlimit, 42)
        oldlimit = sys.getrecursionlimit()
        self.assertRaises(TypeError, sys.setrecursionlimit)
        self.assertRaises(ValueError, sys.setrecursionlimit, -42)
        sys.setrecursionlimit(10000)
        self.assertEqual(sys.getrecursionlimit(), 10000)
        sys.setrecursionlimit(oldlimit)

    def test_recursionlimit_recovery(self):
        if hasattr(sys, 'gettrace') and sys.gettrace():
            self.skipTest('fatal error if run with a trace function')

        
        
        
        
        oldlimit = sys.getrecursionlimit()
        def f():
            f()
        try:
            for i in (50, 1000):
                
                sys.setrecursionlimit(i)
                self.assertRaises(RuntimeError, f)
                self.assertRaises(RuntimeError, f)
        finally:
            sys.setrecursionlimit(oldlimit)

    def test_recursionlimit_fatalerror(self):
        
        
        code = textwrap.dedent("""
            import sys

            def f():
                try:
                    f()
                except RuntimeError:
                    f()

            sys.setrecursionlimit(%d)
            f()""")
        with test.support.SuppressCrashReport():
            for i in (50, 1000):
                sub = subprocess.Popen([sys.executable, '-c', code % i],
                    stderr=subprocess.PIPE)
                err = sub.communicate()[1]
                self.assertTrue(sub.returncode, sub.returncode)
                self.assertIn(
                    b"Fatal Python error: Cannot recover from stack overflow",
                    err)

    def test_getwindowsversion(self):
        
        test.support.get_attribute(sys, "getwindowsversion")
        v = sys.getwindowsversion()
        self.assertEqual(len(v), 5)
        self.assertIsInstance(v[0], int)
        self.assertIsInstance(v[1], int)
        self.assertIsInstance(v[2], int)
        self.assertIsInstance(v[3], int)
        self.assertIsInstance(v[4], str)
        self.assertRaises(IndexError, operator.getitem, v, 5)
        self.assertIsInstance(v.major, int)
        self.assertIsInstance(v.minor, int)
        self.assertIsInstance(v.build, int)
        self.assertIsInstance(v.platform, int)
        self.assertIsInstance(v.service_pack, str)
        self.assertIsInstance(v.service_pack_minor, int)
        self.assertIsInstance(v.service_pack_major, int)
        self.assertIsInstance(v.suite_mask, int)
        self.assertIsInstance(v.product_type, int)
        self.assertEqual(v[0], v.major)
        self.assertEqual(v[1], v.minor)
        self.assertEqual(v[2], v.build)
        self.assertEqual(v[3], v.platform)
        self.assertEqual(v[4], v.service_pack)

        
        
        maj, min, buildno, plat, csd = sys.getwindowsversion()

    def test_call_tracing(self):
        self.assertRaises(TypeError, sys.call_tracing, type, 2)

    @unittest.skipUnless(hasattr(sys, "setdlopenflags"),
                         'test needs sys.setdlopenflags()')
    def test_dlopenflags(self):
        self.assertTrue(hasattr(sys, "getdlopenflags"))
        self.assertRaises(TypeError, sys.getdlopenflags, 42)
        oldflags = sys.getdlopenflags()
        self.assertRaises(TypeError, sys.setdlopenflags)
        sys.setdlopenflags(oldflags+1)
        self.assertEqual(sys.getdlopenflags(), oldflags+1)
        sys.setdlopenflags(oldflags)

    @test.support.refcount_test
    def test_refcount(self):
        
        
        
        
        global n
        self.assertRaises(TypeError, sys.getrefcount)
        c = sys.getrefcount(None)
        n = None
        self.assertEqual(sys.getrefcount(None), c+1)
        del n
        self.assertEqual(sys.getrefcount(None), c)
        if hasattr(sys, "gettotalrefcount"):
            self.assertIsInstance(sys.gettotalrefcount(), int)

    def test_getframe(self):
        self.assertRaises(TypeError, sys._getframe, 42, 42)
        self.assertRaises(ValueError, sys._getframe, 2000000000)
        self.assertTrue(
            SysModuleTest.test_getframe.__code__ \
            is sys._getframe().f_code
        )

    
    def test_current_frames(self):
        have_threads = True
        try:
            import _thread
        except ImportError:
            have_threads = False

        if have_threads:
            self.current_frames_with_threads()
        else:
            self.current_frames_without_threads()

    
    @test.support.reap_threads
    def current_frames_with_threads(self):
        import threading
        import traceback

        
        
        
        entered_g = threading.Event()
        leave_g = threading.Event()
        thread_info = []  

        def f123():
            g456()

        def g456():
            thread_info.append(threading.get_ident())
            entered_g.set()
            leave_g.wait()

        t = threading.Thread(target=f123)
        t.start()
        entered_g.wait()

        
        
        
        self.assertEqual(len(thread_info), 1)
        thread_id = thread_info[0]

        d = sys._current_frames()

        main_id = threading.get_ident()
        self.assertIn(main_id, d)
        self.assertIn(thread_id, d)

        
        frame = d.pop(main_id)
        self.assertTrue(frame is sys._getframe())

        
        
        
        frame = d.pop(thread_id)
        stack = traceback.extract_stack(frame)
        for i, (filename, lineno, funcname, sourceline) in enumerate(stack):
            if funcname == "f123":
                break
        else:
            self.fail("didn't find f123() on thread's call stack")

        self.assertEqual(sourceline, "g456()")

        
        filename, lineno, funcname, sourceline = stack[i+1]
        self.assertEqual(funcname, "g456")
        self.assertIn(sourceline, ["leave_g.wait()", "entered_g.set()"])

        
        leave_g.set()
        t.join()

    
    def current_frames_without_threads(self):
        
        "thread id" 0.
        d = sys._current_frames()
        self.assertEqual(len(d), 1)
        self.assertIn(0, d)
        self.assertTrue(d[0] is sys._getframe())

    def test_attributes(self):
        self.assertIsInstance(sys.api_version, int)
        self.assertIsInstance(sys.argv, list)
        self.assertIn(sys.byteorder, ("little", "big"))
        self.assertIsInstance(sys.builtin_module_names, tuple)
        self.assertIsInstance(sys.copyright, str)
        self.assertIsInstance(sys.exec_prefix, str)
        self.assertIsInstance(sys.base_exec_prefix, str)
        self.assertIsInstance(sys.executable, str)
        self.assertEqual(len(sys.float_info), 11)
        self.assertEqual(sys.float_info.radix, 2)
        self.assertEqual(len(sys.int_info), 2)
        self.assertTrue(sys.int_info.bits_per_digit % 5 == 0)
        self.assertTrue(sys.int_info.sizeof_digit >= 1)
        self.assertEqual(type(sys.int_info.bits_per_digit), int)
        self.assertEqual(type(sys.int_info.sizeof_digit), int)
        self.assertIsInstance(sys.hexversion, int)

        self.assertEqual(len(sys.hash_info), 9)
        self.assertLess(sys.hash_info.modulus, 2**sys.hash_info.width)
        
        
        
        for x in range(1, 100):
            self.assertEqual(
                pow(x, sys.hash_info.modulus-1, sys.hash_info.modulus),
                1,
                "sys.hash_info.modulus {} is a non-prime".format(
                    sys.hash_info.modulus)
                )
        self.assertIsInstance(sys.hash_info.inf, int)
        self.assertIsInstance(sys.hash_info.nan, int)
        self.assertIsInstance(sys.hash_info.imag, int)
        algo = sysconfig.get_config_var("Py_HASH_ALGORITHM")
        if sys.hash_info.algorithm in {"fnv", "siphash24"}:
            self.assertIn(sys.hash_info.hash_bits, {32, 64})
            self.assertIn(sys.hash_info.seed_bits, {32, 64, 128})

            if algo == 1:
                self.assertEqual(sys.hash_info.algorithm, "siphash24")
            elif algo == 2:
                self.assertEqual(sys.hash_info.algorithm, "fnv")
            else:
                self.assertIn(sys.hash_info.algorithm, {"fnv", "siphash24"})
        else:
            
            self.assertEqual(algo, 0)
        self.assertGreaterEqual(sys.hash_info.cutoff, 0)
        self.assertLess(sys.hash_info.cutoff, 8)

        self.assertIsInstance(sys.maxsize, int)
        self.assertIsInstance(sys.maxunicode, int)
        self.assertEqual(sys.maxunicode, 0x10FFFF)
        self.assertIsInstance(sys.platform, str)
        self.assertIsInstance(sys.prefix, str)
        self.assertIsInstance(sys.base_prefix, str)
        self.assertIsInstance(sys.version, str)
        vi = sys.version_info
        self.assertIsInstance(vi[:], tuple)
        self.assertEqual(len(vi), 5)
        self.assertIsInstance(vi[0], int)
        self.assertIsInstance(vi[1], int)
        self.assertIsInstance(vi[2], int)
        self.assertIn(vi[3], ("alpha", "beta", "candidate", "final"))
        self.assertIsInstance(vi[4], int)
        self.assertIsInstance(vi.major, int)
        self.assertIsInstance(vi.minor, int)
        self.assertIsInstance(vi.micro, int)
        self.assertIn(vi.releaselevel, ("alpha", "beta", "candidate", "final"))
        self.assertIsInstance(vi.serial, int)
        self.assertEqual(vi[0], vi.major)
        self.assertEqual(vi[1], vi.minor)
        self.assertEqual(vi[2], vi.micro)
        self.assertEqual(vi[3], vi.releaselevel)
        self.assertEqual(vi[4], vi.serial)
        self.assertTrue(vi > (1,0,0))
        self.assertIsInstance(sys.float_repr_style, str)
        self.assertIn(sys.float_repr_style, ('short', 'legacy'))
        if not sys.platform.startswith('win'):
            self.assertIsInstance(sys.abiflags, str)

    @unittest.skipUnless(hasattr(sys, 'thread_info'),
                         'Threading required for this test.')
    def test_thread_info(self):
        info = sys.thread_info
        self.assertEqual(len(info), 3)
        self.assertIn(info.name, ('nt', 'pthread', 'solaris', None))
        self.assertIn(info.lock, ('semaphore', 'mutex+cond', None))

    def test_43581(self):
        
        
        self.assertEqual(sys.__stdout__.encoding, sys.__stderr__.encoding)

    def test_intern(self):
        global numruns
        numruns += 1
        self.assertRaises(TypeError, sys.intern)
        s = "never interned before" + str(numruns)
        self.assertTrue(sys.intern(s) is s)
        s2 = s.swapcase().swapcase()
        self.assertTrue(sys.intern(s2) is s)

        
        
        
        
        
        class S(str):
            def __hash__(self):
                return 123

        self.assertRaises(TypeError, sys.intern, S("abc"))

    def test_sys_flags(self):
        self.assertTrue(sys.flags)
        attrs = ("debug",
                 "inspect", "interactive", "optimize", "dont_write_bytecode",
                 "no_user_site", "no_site", "ignore_environment", "verbose",
                 "bytes_warning", "quiet", "hash_randomization", "isolated")
        for attr in attrs:
            self.assertTrue(hasattr(sys.flags, attr), attr)
            self.assertEqual(type(getattr(sys.flags, attr)), int, attr)
        self.assertTrue(repr(sys.flags))
        self.assertEqual(len(sys.flags), len(attrs))

    def assert_raise_on_new_sys_type(self, sys_attr):
        
        
        attr_type = type(sys_attr)
        with self.assertRaises(TypeError):
            attr_type()
        with self.assertRaises(TypeError):
            attr_type.__new__(attr_type)

    def test_sys_flags_no_instantiation(self):
        self.assert_raise_on_new_sys_type(sys.flags)

    def test_sys_version_info_no_instantiation(self):
        self.assert_raise_on_new_sys_type(sys.version_info)

    def test_sys_getwindowsversion_no_instantiation(self):
        
        test.support.get_attribute(sys, "getwindowsversion")
        self.assert_raise_on_new_sys_type(sys.getwindowsversion())

    @test.support.cpython_only
    def test_clear_type_cache(self):
        sys._clear_type_cache()

    def test_ioencoding(self):
        env = dict(os.environ)

        
        

        env["PYTHONIOENCODING"] = "cp424"
        p = subprocess.Popen([sys.executable, "-c", 'print(chr(0xa2))'],
                             stdout = subprocess.PIPE, env=env)
        out = p.communicate()[0].strip()
        expected = ("\xa2" + os.linesep).encode("cp424")
        self.assertEqual(out, expected)

        env["PYTHONIOENCODING"] = "ascii:replace"
        p = subprocess.Popen([sys.executable, "-c", 'print(chr(0xa2))'],
                             stdout = subprocess.PIPE, env=env)
        out = p.communicate()[0].strip()
        self.assertEqual(out, b'?')

        env["PYTHONIOENCODING"] = "ascii"
        p = subprocess.Popen([sys.executable, "-c", 'print(chr(0xa2))'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             env=env)
        out, err = p.communicate()
        self.assertEqual(out, b'')
        self.assertIn(b'UnicodeEncodeError:', err)
        self.assertIn(rb"'\xa2'", err)

        env["PYTHONIOENCODING"] = "ascii:"
        p = subprocess.Popen([sys.executable, "-c", 'print(chr(0xa2))'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             env=env)
        out, err = p.communicate()
        self.assertEqual(out, b'')
        self.assertIn(b'UnicodeEncodeError:', err)
        self.assertIn(rb"'\xa2'", err)

        env["PYTHONIOENCODING"] = ":surrogateescape"
        p = subprocess.Popen([sys.executable, "-c", 'print(chr(0xdcbd))'],
                             stdout=subprocess.PIPE, env=env)
        out = p.communicate()[0].strip()
        self.assertEqual(out, b'\xbd')

    @unittest.skipUnless(test.support.FS_NONASCII,
                         'requires OS support of non-ASCII encodings')
    def test_ioencoding_nonascii(self):
        env = dict(os.environ)

        env["PYTHONIOENCODING"] = ""
        p = subprocess.Popen([sys.executable, "-c",
                                'print(%a)' % test.support.FS_NONASCII],
                                stdout=subprocess.PIPE, env=env)
        out = p.communicate()[0].strip()
        self.assertEqual(out, os.fsencode(test.support.FS_NONASCII))

    @unittest.skipIf(sys.base_prefix != sys.prefix,
                     'Test is not venv-compatible')
    def test_executable(self):
        
        self.assertEqual(os.path.abspath(sys.executable), sys.executable)

        
        
        

        
        
        python_dir = os.path.dirname(os.path.realpath(sys.executable))
        p = subprocess.Popen(
            ["nonexistent", "-c",
             'import sys; print(sys.executable.encode("ascii", "backslashreplace"))'],
            executable=sys.executable, stdout=subprocess.PIPE, cwd=python_dir)
        stdout = p.communicate()[0]
        executable = stdout.strip().decode("ASCII")
        p.wait()
        self.assertIn(executable, ["b''", repr(sys.executable.encode("ascii", "backslashreplace"))])

    def check_fsencoding(self, fs_encoding, expected=None):
        self.assertIsNotNone(fs_encoding)
        codecs.lookup(fs_encoding)
        if expected:
            self.assertEqual(fs_encoding, expected)

    def test_getfilesystemencoding(self):
        fs_encoding = sys.getfilesystemencoding()
        if sys.platform == 'darwin':
            expected = 'utf-8'
        elif sys.platform == 'win32':
            expected = 'mbcs'
        else:
            expected = None
        self.check_fsencoding(fs_encoding, expected)

    def test_implementation(self):
        

        levels = {'alpha': 0xA, 'beta': 0xB, 'candidate': 0xC, 'final': 0xF}

        self.assertTrue(hasattr(sys.implementation, 'name'))
        self.assertTrue(hasattr(sys.implementation, 'version'))
        self.assertTrue(hasattr(sys.implementation, 'hexversion'))
        self.assertTrue(hasattr(sys.implementation, 'cache_tag'))

        version = sys.implementation.version
        self.assertEqual(version[:2], (version.major, version.minor))

        hexversion = (version.major << 24 | version.minor << 16 |
                      version.micro << 8 | levels[version.releaselevel] << 4 |
                      version.serial << 0)
        self.assertEqual(sys.implementation.hexversion, hexversion)

        
        self.assertEqual(sys.implementation.name,
                         sys.implementation.name.lower())

    @test.support.cpython_only
    def test_debugmallocstats(self):
        
        from test.script_helper import assert_python_ok
        args = ['-c', 'import sys; sys._debugmallocstats()']
        ret, out, err = assert_python_ok(*args)
        self.assertIn(b"free PyDictObjects", err)

        
        self.assertRaises(TypeError, sys._debugmallocstats, True)

    @unittest.skipUnless(hasattr(sys, "getallocatedblocks"),
                         "sys.getallocatedblocks unavailable on this build")
    def test_getallocatedblocks(self):
        
        with_pymalloc = sysconfig.get_config_var('WITH_PYMALLOC')
        a = sys.getallocatedblocks()
        self.assertIs(type(a), int)
        if with_pymalloc:
            self.assertGreater(a, 0)
        else:
            
            
            
            self.assertGreaterEqual(a, 0)
        try:
            
            
            
            self.assertLess(a, sys.gettotalrefcount())
        except AttributeError:
            
            pass
        gc.collect()
        b = sys.getallocatedblocks()
        self.assertLessEqual(b, a)
        gc.collect()
        c = sys.getallocatedblocks()
        self.assertIn(c, range(b - 50, b + 50))


@test.support.cpython_only
class SizeofTest(unittest.TestCase):

    def setUp(self):
        self.P = struct.calcsize('P')
        self.longdigit = sys.int_info.sizeof_digit
        import _testcapi
        self.gc_headsize = _testcapi.SIZEOF_PYGC_HEAD
        self.file = open(test.support.TESTFN, 'wb')

    def tearDown(self):
        self.file.close()
        test.support.unlink(test.support.TESTFN)

    check_sizeof = test.support.check_sizeof

    def test_gc_head_size(self):
        
        vsize = test.support.calcvobjsize
        gc_header_size = self.gc_headsize
        
        self.assertEqual(sys.getsizeof(True), vsize('') + self.longdigit)
        
        self.assertEqual(sys.getsizeof([]), vsize('Pn') + gc_header_size)

    def test_errors(self):
        class BadSizeof:
            def __sizeof__(self):
                raise ValueError
        self.assertRaises(ValueError, sys.getsizeof, BadSizeof())

        class InvalidSizeof:
            def __sizeof__(self):
                return None
        self.assertRaises(TypeError, sys.getsizeof, InvalidSizeof())
        sentinel = ["sentinel"]
        self.assertIs(sys.getsizeof(InvalidSizeof(), sentinel), sentinel)

        class FloatSizeof:
            def __sizeof__(self):
                return 4.5
        self.assertRaises(TypeError, sys.getsizeof, FloatSizeof())
        self.assertIs(sys.getsizeof(FloatSizeof(), sentinel), sentinel)

        class OverflowSizeof(int):
            def __sizeof__(self):
                return int(self)
        self.assertEqual(sys.getsizeof(OverflowSizeof(sys.maxsize)),
                         sys.maxsize + self.gc_headsize)
        with self.assertRaises(OverflowError):
            sys.getsizeof(OverflowSizeof(sys.maxsize + 1))
        with self.assertRaises(ValueError):
            sys.getsizeof(OverflowSizeof(-1))
        with self.assertRaises((ValueError, OverflowError)):
            sys.getsizeof(OverflowSizeof(-sys.maxsize - 1))

    def test_default(self):
        size = test.support.calcvobjsize
        self.assertEqual(sys.getsizeof(True), size('') + self.longdigit)
        self.assertEqual(sys.getsizeof(True, -1), size('') + self.longdigit)

    def test_objecttypes(self):
        
        size = test.support.calcobjsize
        vsize = test.support.calcvobjsize
        check = self.check_sizeof
        
        check(True, vsize('') + self.longdigit)
        
        
        
        check(len, size('3P')) 
        
        samples = [b'', b'u'*100000]
        for sample in samples:
            x = bytearray(sample)
            check(x, vsize('n2Pi') + x.__alloc__())
        
        check(iter(bytearray()), size('nP'))
        
        check(b'', vsize('n') + 1)
        check(b'x' * 10, vsize('n') + 11)
        
        def get_cell():
            x = 42
            def inner():
                return x
            return inner
        check(get_cell().__closure__[0], size('P'))
        
        check(get_cell().__code__, size('5i9Pi3P'))
        check(get_cell.__code__, size('5i9Pi3P'))
        def get_cell2(x):
            def inner():
                return x
            return inner
        check(get_cell2.__code__, size('5i9Pi3P') + 1)
        
        check(complex(0,1), size('2d'))
        
        check(str.lower, size('3PP'))
        
        
        
        import datetime
        check(datetime.timedelta.days, size('3PP'))
        
        import collections
        check(collections.defaultdict.default_factory, size('3PP'))
        
        check(int.__add__, size('3P2P'))
        
        check({}.__iter__, size('2P'))
        
        check({}, size('n2P' + '2nPn' + 8*'n2P'))
        longdict = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8}
        check(longdict, size('n2P' + '2nPn') + 16*struct.calcsize('n2P'))
        
        check({}.keys(), size('P'))
        
        check({}.values(), size('P'))
        
        check({}.items(), size('P'))
        
        check(iter({}), size('P2nPn'))
        
        class C(object): pass
        check(C.__dict__, size('P'))
        
        check(BaseException(), size('5Pb'))
        
        check(UnicodeEncodeError("", "", 0, 0, ""), size('5Pb 2P2nP'))
        
        check(UnicodeDecodeError("", b"", 0, 0, ""), size('5Pb 2P2nP'))
        
        check(UnicodeTranslateError("", 0, 1, ""), size('5Pb 2P2nP'))
        
        check(Ellipsis, size(''))
        
        import codecs, encodings.iso8859_3
        x = codecs.charmap_build(encodings.iso8859_3.decoding_table)
        check(x, size('32B2iB'))
        
        check(enumerate([]), size('n3P'))
        
        check(reversed(''), size('nP'))
        
        check(float(0), size('d'))
        
        check(sys.float_info, vsize('') + self.P * len(sys.float_info))
        
        import inspect
        CO_MAXBLOCKS = 20
        x = inspect.currentframe()
        ncells = len(x.f_code.co_cellvars)
        nfrees = len(x.f_code.co_freevars)
        extras = x.f_code.co_stacksize + x.f_code.co_nlocals +\
                  ncells + nfrees - 1
        check(x, vsize('12P3ic' + CO_MAXBLOCKS*'3i' + 'P' + extras*'P'))
        
        def func(): pass
        check(func, size('12P'))
        class c():
            @staticmethod
            def foo():
                pass
            @classmethod
            def bar(cls):
                pass
            
            check(foo, size('PP'))
            
            check(bar, size('PP'))
        
        def get_gen(): yield 1
        check(get_gen(), size('Pb2P'))
        
        check(iter('abc'), size('lP'))
        
        import re
        check(re.finditer('',''), size('2P'))
        
        samples = [[], [1,2,3], ['1', '2', '3']]
        for sample in samples:
            check(sample, vsize('Pn') + len(sample)*self.P)
        
        
        
        
        
        check(iter([]), size('lP'))
        
        check(reversed([]), size('nP'))
        
        check(0, vsize(''))
        check(1, vsize('') + self.longdigit)
        check(-1, vsize('') + self.longdigit)
        PyLong_BASE = 2**sys.int_info.bits_per_digit
        check(int(PyLong_BASE), vsize('') + 2*self.longdigit)
        check(int(PyLong_BASE**2-1), vsize('') + 2*self.longdigit)
        check(int(PyLong_BASE**2), vsize('') + 3*self.longdigit)
        
        check(unittest, size('PnPPP'))
        
        check(None, size(''))
        
        check(NotImplemented, size(''))
        
        check(object(), size(''))
        
        class C(object):
            def getx(self): return self.__x
            def setx(self, value): self.__x = value
            def delx(self): del self.__x
            x = property(getx, setx, delx, "")
            check(x, size('4Pi'))
        
        
        
        check(iter(range(1)), size('4l'))
        
        check(reversed(''), size('nP'))
        
        check(range(1), size('4P'))
        check(range(66000), size('4P'))
        
        
        PySet_MINSIZE = 8
        samples = [[], range(10), range(50)]
        s = size('3n2P' + PySet_MINSIZE*'nP' + 'nP')
        for sample in samples:
            minused = len(sample)
            if minused == 0: tmp = 1
            
            
            minused = minused*2
            newsize = PySet_MINSIZE
            while newsize <= minused:
                newsize = newsize << 1
            if newsize <= 8:
                check(set(sample), s)
                check(frozenset(sample), s)
            else:
                check(set(sample), s + newsize*struct.calcsize('nP'))
                check(frozenset(sample), s + newsize*struct.calcsize('nP'))
        
        check(iter(set()), size('P3n'))
        
        check(slice(0), size('3P'))
        
        check(super(int), size('3P'))
        
        check((), vsize(''))
        check((1,2,3), vsize('') + 3*self.P)
        
        
        s = vsize('P2n15Pl4Pn9Pn11PIP')
        check(int, s)
        
        
        s = vsize('P2n15Pl4Pn9Pn11PIP') + struct.calcsize('34P 3P 10P 2P 4P')
        
        s += struct.calcsize("2nPn") + 4*struct.calcsize("n2P")
        
        class newstyleclass(object): pass
        check(newstyleclass, s)
        
        check(newstyleclass().__dict__, size('n2P' + '2nPn'))
        
        
        
        
        samples = ['1'*100, '\xff'*50,
                   '\u0100'*40, '\uffff'*100,
                   '\U00010000'*30, '\U0010ffff'*100]
        asciifields = "nnbP"
        compactfields = asciifields + "nPn"
        unicodefields = compactfields + "P"
        for s in samples:
            maxchar = ord(max(s))
            if maxchar < 128:
                L = size(asciifields) + len(s) + 1
            elif maxchar < 256:
                L = size(compactfields) + len(s) + 1
            elif maxchar < 65536:
                L = size(compactfields) + 2*(len(s) + 1)
            else:
                L = size(compactfields) + 4*(len(s) + 1)
            check(s, L)
        
        s = chr(0x4000)   
        check(s, size(compactfields) + 4)
        
        
        compile(s, "<stdin>", "eval")
        check(s, size(compactfields) + 4 + 4)
        
        
        
        import weakref
        check(weakref.ref(int), size('2Pn2P'))
        
        
        
        check(weakref.proxy(int), size('2Pn2P'))

    def test_pythontypes(self):
        
        size = test.support.calcobjsize
        vsize = test.support.calcvobjsize
        check = self.check_sizeof
        
        import _ast
        check(_ast.AST(), size('P'))
        try:
            raise TypeError
        except TypeError:
            tb = sys.exc_info()[2]
            
            if tb is not None:
                check(tb, size('2P2i'))
        
        
        
        check(sys.flags, vsize('') + self.P * len(sys.flags))


def test_main():
    test.support.run_unittest(SysModuleTest, SizeofTest)

if __name__ == "__main__":
    test_main()
