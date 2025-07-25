import contextlib
import copy
import inspect
import pickle
import re
import sys
import types
import unittest
import warnings
from test import support
from test.support.script_helper import assert_python_ok


class AsyncYieldFrom:
    def __init__(self, obj):
        self.obj = obj

    def __await__(self):
        yield from self.obj


class AsyncYield:
    def __init__(self, value):
        self.value = value

    def __await__(self):
        yield self.value


def run_async(coro):
    assert coro.__class__ in {types.GeneratorType, types.CoroutineType}

    buffer = []
    result = None
    while True:
        try:
            buffer.append(coro.send(None))
        except StopIteration as ex:
            result = ex.args[0] if ex.args else None
            break
    return buffer, result


def run_async__await__(coro):
    assert coro.__class__ is types.CoroutineType
    aw = coro.__await__()
    buffer = []
    result = None
    i = 0
    while True:
        try:
            if i % 2:
                buffer.append(next(aw))
            else:
                buffer.append(aw.send(None))
            i += 1
        except StopIteration as ex:
            result = ex.args[0] if ex.args else None
            break
    return buffer, result


@contextlib.contextmanager
def silence_coro_gc():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        yield
        support.gc_collect()


class AsyncBadSyntaxTest(unittest.TestCase):

    def test_badsyntax_1(self):
        samples = [
            """def foo():
                await something()
            """,

            """await something()""",

            """async def foo():
                yield from []
            """,

            """async def foo():
                await await fut
            """,

            """async def foo(a=await something()):
                pass
            """,

            """async def foo(a:await something()):
                pass
            """,

            """async def foo():
                def bar():
                 [i async for i in els]
            """,

            """async def foo():
                def bar():
                 [await i for i in els]
            """,

            """async def foo():
                def bar():
                 [i for i in els
                    async for b in els]
            """,

            """async def foo():
                def bar():
                 [i for i in els
                    for c in b
                    async for b in els]
            """,

            """async def foo():
                def bar():
                 [i for i in els
                    async for b in els
                    for c in b]
            """,

            """async def foo():
                def bar():
                 [i for i in els
                    for b in await els]
            """,

            """async def foo():
                def bar():
                 [i for i in els
                    for b in els
                        if await b]
            """,

            """async def foo():
                def bar():
                 [i for i in await els]
            """,

            """async def foo():
                def bar():
                 [i for i in els if await i]
            """,

            """def bar():
                 [i async for i in els]
            """,

            """def bar():
                 {i: i async for i in els}
            """,

            """def bar():
                 {i async for i in els}
            """,

            """def bar():
                 [await i for i in els]
            """,

            """def bar():
                 [i for i in els
                    async for b in els]
            """,

            """def bar():
                 [i for i in els
                    for c in b
                    async for b in els]
            """,

            """def bar():
                 [i for i in els
                    async for b in els
                    for c in b]
            """,

            """def bar():
                 [i for i in els
                    for b in await els]
            """,

            """def bar():
                 [i for i in els
                    for b in els
                        if await b]
            """,

            """def bar():
                 [i for i in await els]
            """,

            """def bar():
                 [i for i in els if await i]
            """,

            """async def foo():
                await
            """,

            """async def foo():
                   def bar(): pass
                   await = 1
            """,

            """async def foo():

                   def bar(): pass
                   await = 1
            """,

            """async def foo():
                   def bar(): pass
                   if 1:
                       await = 1
            """,

            """def foo():
                   async def bar(): pass
                   if 1:
                       await a
            """,

            """def foo():
                   async def bar(): pass
                   await a
            """,

            """def foo():
                   def baz(): pass
                   async def bar(): pass
                   await a
            """,

            """def foo():
                   def baz(): pass
                   
                   async def bar(): pass
                   
                   await a
            """,

            """async def foo():
                   def baz(): pass
                   
                   async def bar(): pass
                   
                   await = 2
            """,

            """def foo():

                   def baz(): pass

                   async def bar(): pass

                   await a
            """,

            """async def foo():

                   def baz(): pass

                   async def bar(): pass

                   await = 2
            """,

            """async def foo():
                   def async(): pass
            """,

            """async def foo():
                   def await(): pass
            """,

            """async def foo():
                   def bar():
                       await
            """,

            """async def foo():
                   return lambda async: await
            """,

            """async def foo():
                   return lambda a: await
            """,

            """await a()""",

            """async def foo(a=await b):
                   pass
            """,

            """async def foo(a:await b):
                   pass
            """,

            """def baz():
                   async def foo(a=await b):
                       pass
            """,

            """async def foo(async):
                   pass
            """,

            """async def foo():
                   def bar():
                        def baz():
                            async = 1
            """,

            """async def foo():
                   def bar():
                        def baz():
                            pass
                        async = 1
            """,

            """def foo():
                   async def bar():

                        async def baz():
                            pass

                        def baz():
                            42

                        async = 1
            """,

            """async def foo():
                   def bar():
                        def baz():
                            pass\nawait foo()
            """,

            """def foo():
                   def bar():
                        async def baz():
                            pass\nawait foo()
            """,

            """async def foo(await):
                   pass
            """,

            """def foo():

                   async def bar(): pass

                   await a
            """,

            """def foo():
                   async def bar():
                        pass\nawait a
            """,
            """def foo():
                   async for i in arange(2):
                       pass
            """,
            """def foo():
                   async with resource:
                       pass
            """,
            """async with resource:
                   pass
            """,
            """async for i in arange(2):
                   pass
            """,
            ]

        for code in samples:
            with self.subTest(code=code), self.assertRaises(SyntaxError):
                compile(code, "<test>", "exec")

    def test_badsyntax_2(self):
        samples = [
            """def foo():
                await = 1
            """,

            """class Bar:
                def async(): pass
            """,

            """class Bar:
                async = 1
            """,

            """class async:
                pass
            """,

            """class await:
                pass
            """,

            """import math as await""",

            """def async():
                pass""",

            """def foo(*, await=1):
                pass"""

            """async = 1""",

            """print(await=1)"""
        ]

        for code in samples:
            with self.subTest(code=code), self.assertRaises(SyntaxError):
                compile(code, "<test>", "exec")

    def test_badsyntax_3(self):
        with self.assertRaises(SyntaxError):
            compile("async = 1", "<test>", "exec")

    def test_badsyntax_4(self):
        samples = [
            '''def foo(await):
                async def foo(): pass
                async def foo():
                    pass
                return await + 1
            ''',

            '''def foo(await):
                async def foo(): pass
                async def foo(): pass
                return await + 1
            ''',

            '''def foo(await):

                async def foo(): pass

                async def foo(): pass

                return await + 1
            ''',

            '''def foo(await):
                """spam"""
                async def foo(): \
                    pass
                
                async def foo(): pass
                
                return await + 1
            ''',

            '''def foo(await):
                def foo(): pass
                def foo(): pass
                async def bar(): return await_
                await_ = await
                try:
                    bar().send(None)
                except StopIteration as ex:
                    return ex.args[0] + 1
            '''
        ]

        for code in samples:
            with self.subTest(code=code), self.assertRaises(SyntaxError):
                compile(code, "<test>", "exec")


class TokenizerRegrTest(unittest.TestCase):

    def test_oneline_defs(self):
        buf = []
        for i in range(500):
            buf.append('def i{i}(): return {i}'.format(i=i))
        buf = '\n'.join(buf)

        
        ns = {}
        exec(buf, ns, ns)
        self.assertEqual(ns['i499'](), 499)

        
        
        buf += '\nasync def foo():\n    return'
        ns = {}
        exec(buf, ns, ns)
        self.assertEqual(ns['i499'](), 499)
        self.assertTrue(inspect.iscoroutinefunction(ns['foo']))


class CoroutineTest(unittest.TestCase):

    def test_gen_1(self):
        def gen(): yield
        self.assertFalse(hasattr(gen, '__await__'))

    def test_func_1(self):
        async def foo():
            return 10

        f = foo()
        self.assertIsInstance(f, types.CoroutineType)
        self.assertTrue(bool(foo.__code__.co_flags & inspect.CO_COROUTINE))
        self.assertFalse(bool(foo.__code__.co_flags & inspect.CO_GENERATOR))
        self.assertTrue(bool(f.cr_code.co_flags & inspect.CO_COROUTINE))
        self.assertFalse(bool(f.cr_code.co_flags & inspect.CO_GENERATOR))
        self.assertEqual(run_async(f), ([], 10))

        self.assertEqual(run_async__await__(foo()), ([], 10))

        def bar(): pass
        self.assertFalse(bool(bar.__code__.co_flags & inspect.CO_COROUTINE))

    def test_func_2(self):
        async def foo():
            raise StopIteration

        with self.assertRaisesRegex(
                RuntimeError, "coroutine raised StopIteration"):

            run_async(foo())

    def test_func_3(self):
        async def foo():
            raise StopIteration

        coro = foo()
        self.assertRegex(repr(coro), '^<coroutine object.* at 0x.*>$')
        coro.close()

    def test_func_4(self):
        async def foo():
            raise StopIteration
        coro = foo()

        check = lambda: self.assertRaisesRegex(
            TypeError, "'coroutine' object is not iterable")

        with check():
            list(coro)

        with check():
            tuple(coro)

        with check():
            sum(coro)

        with check():
            iter(coro)

        with check():
            for i in coro:
                pass

        with check():
            [i for i in coro]

        coro.close()

    def test_func_5(self):
        @types.coroutine
        def bar():
            yield 1

        async def foo():
            await bar()

        check = lambda: self.assertRaisesRegex(
            TypeError, "'coroutine' object is not iterable")

        coro = foo()
        with check():
            for el in coro:
                pass
        coro.close()

        
        for el in bar():
            self.assertEqual(el, 1)
        self.assertEqual([el for el in bar()], [1])
        self.assertEqual(tuple(bar()), (1,))
        self.assertEqual(next(iter(bar())), 1)

    def test_func_6(self):
        @types.coroutine
        def bar():
            yield 1
            yield 2

        async def foo():
            await bar()

        f = foo()
        self.assertEqual(f.send(None), 1)
        self.assertEqual(f.send(None), 2)
        with self.assertRaises(StopIteration):
            f.send(None)

    def test_func_7(self):
        async def bar():
            return 10
        coro = bar()

        def foo():
            yield from coro

        with self.assertRaisesRegex(
                TypeError,
                "cannot 'yield from' a coroutine object in "
                "a non-coroutine generator"):
            list(foo())

        coro.close()

    def test_func_8(self):
        @types.coroutine
        def bar():
            return (yield from coro)

        async def foo():
            return 'spam'

        coro = foo()
        self.assertEqual(run_async(bar()), ([], 'spam'))
        coro.close()

    def test_func_9(self):
        async def foo():
            pass

        with self.assertWarnsRegex(
                RuntimeWarning,
                r"coroutine '.*test_func_9.*foo' was never awaited"):

            foo()
            support.gc_collect()

        with self.assertWarnsRegex(
                RuntimeWarning,
                r"coroutine '.*test_func_9.*foo' was never awaited"):

            with self.assertRaises(TypeError):
                
                for _ in foo():
                    pass

            support.gc_collect()

    def test_func_10(self):
        N = 0

        @types.coroutine
        def gen():
            nonlocal N
            try:
                a = yield
                yield (a ** 2)
            except ZeroDivisionError:
                N += 100
                raise
            finally:
                N += 1

        async def foo():
            await gen()

        coro = foo()
        aw = coro.__await__()
        self.assertIs(aw, iter(aw))
        next(aw)
        self.assertEqual(aw.send(10), 100)

        self.assertEqual(N, 0)
        aw.close()
        self.assertEqual(N, 1)

        coro = foo()
        aw = coro.__await__()
        next(aw)
        with self.assertRaises(ZeroDivisionError):
            aw.throw(ZeroDivisionError, None, None)
        self.assertEqual(N, 102)

    def test_func_11(self):
        async def func(): pass
        coro = func()
        
        
        self.assertIn('__await__', dir(coro))
        self.assertIn('__iter__', dir(coro.__await__()))
        self.assertIn('coroutine_wrapper', repr(coro.__await__()))
        coro.close() 

    def test_func_12(self):
        async def g():
            i = me.send(None)
            await foo
        me = g()
        with self.assertRaisesRegex(ValueError,
                                    "coroutine already executing"):
            me.send(None)

    def test_func_13(self):
        async def g():
            pass

        coro = g()
        with self.assertRaisesRegex(
                TypeError,
                "can't send non-None value to a just-started coroutine"):
            coro.send('spam')

        coro.close()

    def test_func_14(self):
        @types.coroutine
        def gen():
            yield
        async def coro():
            try:
                await gen()
            except GeneratorExit:
                await gen()
        c = coro()
        c.send(None)
        with self.assertRaisesRegex(RuntimeError,
                                    "coroutine ignored GeneratorExit"):
            c.close()

    def test_func_15(self):
        

        async def spammer():
            return 'spam'
        async def reader(coro):
            return await coro

        spammer_coro = spammer()

        with self.assertRaisesRegex(StopIteration, 'spam'):
            reader(spammer_coro).send(None)

        with self.assertRaisesRegex(RuntimeError,
                                    'cannot reuse already awaited coroutine'):
            reader(spammer_coro).send(None)

    def test_func_16(self):
        

        @types.coroutine
        def nop():
            yield
        async def send():
            await nop()
            return 'spam'
        async def read(coro):
            await nop()
            return await coro

        spammer = send()

        reader = read(spammer)
        reader.send(None)
        reader.send(None)
        with self.assertRaisesRegex(Exception, 'ham'):
            reader.throw(Exception('ham'))

        reader = read(spammer)
        reader.send(None)
        with self.assertRaisesRegex(RuntimeError,
                                    'cannot reuse already awaited coroutine'):
            reader.send(None)

        with self.assertRaisesRegex(RuntimeError,
                                    'cannot reuse already awaited coroutine'):
            reader.throw(Exception('wat'))

    def test_func_17(self):
        

        async def coroutine():
            return 'spam'

        coro = coroutine()
        with self.assertRaisesRegex(StopIteration, 'spam'):
            coro.send(None)

        with self.assertRaisesRegex(RuntimeError,
                                    'cannot reuse already awaited coroutine'):
            coro.send(None)

        with self.assertRaisesRegex(RuntimeError,
                                    'cannot reuse already awaited coroutine'):
            coro.throw(Exception('wat'))

        
        
        coro.close()
        coro.close()

    def test_func_18(self):
        

        async def coroutine():
            return 'spam'

        coro = coroutine()
        await_iter = coro.__await__()
        it = iter(await_iter)

        with self.assertRaisesRegex(StopIteration, 'spam'):
            it.send(None)

        with self.assertRaisesRegex(RuntimeError,
                                    'cannot reuse already awaited coroutine'):
            it.send(None)

        with self.assertRaisesRegex(RuntimeError,
                                    'cannot reuse already awaited coroutine'):
            
            
            
            
            
            
            next(it)

        with self.assertRaisesRegex(RuntimeError,
                                    'cannot reuse already awaited coroutine'):
            it.throw(Exception('wat'))

        with self.assertRaisesRegex(RuntimeError,
                                    'cannot reuse already awaited coroutine'):
            it.throw(Exception('wat'))

        
        
        it.close()
        it.close()

    def test_func_19(self):
        CHK = 0

        @types.coroutine
        def foo():
            nonlocal CHK
            yield
            try:
                yield
            except GeneratorExit:
                CHK += 1

        async def coroutine():
            await foo()

        coro = coroutine()

        coro.send(None)
        coro.send(None)

        self.assertEqual(CHK, 0)
        coro.close()
        self.assertEqual(CHK, 1)

        for _ in range(3):
            
            
            coro.close()
            self.assertEqual(CHK, 1)

    def test_coro_wrapper_send_tuple(self):
        async def foo():
            return (10,)

        result = run_async__await__(foo())
        self.assertEqual(result, ([], (10,)))

    def test_coro_wrapper_send_stop_iterator(self):
        async def foo():
            return StopIteration(10)

        result = run_async__await__(foo())
        self.assertIsInstance(result[1], StopIteration)
        self.assertEqual(result[1].value, 10)

    def test_cr_await(self):
        @types.coroutine
        def a():
            self.assertEqual(inspect.getcoroutinestate(coro_b), inspect.CORO_RUNNING)
            self.assertIsNone(coro_b.cr_await)
            yield
            self.assertEqual(inspect.getcoroutinestate(coro_b), inspect.CORO_RUNNING)
            self.assertIsNone(coro_b.cr_await)

        async def c():
            await a()

        async def b():
            self.assertIsNone(coro_b.cr_await)
            await c()
            self.assertIsNone(coro_b.cr_await)

        coro_b = b()
        self.assertEqual(inspect.getcoroutinestate(coro_b), inspect.CORO_CREATED)
        self.assertIsNone(coro_b.cr_await)

        coro_b.send(None)
        self.assertEqual(inspect.getcoroutinestate(coro_b), inspect.CORO_SUSPENDED)
        self.assertEqual(coro_b.cr_await.cr_await.gi_code.co_name, 'a')

        with self.assertRaises(StopIteration):
            coro_b.send(None)  
        self.assertEqual(inspect.getcoroutinestate(coro_b), inspect.CORO_CLOSED)
        self.assertIsNone(coro_b.cr_await)

    def test_corotype_1(self):
        ct = types.CoroutineType
        self.assertIn('into coroutine', ct.send.__doc__)
        self.assertIn('inside coroutine', ct.close.__doc__)
        self.assertIn('in coroutine', ct.throw.__doc__)
        self.assertIn('of the coroutine', ct.__dict__['__name__'].__doc__)
        self.assertIn('of the coroutine', ct.__dict__['__qualname__'].__doc__)
        self.assertEqual(ct.__name__, 'coroutine')

        async def f(): pass
        c = f()
        self.assertIn('coroutine object', repr(c))
        c.close()

    def test_await_1(self):

        async def foo():
            await 1
        with self.assertRaisesRegex(TypeError, "object int can.t.*await"):
            run_async(foo())

    def test_await_2(self):
        async def foo():
            await []
        with self.assertRaisesRegex(TypeError, "object list can.t.*await"):
            run_async(foo())

    def test_await_3(self):
        async def foo():
            await AsyncYieldFrom([1, 2, 3])

        self.assertEqual(run_async(foo()), ([1, 2, 3], None))
        self.assertEqual(run_async__await__(foo()), ([1, 2, 3], None))

    def test_await_4(self):
        async def bar():
            return 42

        async def foo():
            return await bar()

        self.assertEqual(run_async(foo()), ([], 42))

    def test_await_5(self):
        class Awaitable:
            def __await__(self):
                return

        async def foo():
            return (await Awaitable())

        with self.assertRaisesRegex(
            TypeError, "__await__.*returned non-iterator of type"):

            run_async(foo())

    def test_await_6(self):
        class Awaitable:
            def __await__(self):
                return iter([52])

        async def foo():
            return (await Awaitable())

        self.assertEqual(run_async(foo()), ([52], None))

    def test_await_7(self):
        class Awaitable:
            def __await__(self):
                yield 42
                return 100

        async def foo():
            return (await Awaitable())

        self.assertEqual(run_async(foo()), ([42], 100))

    def test_await_8(self):
        class Awaitable:
            pass

        async def foo(): return await Awaitable()

        with self.assertRaisesRegex(
            TypeError, "object Awaitable can't be used in 'await' expression"):

            run_async(foo())

    def test_await_9(self):
        def wrap():
            return bar

        async def bar():
            return 42

        async def foo():
            db = {'b':  lambda: wrap}

            class DB:
                b = wrap

            return (await bar() + await wrap()() + await db['b']()()() +
                    await bar() * 1000 + await DB.b()())

        async def foo2():
            return -await bar()

        self.assertEqual(run_async(foo()), ([], 42168))
        self.assertEqual(run_async(foo2()), ([], -42))

    def test_await_10(self):
        async def baz():
            return 42

        async def bar():
            return baz()

        async def foo():
            return await (await bar())

        self.assertEqual(run_async(foo()), ([], 42))

    def test_await_11(self):
        def ident(val):
            return val

        async def bar():
            return 'spam'

        async def foo():
            return ident(val=await bar())

        async def foo2():
            return await bar(), 'ham'

        self.assertEqual(run_async(foo2()), ([], ('spam', 'ham')))

    def test_await_12(self):
        async def coro():
            return 'spam'
        c = coro()

        class Awaitable:
            def __await__(self):
                return c

        async def foo():
            return await Awaitable()

        with self.assertRaisesRegex(
                TypeError, r"__await__\(\) returned a coroutine"):
            run_async(foo())

        c.close()

    def test_await_13(self):
        class Awaitable:
            def __await__(self):
                return self

        async def foo():
            return await Awaitable()

        with self.assertRaisesRegex(
            TypeError, "__await__.*returned non-iterator of type"):

            run_async(foo())

    def test_await_14(self):
        class Wrapper:
            
            def __init__(self, coro):
                assert coro.__class__ is types.CoroutineType
                self.coro = coro
            def __await__(self):
                return self.coro.__await__()

        class FutureLike:
            def __await__(self):
                return (yield)

        class Marker(Exception):
            pass

        async def coro1():
            try:
                return await FutureLike()
            except ZeroDivisionError:
                raise Marker
        async def coro2():
            return await Wrapper(coro1())

        c = coro2()
        c.send(None)
        with self.assertRaisesRegex(StopIteration, 'spam'):
            c.send('spam')

        c = coro2()
        c.send(None)
        with self.assertRaises(Marker):
            c.throw(ZeroDivisionError)

    def test_await_15(self):
        @types.coroutine
        def nop():
            yield

        async def coroutine():
            await nop()

        async def waiter(coro):
            await coro

        coro = coroutine()
        coro.send(None)

        with self.assertRaisesRegex(RuntimeError,
                                    "coroutine is being awaited already"):
            waiter(coro).send(None)

    def test_await_16(self):
        

        async def f():
            return ValueError()

        async def g():
            try:
                raise KeyError
            except:
                return await f()

        _, result = run_async(g())
        self.assertIsNone(result.__context__)

    def test_with_1(self):
        class Manager:
            def __init__(self, name):
                self.name = name

            async def __aenter__(self):
                await AsyncYieldFrom(['enter-1-' + self.name,
                                      'enter-2-' + self.name])
                return self

            async def __aexit__(self, *args):
                await AsyncYieldFrom(['exit-1-' + self.name,
                                      'exit-2-' + self.name])

                if self.name == 'B':
                    return True


        async def foo():
            async with Manager("A") as a, Manager("B") as b:
                await AsyncYieldFrom([('managers', a.name, b.name)])
                1/0

        f = foo()
        result, _ = run_async(f)

        self.assertEqual(
            result, ['enter-1-A', 'enter-2-A', 'enter-1-B', 'enter-2-B',
                     ('managers', 'A', 'B'),
                     'exit-1-B', 'exit-2-B', 'exit-1-A', 'exit-2-A']
        )

        async def foo():
            async with Manager("A") as a, Manager("C") as c:
                await AsyncYieldFrom([('managers', a.name, c.name)])
                1/0

        with self.assertRaises(ZeroDivisionError):
            run_async(foo())

    def test_with_2(self):
        class CM:
            def __aenter__(self):
                pass

        async def foo():
            async with CM():
                pass

        with self.assertRaisesRegex(AttributeError, '__aexit__'):
            run_async(foo())

    def test_with_3(self):
        class CM:
            def __aexit__(self):
                pass

        async def foo():
            async with CM():
                pass

        with self.assertRaisesRegex(AttributeError, '__aenter__'):
            run_async(foo())

    def test_with_4(self):
        class CM:
            def __enter__(self):
                pass

            def __exit__(self):
                pass

        async def foo():
            async with CM():
                pass

        with self.assertRaisesRegex(AttributeError, '__aexit__'):
            run_async(foo())

    def test_with_5(self):
        
        
        

        class CM:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *exc):
                pass

        async def func():
            async with CM():
                assert (1, ) == 1

        with self.assertRaises(AssertionError):
            run_async(func())

    def test_with_6(self):
        class CM:
            def __aenter__(self):
                return 123

            def __aexit__(self, *e):
                return 456

        async def foo():
            async with CM():
                pass

        with self.assertRaisesRegex(
                TypeError,
                "'async with' received an object from __aenter__ "
                "that does not implement __await__: int"):
            
            run_async(foo())

    def test_with_7(self):
        class CM:
            async def __aenter__(self):
                return self

            def __aexit__(self, *e):
                return 444

        
        async def foo():
            async with CM():
                1/0

        try:
            run_async(foo())
        except TypeError as exc:
            self.assertRegex(
                exc.args[0],
                "'async with' received an object from __aexit__ "
                "that does not implement __await__: int")
            self.assertTrue(exc.__context__ is not None)
            self.assertTrue(isinstance(exc.__context__, ZeroDivisionError))
        else:
            self.fail('invalid asynchronous context manager did not fail')


    def test_with_8(self):
        CNT = 0

        class CM:
            async def __aenter__(self):
                return self

            def __aexit__(self, *e):
                return 456

        
        async def foo():
            nonlocal CNT
            async with CM():
                CNT += 1
        with self.assertRaisesRegex(
                TypeError,
                "'async with' received an object from __aexit__ "
                "that does not implement __await__: int"):
            run_async(foo())
        self.assertEqual(CNT, 1)

        
        async def foo():
            nonlocal CNT
            for i in range(2):
                async with CM():
                    CNT += 1
                    break
        with self.assertRaisesRegex(
                TypeError,
                "'async with' received an object from __aexit__ "
                "that does not implement __await__: int"):
            run_async(foo())
        self.assertEqual(CNT, 2)

        
        async def foo():
            nonlocal CNT
            for i in range(2):
                async with CM():
                    CNT += 1
                    continue
        with self.assertRaisesRegex(
                TypeError,
                "'async with' received an object from __aexit__ "
                "that does not implement __await__: int"):
            run_async(foo())
        self.assertEqual(CNT, 3)

        
        async def foo():
            nonlocal CNT
            async with CM():
                CNT += 1
                return
        with self.assertRaisesRegex(
                TypeError,
                "'async with' received an object from __aexit__ "
                "that does not implement __await__: int"):
            run_async(foo())
        self.assertEqual(CNT, 4)


    def test_with_9(self):
        CNT = 0

        class CM:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *e):
                1/0

        async def foo():
            nonlocal CNT
            async with CM():
                CNT += 1

        with self.assertRaises(ZeroDivisionError):
            run_async(foo())

        self.assertEqual(CNT, 1)

    def test_with_10(self):
        CNT = 0

        class CM:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *e):
                1/0

        async def foo():
            nonlocal CNT
            async with CM():
                async with CM():
                    raise RuntimeError

        try:
            run_async(foo())
        except ZeroDivisionError as exc:
            self.assertTrue(exc.__context__ is not None)
            self.assertTrue(isinstance(exc.__context__, ZeroDivisionError))
            self.assertTrue(isinstance(exc.__context__.__context__,
                                       RuntimeError))
        else:
            self.fail('exception from __aexit__ did not propagate')

    def test_with_11(self):
        CNT = 0

        class CM:
            async def __aenter__(self):
                raise NotImplementedError

            async def __aexit__(self, *e):
                1/0

        async def foo():
            nonlocal CNT
            async with CM():
                raise RuntimeError

        try:
            run_async(foo())
        except NotImplementedError as exc:
            self.assertTrue(exc.__context__ is None)
        else:
            self.fail('exception from __aenter__ did not propagate')

    def test_with_12(self):
        CNT = 0

        class CM:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *e):
                return True

        async def foo():
            nonlocal CNT
            async with CM() as cm:
                self.assertIs(cm.__class__, CM)
                raise RuntimeError

        run_async(foo())

    def test_with_13(self):
        CNT = 0

        class CM:
            async def __aenter__(self):
                1/0

            async def __aexit__(self, *e):
                return True

        async def foo():
            nonlocal CNT
            CNT += 1
            async with CM():
                CNT += 1000
            CNT += 10000

        with self.assertRaises(ZeroDivisionError):
            run_async(foo())
        self.assertEqual(CNT, 1)

    def test_for_1(self):
        aiter_calls = 0

        class AsyncIter:
            def __init__(self):
                self.i = 0

            def __aiter__(self):
                nonlocal aiter_calls
                aiter_calls += 1
                return self

            async def __anext__(self):
                self.i += 1

                if not (self.i % 10):
                    await AsyncYield(self.i * 10)

                if self.i > 100:
                    raise StopAsyncIteration

                return self.i, self.i


        buffer = []
        async def test1():
            async for i1, i2 in AsyncIter():
                buffer.append(i1 + i2)

        yielded, _ = run_async(test1())
        
        self.assertEqual(aiter_calls, 1)
        self.assertEqual(yielded, [i * 100 for i in range(1, 11)])
        self.assertEqual(buffer, [i*2 for i in range(1, 101)])


        buffer = []
        async def test2():
            nonlocal buffer
            async for i in AsyncIter():
                buffer.append(i[0])
                if i[0] == 20:
                    break
            else:
                buffer.append('what?')
            buffer.append('end')

        yielded, _ = run_async(test2())
        
        self.assertEqual(aiter_calls, 2)
        self.assertEqual(yielded, [100, 200])
        self.assertEqual(buffer, [i for i in range(1, 21)] + ['end'])


        buffer = []
        async def test3():
            nonlocal buffer
            async for i in AsyncIter():
                if i[0] > 20:
                    continue
                buffer.append(i[0])
            else:
                buffer.append('what?')
            buffer.append('end')

        yielded, _ = run_async(test3())
        
        self.assertEqual(aiter_calls, 3)
        self.assertEqual(yielded, [i * 100 for i in range(1, 11)])
        self.assertEqual(buffer, [i for i in range(1, 21)] +
                                 ['what?', 'end'])

    def test_for_2(self):
        tup = (1, 2, 3)
        refs_before = sys.getrefcount(tup)

        async def foo():
            async for i in tup:
                print('never going to happen')

        with self.assertRaisesRegex(
                TypeError, "async for' requires an object.*__aiter__.*tuple"):

            run_async(foo())

        self.assertEqual(sys.getrefcount(tup), refs_before)

    def test_for_3(self):
        class I:
            def __aiter__(self):
                return self

        aiter = I()
        refs_before = sys.getrefcount(aiter)

        async def foo():
            async for i in aiter:
                print('never going to happen')

        with self.assertRaisesRegex(
                TypeError,
                r"that does not implement __anext__"):

            run_async(foo())

        self.assertEqual(sys.getrefcount(aiter), refs_before)

    def test_for_4(self):
        class I:
            def __aiter__(self):
                return self

            def __anext__(self):
                return ()

        aiter = I()
        refs_before = sys.getrefcount(aiter)

        async def foo():
            async for i in aiter:
                print('never going to happen')

        with self.assertRaisesRegex(
                TypeError,
                "async for' received an invalid object.*__anext__.*tuple"):

            run_async(foo())

        self.assertEqual(sys.getrefcount(aiter), refs_before)

    def test_for_6(self):
        I = 0

        class Manager:
            async def __aenter__(self):
                nonlocal I
                I += 10000

            async def __aexit__(self, *args):
                nonlocal I
                I += 100000

        class Iterable:
            def __init__(self):
                self.i = 0

            def __aiter__(self):
                return self

            async def __anext__(self):
                if self.i > 10:
                    raise StopAsyncIteration
                self.i += 1
                return self.i

        

        manager = Manager()
        iterable = Iterable()
        mrefs_before = sys.getrefcount(manager)
        irefs_before = sys.getrefcount(iterable)

        async def main():
            nonlocal I

            async with manager:
                async for i in iterable:
                    I += 1
            I += 1000

        with warnings.catch_warnings():
            warnings.simplefilter("error")
            
            
            run_async(main())
        self.assertEqual(I, 111011)

        self.assertEqual(sys.getrefcount(manager), mrefs_before)
        self.assertEqual(sys.getrefcount(iterable), irefs_before)

        

        async def main():
            nonlocal I

            async with Manager():
                async for i in Iterable():
                    I += 1
            I += 1000

            async with Manager():
                async for i in Iterable():
                    I += 1
            I += 1000

        run_async(main())
        self.assertEqual(I, 333033)

        

        async def main():
            nonlocal I

            async with Manager():
                I += 100
                async for i in Iterable():
                    I += 1
                else:
                    I += 10000000
            I += 1000

            async with Manager():
                I += 100
                async for i in Iterable():
                    I += 1
                else:
                    I += 10000000
            I += 1000

        run_async(main())
        self.assertEqual(I, 20555255)

    def test_for_7(self):
        CNT = 0
        class AI:
            def __aiter__(self):
                1/0
        async def foo():
            nonlocal CNT
            async for i in AI():
                CNT += 1
            CNT += 10
        with self.assertRaises(ZeroDivisionError):
            run_async(foo())
        self.assertEqual(CNT, 0)

    def test_for_8(self):
        CNT = 0
        class AI:
            def __aiter__(self):
                1/0
        async def foo():
            nonlocal CNT
            async for i in AI():
                CNT += 1
            CNT += 10
        with self.assertRaises(ZeroDivisionError):
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                
                
                run_async(foo())
        self.assertEqual(CNT, 0)

    def test_for_11(self):
        class F:
            def __aiter__(self):
                return self
            def __anext__(self):
                return self
            def __await__(self):
                1 / 0

        async def main():
            async for _ in F():
                pass

        with self.assertRaisesRegex(TypeError,
                                    'an invalid object from __anext__') as c:
            main().send(None)

        err = c.exception
        self.assertIsInstance(err.__cause__, ZeroDivisionError)

    def test_for_tuple(self):
        class Done(Exception): pass

        class AIter(tuple):
            i = 0
            def __aiter__(self):
                return self
            async def __anext__(self):
                if self.i >= len(self):
                    raise StopAsyncIteration
                self.i += 1
                return self[self.i - 1]

        result = []
        async def foo():
            async for i in AIter([42]):
                result.append(i)
            raise Done

        with self.assertRaises(Done):
            foo().send(None)
        self.assertEqual(result, [42])

    def test_for_stop_iteration(self):
        class Done(Exception): pass

        class AIter(StopIteration):
            i = 0
            def __aiter__(self):
                return self
            async def __anext__(self):
                if self.i:
                    raise StopAsyncIteration
                self.i += 1
                return self.value

        result = []
        async def foo():
            async for i in AIter(42):
                result.append(i)
            raise Done

        with self.assertRaises(Done):
            foo().send(None)
        self.assertEqual(result, [42])

    def test_comp_1(self):
        async def f(i):
            return i

        async def run_list():
            return [await c for c in [f(1), f(41)]]

        async def run_set():
            return {await c for c in [f(1), f(41)]}

        async def run_dict1():
            return {await c: 'a' for c in [f(1), f(41)]}

        async def run_dict2():
            return {i: await c for i, c in enumerate([f(1), f(41)])}

        self.assertEqual(run_async(run_list()), ([], [1, 41]))
        self.assertEqual(run_async(run_set()), ([], {1, 41}))
        self.assertEqual(run_async(run_dict1()), ([], {1: 'a', 41: 'a'}))
        self.assertEqual(run_async(run_dict2()), ([], {0: 1, 1: 41}))

    def test_comp_2(self):
        async def f(i):
            return i

        async def run_list():
            return [s for c in [f(''), f('abc'), f(''), f(['de', 'fg'])]
                    for s in await c]

        self.assertEqual(
            run_async(run_list()),
            ([], ['a', 'b', 'c', 'de', 'fg']))

        async def run_set():
            return {d
                    for c in [f([f([10, 30]),
                                 f([20])])]
                    for s in await c
                    for d in await s}

        self.assertEqual(
            run_async(run_set()),
            ([], {10, 20, 30}))

        async def run_set2():
            return {await s
                    for c in [f([f(10), f(20)])]
                    for s in await c}

        self.assertEqual(
            run_async(run_set2()),
            ([], {10, 20}))

    def test_comp_3(self):
        async def f(it):
            for i in it:
                yield i

        async def run_list():
            return [i + 1 async for i in f([10, 20])]
        self.assertEqual(
            run_async(run_list()),
            ([], [11, 21]))

        async def run_set():
            return {i + 1 async for i in f([10, 20])}
        self.assertEqual(
            run_async(run_set()),
            ([], {11, 21}))

        async def run_dict():
            return {i + 1: i + 2 async for i in f([10, 20])}
        self.assertEqual(
            run_async(run_dict()),
            ([], {11: 12, 21: 22}))

        async def run_gen():
            gen = (i + 1 async for i in f([10, 20]))
            return [g + 100 async for g in gen]
        self.assertEqual(
            run_async(run_gen()),
            ([], [111, 121]))

    def test_comp_4(self):
        async def f(it):
            for i in it:
                yield i

        async def run_list():
            return [i + 1 async for i in f([10, 20]) if i > 10]
        self.assertEqual(
            run_async(run_list()),
            ([], [21]))

        async def run_set():
            return {i + 1 async for i in f([10, 20]) if i > 10}
        self.assertEqual(
            run_async(run_set()),
            ([], {21}))

        async def run_dict():
            return {i + 1: i + 2 async for i in f([10, 20]) if i > 10}
        self.assertEqual(
            run_async(run_dict()),
            ([], {21: 22}))

        async def run_gen():
            gen = (i + 1 async for i in f([10, 20]) if i > 10)
            return [g + 100 async for g in gen]
        self.assertEqual(
            run_async(run_gen()),
            ([], [121]))

    def test_comp_4_2(self):
        async def f(it):
            for i in it:
                yield i

        async def run_list():
            return [i + 10 async for i in f(range(5)) if 0 < i < 4]
        self.assertEqual(
            run_async(run_list()),
            ([], [11, 12, 13]))

        async def run_set():
            return {i + 10 async for i in f(range(5)) if 0 < i < 4}
        self.assertEqual(
            run_async(run_set()),
            ([], {11, 12, 13}))

        async def run_dict():
            return {i + 10: i + 100 async for i in f(range(5)) if 0 < i < 4}
        self.assertEqual(
            run_async(run_dict()),
            ([], {11: 101, 12: 102, 13: 103}))

        async def run_gen():
            gen = (i + 10 async for i in f(range(5)) if 0 < i < 4)
            return [g + 100 async for g in gen]
        self.assertEqual(
            run_async(run_gen()),
            ([], [111, 112, 113]))

    def test_comp_5(self):
        async def f(it):
            for i in it:
                yield i

        async def run_list():
            return [i + 1 for pair in ([10, 20], [30, 40]) if pair[0] > 10
                    async for i in f(pair) if i > 30]
        self.assertEqual(
            run_async(run_list()),
            ([], [41]))

    def test_comp_6(self):
        async def f(it):
            for i in it:
                yield i

        async def run_list():
            return [i + 1 async for seq in f([(10, 20), (30,)])
                    for i in seq]

        self.assertEqual(
            run_async(run_list()),
            ([], [11, 21, 31]))

    def test_comp_7(self):
        async def f():
            yield 1
            yield 2
            raise Exception('aaa')

        async def run_list():
            return [i async for i in f()]

        with self.assertRaisesRegex(Exception, 'aaa'):
            run_async(run_list())

    def test_comp_8(self):
        async def f():
            return [i for i in [1, 2, 3]]

        self.assertEqual(
            run_async(f()),
            ([], [1, 2, 3]))

    def test_comp_9(self):
        async def gen():
            yield 1
            yield 2
        async def f():
            l = [i async for i in gen()]
            return [i for i in l]

        self.assertEqual(
            run_async(f()),
            ([], [1, 2]))

    def test_comp_10(self):
        async def f():
            xx = {i for i in [1, 2, 3]}
            return {x: x for x in xx}

        self.assertEqual(
            run_async(f()),
            ([], {1: 1, 2: 2, 3: 3}))

    def test_copy(self):
        async def func(): pass
        coro = func()
        with self.assertRaises(TypeError):
            copy.copy(coro)

        aw = coro.__await__()
        try:
            with self.assertRaises(TypeError):
                copy.copy(aw)
        finally:
            aw.close()

    def test_pickle(self):
        async def func(): pass
        coro = func()
        for proto in range(pickle.HIGHEST_PROTOCOL + 1):
            with self.assertRaises((TypeError, pickle.PicklingError)):
                pickle.dumps(coro, proto)

        aw = coro.__await__()
        try:
            for proto in range(pickle.HIGHEST_PROTOCOL + 1):
                with self.assertRaises((TypeError, pickle.PicklingError)):
                    pickle.dumps(aw, proto)
        finally:
            aw.close()

    def test_fatal_coro_warning(self):
        
        async def func(): pass
        with warnings.catch_warnings(), support.captured_stderr() as stderr:
            warnings.filterwarnings("error")
            func()
            support.gc_collect()
        self.assertIn("was never awaited", stderr.getvalue())


class CoroAsyncIOCompatTest(unittest.TestCase):

    def test_asyncio_1(self):
        
        
        asyncio = support.import_module('asyncio')

        class MyException(Exception):
            pass

        buffer = []

        class CM:
            async def __aenter__(self):
                buffer.append(1)
                await asyncio.sleep(0.01)
                buffer.append(2)
                return self

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                await asyncio.sleep(0.01)
                buffer.append(exc_type.__name__)

        async def f():
            async with CM() as c:
                await asyncio.sleep(0.01)
                raise MyException
            buffer.append('unreachable')

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(f())
        except MyException:
            pass
        finally:
            loop.close()
            asyncio.set_event_loop(None)

        self.assertEqual(buffer, [1, 2, 'MyException'])


class SysSetCoroWrapperTest(unittest.TestCase):

    def test_set_wrapper_1(self):
        async def foo():
            return 'spam'

        wrapped = None
        def wrap(gen):
            nonlocal wrapped
            wrapped = gen
            return gen

        with self.assertWarns(DeprecationWarning):
            self.assertIsNone(sys.get_coroutine_wrapper())

        with self.assertWarns(DeprecationWarning):
            sys.set_coroutine_wrapper(wrap)
        with self.assertWarns(DeprecationWarning):
            self.assertIs(sys.get_coroutine_wrapper(), wrap)
        try:
            f = foo()
            self.assertTrue(wrapped)

            self.assertEqual(run_async(f), ([], 'spam'))
        finally:
            with self.assertWarns(DeprecationWarning):
                sys.set_coroutine_wrapper(None)
            f.close()

        with self.assertWarns(DeprecationWarning):
            self.assertIsNone(sys.get_coroutine_wrapper())

        wrapped = None
        coro = foo()
        self.assertFalse(wrapped)
        coro.close()

    def test_set_wrapper_2(self):
        with self.assertWarns(DeprecationWarning):
            self.assertIsNone(sys.get_coroutine_wrapper())
        with self.assertRaisesRegex(TypeError, "callable expected, got int"):
            with self.assertWarns(DeprecationWarning):
                sys.set_coroutine_wrapper(1)
        with self.assertWarns(DeprecationWarning):
            self.assertIsNone(sys.get_coroutine_wrapper())

    def test_set_wrapper_3(self):
        async def foo():
            return 'spam'

        def wrapper(coro):
            async def wrap(coro):
                return await coro
            return wrap(coro)

        with self.assertWarns(DeprecationWarning):
            sys.set_coroutine_wrapper(wrapper)
        try:
            with silence_coro_gc(), self.assertRaisesRegex(
                    RuntimeError,
                    r"coroutine wrapper.*\.wrapper at 0x.*attempted to "
                    r"recursively wrap .* wrap .*"):

                foo()

        finally:
            with self.assertWarns(DeprecationWarning):
                sys.set_coroutine_wrapper(None)

    def test_set_wrapper_4(self):
        @types.coroutine
        def foo():
            return 'spam'

        wrapped = None
        def wrap(gen):
            nonlocal wrapped
            wrapped = gen
            return gen

        with self.assertWarns(DeprecationWarning):
            sys.set_coroutine_wrapper(wrap)
        try:
            foo()
            self.assertIs(
                wrapped, None,
                "generator-based coroutine was wrapped via "
                "sys.set_coroutine_wrapper")
        finally:
            with self.assertWarns(DeprecationWarning):
                sys.set_coroutine_wrapper(None)


class OriginTrackingTest(unittest.TestCase):
    def here(self):
        info = inspect.getframeinfo(inspect.currentframe().f_back)
        return (info.filename, info.lineno)

    def test_origin_tracking(self):
        orig_depth = sys.get_coroutine_origin_tracking_depth()
        try:
            async def corofn():
                pass

            sys.set_coroutine_origin_tracking_depth(0)
            self.assertEqual(sys.get_coroutine_origin_tracking_depth(), 0)

            with contextlib.closing(corofn()) as coro:
                self.assertIsNone(coro.cr_origin)

            sys.set_coroutine_origin_tracking_depth(1)
            self.assertEqual(sys.get_coroutine_origin_tracking_depth(), 1)

            fname, lineno = self.here()
            with contextlib.closing(corofn()) as coro:
                self.assertEqual(coro.cr_origin,
                                 ((fname, lineno + 1, "test_origin_tracking"),))

            sys.set_coroutine_origin_tracking_depth(2)
            self.assertEqual(sys.get_coroutine_origin_tracking_depth(), 2)

            def nested():
                return (self.here(), corofn())
            fname, lineno = self.here()
            ((nested_fname, nested_lineno), coro) = nested()
            with contextlib.closing(coro):
                self.assertEqual(coro.cr_origin,
                                 ((nested_fname, nested_lineno, "nested"),
                                  (fname, lineno + 1, "test_origin_tracking")))

            
            sys.set_coroutine_origin_tracking_depth(1000)
            with contextlib.closing(corofn()) as coro:
                self.assertTrue(2 < len(coro.cr_origin) < 1000)

            
            with self.assertRaises(ValueError):
                sys.set_coroutine_origin_tracking_depth(-1)
            
            self.assertEqual(sys.get_coroutine_origin_tracking_depth(), 1000)

        finally:
            sys.set_coroutine_origin_tracking_depth(orig_depth)

    def test_origin_tracking_warning(self):
        async def corofn():
            pass

        a1_filename, a1_lineno = self.here()
        def a1():
            return corofn()  
        a1_lineno += 2

        a2_filename, a2_lineno = self.here()
        def a2():
            return a1()  
        a2_lineno += 2

        def check(depth, msg):
            sys.set_coroutine_origin_tracking_depth(depth)
            with self.assertWarns(RuntimeWarning) as cm:
                a2()
                support.gc_collect()
            self.assertEqual(msg, str(cm.warning))

        orig_depth = sys.get_coroutine_origin_tracking_depth()
        try:
            msg = check(0, f"coroutine '{corofn.__qualname__}' was never awaited")
            check(1, "".join([
                f"coroutine '{corofn.__qualname__}' was never awaited\n",
                "Coroutine created at (most recent call last)\n",
                f'  File "{a1_filename}", line {a1_lineno}, in a1\n',
                f'    return corofn()  
            ]))
            check(2, "".join([
                f"coroutine '{corofn.__qualname__}' was never awaited\n",
                "Coroutine created at (most recent call last)\n",
                f'  File "{a2_filename}", line {a2_lineno}, in a2\n',
                f'    return a1()  
                f'  File "{a1_filename}", line {a1_lineno}, in a1\n',
                f'    return corofn()  
            ]))

        finally:
            sys.set_coroutine_origin_tracking_depth(orig_depth)

    def test_unawaited_warning_when_module_broken(self):
        
        
        
        async def corofn():
            pass

        orig_wuc = warnings._warn_unawaited_coroutine
        try:
            warnings._warn_unawaited_coroutine = lambda coro: 1/0
            with support.captured_stderr() as stream:
                corofn()
                support.gc_collect()
            self.assertIn("Exception ignored in", stream.getvalue())
            self.assertIn("ZeroDivisionError", stream.getvalue())
            self.assertIn("was never awaited", stream.getvalue())

            del warnings._warn_unawaited_coroutine
            with support.captured_stderr() as stream:
                corofn()
                support.gc_collect()
            self.assertIn("was never awaited", stream.getvalue())

        finally:
            warnings._warn_unawaited_coroutine = orig_wuc


class UnawaitedWarningDuringShutdownTest(unittest.TestCase):
    
    def test_unawaited_warning_during_shutdown(self):
        code = ("import asyncio\n"
                "async def f(): pass\n"
                "asyncio.gather(f())\n")
        assert_python_ok("-c", code)

        code = ("import sys\n"
                "async def f(): pass\n"
                "sys.coro = f()\n")
        assert_python_ok("-c", code)

        code = ("import sys\n"
                "async def f(): pass\n"
                "sys.corocycle = [f()]\n"
                "sys.corocycle.append(sys.corocycle)\n")
        assert_python_ok("-c", code)


@support.cpython_only
class CAPITest(unittest.TestCase):

    def test_tp_await_1(self):
        from _testcapi import awaitType as at

        async def foo():
            future = at(iter([1]))
            return (await future)

        self.assertEqual(foo().send(None), 1)

    def test_tp_await_2(self):
        
        from _testcapi import awaitType as at
        future = at(iter([1]))
        self.assertEqual(next(future.__await__()), 1)

    def test_tp_await_3(self):
        from _testcapi import awaitType as at

        async def foo():
            future = at(1)
            return (await future)

        with self.assertRaisesRegex(
                TypeError, "__await__.*returned non-iterator of type 'int'"):
            self.assertEqual(foo().send(None), 1)


if __name__=="__main__":
    unittest.main()
