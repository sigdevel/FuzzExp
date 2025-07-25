import collections
import datetime
import functools
import importlib
import inspect
import io
import linecache
import os
from os.path import normcase
import _pickle
import re
import shutil
import sys
import types
import textwrap
import unicodedata
import unittest
import unittest.mock

try:
    from concurrent.futures import ThreadPoolExecutor
except ImportError:
    ThreadPoolExecutor = None

from test.support import run_unittest, TESTFN, DirsOnSysPath, cpython_only
from test.support import MISSING_C_DOCSTRINGS
from test.script_helper import assert_python_ok, assert_python_failure
from test import inspect_fodder as mod
from test import inspect_fodder2 as mod2

from test.test_import import _ready_to_import












modfile = mod.__file__
if modfile.endswith(('c', 'o')):
    modfile = modfile[:-1]



modfile = normcase(modfile)

def revise(filename, *args):
    return (normcase(filename),) + args

import builtins

git = mod.StupidGit()

class IsTestBase(unittest.TestCase):
    predicates = set([inspect.isbuiltin, inspect.isclass, inspect.iscode,
                      inspect.isframe, inspect.isfunction, inspect.ismethod,
                      inspect.ismodule, inspect.istraceback,
                      inspect.isgenerator, inspect.isgeneratorfunction])

    def istest(self, predicate, exp):
        obj = eval(exp)
        self.assertTrue(predicate(obj), '%s(%s)' % (predicate.__name__, exp))

        for other in self.predicates - set([predicate]):
            if predicate == inspect.isgeneratorfunction and\
               other == inspect.isfunction:
                continue
            self.assertFalse(other(obj), 'not %s(%s)' % (other.__name__, exp))

def generator_function_example(self):
    for i in range(2):
        yield i

class EqualsToAll:
    def __eq__(self, other):
        return True

class TestPredicates(IsTestBase):
    def test_sixteen(self):
        count = len([x for x in dir(inspect) if x.startswith('is')])
        
        
        expected = 16
        err_msg = "There are %d (not %d) is* functions" % (count, expected)
        self.assertEqual(count, expected, err_msg)


    def test_excluding_predicates(self):
        global tb
        self.istest(inspect.isbuiltin, 'sys.exit')
        self.istest(inspect.isbuiltin, '[].append')
        self.istest(inspect.iscode, 'mod.spam.__code__')
        try:
            1/0
        except:
            tb = sys.exc_info()[2]
            self.istest(inspect.isframe, 'tb.tb_frame')
            self.istest(inspect.istraceback, 'tb')
            if hasattr(types, 'GetSetDescriptorType'):
                self.istest(inspect.isgetsetdescriptor,
                            'type(tb.tb_frame).f_locals')
            else:
                self.assertFalse(inspect.isgetsetdescriptor(type(tb.tb_frame).f_locals))
        finally:
            
            tb = None
        self.istest(inspect.isfunction, 'mod.spam')
        self.istest(inspect.isfunction, 'mod.StupidGit.abuse')
        self.istest(inspect.ismethod, 'git.argue')
        self.istest(inspect.ismodule, 'mod')
        self.istest(inspect.isdatadescriptor, 'collections.defaultdict.default_factory')
        self.istest(inspect.isgenerator, '(x for x in range(2))')
        self.istest(inspect.isgeneratorfunction, 'generator_function_example')
        if hasattr(types, 'MemberDescriptorType'):
            self.istest(inspect.ismemberdescriptor, 'datetime.timedelta.days')
        else:
            self.assertFalse(inspect.ismemberdescriptor(datetime.timedelta.days))

    def test_isroutine(self):
        self.assertTrue(inspect.isroutine(mod.spam))
        self.assertTrue(inspect.isroutine([].count))

    def test_isclass(self):
        self.istest(inspect.isclass, 'mod.StupidGit')
        self.assertTrue(inspect.isclass(list))

        class CustomGetattr(object):
            def __getattr__(self, attr):
                return None
        self.assertFalse(inspect.isclass(CustomGetattr()))

    def test_get_slot_members(self):
        class C(object):
            __slots__ = ("a", "b")
        x = C()
        x.a = 42
        members = dict(inspect.getmembers(x))
        self.assertIn('a', members)
        self.assertNotIn('b', members)

    def test_isabstract(self):
        from abc import ABCMeta, abstractmethod

        class AbstractClassExample(metaclass=ABCMeta):

            @abstractmethod
            def foo(self):
                pass

        class ClassExample(AbstractClassExample):
            def foo(self):
                pass

        a = ClassExample()

        
        self.assertTrue(inspect.isabstract(AbstractClassExample))
        self.assertFalse(inspect.isabstract(ClassExample))
        self.assertFalse(inspect.isabstract(a))
        self.assertFalse(inspect.isabstract(int))
        self.assertFalse(inspect.isabstract(5))


class TestInterpreterStack(IsTestBase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

        git.abuse(7, 8, 9)

    def test_abuse_done(self):
        self.istest(inspect.istraceback, 'git.ex[2]')
        self.istest(inspect.isframe, 'mod.fr')

    def test_stack(self):
        self.assertTrue(len(mod.st) >= 5)
        self.assertEqual(revise(*mod.st[0][1:]),
             (modfile, 16, 'eggs', ['    st = inspect.stack()\n'], 0))
        self.assertEqual(revise(*mod.st[1][1:]),
             (modfile, 9, 'spam', ['    eggs(b + d, c + f)\n'], 0))
        self.assertEqual(revise(*mod.st[2][1:]),
             (modfile, 43, 'argue', ['            spam(a, b, c)\n'], 0))
        self.assertEqual(revise(*mod.st[3][1:]),
             (modfile, 39, 'abuse', ['        self.argue(a, b, c)\n'], 0))

    def test_trace(self):
        self.assertEqual(len(git.tr), 3)
        self.assertEqual(revise(*git.tr[0][1:]),
             (modfile, 43, 'argue', ['            spam(a, b, c)\n'], 0))
        self.assertEqual(revise(*git.tr[1][1:]),
             (modfile, 9, 'spam', ['    eggs(b + d, c + f)\n'], 0))
        self.assertEqual(revise(*git.tr[2][1:]),
             (modfile, 18, 'eggs', ['    q = y / 0\n'], 0))

    def test_frame(self):
        args, varargs, varkw, locals = inspect.getargvalues(mod.fr)
        self.assertEqual(args, ['x', 'y'])
        self.assertEqual(varargs, None)
        self.assertEqual(varkw, None)
        self.assertEqual(locals, {'x': 11, 'p': 11, 'y': 14})
        self.assertEqual(inspect.formatargvalues(args, varargs, varkw, locals),
                         '(x=11, y=14)')

    def test_previous_frame(self):
        args, varargs, varkw, locals = inspect.getargvalues(mod.fr.f_back)
        self.assertEqual(args, ['a', 'b', 'c', 'd', 'e', 'f'])
        self.assertEqual(varargs, 'g')
        self.assertEqual(varkw, 'h')
        self.assertEqual(inspect.formatargvalues(args, varargs, varkw, locals),
             '(a=7, b=8, c=9, d=3, e=4, f=5, *g=(), **h={})')

class GetSourceBase(unittest.TestCase):
    
    fodderModule = None

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

        with open(inspect.getsourcefile(self.fodderModule)) as fp:
            self.source = fp.read()

    def sourcerange(self, top, bottom):
        lines = self.source.split("\n")
        return "\n".join(lines[top-1:bottom]) + "\n"

    def assertSourceEqual(self, obj, top, bottom):
        self.assertEqual(inspect.getsource(obj),
                         self.sourcerange(top, bottom))

class TestRetrievingSourceCode(GetSourceBase):
    fodderModule = mod

    def test_getclasses(self):
        classes = inspect.getmembers(mod, inspect.isclass)
        self.assertEqual(classes,
                         [('FesteringGob', mod.FesteringGob),
                          ('MalodorousPervert', mod.MalodorousPervert),
                          ('ParrotDroppings', mod.ParrotDroppings),
                          ('StupidGit', mod.StupidGit),
                          ('Tit', mod.MalodorousPervert),
                         ])
        tree = inspect.getclasstree([cls[1] for cls in classes])
        self.assertEqual(tree,
                         [(object, ()),
                          [(mod.ParrotDroppings, (object,)),
                           [(mod.FesteringGob, (mod.MalodorousPervert,
                                                   mod.ParrotDroppings))
                            ],
                           (mod.StupidGit, (object,)),
                           [(mod.MalodorousPervert, (mod.StupidGit,)),
                            [(mod.FesteringGob, (mod.MalodorousPervert,
                                                    mod.ParrotDroppings))
                             ]
                            ]
                           ]
                          ])
        tree = inspect.getclasstree([cls[1] for cls in classes], True)
        self.assertEqual(tree,
                         [(object, ()),
                          [(mod.ParrotDroppings, (object,)),
                           (mod.StupidGit, (object,)),
                           [(mod.MalodorousPervert, (mod.StupidGit,)),
                            [(mod.FesteringGob, (mod.MalodorousPervert,
                                                    mod.ParrotDroppings))
                             ]
                            ]
                           ]
                          ])

    def test_getfunctions(self):
        functions = inspect.getmembers(mod, inspect.isfunction)
        self.assertEqual(functions, [('eggs', mod.eggs),
                                     ('spam', mod.spam)])

    @unittest.skipIf(sys.flags.optimize >= 2,
                     "Docstrings are omitted with -O2 and above")
    def test_getdoc(self):
        self.assertEqual(inspect.getdoc(mod), 'A module docstring.')
        self.assertEqual(inspect.getdoc(mod.StupidGit),
                         'A longer,\n\nindented\n\ndocstring.')
        self.assertEqual(inspect.getdoc(git.abuse),
                         'Another\n\ndocstring\n\ncontaining\n\ntabs')

    def test_cleandoc(self):
        self.assertEqual(inspect.cleandoc('An\n    indented\n    docstring.'),
                         'An\nindented\ndocstring.')

    def test_getcomments(self):
        self.assertEqual(inspect.getcomments(mod), '
        self.assertEqual(inspect.getcomments(mod.StupidGit), '

    def test_getmodule(self):
        
        self.assertEqual(inspect.getmodule(mod), mod)
        
        self.assertEqual(inspect.getmodule(mod.StupidGit), mod)
        
        self.assertEqual(inspect.getmodule(mod.StupidGit.abuse), mod)
        
        self.assertEqual(inspect.getmodule(mod.StupidGit.abuse), mod)
        
        self.assertEqual(inspect.getmodule(str), sys.modules["builtins"])
        
        self.assertEqual(inspect.getmodule(None, modfile), mod)

    def test_getsource(self):
        self.assertSourceEqual(git.abuse, 29, 39)
        self.assertSourceEqual(mod.StupidGit, 21, 46)

    def test_getsourcefile(self):
        self.assertEqual(normcase(inspect.getsourcefile(mod.spam)), modfile)
        self.assertEqual(normcase(inspect.getsourcefile(git.abuse)), modfile)
        fn = "_non_existing_filename_used_for_sourcefile_test.py"
        co = compile("None", fn, "exec")
        self.assertEqual(inspect.getsourcefile(co), None)
        linecache.cache[co.co_filename] = (1, None, "None", co.co_filename)
        try:
            self.assertEqual(normcase(inspect.getsourcefile(co)), fn)
        finally:
            del linecache.cache[co.co_filename]

    def test_getfile(self):
        self.assertEqual(inspect.getfile(mod.StupidGit), mod.__file__)

    def test_getfile_class_without_module(self):
        class CM(type):
            @property
            def __module__(cls):
                raise AttributeError
        class C(metaclass=CM):
            pass
        with self.assertRaises(TypeError):
            inspect.getfile(C)

    def test_getmodule_recursion(self):
        from types import ModuleType
        name = '__inspect_dummy'
        m = sys.modules[name] = ModuleType(name)
        m.__file__ = "<string>" 
        m.__loader__ = "dummy"  
        exec("def x(): pass", m.__dict__)
        self.assertEqual(inspect.getsourcefile(m.x.__code__), '<string>')
        del sys.modules[name]
        inspect.getmodule(compile('a=10','','single'))

    def test_proceed_with_fake_filename(self):
        '''doctest monkeypatches linecache to enable inspection'''
        fn, source = '<test>', 'def x(): pass\n'
        getlines = linecache.getlines
        def monkey(filename, module_globals=None):
            if filename == fn:
                return source.splitlines(keepends=True)
            else:
                return getlines(filename, module_globals)
        linecache.getlines = monkey
        try:
            ns = {}
            exec(compile(source, fn, 'single'), ns)
            inspect.getsource(ns["x"])
        finally:
            linecache.getlines = getlines

class TestDecorators(GetSourceBase):
    fodderModule = mod2

    def test_wrapped_decorator(self):
        self.assertSourceEqual(mod2.wrapped, 14, 17)

    def test_replacing_decorator(self):
        self.assertSourceEqual(mod2.gone, 9, 10)

class TestOneliners(GetSourceBase):
    fodderModule = mod2
    def test_oneline_lambda(self):
        
        self.assertSourceEqual(mod2.oll, 25, 25)

    def test_threeline_lambda(self):
        
        
        self.assertSourceEqual(mod2.tll, 28, 30)

    def test_twoline_indented_lambda(self):
        
        
        self.assertSourceEqual(mod2.tlli, 33, 34)

    def test_onelinefunc(self):
        
        self.assertSourceEqual(mod2.onelinefunc, 37, 37)

    def test_manyargs(self):
        
        
        
        self.assertSourceEqual(mod2.manyargs, 40, 41)

    def test_twolinefunc(self):
        
        
        
        self.assertSourceEqual(mod2.twolinefunc, 44, 45)

    def test_lambda_in_list(self):
        
        
        self.assertSourceEqual(mod2.a[1], 49, 49)

    def test_anonymous(self):
        
        
        self.assertSourceEqual(mod2.anonymous, 55, 55)

class TestBuggyCases(GetSourceBase):
    fodderModule = mod2

    def test_with_comment(self):
        self.assertSourceEqual(mod2.with_comment, 58, 59)

    def test_multiline_sig(self):
        self.assertSourceEqual(mod2.multiline_sig[0], 63, 64)

    def test_nested_class(self):
        self.assertSourceEqual(mod2.func69().func71, 71, 72)

    def test_one_liner_followed_by_non_name(self):
        self.assertSourceEqual(mod2.func77, 77, 77)

    def test_one_liner_dedent_non_name(self):
        self.assertSourceEqual(mod2.cls82.func83, 83, 83)

    def test_with_comment_instead_of_docstring(self):
        self.assertSourceEqual(mod2.func88, 88, 90)

    def test_method_in_dynamic_class(self):
        self.assertSourceEqual(mod2.method_in_dynamic_class, 95, 97)

    
    
    @unittest.skipIf(not hasattr(unicodedata, '__file__') or
                                 unicodedata.__file__.endswith('.py'),
                     "unicodedata is not an external binary module")
    def test_findsource_binary(self):
        self.assertRaises(OSError, inspect.getsource, unicodedata)
        self.assertRaises(OSError, inspect.findsource, unicodedata)

    def test_findsource_code_in_linecache(self):
        lines = ["x=1"]
        co = compile(lines[0], "_dynamically_created_file", "exec")
        self.assertRaises(OSError, inspect.findsource, co)
        self.assertRaises(OSError, inspect.getsource, co)
        linecache.cache[co.co_filename] = (1, None, lines, co.co_filename)
        try:
            self.assertEqual(inspect.findsource(co), (lines,0))
            self.assertEqual(inspect.getsource(co), lines[0])
        finally:
            del linecache.cache[co.co_filename]

    def test_findsource_without_filename(self):
        for fname in ['', '<string>']:
            co = compile('x=1', fname, "exec")
            self.assertRaises(IOError, inspect.findsource, co)
            self.assertRaises(IOError, inspect.getsource, co)

class TestNoEOL(GetSourceBase):
    def __init__(self, *args, **kwargs):
        self.tempdir = TESTFN + '_dir'
        os.mkdir(self.tempdir)
        with open(os.path.join(self.tempdir,
                               'inspect_fodder3%spy' % os.extsep), 'w') as f:
            f.write("class X:\n    pass ")
        with DirsOnSysPath(self.tempdir):
            import inspect_fodder3 as mod3
        self.fodderModule = mod3
        GetSourceBase.__init__(self, *args, **kwargs)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_class(self):
        self.assertSourceEqual(self.fodderModule.X, 1, 2)


class _BrokenDataDescriptor(object):
    """
    A broken data descriptor. See bug 
    """
    def __get__(*args):
        raise AttributeError("broken data descriptor")

    def __set__(*args):
        raise RuntimeError

    def __getattr__(*args):
        raise AttributeError("broken data descriptor")


class _BrokenMethodDescriptor(object):
    """
    A broken method descriptor. See bug 
    """
    def __get__(*args):
        raise AttributeError("broken method descriptor")

    def __getattr__(*args):
        raise AttributeError("broken method descriptor")



def attrs_wo_objs(cls):
    return [t[:3] for t in inspect.classify_class_attrs(cls)]


class TestClassesAndFunctions(unittest.TestCase):
    def test_newstyle_mro(self):
        
        class A(object):    pass
        class B(A): pass
        class C(A): pass
        class D(B, C): pass

        expected = (D, B, C, A, object)
        got = inspect.getmro(D)
        self.assertEqual(expected, got)

    def assertArgSpecEquals(self, routine, args_e, varargs_e=None,
                            varkw_e=None, defaults_e=None, formatted=None):
        args, varargs, varkw, defaults = inspect.getargspec(routine)
        self.assertEqual(args, args_e)
        self.assertEqual(varargs, varargs_e)
        self.assertEqual(varkw, varkw_e)
        self.assertEqual(defaults, defaults_e)
        if formatted is not None:
            self.assertEqual(inspect.formatargspec(args, varargs, varkw, defaults),
                             formatted)

    def assertFullArgSpecEquals(self, routine, args_e, varargs_e=None,
                                    varkw_e=None, defaults_e=None,
                                    kwonlyargs_e=[], kwonlydefaults_e=None,
                                    ann_e={}, formatted=None):
        args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, ann = \
            inspect.getfullargspec(routine)
        self.assertEqual(args, args_e)
        self.assertEqual(varargs, varargs_e)
        self.assertEqual(varkw, varkw_e)
        self.assertEqual(defaults, defaults_e)
        self.assertEqual(kwonlyargs, kwonlyargs_e)
        self.assertEqual(kwonlydefaults, kwonlydefaults_e)
        self.assertEqual(ann, ann_e)
        if formatted is not None:
            self.assertEqual(inspect.formatargspec(args, varargs, varkw, defaults,
                                                    kwonlyargs, kwonlydefaults, ann),
                             formatted)

    def test_getargspec(self):
        self.assertArgSpecEquals(mod.eggs, ['x', 'y'], formatted='(x, y)')

        self.assertArgSpecEquals(mod.spam,
                                 ['a', 'b', 'c', 'd', 'e', 'f'],
                                 'g', 'h', (3, 4, 5),
                                 '(a, b, c, d=3, e=4, f=5, *g, **h)')

        self.assertRaises(ValueError, self.assertArgSpecEquals,
                          mod2.keyworded, [])

        self.assertRaises(ValueError, self.assertArgSpecEquals,
                          mod2.annotated, [])
        self.assertRaises(ValueError, self.assertArgSpecEquals,
                          mod2.keyword_only_arg, [])


    def test_getfullargspec(self):
        self.assertFullArgSpecEquals(mod2.keyworded, [], varargs_e='arg1',
                                     kwonlyargs_e=['arg2'],
                                     kwonlydefaults_e={'arg2':1},
                                     formatted='(*arg1, arg2=1)')

        self.assertFullArgSpecEquals(mod2.annotated, ['arg1'],
                                     ann_e={'arg1' : list},
                                     formatted='(arg1: list)')
        self.assertFullArgSpecEquals(mod2.keyword_only_arg, [],
                                     kwonlyargs_e=['arg'],
                                     formatted='(*, arg)')

    def test_argspec_api_ignores_wrapped(self):
        
        @functools.wraps(mod.spam)
        def ham(x, y):
            pass
        
        self.assertArgSpecEquals(ham, ['x', 'y'], formatted='(x, y)')
        self.assertFullArgSpecEquals(ham, ['x', 'y'], formatted='(x, y)')
        self.assertFullArgSpecEquals(functools.partial(ham),
                                     ['x', 'y'], formatted='(x, y)')
        
        def check_method(f):
            self.assertArgSpecEquals(f, ['self', 'x', 'y'],
                                        formatted='(self, x, y)')
        class C:
            @functools.wraps(mod.spam)
            def ham(self, x, y):
                pass
            pham = functools.partialmethod(ham)
            @functools.wraps(mod.spam)
            def __call__(self, x, y):
                pass
        check_method(C())
        check_method(C.ham)
        check_method(C().ham)
        check_method(C.pham)
        check_method(C().pham)

        class C_new:
            @functools.wraps(mod.spam)
            def __new__(self, x, y):
                pass
        check_method(C_new)

        class C_init:
            @functools.wraps(mod.spam)
            def __init__(self, x, y):
                pass
        check_method(C_init)

    def test_getfullargspec_signature_attr(self):
        def test():
            pass
        spam_param = inspect.Parameter('spam', inspect.Parameter.POSITIONAL_ONLY)
        test.__signature__ = inspect.Signature(parameters=(spam_param,))

        self.assertFullArgSpecEquals(test, args_e=['spam'], formatted='(spam)')

    def test_getfullargspec_signature_annos(self):
        def test(a:'spam') -> 'ham': pass
        spec = inspect.getfullargspec(test)
        self.assertEqual(test.__annotations__, spec.annotations)

        def test(): pass
        spec = inspect.getfullargspec(test)
        self.assertEqual(test.__annotations__, spec.annotations)

    @unittest.skipIf(MISSING_C_DOCSTRINGS,
                     "Signature information for builtins requires docstrings")
    def test_getfullargspec_builtin_methods(self):
        self.assertFullArgSpecEquals(_pickle.Pickler.dump,
                                     args_e=['self', 'obj'], formatted='(self, obj)')

        self.assertFullArgSpecEquals(_pickle.Pickler(io.BytesIO()).dump,
                                     args_e=['self', 'obj'], formatted='(self, obj)')

        self.assertFullArgSpecEquals(
             os.stat,
             args_e=['path'],
             kwonlyargs_e=['dir_fd', 'follow_symlinks'],
             kwonlydefaults_e={'dir_fd': None, 'follow_symlinks': True},
             formatted='(path, *, dir_fd=None, follow_symlinks=True)')

    @cpython_only
    @unittest.skipIf(MISSING_C_DOCSTRINGS,
                     "Signature information for builtins requires docstrings")
    def test_getfullagrspec_builtin_func(self):
        import _testcapi
        builtin = _testcapi.docstring_with_signature_with_defaults
        spec = inspect.getfullargspec(builtin)
        self.assertEqual(spec.defaults[0], 'avocado')

    @cpython_only
    @unittest.skipIf(MISSING_C_DOCSTRINGS,
                     "Signature information for builtins requires docstrings")
    def test_getfullagrspec_builtin_func_no_signature(self):
        import _testcapi
        builtin = _testcapi.docstring_no_signature
        with self.assertRaises(TypeError):
            inspect.getfullargspec(builtin)

    def test_getargspec_method(self):
        class A(object):
            def m(self):
                pass
        self.assertArgSpecEquals(A.m, ['self'])

    def test_classify_newstyle(self):
        class A(object):

            def s(): pass
            s = staticmethod(s)

            def c(cls): pass
            c = classmethod(c)

            def getp(self): pass
            p = property(getp)

            def m(self): pass

            def m1(self): pass

            datablob = '1'

            dd = _BrokenDataDescriptor()
            md = _BrokenMethodDescriptor()

        attrs = attrs_wo_objs(A)

        self.assertIn(('__new__', 'method', object), attrs, 'missing __new__')
        self.assertIn(('__init__', 'method', object), attrs, 'missing __init__')

        self.assertIn(('s', 'static method', A), attrs, 'missing static method')
        self.assertIn(('c', 'class method', A), attrs, 'missing class method')
        self.assertIn(('p', 'property', A), attrs, 'missing property')
        self.assertIn(('m', 'method', A), attrs,
                      'missing plain method: %r' % attrs)
        self.assertIn(('m1', 'method', A), attrs, 'missing plain method')
        self.assertIn(('datablob', 'data', A), attrs, 'missing data')
        self.assertIn(('md', 'method', A), attrs, 'missing method descriptor')
        self.assertIn(('dd', 'data', A), attrs, 'missing data descriptor')

        class B(A):

            def m(self): pass

        attrs = attrs_wo_objs(B)
        self.assertIn(('s', 'static method', A), attrs, 'missing static method')
        self.assertIn(('c', 'class method', A), attrs, 'missing class method')
        self.assertIn(('p', 'property', A), attrs, 'missing property')
        self.assertIn(('m', 'method', B), attrs, 'missing plain method')
        self.assertIn(('m1', 'method', A), attrs, 'missing plain method')
        self.assertIn(('datablob', 'data', A), attrs, 'missing data')
        self.assertIn(('md', 'method', A), attrs, 'missing method descriptor')
        self.assertIn(('dd', 'data', A), attrs, 'missing data descriptor')


        class C(A):

            def m(self): pass
            def c(self): pass

        attrs = attrs_wo_objs(C)
        self.assertIn(('s', 'static method', A), attrs, 'missing static method')
        self.assertIn(('c', 'method', C), attrs, 'missing plain method')
        self.assertIn(('p', 'property', A), attrs, 'missing property')
        self.assertIn(('m', 'method', C), attrs, 'missing plain method')
        self.assertIn(('m1', 'method', A), attrs, 'missing plain method')
        self.assertIn(('datablob', 'data', A), attrs, 'missing data')
        self.assertIn(('md', 'method', A), attrs, 'missing method descriptor')
        self.assertIn(('dd', 'data', A), attrs, 'missing data descriptor')

        class D(B, C):

            def m1(self): pass

        attrs = attrs_wo_objs(D)
        self.assertIn(('s', 'static method', A), attrs, 'missing static method')
        self.assertIn(('c', 'method', C), attrs, 'missing plain method')
        self.assertIn(('p', 'property', A), attrs, 'missing property')
        self.assertIn(('m', 'method', B), attrs, 'missing plain method')
        self.assertIn(('m1', 'method', D), attrs, 'missing plain method')
        self.assertIn(('datablob', 'data', A), attrs, 'missing data')
        self.assertIn(('md', 'method', A), attrs, 'missing method descriptor')
        self.assertIn(('dd', 'data', A), attrs, 'missing data descriptor')

    def test_classify_builtin_types(self):
        
        
        for name in dir(__builtins__):
            builtin = getattr(__builtins__, name)
            if isinstance(builtin, type):
                inspect.classify_class_attrs(builtin)

    def test_classify_DynamicClassAttribute(self):
        class Meta(type):
            def __getattr__(self, name):
                if name == 'ham':
                    return 'spam'
                return super().__getattr__(name)
        class VA(metaclass=Meta):
            @types.DynamicClassAttribute
            def ham(self):
                return 'eggs'
        should_find_dca = inspect.Attribute('ham', 'data', VA, VA.__dict__['ham'])
        self.assertIn(should_find_dca, inspect.classify_class_attrs(VA))
        should_find_ga = inspect.Attribute('ham', 'data', Meta, 'spam')
        self.assertIn(should_find_ga, inspect.classify_class_attrs(VA))

    def test_classify_overrides_bool(self):
        class NoBool(object):
            def __eq__(self, other):
                return NoBool()

            def __bool__(self):
                raise NotImplementedError(
                    "This object does not specify a boolean value")

        class HasNB(object):
            dd = NoBool()

        should_find_attr = inspect.Attribute('dd', 'data', HasNB, HasNB.dd)
        self.assertIn(should_find_attr, inspect.classify_class_attrs(HasNB))

    def test_classify_metaclass_class_attribute(self):
        class Meta(type):
            fish = 'slap'
            def __dir__(self):
                return ['__class__', '__module__', '__name__', 'fish']
        class Class(metaclass=Meta):
            pass
        should_find = inspect.Attribute('fish', 'data', Meta, 'slap')
        self.assertIn(should_find, inspect.classify_class_attrs(Class))

    def test_classify_VirtualAttribute(self):
        class Meta(type):
            def __dir__(cls):
                return ['__class__', '__module__', '__name__', 'BOOM']
            def __getattr__(self, name):
                if name =='BOOM':
                    return 42
                return super().__getattr(name)
        class Class(metaclass=Meta):
            pass
        should_find = inspect.Attribute('BOOM', 'data', Meta, 42)
        self.assertIn(should_find, inspect.classify_class_attrs(Class))

    def test_classify_VirtualAttribute_multi_classes(self):
        class Meta1(type):
            def __dir__(cls):
                return ['__class__', '__module__', '__name__', 'one']
            def __getattr__(self, name):
                if name =='one':
                    return 1
                return super().__getattr__(name)
        class Meta2(type):
            def __dir__(cls):
                return ['__class__', '__module__', '__name__', 'two']
            def __getattr__(self, name):
                if name =='two':
                    return 2
                return super().__getattr__(name)
        class Meta3(Meta1, Meta2):
            def __dir__(cls):
                return list(sorted(set(['__class__', '__module__', '__name__', 'three'] +
                    Meta1.__dir__(cls) + Meta2.__dir__(cls))))
            def __getattr__(self, name):
                if name =='three':
                    return 3
                return super().__getattr__(name)
        class Class1(metaclass=Meta1):
            pass
        class Class2(Class1, metaclass=Meta3):
            pass

        should_find1 = inspect.Attribute('one', 'data', Meta1, 1)
        should_find2 = inspect.Attribute('two', 'data', Meta2, 2)
        should_find3 = inspect.Attribute('three', 'data', Meta3, 3)
        cca = inspect.classify_class_attrs(Class2)
        for sf in (should_find1, should_find2, should_find3):
            self.assertIn(sf, cca)

    def test_classify_class_attrs_with_buggy_dir(self):
        class M(type):
            def __dir__(cls):
                return ['__class__', '__name__', 'missing']
        class C(metaclass=M):
            pass
        attrs = [a[0] for a in inspect.classify_class_attrs(C)]
        self.assertNotIn('missing', attrs)

    def test_getmembers_descriptors(self):
        class A(object):
            dd = _BrokenDataDescriptor()
            md = _BrokenMethodDescriptor()

        def pred_wrapper(pred):
            
            
            class Empty(object):
                pass
            def wrapped(x):
                if '__name__' in dir(x) and hasattr(Empty, x.__name__):
                    return False
                return pred(x)
            return wrapped

        ismethoddescriptor = pred_wrapper(inspect.ismethoddescriptor)
        isdatadescriptor = pred_wrapper(inspect.isdatadescriptor)

        self.assertEqual(inspect.getmembers(A, ismethoddescriptor),
            [('md', A.__dict__['md'])])
        self.assertEqual(inspect.getmembers(A, isdatadescriptor),
            [('dd', A.__dict__['dd'])])

        class B(A):
            pass

        self.assertEqual(inspect.getmembers(B, ismethoddescriptor),
            [('md', A.__dict__['md'])])
        self.assertEqual(inspect.getmembers(B, isdatadescriptor),
            [('dd', A.__dict__['dd'])])

    def test_getmembers_method(self):
        class B:
            def f(self):
                pass

        self.assertIn(('f', B.f), inspect.getmembers(B))
        self.assertNotIn(('f', B.f), inspect.getmembers(B, inspect.ismethod))
        b = B()
        self.assertIn(('f', b.f), inspect.getmembers(b))
        self.assertIn(('f', b.f), inspect.getmembers(b, inspect.ismethod))

    def test_getmembers_VirtualAttribute(self):
        class M(type):
            def __getattr__(cls, name):
                if name == 'eggs':
                    return 'scrambled'
                return super().__getattr__(name)
        class A(metaclass=M):
            @types.DynamicClassAttribute
            def eggs(self):
                return 'spam'
        self.assertIn(('eggs', 'scrambled'), inspect.getmembers(A))
        self.assertIn(('eggs', 'spam'), inspect.getmembers(A()))

    def test_getmembers_with_buggy_dir(self):
        class M(type):
            def __dir__(cls):
                return ['__class__', '__name__', 'missing']
        class C(metaclass=M):
            pass
        attrs = [a[0] for a in inspect.getmembers(C)]
        self.assertNotIn('missing', attrs)


_global_ref = object()
class TestGetClosureVars(unittest.TestCase):

    def test_name_resolution(self):
        
        def f(nonlocal_ref):
            def g(local_ref):
                print(local_ref, nonlocal_ref, _global_ref, unbound_ref)
            return g
        _arg = object()
        nonlocal_vars = {"nonlocal_ref": _arg}
        global_vars = {"_global_ref": _global_ref}
        builtin_vars = {"print": print}
        unbound_names = {"unbound_ref"}
        expected = inspect.ClosureVars(nonlocal_vars, global_vars,
                                       builtin_vars, unbound_names)
        self.assertEqual(inspect.getclosurevars(f(_arg)), expected)

    def test_generator_closure(self):
        def f(nonlocal_ref):
            def g(local_ref):
                print(local_ref, nonlocal_ref, _global_ref, unbound_ref)
                yield
            return g
        _arg = object()
        nonlocal_vars = {"nonlocal_ref": _arg}
        global_vars = {"_global_ref": _global_ref}
        builtin_vars = {"print": print}
        unbound_names = {"unbound_ref"}
        expected = inspect.ClosureVars(nonlocal_vars, global_vars,
                                       builtin_vars, unbound_names)
        self.assertEqual(inspect.getclosurevars(f(_arg)), expected)

    def test_method_closure(self):
        class C:
            def f(self, nonlocal_ref):
                def g(local_ref):
                    print(local_ref, nonlocal_ref, _global_ref, unbound_ref)
                return g
        _arg = object()
        nonlocal_vars = {"nonlocal_ref": _arg}
        global_vars = {"_global_ref": _global_ref}
        builtin_vars = {"print": print}
        unbound_names = {"unbound_ref"}
        expected = inspect.ClosureVars(nonlocal_vars, global_vars,
                                       builtin_vars, unbound_names)
        self.assertEqual(inspect.getclosurevars(C().f(_arg)), expected)

    def test_nonlocal_vars(self):
        
        def _nonlocal_vars(f):
            return inspect.getclosurevars(f).nonlocals

        def make_adder(x):
            def add(y):
                return x + y
            return add

        def curry(func, arg1):
            return lambda arg2: func(arg1, arg2)

        def less_than(a, b):
            return a < b

        
        def Y(le):
            def g(f):
                return le(lambda x: f(f)(x))
            Y.g_ref = g
            return g(g)

        def check_y_combinator(func):
            self.assertEqual(_nonlocal_vars(func), {'f': Y.g_ref})

        inc = make_adder(1)
        add_two = make_adder(2)
        greater_than_five = curry(less_than, 5)

        self.assertEqual(_nonlocal_vars(inc), {'x': 1})
        self.assertEqual(_nonlocal_vars(add_two), {'x': 2})
        self.assertEqual(_nonlocal_vars(greater_than_five),
                         {'arg1': 5, 'func': less_than})
        self.assertEqual(_nonlocal_vars((lambda x: lambda y: x + y)(3)),
                         {'x': 3})
        Y(check_y_combinator)

    def test_getclosurevars_empty(self):
        def foo(): pass
        _empty = inspect.ClosureVars({}, {}, {}, set())
        self.assertEqual(inspect.getclosurevars(lambda: True), _empty)
        self.assertEqual(inspect.getclosurevars(foo), _empty)

    def test_getclosurevars_error(self):
        class T: pass
        self.assertRaises(TypeError, inspect.getclosurevars, 1)
        self.assertRaises(TypeError, inspect.getclosurevars, list)
        self.assertRaises(TypeError, inspect.getclosurevars, {})

    def _private_globals(self):
        code = """def f(): print(path)"""
        ns = {}
        exec(code, ns)
        return ns["f"], ns

    def test_builtins_fallback(self):
        f, ns = self._private_globals()
        ns.pop("__builtins__", None)
        expected = inspect.ClosureVars({}, {}, {"print":print}, {"path"})
        self.assertEqual(inspect.getclosurevars(f), expected)

    def test_builtins_as_dict(self):
        f, ns = self._private_globals()
        ns["__builtins__"] = {"path":1}
        expected = inspect.ClosureVars({}, {}, {"path":1}, {"print"})
        self.assertEqual(inspect.getclosurevars(f), expected)

    def test_builtins_as_module(self):
        f, ns = self._private_globals()
        ns["__builtins__"] = os
        expected = inspect.ClosureVars({}, {}, {"path":os.path}, {"print"})
        self.assertEqual(inspect.getclosurevars(f), expected)


class TestGetcallargsFunctions(unittest.TestCase):

    def assertEqualCallArgs(self, func, call_params_string, locs=None):
        locs = dict(locs or {}, func=func)
        r1 = eval('func(%s)' % call_params_string, None, locs)
        r2 = eval('inspect.getcallargs(func, %s)' % call_params_string, None,
                  locs)
        self.assertEqual(r1, r2)

    def assertEqualException(self, func, call_param_string, locs=None):
        locs = dict(locs or {}, func=func)
        try:
            eval('func(%s)' % call_param_string, None, locs)
        except Exception as e:
            ex1 = e
        else:
            self.fail('Exception not raised')
        try:
            eval('inspect.getcallargs(func, %s)' % call_param_string, None,
                 locs)
        except Exception as e:
            ex2 = e
        else:
            self.fail('Exception not raised')
        self.assertIs(type(ex1), type(ex2))
        self.assertEqual(str(ex1), str(ex2))
        del ex1, ex2

    def makeCallable(self, signature):
        """Create a function that returns its locals()"""
        code = "lambda %s: locals()"
        return eval(code % signature)

    def test_plain(self):
        f = self.makeCallable('a, b=1')
        self.assertEqualCallArgs(f, '2')
        self.assertEqualCallArgs(f, '2, 3')
        self.assertEqualCallArgs(f, 'a=2')
        self.assertEqualCallArgs(f, 'b=3, a=2')
        self.assertEqualCallArgs(f, '2, b=3')
        
        self.assertEqualCallArgs(f, '*(2,)')
        self.assertEqualCallArgs(f, '*[2]')
        self.assertEqualCallArgs(f, '*(2, 3)')
        self.assertEqualCallArgs(f, '*[2, 3]')
        self.assertEqualCallArgs(f, '**{"a":2}')
        self.assertEqualCallArgs(f, 'b=3, **{"a":2}')
        self.assertEqualCallArgs(f, '2, **{"b":3}')
        self.assertEqualCallArgs(f, '**{"b":3, "a":2}')
        
        self.assertEqualCallArgs(f, '*collections.UserList([2])')
        self.assertEqualCallArgs(f, '*collections.UserList([2, 3])')
        self.assertEqualCallArgs(f, '**collections.UserDict(a=2)')
        self.assertEqualCallArgs(f, '2, **collections.UserDict(b=3)')
        self.assertEqualCallArgs(f, 'b=2, **collections.UserDict(a=3)')

    def test_varargs(self):
        f = self.makeCallable('a, b=1, *c')
        self.assertEqualCallArgs(f, '2')
        self.assertEqualCallArgs(f, '2, 3')
        self.assertEqualCallArgs(f, '2, 3, 4')
        self.assertEqualCallArgs(f, '*(2,3,4)')
        self.assertEqualCallArgs(f, '2, *[3,4]')
        self.assertEqualCallArgs(f, '2, 3, *collections.UserList([4])')

    def test_varkw(self):
        f = self.makeCallable('a, b=1, **c')
        self.assertEqualCallArgs(f, 'a=2')
        self.assertEqualCallArgs(f, '2, b=3, c=4')
        self.assertEqualCallArgs(f, 'b=3, a=2, c=4')
        self.assertEqualCallArgs(f, 'c=4, **{"a":2, "b":3}')
        self.assertEqualCallArgs(f, '2, c=4, **{"b":3}')
        self.assertEqualCallArgs(f, 'b=2, **{"a":3, "c":4}')
        self.assertEqualCallArgs(f, '**collections.UserDict(a=2, b=3, c=4)')
        self.assertEqualCallArgs(f, '2, c=4, **collections.UserDict(b=3)')
        self.assertEqualCallArgs(f, 'b=2, **collections.UserDict(a=3, c=4)')

    def test_varkw_only(self):
        
        f = self.makeCallable('**c')
        self.assertEqualCallArgs(f, '')
        self.assertEqualCallArgs(f, 'a=1')
        self.assertEqualCallArgs(f, 'a=1, b=2')
        self.assertEqualCallArgs(f, 'c=3, **{"a": 1, "b": 2}')
        self.assertEqualCallArgs(f, '**collections.UserDict(a=1, b=2)')
        self.assertEqualCallArgs(f, 'c=3, **collections.UserDict(a=1, b=2)')

    def test_keyword_only(self):
        f = self.makeCallable('a=3, *, c, d=2')
        self.assertEqualCallArgs(f, 'c=3')
        self.assertEqualCallArgs(f, 'c=3, a=3')
        self.assertEqualCallArgs(f, 'a=2, c=4')
        self.assertEqualCallArgs(f, '4, c=4')
        self.assertEqualException(f, '')
        self.assertEqualException(f, '3')
        self.assertEqualException(f, 'a=3')
        self.assertEqualException(f, 'd=4')

        f = self.makeCallable('*, c, d=2')
        self.assertEqualCallArgs(f, 'c=3')
        self.assertEqualCallArgs(f, 'c=3, d=4')
        self.assertEqualCallArgs(f, 'd=4, c=3')

    def test_multiple_features(self):
        f = self.makeCallable('a, b=2, *f, **g')
        self.assertEqualCallArgs(f, '2, 3, 7')
        self.assertEqualCallArgs(f, '2, 3, x=8')
        self.assertEqualCallArgs(f, '2, 3, x=8, *[(4,[5,6]), 7]')
        self.assertEqualCallArgs(f, '2, x=8, *[3, (4,[5,6]), 7], y=9')
        self.assertEqualCallArgs(f, 'x=8, *[2, 3, (4,[5,6])], y=9')
        self.assertEqualCallArgs(f, 'x=8, *collections.UserList('
                                 '[2, 3, (4,[5,6])]), **{"y":9, "z":10}')
        self.assertEqualCallArgs(f, '2, x=8, *collections.UserList([3, '
                                 '(4,[5,6])]), **collections.UserDict('
                                 'y=9, z=10)')

        f = self.makeCallable('a, b=2, *f, x, y=99, **g')
        self.assertEqualCallArgs(f, '2, 3, x=8')
        self.assertEqualCallArgs(f, '2, 3, x=8, *[(4,[5,6]), 7]')
        self.assertEqualCallArgs(f, '2, x=8, *[3, (4,[5,6]), 7], y=9, z=10')
        self.assertEqualCallArgs(f, 'x=8, *[2, 3, (4,[5,6])], y=9, z=10')
        self.assertEqualCallArgs(f, 'x=8, *collections.UserList('
                                 '[2, 3, (4,[5,6])]), q=0, **{"y":9, "z":10}')
        self.assertEqualCallArgs(f, '2, x=8, *collections.UserList([3, '
                                 '(4,[5,6])]), q=0, **collections.UserDict('
                                 'y=9, z=10)')

    def test_errors(self):
        f0 = self.makeCallable('')
        f1 = self.makeCallable('a, b')
        f2 = self.makeCallable('a, b=1')
        
        self.assertEqualException(f0, '1')
        self.assertEqualException(f0, 'x=1')
        self.assertEqualException(f0, '1,x=1')
        
        self.assertEqualException(f1, '')
        self.assertEqualException(f1, '1')
        self.assertEqualException(f1, 'a=2')
        self.assertEqualException(f1, 'b=3')
        
        self.assertEqualException(f2, '')
        self.assertEqualException(f2, 'b=3')
        for f in f1, f2:
            
            self.assertEqualException(f, '2, 3, 4')
            self.assertEqualException(f, '1, 2, 3, a=1')
            self.assertEqualException(f, '2, 3, 4, c=5')
            
            
            
            self.assertEqualException(f, 'c=2')
            self.assertEqualException(f, '2, c=3')
            self.assertEqualException(f, '2, 3, c=4')
            self.assertEqualException(f, '2, c=4, b=3')
            self.assertEqualException(f, '**{u"\u03c0\u03b9": 4}')
            
            self.assertEqualException(f, '1, a=2')
            self.assertEqualException(f, '1, **{"a":2}')
            self.assertEqualException(f, '1, 2, b=3')
            
            
            
            
        
        f3 = self.makeCallable('**c')
        self.assertEqualException(f3, '1, 2')
        self.assertEqualException(f3, '1, 2, a=1, b=2')
        f4 = self.makeCallable('*, a, b=0')
        self.assertEqualException(f3, '1, 2')
        self.assertEqualException(f3, '1, 2, a=1, b=2')

        
        
        def f5(*, a): pass
        with self.assertRaisesRegex(TypeError,
                                    'missing 1 required keyword-only'):
            inspect.getcallargs(f5)


        
        def f6(a, b, c):
            pass
        with self.assertRaisesRegex(TypeError, "'a', 'b' and 'c'"):
            inspect.getcallargs(f6)

class TestGetcallargsMethods(TestGetcallargsFunctions):

    def setUp(self):
        class Foo(object):
            pass
        self.cls = Foo
        self.inst = Foo()

    def makeCallable(self, signature):
        assert 'self' not in signature
        mk = super(TestGetcallargsMethods, self).makeCallable
        self.cls.method = mk('self, ' + signature)
        return self.inst.method

class TestGetcallargsUnboundMethods(TestGetcallargsMethods):

    def makeCallable(self, signature):
        super(TestGetcallargsUnboundMethods, self).makeCallable(signature)
        return self.cls.method

    def assertEqualCallArgs(self, func, call_params_string, locs=None):
        return super(TestGetcallargsUnboundMethods, self).assertEqualCallArgs(
            *self._getAssertEqualParams(func, call_params_string, locs))

    def assertEqualException(self, func, call_params_string, locs=None):
        return super(TestGetcallargsUnboundMethods, self).assertEqualException(
            *self._getAssertEqualParams(func, call_params_string, locs))

    def _getAssertEqualParams(self, func, call_params_string, locs=None):
        assert 'inst' not in call_params_string
        locs = dict(locs or {}, inst=self.inst)
        return (func, 'inst,' + call_params_string, locs)


class TestGetattrStatic(unittest.TestCase):

    def test_basic(self):
        class Thing(object):
            x = object()

        thing = Thing()
        self.assertEqual(inspect.getattr_static(thing, 'x'), Thing.x)
        self.assertEqual(inspect.getattr_static(thing, 'x', None), Thing.x)
        with self.assertRaises(AttributeError):
            inspect.getattr_static(thing, 'y')

        self.assertEqual(inspect.getattr_static(thing, 'y', 3), 3)

    def test_inherited(self):
        class Thing(object):
            x = object()
        class OtherThing(Thing):
            pass

        something = OtherThing()
        self.assertEqual(inspect.getattr_static(something, 'x'), Thing.x)

    def test_instance_attr(self):
        class Thing(object):
            x = 2
            def __init__(self, x):
                self.x = x
        thing = Thing(3)
        self.assertEqual(inspect.getattr_static(thing, 'x'), 3)
        del thing.x
        self.assertEqual(inspect.getattr_static(thing, 'x'), 2)

    def test_property(self):
        class Thing(object):
            @property
            def x(self):
                raise AttributeError("I'm pretending not to exist")
        thing = Thing()
        self.assertEqual(inspect.getattr_static(thing, 'x'), Thing.x)

    def test_descriptor_raises_AttributeError(self):
        class descriptor(object):
            def __get__(*_):
                raise AttributeError("I'm pretending not to exist")
        desc = descriptor()
        class Thing(object):
            x = desc
        thing = Thing()
        self.assertEqual(inspect.getattr_static(thing, 'x'), desc)

    def test_classAttribute(self):
        class Thing(object):
            x = object()

        self.assertEqual(inspect.getattr_static(Thing, 'x'), Thing.x)

    def test_classVirtualAttribute(self):
        class Thing(object):
            @types.DynamicClassAttribute
            def x(self):
                return self._x
            _x = object()

        self.assertEqual(inspect.getattr_static(Thing, 'x'), Thing.__dict__['x'])

    def test_inherited_classattribute(self):
        class Thing(object):
            x = object()
        class OtherThing(Thing):
            pass

        self.assertEqual(inspect.getattr_static(OtherThing, 'x'), Thing.x)

    def test_slots(self):
        class Thing(object):
            y = 'bar'
            __slots__ = ['x']
            def __init__(self):
                self.x = 'foo'
        thing = Thing()
        self.assertEqual(inspect.getattr_static(thing, 'x'), Thing.x)
        self.assertEqual(inspect.getattr_static(thing, 'y'), 'bar')

        del thing.x
        self.assertEqual(inspect.getattr_static(thing, 'x'), Thing.x)

    def test_metaclass(self):
        class meta(type):
            attr = 'foo'
        class Thing(object, metaclass=meta):
            pass
        self.assertEqual(inspect.getattr_static(Thing, 'attr'), 'foo')

        class sub(meta):
            pass
        class OtherThing(object, metaclass=sub):
            x = 3
        self.assertEqual(inspect.getattr_static(OtherThing, 'attr'), 'foo')

        class OtherOtherThing(OtherThing):
            pass
        
        self.assertEqual(inspect.getattr_static(OtherOtherThing, 'x'), 3)

    def test_no_dict_no_slots(self):
        self.assertEqual(inspect.getattr_static(1, 'foo', None), None)
        self.assertNotEqual(inspect.getattr_static('foo', 'lower'), None)

    def test_no_dict_no_slots_instance_member(self):
        
        with open(__file__) as handle:
            self.assertEqual(inspect.getattr_static(handle, 'name'), type(handle).name)

    def test_inherited_slots(self):
        
        class Thing(object):
            __slots__ = ['x']
            def __init__(self):
                self.x = 'foo'

        class OtherThing(Thing):
            pass
        
        
        self.assertEqual(inspect.getattr_static(OtherThing(), 'x'), Thing.x)

    def test_descriptor(self):
        class descriptor(object):
            def __get__(self, instance, owner):
                return 3
        class Foo(object):
            d = descriptor()

        foo = Foo()

        
        foo.__dict__['d'] = 1
        self.assertEqual(inspect.getattr_static(foo, 'd'), 1)

        
        
        descriptor.__set__ = lambda s, i, v: None
        self.assertEqual(inspect.getattr_static(foo, 'd'), Foo.__dict__['d'])


    def test_metaclass_with_descriptor(self):
        class descriptor(object):
            def __get__(self, instance, owner):
                return 3
        class meta(type):
            d = descriptor()
        class Thing(object, metaclass=meta):
            pass
        self.assertEqual(inspect.getattr_static(Thing, 'd'), meta.__dict__['d'])


    def test_class_as_property(self):
        class Base(object):
            foo = 3

        class Something(Base):
            executed = False
            @property
            def __class__(self):
                self.executed = True
                return object

        instance = Something()
        self.assertEqual(inspect.getattr_static(instance, 'foo'), 3)
        self.assertFalse(instance.executed)
        self.assertEqual(inspect.getattr_static(Something, 'foo'), 3)

    def test_mro_as_property(self):
        class Meta(type):
            @property
            def __mro__(self):
                return (object,)

        class Base(object):
            foo = 3

        class Something(Base, metaclass=Meta):
            pass

        self.assertEqual(inspect.getattr_static(Something(), 'foo'), 3)
        self.assertEqual(inspect.getattr_static(Something, 'foo'), 3)

    def test_dict_as_property(self):
        test = self
        test.called = False

        class Foo(dict):
            a = 3
            @property
            def __dict__(self):
                test.called = True
                return {}

        foo = Foo()
        foo.a = 4
        self.assertEqual(inspect.getattr_static(foo, 'a'), 3)
        self.assertFalse(test.called)

    def test_custom_object_dict(self):
        test = self
        test.called = False

        class Custom(dict):
            def get(self, key, default=None):
                test.called = True
                super().get(key, default)

        class Foo(object):
            a = 3
        foo = Foo()
        foo.__dict__ = Custom()
        self.assertEqual(inspect.getattr_static(foo, 'a'), 3)
        self.assertFalse(test.called)

    def test_metaclass_dict_as_property(self):
        class Meta(type):
            @property
            def __dict__(self):
                self.executed = True

        class Thing(metaclass=Meta):
            executed = False

            def __init__(self):
                self.spam = 42

        instance = Thing()
        self.assertEqual(inspect.getattr_static(instance, "spam"), 42)
        self.assertFalse(Thing.executed)

    def test_module(self):
        sentinel = object()
        self.assertIsNot(inspect.getattr_static(sys, "version", sentinel),
                         sentinel)

    def test_metaclass_with_metaclass_with_dict_as_property(self):
        class MetaMeta(type):
            @property
            def __dict__(self):
                self.executed = True
                return dict(spam=42)

        class Meta(type, metaclass=MetaMeta):
            executed = False

        class Thing(metaclass=Meta):
            pass

        with self.assertRaises(AttributeError):
            inspect.getattr_static(Thing, "spam")
        self.assertFalse(Thing.executed)

class TestGetGeneratorState(unittest.TestCase):

    def setUp(self):
        def number_generator():
            for number in range(5):
                yield number
        self.generator = number_generator()

    def _generatorstate(self):
        return inspect.getgeneratorstate(self.generator)

    def test_created(self):
        self.assertEqual(self._generatorstate(), inspect.GEN_CREATED)

    def test_suspended(self):
        next(self.generator)
        self.assertEqual(self._generatorstate(), inspect.GEN_SUSPENDED)

    def test_closed_after_exhaustion(self):
        for i in self.generator:
            pass
        self.assertEqual(self._generatorstate(), inspect.GEN_CLOSED)

    def test_closed_after_immediate_exception(self):
        with self.assertRaises(RuntimeError):
            self.generator.throw(RuntimeError)
        self.assertEqual(self._generatorstate(), inspect.GEN_CLOSED)

    def test_running(self):
        
        
        
        
        def running_check_generator():
            for number in range(5):
                self.assertEqual(self._generatorstate(), inspect.GEN_RUNNING)
                yield number
                self.assertEqual(self._generatorstate(), inspect.GEN_RUNNING)
        self.generator = running_check_generator()
        
        next(self.generator)
        
        next(self.generator)

    def test_easy_debugging(self):
        
        names = 'GEN_CREATED GEN_RUNNING GEN_SUSPENDED GEN_CLOSED'.split()
        for name in names:
            state = getattr(inspect, name)
            self.assertIn(name, repr(state))
            self.assertIn(name, str(state))

    def test_getgeneratorlocals(self):
        def each(lst, a=None):
            b=(1, 2, 3)
            for v in lst:
                if v == 3:
                    c = 12
                yield v

        numbers = each([1, 2, 3])
        self.assertEqual(inspect.getgeneratorlocals(numbers),
                         {'a': None, 'lst': [1, 2, 3]})
        next(numbers)
        self.assertEqual(inspect.getgeneratorlocals(numbers),
                         {'a': None, 'lst': [1, 2, 3], 'v': 1,
                          'b': (1, 2, 3)})
        next(numbers)
        self.assertEqual(inspect.getgeneratorlocals(numbers),
                         {'a': None, 'lst': [1, 2, 3], 'v': 2,
                          'b': (1, 2, 3)})
        next(numbers)
        self.assertEqual(inspect.getgeneratorlocals(numbers),
                         {'a': None, 'lst': [1, 2, 3], 'v': 3,
                          'b': (1, 2, 3), 'c': 12})
        try:
            next(numbers)
        except StopIteration:
            pass
        self.assertEqual(inspect.getgeneratorlocals(numbers), {})

    def test_getgeneratorlocals_empty(self):
        def yield_one():
            yield 1
        one = yield_one()
        self.assertEqual(inspect.getgeneratorlocals(one), {})
        try:
            next(one)
        except StopIteration:
            pass
        self.assertEqual(inspect.getgeneratorlocals(one), {})

    def test_getgeneratorlocals_error(self):
        self.assertRaises(TypeError, inspect.getgeneratorlocals, 1)
        self.assertRaises(TypeError, inspect.getgeneratorlocals, lambda x: True)
        self.assertRaises(TypeError, inspect.getgeneratorlocals, set)
        self.assertRaises(TypeError, inspect.getgeneratorlocals, (2,3))


class TestSignatureObject(unittest.TestCase):
    @staticmethod
    def signature(func):
        sig = inspect.signature(func)
        return (tuple((param.name,
                       (... if param.default is param.empty else param.default),
                       (... if param.annotation is param.empty
                                                        else param.annotation),
                       str(param.kind).lower())
                                    for param in sig.parameters.values()),
                (... if sig.return_annotation is sig.empty
                                            else sig.return_annotation))

    def test_signature_object(self):
        S = inspect.Signature
        P = inspect.Parameter

        self.assertEqual(str(S()), '()')

        def test(po, pk, pod=42, pkd=100, *args, ko, **kwargs):
            pass
        sig = inspect.signature(test)
        po = sig.parameters['po'].replace(kind=P.POSITIONAL_ONLY)
        pod = sig.parameters['pod'].replace(kind=P.POSITIONAL_ONLY)
        pk = sig.parameters['pk']
        pkd = sig.parameters['pkd']
        args = sig.parameters['args']
        ko = sig.parameters['ko']
        kwargs = sig.parameters['kwargs']

        S((po, pk, args, ko, kwargs))

        with self.assertRaisesRegex(ValueError, 'wrong parameter order'):
            S((pk, po, args, ko, kwargs))

        with self.assertRaisesRegex(ValueError, 'wrong parameter order'):
            S((po, args, pk, ko, kwargs))

        with self.assertRaisesRegex(ValueError, 'wrong parameter order'):
            S((args, po, pk, ko, kwargs))

        with self.assertRaisesRegex(ValueError, 'wrong parameter order'):
            S((po, pk, args, kwargs, ko))

        kwargs2 = kwargs.replace(name='args')
        with self.assertRaisesRegex(ValueError, 'duplicate parameter name'):
            S((po, pk, args, kwargs2, ko))

        with self.assertRaisesRegex(ValueError, 'follows default argument'):
            S((pod, po))

        with self.assertRaisesRegex(ValueError, 'follows default argument'):
            S((po, pkd, pk))

        with self.assertRaisesRegex(ValueError, 'follows default argument'):
            S((pkd, pk))

    def test_signature_immutability(self):
        def test(a):
            pass
        sig = inspect.signature(test)

        with self.assertRaises(AttributeError):
            sig.foo = 'bar'

        with self.assertRaises(TypeError):
            sig.parameters['a'] = None

    def test_signature_on_noarg(self):
        def test():
            pass
        self.assertEqual(self.signature(test), ((), ...))

    def test_signature_on_wargs(self):
        def test(a, b:'foo') -> 123:
            pass
        self.assertEqual(self.signature(test),
                         ((('a', ..., ..., "positional_or_keyword"),
                           ('b', ..., 'foo', "positional_or_keyword")),
                          123))

    def test_signature_on_wkwonly(self):
        def test(*, a:float, b:str) -> int:
            pass
        self.assertEqual(self.signature(test),
                         ((('a', ..., float, "keyword_only"),
                           ('b', ..., str, "keyword_only")),
                           int))

    def test_signature_on_complex_args(self):
        def test(a, b:'foo'=10, *args:'bar', spam:'baz', ham=123, **kwargs:int):
            pass
        self.assertEqual(self.signature(test),
                         ((('a', ..., ..., "positional_or_keyword"),
                           ('b', 10, 'foo', "positional_or_keyword"),
                           ('args', ..., 'bar', "var_positional"),
                           ('spam', ..., 'baz', "keyword_only"),
                           ('ham', 123, ..., "keyword_only"),
                           ('kwargs', ..., int, "var_keyword")),
                          ...))

    @cpython_only
    @unittest.skipIf(MISSING_C_DOCSTRINGS,
                     "Signature information for builtins requires docstrings")
    def test_signature_on_builtins(self):
        import _testcapi

        def test_unbound_method(o):
            """Use this to test unbound methods (things that should have a self)"""
            signature = inspect.signature(o)
            self.assertTrue(isinstance(signature, inspect.Signature))
            self.assertEqual(list(signature.parameters.values())[0].name, 'self')
            return signature

        def test_callable(o):
            """Use this to test bound methods or normal callables (things that don't expect self)"""
            signature = inspect.signature(o)
            self.assertTrue(isinstance(signature, inspect.Signature))
            if signature.parameters:
                self.assertNotEqual(list(signature.parameters.values())[0].name, 'self')
            return signature

        signature = test_callable(_testcapi.docstring_with_signature_with_defaults)
        def p(name): return signature.parameters[name].default
        self.assertEqual(p('s'), 'avocado')
        self.assertEqual(p('b'), b'bytes')
        self.assertEqual(p('d'), 3.14)
        self.assertEqual(p('i'), 35)
        self.assertEqual(p('n'), None)
        self.assertEqual(p('t'), True)
        self.assertEqual(p('f'), False)
        self.assertEqual(p('local'), 3)
        self.assertEqual(p('sys'), sys.maxsize)
        self.assertEqual(p('exp'), sys.maxsize - 1)

        test_callable(object)

        
        "method_descriptor")
        test_unbound_method(_pickle.Pickler.dump)
        d = _pickle.Pickler(io.StringIO())
        test_callable(d.dump)

        
        test_callable(str.maketrans)
        test_callable('abc'.maketrans)

        
        test_callable(dict.fromkeys)
        test_callable({}.fromkeys)

        "wrapper_descriptor")
        test_unbound_method(type.__call__)
        test_unbound_method(int.__add__)
        test_callable((3).__add__)

        
        
        test_callable(min.__call__)

        
        "type" in 3.4)
        with self.assertRaisesRegex(ValueError, "no signature found"):
            class ThisWorksNow:
                __call__ = type
            test_callable(ThisWorksNow())

        
        test_unbound_method(dict.__delitem__)
        test_unbound_method(property.__delete__)


    @cpython_only
    @unittest.skipIf(MISSING_C_DOCSTRINGS,
                     "Signature information for builtins requires docstrings")
    def test_signature_on_decorated_builtins(self):
        import _testcapi
        func = _testcapi.docstring_with_signature_with_defaults

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> int:
                return func(*args, **kwargs)
            return wrapper

        decorated_func = decorator(func)

        self.assertEqual(inspect.signature(func),
                         inspect.signature(decorated_func))

    @cpython_only
    def test_signature_on_builtins_no_signature(self):
        import _testcapi
        with self.assertRaisesRegex(ValueError, 'no signature found for builtin'):
            inspect.signature(_testcapi.docstring_no_signature)

    def test_signature_on_non_function(self):
        with self.assertRaisesRegex(TypeError, 'is not a callable object'):
            inspect.signature(42)

        with self.assertRaisesRegex(TypeError, 'is not a Python function'):
            inspect.Signature.from_function(42)

    def test_signature_from_builtin_errors(self):
        with self.assertRaisesRegex(TypeError, 'is not a Python builtin'):
            inspect.Signature.from_builtin(42)

    def test_signature_from_functionlike_object(self):
        def func(a,b, *args, kwonly=True, kwonlyreq, **kwargs):
            pass

        class funclike:
            
            
            

            def __init__(self, func):
                self.__name__ = func.__name__
                self.__code__ = func.__code__
                self.__annotations__ = func.__annotations__
                self.__defaults__ = func.__defaults__
                self.__kwdefaults__ = func.__kwdefaults__
                self.func = func

            def __call__(self, *args, **kwargs):
                return self.func(*args, **kwargs)

        sig_func = inspect.Signature.from_function(func)

        sig_funclike = inspect.Signature.from_function(funclike(func))
        self.assertEqual(sig_funclike, sig_func)

        sig_funclike = inspect.signature(funclike(func))
        self.assertEqual(sig_funclike, sig_func)

        
        
        
        fl = funclike(func)
        del fl.__defaults__
        self.assertEqual(self.signature(fl),
                         ((('args', ..., ..., "var_positional"),
                           ('kwargs', ..., ..., "var_keyword")),
                           ...))

        
        _orig_isdesc = inspect.ismethoddescriptor
        def _isdesc(obj):
            if hasattr(obj, '_builtinmock'):
                return True
            return _orig_isdesc(obj)

        with unittest.mock.patch('inspect.ismethoddescriptor', _isdesc):
            builtin_func = funclike(func)
            
            self.assertFalse(inspect.ismethoddescriptor(builtin_func))
            builtin_func._builtinmock = True
            self.assertTrue(inspect.ismethoddescriptor(builtin_func))
            self.assertEqual(inspect.signature(builtin_func), sig_func)

    def test_signature_functionlike_class(self):
        
        

        def func(a,b, *args, kwonly=True, kwonlyreq, **kwargs):
            pass

        class funclike:
            def __init__(self, marker):
                pass

            __name__ = func.__name__
            __code__ = func.__code__
            __annotations__ = func.__annotations__
            __defaults__ = func.__defaults__
            __kwdefaults__ = func.__kwdefaults__

        with self.assertRaisesRegex(TypeError, 'is not a Python function'):
            inspect.Signature.from_function(funclike)

        self.assertEqual(str(inspect.signature(funclike)), '(marker)')

    def test_signature_on_method(self):
        class Test:
            def __init__(*args):
                pass
            def m1(self, arg1, arg2=1) -> int:
                pass
            def m2(*args):
                pass
            def __call__(*, a):
                pass

        self.assertEqual(self.signature(Test().m1),
                         ((('arg1', ..., ..., "positional_or_keyword"),
                           ('arg2', 1, ..., "positional_or_keyword")),
                          int))

        self.assertEqual(self.signature(Test().m2),
                         ((('args', ..., ..., "var_positional"),),
                          ...))

        self.assertEqual(self.signature(Test),
                         ((('args', ..., ..., "var_positional"),),
                          ...))

        with self.assertRaisesRegex(ValueError, 'invalid method signature'):
            self.signature(Test())

    def test_signature_wrapped_bound_method(self):
        
        class Test:
            def m1(self, arg1, arg2=1) -> int:
                pass
        @functools.wraps(Test().m1)
        def m1d(*args, **kwargs):
            pass
        self.assertEqual(self.signature(m1d),
                         ((('arg1', ..., ..., "positional_or_keyword"),
                           ('arg2', 1, ..., "positional_or_keyword")),
                          int))

    def test_signature_on_classmethod(self):
        class Test:
            @classmethod
            def foo(cls, arg1, *, arg2=1):
                pass

        meth = Test().foo
        self.assertEqual(self.signature(meth),
                         ((('arg1', ..., ..., "positional_or_keyword"),
                           ('arg2', 1, ..., "keyword_only")),
                          ...))

        meth = Test.foo
        self.assertEqual(self.signature(meth),
                         ((('arg1', ..., ..., "positional_or_keyword"),
                           ('arg2', 1, ..., "keyword_only")),
                          ...))

    def test_signature_on_staticmethod(self):
        class Test:
            @staticmethod
            def foo(cls, *, arg):
                pass

        meth = Test().foo
        self.assertEqual(self.signature(meth),
                         ((('cls', ..., ..., "positional_or_keyword"),
                           ('arg', ..., ..., "keyword_only")),
                          ...))

        meth = Test.foo
        self.assertEqual(self.signature(meth),
                         ((('cls', ..., ..., "positional_or_keyword"),
                           ('arg', ..., ..., "keyword_only")),
                          ...))

    def test_signature_on_partial(self):
        from functools import partial

        Parameter = inspect.Parameter

        def test():
            pass

        self.assertEqual(self.signature(partial(test)), ((), ...))

        with self.assertRaisesRegex(ValueError, "has incorrect arguments"):
            inspect.signature(partial(test, 1))

        with self.assertRaisesRegex(ValueError, "has incorrect arguments"):
            inspect.signature(partial(test, a=1))

        def test(a, b, *, c, d):
            pass

        self.assertEqual(self.signature(partial(test)),
                         ((('a', ..., ..., "positional_or_keyword"),
                           ('b', ..., ..., "positional_or_keyword"),
                           ('c', ..., ..., "keyword_only"),
                           ('d', ..., ..., "keyword_only")),
                          ...))

        self.assertEqual(self.signature(partial(test, 1)),
                         ((('b', ..., ..., "positional_or_keyword"),
                           ('c', ..., ..., "keyword_only"),
                           ('d', ..., ..., "keyword_only")),
                          ...))

        self.assertEqual(self.signature(partial(test, 1, c=2)),
                         ((('b', ..., ..., "positional_or_keyword"),
                           ('c', 2, ..., "keyword_only"),
                           ('d', ..., ..., "keyword_only")),
                          ...))

        self.assertEqual(self.signature(partial(test, b=1, c=2)),
                         ((('a', ..., ..., "positional_or_keyword"),
                           ('b', 1, ..., "keyword_only"),
                           ('c', 2, ..., "keyword_only"),
                           ('d', ..., ..., "keyword_only")),
                          ...))

        self.assertEqual(self.signature(partial(test, 0, b=1, c=2)),
                         ((('b', 1, ..., "keyword_only"),
                           ('c', 2, ..., "keyword_only"),
                           ('d', ..., ..., "keyword_only")),
                          ...))

        self.assertEqual(self.signature(partial(test, a=1)),
                         ((('a', 1, ..., "keyword_only"),
                           ('b', ..., ..., "keyword_only"),
                           ('c', ..., ..., "keyword_only"),
                           ('d', ..., ..., "keyword_only")),
                          ...))

        def test(a, *args, b, **kwargs):
            pass

        self.assertEqual(self.signature(partial(test, 1)),
                         ((('args', ..., ..., "var_positional"),
                           ('b', ..., ..., "keyword_only"),
                           ('kwargs', ..., ..., "var_keyword")),
                          ...))

        self.assertEqual(self.signature(partial(test, a=1)),
                         ((('a', 1, ..., "keyword_only"),
                           ('b', ..., ..., "keyword_only"),
                           ('kwargs', ..., ..., "var_keyword")),
                          ...))

        self.assertEqual(self.signature(partial(test, 1, 2, 3)),
                         ((('args', ..., ..., "var_positional"),
                           ('b', ..., ..., "keyword_only"),
                           ('kwargs', ..., ..., "var_keyword")),
                          ...))

        self.assertEqual(self.signature(partial(test, 1, 2, 3, test=True)),
                         ((('args', ..., ..., "var_positional"),
                           ('b', ..., ..., "keyword_only"),
                           ('kwargs', ..., ..., "var_keyword")),
                          ...))

        self.assertEqual(self.signature(partial(test, 1, 2, 3, test=1, b=0)),
                         ((('args', ..., ..., "var_positional"),
                           ('b', 0, ..., "keyword_only"),
                           ('kwargs', ..., ..., "var_keyword")),
                          ...))

        self.assertEqual(self.signature(partial(test, b=0)),
                         ((('a', ..., ..., "positional_or_keyword"),
                           ('args', ..., ..., "var_positional"),
                           ('b', 0, ..., "keyword_only"),
                           ('kwargs', ..., ..., "var_keyword")),
                          ...))

        self.assertEqual(self.signature(partial(test, b=0, test=1)),
                         ((('a', ..., ..., "positional_or_keyword"),
                           ('args', ..., ..., "var_positional"),
                           ('b', 0, ..., "keyword_only"),
                           ('kwargs', ..., ..., "var_keyword")),
                          ...))

        def test(a, b, c:int) -> 42:
            pass

        sig = test.__signature__ = inspect.signature(test)

        self.assertEqual(self.signature(partial(partial(test, 1))),
                         ((('b', ..., ..., "positional_or_keyword"),
                           ('c', ..., int, "positional_or_keyword")),
                          42))

        self.assertEqual(self.signature(partial(partial(test, 1), 2)),
                         ((('c', ..., int, "positional_or_keyword"),),
                          42))

        psig = inspect.signature(partial(partial(test, 1), 2))

        def foo(a):
            return a
        _foo = partial(partial(foo, a=10), a=20)
        self.assertEqual(self.signature(_foo),
                         ((('a', 20, ..., "keyword_only"),),
                          ...))
        
        
        self.assertEqual(_foo(), 20)

        def foo(a, b, c):
            return a, b, c
        _foo = partial(partial(foo, 1, b=20), b=30)

        self.assertEqual(self.signature(_foo),
                         ((('b', 30, ..., "keyword_only"),
                           ('c', ..., ..., "keyword_only")),
                          ...))
        self.assertEqual(_foo(c=10), (1, 30, 10))

        def foo(a, b, c, *, d):
            return a, b, c, d
        _foo = partial(partial(foo, d=20, c=20), b=10, d=30)
        self.assertEqual(self.signature(_foo),
                         ((('a', ..., ..., "positional_or_keyword"),
                           ('b', 10, ..., "keyword_only"),
                           ('c', 20, ..., "keyword_only"),
                           ('d', 30, ..., "keyword_only"),
                           ),
                          ...))
        ba = inspect.signature(_foo).bind(a=200, b=11)
        self.assertEqual(_foo(*ba.args, **ba.kwargs), (200, 11, 20, 30))

        def foo(a=1, b=2, c=3):
            return a, b, c
        _foo = partial(foo, c=13) 

        ba = inspect.signature(_foo).bind(a=11)
        self.assertEqual(_foo(*ba.args, **ba.kwargs), (11, 2, 13))

        ba = inspect.signature(_foo).bind(11, 12)
        self.assertEqual(_foo(*ba.args, **ba.kwargs), (11, 12, 13))

        ba = inspect.signature(_foo).bind(11, b=12)
        self.assertEqual(_foo(*ba.args, **ba.kwargs), (11, 12, 13))

        ba = inspect.signature(_foo).bind(b=12)
        self.assertEqual(_foo(*ba.args, **ba.kwargs), (1, 12, 13))

        _foo = partial(_foo, b=10, c=20)
        ba = inspect.signature(_foo).bind(12)
        self.assertEqual(_foo(*ba.args, **ba.kwargs), (12, 10, 20))


        def foo(a, b, c, d, **kwargs):
            pass
        sig = inspect.signature(foo)
        params = sig.parameters.copy()
        params['a'] = params['a'].replace(kind=Parameter.POSITIONAL_ONLY)
        params['b'] = params['b'].replace(kind=Parameter.POSITIONAL_ONLY)
        foo.__signature__ = inspect.Signature(params.values())
        sig = inspect.signature(foo)
        self.assertEqual(str(sig), '(a, b, /, c, d, **kwargs)')

        self.assertEqual(self.signature(partial(foo, 1)),
                         ((('b', ..., ..., 'positional_only'),
                           ('c', ..., ..., 'positional_or_keyword'),
                           ('d', ..., ..., 'positional_or_keyword'),
                           ('kwargs', ..., ..., 'var_keyword')),
                         ...))

        self.assertEqual(self.signature(partial(foo, 1, 2)),
                         ((('c', ..., ..., 'positional_or_keyword'),
                           ('d', ..., ..., 'positional_or_keyword'),
                           ('kwargs', ..., ..., 'var_keyword')),
                         ...))

        self.assertEqual(self.signature(partial(foo, 1, 2, 3)),
                         ((('d', ..., ..., 'positional_or_keyword'),
                           ('kwargs', ..., ..., 'var_keyword')),
                         ...))

        self.assertEqual(self.signature(partial(foo, 1, 2, c=3)),
                         ((('c', 3, ..., 'keyword_only'),
                           ('d', ..., ..., 'keyword_only'),
                           ('kwargs', ..., ..., 'var_keyword')),
                         ...))

        self.assertEqual(self.signature(partial(foo, 1, c=3)),
                         ((('b', ..., ..., 'positional_only'),
                           ('c', 3, ..., 'keyword_only'),
                           ('d', ..., ..., 'keyword_only'),
                           ('kwargs', ..., ..., 'var_keyword')),
                         ...))

    def test_signature_on_partialmethod(self):
        from functools import partialmethod

        class Spam:
            def test():
                pass
            ham = partialmethod(test)

        with self.assertRaisesRegex(ValueError, "has incorrect arguments"):
            inspect.signature(Spam.ham)

        class Spam:
            def test(it, a, *, c) -> 'spam':
                pass
            ham = partialmethod(test, c=1)

        self.assertEqual(self.signature(Spam.ham),
                         ((('it', ..., ..., 'positional_or_keyword'),
                           ('a', ..., ..., 'positional_or_keyword'),
                           ('c', 1, ..., 'keyword_only')),
                          'spam'))

        self.assertEqual(self.signature(Spam().ham),
                         ((('a', ..., ..., 'positional_or_keyword'),
                           ('c', 1, ..., 'keyword_only')),
                          'spam'))

    def test_signature_on_fake_partialmethod(self):
        def foo(a): pass
        foo._partialmethod = 'spam'
        self.assertEqual(str(inspect.signature(foo)), '(a)')

    def test_signature_on_decorated(self):
        import functools

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> int:
                return func(*args, **kwargs)
            return wrapper

        class Foo:
            @decorator
            def bar(self, a, b):
                pass

        self.assertEqual(self.signature(Foo.bar),
                         ((('self', ..., ..., "positional_or_keyword"),
                           ('a', ..., ..., "positional_or_keyword"),
                           ('b', ..., ..., "positional_or_keyword")),
                          ...))

        self.assertEqual(self.signature(Foo().bar),
                         ((('a', ..., ..., "positional_or_keyword"),
                           ('b', ..., ..., "positional_or_keyword")),
                          ...))

        
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> int:
                return func(42, *args, **kwargs)
            sig = inspect.signature(func)
            new_params = tuple(sig.parameters.values())[1:]
            wrapper.__signature__ = sig.replace(parameters=new_params)
            return wrapper

        class Foo:
            @decorator
            def __call__(self, a, b):
                pass

        self.assertEqual(self.signature(Foo.__call__),
                         ((('a', ..., ..., "positional_or_keyword"),
                           ('b', ..., ..., "positional_or_keyword")),
                          ...))

        self.assertEqual(self.signature(Foo().__call__),
                         ((('b', ..., ..., "positional_or_keyword"),),
                          ...))

        
        def wrapped_foo_call():
            pass
        wrapped_foo_call.__wrapped__ = Foo.__call__

        self.assertEqual(self.signature(wrapped_foo_call),
                         ((('a', ..., ..., "positional_or_keyword"),
                           ('b', ..., ..., "positional_or_keyword")),
                          ...))


    def test_signature_on_class(self):
        class C:
            def __init__(self, a):
                pass

        self.assertEqual(self.signature(C),
                         ((('a', ..., ..., "positional_or_keyword"),),
                          ...))

        class CM(type):
            def __call__(cls, a):
                pass
        class C(metaclass=CM):
            def __init__(self, b):
                pass

        self.assertEqual(self.signature(C),
                         ((('a', ..., ..., "positional_or_keyword"),),
                          ...))

        class CM(type):
            def __new__(mcls, name, bases, dct, *, foo=1):
                return super().__new__(mcls, name, bases, dct)
        class C(metaclass=CM):
            def __init__(self, b):
                pass

        self.assertEqual(self.signature(C),
                         ((('b', ..., ..., "positional_or_keyword"),),
                          ...))

        self.assertEqual(self.signature(CM),
                         ((('name', ..., ..., "positional_or_keyword"),
                           ('bases', ..., ..., "positional_or_keyword"),
                           ('dct', ..., ..., "positional_or_keyword"),
                           ('foo', 1, ..., "keyword_only")),
                          ...))

        class CMM(type):
            def __new__(mcls, name, bases, dct, *, foo=1):
                return super().__new__(mcls, name, bases, dct)
            def __call__(cls, nm, bs, dt):
                return type(nm, bs, dt)
        class CM(type, metaclass=CMM):
            def __new__(mcls, name, bases, dct, *, bar=2):
                return super().__new__(mcls, name, bases, dct)
        class C(metaclass=CM):
            def __init__(self, b):
                pass

        self.assertEqual(self.signature(CMM),
                         ((('name', ..., ..., "positional_or_keyword"),
                           ('bases', ..., ..., "positional_or_keyword"),
                           ('dct', ..., ..., "positional_or_keyword"),
                           ('foo', 1, ..., "keyword_only")),
                          ...))

        self.assertEqual(self.signature(CM),
                         ((('nm', ..., ..., "positional_or_keyword"),
                           ('bs', ..., ..., "positional_or_keyword"),
                           ('dt', ..., ..., "positional_or_keyword")),
                          ...))

        self.assertEqual(self.signature(C),
                         ((('b', ..., ..., "positional_or_keyword"),),
                          ...))

        class CM(type):
            def __init__(cls, name, bases, dct, *, bar=2):
                return super().__init__(name, bases, dct)
        class C(metaclass=CM):
            def __init__(self, b):
                pass

        self.assertEqual(self.signature(CM),
                         ((('name', ..., ..., "positional_or_keyword"),
                           ('bases', ..., ..., "positional_or_keyword"),
                           ('dct', ..., ..., "positional_or_keyword"),
                           ('bar', 2, ..., "keyword_only")),
                          ...))

    @unittest.skipIf(MISSING_C_DOCSTRINGS,
                     "Signature information for builtins requires docstrings")
    def test_signature_on_class_without_init(self):
        
        class C: pass
        self.assertEqual(str(inspect.signature(C)), '()')
        class D(C): pass
        self.assertEqual(str(inspect.signature(D)), '()')

        
        class C(type): pass
        class D(C): pass
        with self.assertRaisesRegex(ValueError, "callable.*is not supported"):
            self.assertEqual(inspect.signature(C), None)
        with self.assertRaisesRegex(ValueError, "callable.*is not supported"):
            self.assertEqual(inspect.signature(D), None)

    @unittest.skipIf(MISSING_C_DOCSTRINGS,
                     "Signature information for builtins requires docstrings")
    def test_signature_on_builtin_class(self):
        self.assertEqual(str(inspect.signature(_pickle.Pickler)),
                         '(file, protocol=None, fix_imports=True)')

        class P(_pickle.Pickler): pass
        class EmptyTrait: pass
        class P2(EmptyTrait, P): pass
        self.assertEqual(str(inspect.signature(P)),
                         '(file, protocol=None, fix_imports=True)')
        self.assertEqual(str(inspect.signature(P2)),
                         '(file, protocol=None, fix_imports=True)')

        class P3(P2):
            def __init__(self, spam):
                pass
        self.assertEqual(str(inspect.signature(P3)), '(spam)')

        class MetaP(type):
            def __call__(cls, foo, bar):
                pass
        class P4(P2, metaclass=MetaP):
            pass
        self.assertEqual(str(inspect.signature(P4)), '(foo, bar)')

    def test_signature_on_callable_objects(self):
        class Foo:
            def __call__(self, a):
                pass

        self.assertEqual(self.signature(Foo()),
                         ((('a', ..., ..., "positional_or_keyword"),),
                          ...))

        class Spam:
            pass
        with self.assertRaisesRegex(TypeError, "is not a callable object"):
            inspect.signature(Spam())

        class Bar(Spam, Foo):
            pass

        self.assertEqual(self.signature(Bar()),
                         ((('a', ..., ..., "positional_or_keyword"),),
                          ...))

        class Wrapped:
            pass
        Wrapped.__wrapped__ = lambda a: None
        self.assertEqual(self.signature(Wrapped),
                         ((('a', ..., ..., "positional_or_keyword"),),
                          ...))
        
        Wrapped.__wrapped__ = Wrapped
        with self.assertRaisesRegex(ValueError, 'wrapper loop'):
            self.signature(Wrapped)

    def test_signature_on_lambdas(self):
        self.assertEqual(self.signature((lambda a=10: a)),
                         ((('a', 10, ..., "positional_or_keyword"),),
                          ...))

    def test_signature_equality(self):
        def foo(a, *, b:int) -> float: pass
        self.assertFalse(inspect.signature(foo) == 42)
        self.assertTrue(inspect.signature(foo) != 42)
        self.assertTrue(inspect.signature(foo) == EqualsToAll())
        self.assertFalse(inspect.signature(foo) != EqualsToAll())

        def bar(a, *, b:int) -> float: pass
        self.assertTrue(inspect.signature(foo) == inspect.signature(bar))
        self.assertFalse(inspect.signature(foo) != inspect.signature(bar))

        def bar(a, *, b:int) -> int: pass
        self.assertFalse(inspect.signature(foo) == inspect.signature(bar))
        self.assertTrue(inspect.signature(foo) != inspect.signature(bar))

        def bar(a, *, b:int): pass
        self.assertFalse(inspect.signature(foo) == inspect.signature(bar))
        self.assertTrue(inspect.signature(foo) != inspect.signature(bar))

        def bar(a, *, b:int=42) -> float: pass
        self.assertFalse(inspect.signature(foo) == inspect.signature(bar))
        self.assertTrue(inspect.signature(foo) != inspect.signature(bar))

        def bar(a, *, c) -> float: pass
        self.assertFalse(inspect.signature(foo) == inspect.signature(bar))
        self.assertTrue(inspect.signature(foo) != inspect.signature(bar))

        def bar(a, b:int) -> float: pass
        self.assertFalse(inspect.signature(foo) == inspect.signature(bar))
        self.assertTrue(inspect.signature(foo) != inspect.signature(bar))
        def spam(b:int, a) -> float: pass
        self.assertFalse(inspect.signature(spam) == inspect.signature(bar))
        self.assertTrue(inspect.signature(spam) != inspect.signature(bar))

        def foo(*, a, b, c): pass
        def bar(*, c, b, a): pass
        self.assertTrue(inspect.signature(foo) == inspect.signature(bar))
        self.assertFalse(inspect.signature(foo) != inspect.signature(bar))

        def foo(*, a=1, b, c): pass
        def bar(*, c, b, a=1): pass
        self.assertTrue(inspect.signature(foo) == inspect.signature(bar))
        self.assertFalse(inspect.signature(foo) != inspect.signature(bar))

        def foo(pos, *, a=1, b, c): pass
        def bar(pos, *, c, b, a=1): pass
        self.assertTrue(inspect.signature(foo) == inspect.signature(bar))
        self.assertFalse(inspect.signature(foo) != inspect.signature(bar))

        def foo(pos, *, a, b, c): pass
        def bar(pos, *, c, b, a=1): pass
        self.assertFalse(inspect.signature(foo) == inspect.signature(bar))
        self.assertTrue(inspect.signature(foo) != inspect.signature(bar))

        def foo(pos, *args, a=42, b, c, **kwargs:int): pass
        def bar(pos, *args, c, b, a=42, **kwargs:int): pass
        self.assertTrue(inspect.signature(foo) == inspect.signature(bar))
        self.assertFalse(inspect.signature(foo) != inspect.signature(bar))

    def test_signature_unhashable(self):
        def foo(a): pass
        sig = inspect.signature(foo)
        with self.assertRaisesRegex(TypeError, 'unhashable type'):
            hash(sig)

    def test_signature_str(self):
        def foo(a:int=1, *, b, c=None, **kwargs) -> 42:
            pass
        self.assertEqual(str(inspect.signature(foo)),
                         '(a:int=1, *, b, c=None, **kwargs) -> 42')

        def foo(a:int=1, *args, b, c=None, **kwargs) -> 42:
            pass
        self.assertEqual(str(inspect.signature(foo)),
                         '(a:int=1, *args, b, c=None, **kwargs) -> 42')

        def foo():
            pass
        self.assertEqual(str(inspect.signature(foo)), '()')

    def test_signature_str_positional_only(self):
        P = inspect.Parameter
        S = inspect.Signature

        def test(a_po, *, b, **kwargs):
            return a_po, kwargs

        sig = inspect.signature(test)
        new_params = list(sig.parameters.values())
        new_params[0] = new_params[0].replace(kind=P.POSITIONAL_ONLY)
        test.__signature__ = sig.replace(parameters=new_params)

        self.assertEqual(str(inspect.signature(test)),
                         '(a_po, /, *, b, **kwargs)')

        self.assertEqual(str(S(parameters=[P('foo', P.POSITIONAL_ONLY)])),
                         '(foo, /)')

        self.assertEqual(str(S(parameters=[
                                P('foo', P.POSITIONAL_ONLY),
                                P('bar', P.VAR_KEYWORD)])),
                         '(foo, /, **bar)')

        self.assertEqual(str(S(parameters=[
                                P('foo', P.POSITIONAL_ONLY),
                                P('bar', P.VAR_POSITIONAL)])),
                         '(foo, /, *bar)')

    def test_signature_replace_anno(self):
        def test() -> 42:
            pass

        sig = inspect.signature(test)
        sig = sig.replace(return_annotation=None)
        self.assertIs(sig.return_annotation, None)
        sig = sig.replace(return_annotation=sig.empty)
        self.assertIs(sig.return_annotation, sig.empty)
        sig = sig.replace(return_annotation=42)
        self.assertEqual(sig.return_annotation, 42)
        self.assertEqual(sig, inspect.signature(test))

    def test_signature_on_mangled_parameters(self):
        class Spam:
            def foo(self, __p1:1=2, *, __p2:2=3):
                pass
        class Ham(Spam):
            pass

        self.assertEqual(self.signature(Spam.foo),
                         ((('self', ..., ..., "positional_or_keyword"),
                           ('_Spam__p1', 2, 1, "positional_or_keyword"),
                           ('_Spam__p2', 3, 2, "keyword_only")),
                          ...))

        self.assertEqual(self.signature(Spam.foo),
                         self.signature(Ham.foo))


class TestParameterObject(unittest.TestCase):
    def test_signature_parameter_kinds(self):
        P = inspect.Parameter
        self.assertTrue(P.POSITIONAL_ONLY < P.POSITIONAL_OR_KEYWORD < \
                        P.VAR_POSITIONAL < P.KEYWORD_ONLY < P.VAR_KEYWORD)

        self.assertEqual(str(P.POSITIONAL_ONLY), 'POSITIONAL_ONLY')
        self.assertTrue('POSITIONAL_ONLY' in repr(P.POSITIONAL_ONLY))

    def test_signature_parameter_object(self):
        p = inspect.Parameter('foo', default=10,
                              kind=inspect.Parameter.POSITIONAL_ONLY)
        self.assertEqual(p.name, 'foo')
        self.assertEqual(p.default, 10)
        self.assertIs(p.annotation, p.empty)
        self.assertEqual(p.kind, inspect.Parameter.POSITIONAL_ONLY)

        with self.assertRaisesRegex(ValueError, 'invalid value'):
            inspect.Parameter('foo', default=10, kind='123')

        with self.assertRaisesRegex(ValueError, 'not a valid parameter name'):
            inspect.Parameter('1', kind=inspect.Parameter.VAR_KEYWORD)

        with self.assertRaisesRegex(TypeError, 'name must be a str'):
            inspect.Parameter(None, kind=inspect.Parameter.VAR_KEYWORD)

        with self.assertRaisesRegex(ValueError,
                                    'is not a valid parameter name'):
            inspect.Parameter('$', kind=inspect.Parameter.VAR_KEYWORD)

        with self.assertRaisesRegex(ValueError, 'cannot have default values'):
            inspect.Parameter('a', default=42,
                              kind=inspect.Parameter.VAR_KEYWORD)

        with self.assertRaisesRegex(ValueError, 'cannot have default values'):
            inspect.Parameter('a', default=42,
                              kind=inspect.Parameter.VAR_POSITIONAL)

        p = inspect.Parameter('a', default=42,
                              kind=inspect.Parameter.POSITIONAL_OR_KEYWORD)
        with self.assertRaisesRegex(ValueError, 'cannot have default values'):
            p.replace(kind=inspect.Parameter.VAR_POSITIONAL)

        self.assertTrue(repr(p).startswith('<Parameter'))

    def test_signature_parameter_equality(self):
        P = inspect.Parameter
        p = P('foo', default=42, kind=inspect.Parameter.KEYWORD_ONLY)

        self.assertTrue(p == p)
        self.assertFalse(p != p)
        self.assertFalse(p == 42)
        self.assertTrue(p != 42)
        self.assertTrue(p == EqualsToAll())
        self.assertFalse(p != EqualsToAll())

        self.assertTrue(p == P('foo', default=42,
                               kind=inspect.Parameter.KEYWORD_ONLY))
        self.assertFalse(p != P('foo', default=42,
                                kind=inspect.Parameter.KEYWORD_ONLY))

    def test_signature_parameter_unhashable(self):
        p = inspect.Parameter('foo', default=42,
                              kind=inspect.Parameter.KEYWORD_ONLY)

        with self.assertRaisesRegex(TypeError, 'unhashable type'):
            hash(p)

    def test_signature_parameter_replace(self):
        p = inspect.Parameter('foo', default=42,
                              kind=inspect.Parameter.KEYWORD_ONLY)

        self.assertIsNot(p, p.replace())
        self.assertEqual(p, p.replace())

        p2 = p.replace(annotation=1)
        self.assertEqual(p2.annotation, 1)
        p2 = p2.replace(annotation=p2.empty)
        self.assertEqual(p, p2)

        p2 = p2.replace(name='bar')
        self.assertEqual(p2.name, 'bar')
        self.assertNotEqual(p2, p)

        with self.assertRaisesRegex(ValueError,
                                    'name is a required attribute'):
            p2 = p2.replace(name=p2.empty)

        p2 = p2.replace(name='foo', default=None)
        self.assertIs(p2.default, None)
        self.assertNotEqual(p2, p)

        p2 = p2.replace(name='foo', default=p2.empty)
        self.assertIs(p2.default, p2.empty)


        p2 = p2.replace(default=42, kind=p2.POSITIONAL_OR_KEYWORD)
        self.assertEqual(p2.kind, p2.POSITIONAL_OR_KEYWORD)
        self.assertNotEqual(p2, p)

        with self.assertRaisesRegex(ValueError, 'invalid value for'):
            p2 = p2.replace(kind=p2.empty)

        p2 = p2.replace(kind=p2.KEYWORD_ONLY)
        self.assertEqual(p2, p)

    def test_signature_parameter_positional_only(self):
        with self.assertRaisesRegex(TypeError, 'name must be a str'):
            inspect.Parameter(None, kind=inspect.Parameter.POSITIONAL_ONLY)

    def test_signature_parameter_immutability(self):
        p = inspect.Parameter('spam', kind=inspect.Parameter.KEYWORD_ONLY)

        with self.assertRaises(AttributeError):
            p.foo = 'bar'

        with self.assertRaises(AttributeError):
            p.kind = 123


class TestSignatureBind(unittest.TestCase):
    @staticmethod
    def call(func, *args, **kwargs):
        sig = inspect.signature(func)
        ba = sig.bind(*args, **kwargs)
        return func(*ba.args, **ba.kwargs)

    def test_signature_bind_empty(self):
        def test():
            return 42

        self.assertEqual(self.call(test), 42)
        with self.assertRaisesRegex(TypeError, 'too many positional arguments'):
            self.call(test, 1)
        with self.assertRaisesRegex(TypeError, 'too many positional arguments'):
            self.call(test, 1, spam=10)
        with self.assertRaisesRegex(TypeError, 'too many keyword arguments'):
            self.call(test, spam=1)

    def test_signature_bind_var(self):
        def test(*args, **kwargs):
            return args, kwargs

        self.assertEqual(self.call(test), ((), {}))
        self.assertEqual(self.call(test, 1), ((1,), {}))
        self.assertEqual(self.call(test, 1, 2), ((1, 2), {}))
        self.assertEqual(self.call(test, foo='bar'), ((), {'foo': 'bar'}))
        self.assertEqual(self.call(test, 1, foo='bar'), ((1,), {'foo': 'bar'}))
        self.assertEqual(self.call(test, args=10), ((), {'args': 10}))
        self.assertEqual(self.call(test, 1, 2, foo='bar'),
                         ((1, 2), {'foo': 'bar'}))

    def test_signature_bind_just_args(self):
        def test(a, b, c):
            return a, b, c

        self.assertEqual(self.call(test, 1, 2, 3), (1, 2, 3))

        with self.assertRaisesRegex(TypeError, 'too many positional arguments'):
            self.call(test, 1, 2, 3, 4)

        with self.assertRaisesRegex(TypeError, "'b' parameter lacking default"):
            self.call(test, 1)

        with self.assertRaisesRegex(TypeError, "'a' parameter lacking default"):
            self.call(test)

        def test(a, b, c=10):
            return a, b, c
        self.assertEqual(self.call(test, 1, 2, 3), (1, 2, 3))
        self.assertEqual(self.call(test, 1, 2), (1, 2, 10))

        def test(a=1, b=2, c=3):
            return a, b, c
        self.assertEqual(self.call(test, a=10, c=13), (10, 2, 13))
        self.assertEqual(self.call(test, a=10), (10, 2, 3))
        self.assertEqual(self.call(test, b=10), (1, 10, 3))

    def test_signature_bind_varargs_order(self):
        def test(*args):
            return args

        self.assertEqual(self.call(test), ())
        self.assertEqual(self.call(test, 1, 2, 3), (1, 2, 3))

    def test_signature_bind_args_and_varargs(self):
        def test(a, b, c=3, *args):
            return a, b, c, args

        self.assertEqual(self.call(test, 1, 2, 3, 4, 5), (1, 2, 3, (4, 5)))
        self.assertEqual(self.call(test, 1, 2), (1, 2, 3, ()))
        self.assertEqual(self.call(test, b=1, a=2), (2, 1, 3, ()))
        self.assertEqual(self.call(test, 1, b=2), (1, 2, 3, ()))

        with self.assertRaisesRegex(TypeError,
                                     "multiple values for argument 'c'"):
            self.call(test, 1, 2, 3, c=4)

    def test_signature_bind_just_kwargs(self):
        def test(**kwargs):
            return kwargs

        self.assertEqual(self.call(test), {})
        self.assertEqual(self.call(test, foo='bar', spam='ham'),
                         {'foo': 'bar', 'spam': 'ham'})

    def test_signature_bind_args_and_kwargs(self):
        def test(a, b, c=3, **kwargs):
            return a, b, c, kwargs

        self.assertEqual(self.call(test, 1, 2), (1, 2, 3, {}))
        self.assertEqual(self.call(test, 1, 2, foo='bar', spam='ham'),
                         (1, 2, 3, {'foo': 'bar', 'spam': 'ham'}))
        self.assertEqual(self.call(test, b=2, a=1, foo='bar', spam='ham'),
                         (1, 2, 3, {'foo': 'bar', 'spam': 'ham'}))
        self.assertEqual(self.call(test, a=1, b=2, foo='bar', spam='ham'),
                         (1, 2, 3, {'foo': 'bar', 'spam': 'ham'}))
        self.assertEqual(self.call(test, 1, b=2, foo='bar', spam='ham'),
                         (1, 2, 3, {'foo': 'bar', 'spam': 'ham'}))
        self.assertEqual(self.call(test, 1, b=2, c=4, foo='bar', spam='ham'),
                         (1, 2, 4, {'foo': 'bar', 'spam': 'ham'}))
        self.assertEqual(self.call(test, 1, 2, 4, foo='bar'),
                         (1, 2, 4, {'foo': 'bar'}))
        self.assertEqual(self.call(test, c=5, a=4, b=3),
                         (4, 3, 5, {}))

    def test_signature_bind_kwonly(self):
        def test(*, foo):
            return foo
        with self.assertRaisesRegex(TypeError,
                                     'too many positional arguments'):
            self.call(test, 1)
        self.assertEqual(self.call(test, foo=1), 1)

        def test(a, *, foo=1, bar):
            return foo
        with self.assertRaisesRegex(TypeError,
                                     "'bar' parameter lacking default value"):
            self.call(test, 1)

        def test(foo, *, bar):
            return foo, bar
        self.assertEqual(self.call(test, 1, bar=2), (1, 2))
        self.assertEqual(self.call(test, bar=2, foo=1), (1, 2))

        with self.assertRaisesRegex(TypeError,
                                     'too many keyword arguments'):
            self.call(test, bar=2, foo=1, spam=10)

        with self.assertRaisesRegex(TypeError,
                                     'too many positional arguments'):
            self.call(test, 1, 2)

        with self.assertRaisesRegex(TypeError,
                                     'too many positional arguments'):
            self.call(test, 1, 2, bar=2)

        with self.assertRaisesRegex(TypeError,
                                     'too many keyword arguments'):
            self.call(test, 1, bar=2, spam='ham')

        with self.assertRaisesRegex(TypeError,
                                     "'bar' parameter lacking default value"):
            self.call(test, 1)

        def test(foo, *, bar, **bin):
            return foo, bar, bin
        self.assertEqual(self.call(test, 1, bar=2), (1, 2, {}))
        self.assertEqual(self.call(test, foo=1, bar=2), (1, 2, {}))
        self.assertEqual(self.call(test, 1, bar=2, spam='ham'),
                         (1, 2, {'spam': 'ham'}))
        self.assertEqual(self.call(test, spam='ham', foo=1, bar=2),
                         (1, 2, {'spam': 'ham'}))
        with self.assertRaisesRegex(TypeError,
                                     "'foo' parameter lacking default value"):
            self.call(test, spam='ham', bar=2)
        self.assertEqual(self.call(test, 1, bar=2, bin=1, spam=10),
                         (1, 2, {'bin': 1, 'spam': 10}))

    def test_signature_bind_arguments(self):
        def test(a, *args, b, z=100, **kwargs):
            pass
        sig = inspect.signature(test)
        ba = sig.bind(10, 20, b=30, c=40, args=50, kwargs=60)
        
        
        self.assertEqual(tuple(ba.arguments.items()),
                         (('a', 10), ('args', (20,)), ('b', 30),
                          ('kwargs', {'c': 40, 'args': 50, 'kwargs': 60})))
        self.assertEqual(ba.kwargs,
                         {'b': 30, 'c': 40, 'args': 50, 'kwargs': 60})
        self.assertEqual(ba.args, (10, 20))

    def test_signature_bind_positional_only(self):
        P = inspect.Parameter

        def test(a_po, b_po, c_po=3, foo=42, *, bar=50, **kwargs):
            return a_po, b_po, c_po, foo, bar, kwargs

        sig = inspect.signature(test)
        new_params = collections.OrderedDict(tuple(sig.parameters.items()))
        for name in ('a_po', 'b_po', 'c_po'):
            new_params[name] = new_params[name].replace(kind=P.POSITIONAL_ONLY)
        new_sig = sig.replace(parameters=new_params.values())
        test.__signature__ = new_sig

        self.assertEqual(self.call(test, 1, 2, 4, 5, bar=6),
                         (1, 2, 4, 5, 6, {}))

        self.assertEqual(self.call(test, 1, 2),
                         (1, 2, 3, 42, 50, {}))

        self.assertEqual(self.call(test, 1, 2, foo=4, bar=5),
                         (1, 2, 3, 4, 5, {}))

        with self.assertRaisesRegex(TypeError, "but was passed as a keyword"):
            self.call(test, 1, 2, foo=4, bar=5, c_po=10)

        with self.assertRaisesRegex(TypeError, "parameter is positional only"):
            self.call(test, 1, 2, c_po=4)

        with self.assertRaisesRegex(TypeError, "parameter is positional only"):
            self.call(test, a_po=1, b_po=2)

    def test_signature_bind_with_self_arg(self):
        "self
        def test(a, self, b):
            pass
        sig = inspect.signature(test)
        ba = sig.bind(1, 2, 3)
        self.assertEqual(ba.args, (1, 2, 3))
        ba = sig.bind(1, self=2, b=3)
        self.assertEqual(ba.args, (1, 2, 3))

    def test_signature_bind_vararg_name(self):
        def test(a, *args):
            return a, args
        sig = inspect.signature(test)

        with self.assertRaisesRegex(TypeError, "too many keyword arguments"):
            sig.bind(a=0, args=1)

        def test(*args, **kwargs):
            return args, kwargs
        self.assertEqual(self.call(test, args=1), ((), {'args': 1}))

        sig = inspect.signature(test)
        ba = sig.bind(args=1)
        self.assertEqual(ba.arguments, {'kwargs': {'args': 1}})


class TestBoundArguments(unittest.TestCase):
    def test_signature_bound_arguments_unhashable(self):
        def foo(a): pass
        ba = inspect.signature(foo).bind(1)

        with self.assertRaisesRegex(TypeError, 'unhashable type'):
            hash(ba)

    def test_signature_bound_arguments_equality(self):
        def foo(a): pass
        ba = inspect.signature(foo).bind(1)
        self.assertTrue(ba == ba)
        self.assertFalse(ba != ba)
        self.assertTrue(ba == EqualsToAll())
        self.assertFalse(ba != EqualsToAll())

        ba2 = inspect.signature(foo).bind(1)
        self.assertTrue(ba == ba2)
        self.assertFalse(ba != ba2)

        ba3 = inspect.signature(foo).bind(2)
        self.assertFalse(ba == ba3)
        self.assertTrue(ba != ba3)
        ba3.arguments['a'] = 1
        self.assertTrue(ba == ba3)
        self.assertFalse(ba != ba3)

        def bar(b): pass
        ba4 = inspect.signature(bar).bind(1)
        self.assertFalse(ba == ba4)
        self.assertTrue(ba != ba4)


class TestSignaturePrivateHelpers(unittest.TestCase):
    def test_signature_get_bound_param(self):
        getter = inspect._signature_get_bound_param

        self.assertEqual(getter('($self)'), 'self')
        self.assertEqual(getter('($self, obj)'), 'self')
        self.assertEqual(getter('($cls, /, obj)'), 'cls')

    def _strip_non_python_syntax(self, input,
        clean_signature, self_parameter, last_positional_only):
        computed_clean_signature, \
            computed_self_parameter, \
            computed_last_positional_only = \
            inspect._signature_strip_non_python_syntax(input)
        self.assertEqual(computed_clean_signature, clean_signature)
        self.assertEqual(computed_self_parameter, self_parameter)
        self.assertEqual(computed_last_positional_only, last_positional_only)

    def test_signature_strip_non_python_syntax(self):
        self._strip_non_python_syntax(
            "($module, /, path, mode, *, dir_fd=None, " +
                "effective_ids=False,\n       follow_symlinks=True)",
            "(module, path, mode, *, dir_fd=None, " +
                "effective_ids=False, follow_symlinks=True)",
            0,
            0)

        self._strip_non_python_syntax(
            "($module, word, salt, /)",
            "(module, word, salt)",
            0,
            2)

        self._strip_non_python_syntax(
            "(x, y=None, z=None, /)",
            "(x, y=None, z=None)",
            None,
            2)

        self._strip_non_python_syntax(
            "(x, y=None, z=None)",
            "(x, y=None, z=None)",
            None,
            None)

        self._strip_non_python_syntax(
            "(x,\n    y=None,\n      z = None  )",
            "(x, y=None, z=None)",
            None,
            None)

        self._strip_non_python_syntax(
            "",
            "",
            None,
            None)

        self._strip_non_python_syntax(
            None,
            None,
            None,
            None)


class TestUnwrap(unittest.TestCase):

    def test_unwrap_one(self):
        def func(a, b):
            return a + b
        wrapper = functools.lru_cache(maxsize=20)(func)
        self.assertIs(inspect.unwrap(wrapper), func)

    def test_unwrap_several(self):
        def func(a, b):
            return a + b
        wrapper = func
        for __ in range(10):
            @functools.wraps(wrapper)
            def wrapper():
                pass
        self.assertIsNot(wrapper.__wrapped__, func)
        self.assertIs(inspect.unwrap(wrapper), func)

    def test_stop(self):
        def func1(a, b):
            return a + b
        @functools.wraps(func1)
        def func2():
            pass
        @functools.wraps(func2)
        def wrapper():
            pass
        func2.stop_here = 1
        unwrapped = inspect.unwrap(wrapper,
                                   stop=(lambda f: hasattr(f, "stop_here")))
        self.assertIs(unwrapped, func2)

    def test_cycle(self):
        def func1(): pass
        func1.__wrapped__ = func1
        with self.assertRaisesRegex(ValueError, 'wrapper loop'):
            inspect.unwrap(func1)

        def func2(): pass
        func2.__wrapped__ = func1
        func1.__wrapped__ = func2
        with self.assertRaisesRegex(ValueError, 'wrapper loop'):
            inspect.unwrap(func1)
        with self.assertRaisesRegex(ValueError, 'wrapper loop'):
            inspect.unwrap(func2)

    def test_unhashable(self):
        def func(): pass
        func.__wrapped__ = None
        class C:
            __hash__ = None
            __wrapped__ = func
        self.assertIsNone(inspect.unwrap(C()))

class TestMain(unittest.TestCase):
    def test_only_source(self):
        module = importlib.import_module('unittest')
        rc, out, err = assert_python_ok('-m', 'inspect',
                                        'unittest')
        lines = out.decode().splitlines()
        
        self.assertEqual(lines[:-1], inspect.getsource(module).splitlines())
        self.assertEqual(err, b'')

    def test_custom_getattr(self):
        def foo():
            pass
        foo.__signature__ = 42
        with self.assertRaises(TypeError):
            inspect.signature(foo)

    @unittest.skipIf(ThreadPoolExecutor is None,
            'threads required to test __qualname__ for source files')
    def test_qualname_source(self):
        rc, out, err = assert_python_ok('-m', 'inspect',
                                     'concurrent.futures:ThreadPoolExecutor')
        lines = out.decode().splitlines()
        
        self.assertEqual(lines[:-1],
                         inspect.getsource(ThreadPoolExecutor).splitlines())
        self.assertEqual(err, b'')

    def test_builtins(self):
        module = importlib.import_module('unittest')
        _, out, err = assert_python_failure('-m', 'inspect',
                                            'sys')
        lines = err.decode().splitlines()
        self.assertEqual(lines, ["Can't get info for builtin modules."])

    def test_details(self):
        module = importlib.import_module('unittest')
        rc, out, err = assert_python_ok('-m', 'inspect',
                                        'unittest', '--details')
        output = out.decode()
        
        self.assertIn(module.__name__, output)
        self.assertIn(module.__file__, output)
        if not sys.flags.optimize:
            self.assertIn(module.__cached__, output)
        self.assertEqual(err, b'')


class TestReload(unittest.TestCase):

    src_before = textwrap.dedent("""\
def foo():
    print("Bla")
    """)

    src_after = textwrap.dedent("""\
def foo():
    print("Oh no!")
    """)

    def assertInspectEqual(self, path, source):
        inspected_src = inspect.getsource(source)
        with open(path) as src:
            self.assertEqual(
                src.read().splitlines(True),
                inspected_src.splitlines(True)
            )

    def test_getsource_reload(self):
        
        with _ready_to_import('reload_bug', self.src_before) as (name, path):
            module = importlib.import_module(name)
            self.assertInspectEqual(path, module)
            with open(path, 'w') as src:
                src.write(self.src_after)
            self.assertInspectEqual(path, module)


def test_main():
    run_unittest(
        TestDecorators, TestRetrievingSourceCode, TestOneliners, TestBuggyCases,
        TestInterpreterStack, TestClassesAndFunctions, TestPredicates,
        TestGetcallargsFunctions, TestGetcallargsMethods,
        TestGetcallargsUnboundMethods, TestGetattrStatic, TestGetGeneratorState,
        TestNoEOL, TestSignatureObject, TestSignatureBind, TestParameterObject,
        TestBoundArguments, TestSignaturePrivateHelpers, TestGetClosureVars,
        TestUnwrap, TestMain, TestReload
    )

if __name__ == "__main__":
    test_main()
