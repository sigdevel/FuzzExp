

"License");






"AS IS" BASIS,




"""Tests for absl.testing.parameterized."""

from collections import abc
import sys
import unittest

from absl.testing import absltest
from absl.testing import parameterized


class MyOwnClass(object):
  pass


def dummy_decorator(method):

  def decorated(*args, **kwargs):
    return method(*args, **kwargs)

  return decorated


def dict_decorator(key, value):
  """Sample implementation of a chained decorator.

  Sets a single field in a dict on a test with a dict parameter.
  Uses the exposed '_ParameterizedTestIter.testcases' field to
  modify arguments from previous decorators to allow decorator chains.

  Args:
    key: key to map to
    value: value to set

  Returns:
    The test decorator
  """
  def decorator(test_method):
    
    if isinstance(test_method, abc.Iterable):
      actual_tests = []
      for old_test in test_method.testcases:
        
        new_dict = old_test[1].copy()
        new_dict[key] = value
        test_suffix = '%s_%s_%s' % (old_test[0], key, value)
        actual_tests.append((test_suffix, new_dict))

      test_method.testcases = actual_tests
      return test_method
    else:
      test_suffix = ('_%s_%s') % (key, value)
      tests_to_make = ((test_suffix, {key: value}),)
      
      return parameterized.named_parameters(*tests_to_make)(test_method)
  return decorator


class ParameterizedTestsTest(absltest.TestCase):
  
  

  class GoodAdditionParams(parameterized.TestCase):

    @parameterized.parameters(
        (1, 2, 3),
        (4, 5, 9))
    def test_addition(self, op1, op2, result):
      self.arguments = (op1, op2, result)
      self.assertEqual(result, op1 + op2)

  
  class BadAdditionParams(absltest.TestCase):

    @parameterized.parameters(
        (1, 2, 3),
        (4, 5, 9))
    def test_addition(self, op1, op2, result):
      pass  

  class MixedAdditionParams(parameterized.TestCase):

    @parameterized.parameters(
        (1, 2, 1),
        (4, 5, 9))
    def test_addition(self, op1, op2, result):
      self.arguments = (op1, op2, result)
      self.assertEqual(result, op1 + op2)

  class DictionaryArguments(parameterized.TestCase):

    @parameterized.parameters(
        {'op1': 1, 'op2': 2, 'result': 3},
        {'op1': 4, 'op2': 5, 'result': 9})
    def test_addition(self, op1, op2, result):
      self.assertEqual(result, op1 + op2)

  class NoParameterizedTests(parameterized.TestCase):
    
    a = 'BCD'
    
    testInstanceMember = None  
    test_instance_member = None

    
    testString = 'foo'  
    test_string = 'foo'

    
    def someGenerator(self):  
      yield
      yield
      yield

    def some_generator(self):
      yield
      yield
      yield

    
    def testGenerator(self):
      yield
      yield
      yield

    def test_generator(self):
      yield
      yield
      yield

    def testNormal(self):
      self.assertEqual(3, 1 + 2)

    def test_normal(self):
      self.assertEqual(3, 1 + 2)

  class ArgumentsWithAddresses(parameterized.TestCase):

    @parameterized.parameters(
        (object(),),
        (MyOwnClass(),),
    )
    def test_something(self, case):
      pass

  class CamelCaseNamedTests(parameterized.TestCase):

    @parameterized.named_parameters(
        ('Interesting', 0),
    )
    def testSingle(self, case):
      pass

    @parameterized.named_parameters(
        {'testcase_name': 'Interesting', 'case': 0},
    )
    def testDictSingle(self, case):
      pass

    @parameterized.named_parameters(
        ('Interesting', 0),
        ('Boring', 1),
    )
    def testSomething(self, case):
      pass

    @parameterized.named_parameters(
        {'testcase_name': 'Interesting', 'case': 0},
        {'testcase_name': 'Boring', 'case': 1},
    )
    def testDictSomething(self, case):
      pass

    @parameterized.named_parameters(
        {'testcase_name': 'Interesting', 'case': 0},
        ('Boring', 1),
    )
    def testMixedSomething(self, case):
      pass

    def testWithoutParameters(self):
      pass

  class NamedTests(parameterized.TestCase):
    """Example tests using PEP-8 style names instead of camel-case."""

    @parameterized.named_parameters(
        ('interesting', 0),
    )
    def test_single(self, case):
      pass

    @parameterized.named_parameters(
        {'testcase_name': 'interesting', 'case': 0},
    )
    def test_dict_single(self, case):
      pass

    @parameterized.named_parameters(
        ('interesting', 0),
        ('boring', 1),
    )
    def test_something(self, case):
      pass

    @parameterized.named_parameters(
        {'testcase_name': 'interesting', 'case': 0},
        {'testcase_name': 'boring', 'case': 1},
    )
    def test_dict_something(self, case):
      pass

    @parameterized.named_parameters(
        {'testcase_name': 'interesting', 'case': 0},
        ('boring', 1),
    )
    def test_mixed_something(self, case):
      pass

    def test_without_parameters(self):
      pass

  class ChainedTests(parameterized.TestCase):

    @dict_decorator('cone', 'waffle')
    @dict_decorator('flavor', 'strawberry')
    def test_chained(self, dictionary):
      self.assertDictEqual(dictionary, {'cone': 'waffle',
                                        'flavor': 'strawberry'})

  class SingletonListExtraction(parameterized.TestCase):

    @parameterized.parameters(
        (i, i * 2) for i in range(10))
    def test_something(self, unused_1, unused_2):
      pass

  class SingletonArgumentExtraction(parameterized.TestCase):

    @parameterized.parameters(1, 2, 3, 4, 5, 6)
    def test_numbers(self, unused_1):
      pass

    @parameterized.parameters('foo', 'bar', 'baz')
    def test_strings(self, unused_1):
      pass

  class SingletonDictArgument(parameterized.TestCase):

    @parameterized.parameters({'op1': 1, 'op2': 2})
    def test_something(self, op1, op2):
      del op1, op2

  @parameterized.parameters(
      (1, 2, 3),
      (4, 5, 9))
  class DecoratedClass(parameterized.TestCase):

    def test_add(self, arg1, arg2, arg3):
      self.assertEqual(arg1 + arg2, arg3)

    def test_subtract_fail(self, arg1, arg2, arg3):
      self.assertEqual(arg3 + arg2, arg1)

  @parameterized.parameters(
      (a, b, a+b) for a in range(1, 5) for b in range(1, 5))
  class GeneratorDecoratedClass(parameterized.TestCase):

    def test_add(self, arg1, arg2, arg3):
      self.assertEqual(arg1 + arg2, arg3)

    def test_subtract_fail(self, arg1, arg2, arg3):
      self.assertEqual(arg3 + arg2, arg1)

  @parameterized.parameters(
      (1, 2, 3),
      (4, 5, 9),
  )
  class DecoratedBareClass(absltest.TestCase):

    def test_add(self, arg1, arg2, arg3):
      self.assertEqual(arg1 + arg2, arg3)

  class OtherDecoratorUnnamed(parameterized.TestCase):

    @dummy_decorator
    @parameterized.parameters((1), (2))
    def test_other_then_parameterized(self, arg1):
      pass

    @parameterized.parameters((1), (2))
    @dummy_decorator
    def test_parameterized_then_other(self, arg1):
      pass

  class OtherDecoratorNamed(parameterized.TestCase):

    @dummy_decorator
    @parameterized.named_parameters(('a', 1), ('b', 2))
    def test_other_then_parameterized(self, arg1):
      pass

    @parameterized.named_parameters(('a', 1), ('b', 2))
    @dummy_decorator
    def test_parameterized_then_other(self, arg1):
      pass

  class OtherDecoratorNamedWithDict(parameterized.TestCase):

    @dummy_decorator
    @parameterized.named_parameters(
        {'testcase_name': 'a', 'arg1': 1},
        {'testcase_name': 'b', 'arg1': 2})
    def test_other_then_parameterized(self, arg1):
      pass

    @parameterized.named_parameters(
        {'testcase_name': 'a', 'arg1': 1},
        {'testcase_name': 'b', 'arg1': 2})
    @dummy_decorator
    def test_parameterized_then_other(self, arg1):
      pass

  class UniqueDescriptiveNamesTest(parameterized.TestCase):

    @parameterized.parameters(13, 13)
    def test_normal(self, number):
      del number

  class MultiGeneratorsTestCase(parameterized.TestCase):

    @parameterized.parameters((i for i in (1, 2, 3)), (i for i in (3, 2, 1)))
    def test_sum(self, a, b, c):
      self.assertEqual(6, sum([a, b, c]))

  class NamedParametersReusableTestCase(parameterized.TestCase):
    named_params_a = (
        {'testcase_name': 'dict_a', 'unused_obj': 0},
        ('list_a', 1),
    )
    named_params_b = (
        {'testcase_name': 'dict_b', 'unused_obj': 2},
        ('list_b', 3),
    )
    named_params_c = (
        {'testcase_name': 'dict_c', 'unused_obj': 4},
        ('list_b', 5),
    )

    @parameterized.named_parameters(*(named_params_a + named_params_b))
    def testSomething(self, unused_obj):
      pass

    @parameterized.named_parameters(*(named_params_a + named_params_c))
    def testSomethingElse(self, unused_obj):
      pass

  class SuperclassTestCase(parameterized.TestCase):

    @parameterized.parameters('foo', 'bar')
    def test_name(self, name):
      del name

  class SubclassTestCase(SuperclassTestCase):
    pass

  @unittest.skipIf(
      (sys.version_info[:2] == (3, 7) and sys.version_info[2] in {0, 1, 2}),
      'Python 3.7.0 to 3.7.2 have a bug that breaks this test, see '
      'https://bugs.python.org/issue35767')
  def test_missing_inheritance(self):
    ts = unittest.makeSuite(self.BadAdditionParams)
    self.assertEqual(1, ts.countTestCases())

    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(1, res.testsRun)
    self.assertFalse(res.wasSuccessful())
    self.assertIn('without having inherited', str(res.errors[0]))

  def test_correct_extraction_numbers(self):
    ts = unittest.makeSuite(self.GoodAdditionParams)
    self.assertEqual(2, ts.countTestCases())

  def test_successful_execution(self):
    ts = unittest.makeSuite(self.GoodAdditionParams)

    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(2, res.testsRun)
    self.assertTrue(res.wasSuccessful())

  def test_correct_arguments(self):
    ts = unittest.makeSuite(self.GoodAdditionParams)
    res = unittest.TestResult()

    params = set([
        (1, 2, 3),
        (4, 5, 9)])
    for test in ts:
      test(res)
      self.assertIn(test.arguments, params)
      params.remove(test.arguments)
    self.assertEmpty(params)

  def test_recorded_failures(self):
    ts = unittest.makeSuite(self.MixedAdditionParams)
    self.assertEqual(2, ts.countTestCases())

    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(2, res.testsRun)
    self.assertFalse(res.wasSuccessful())
    self.assertLen(res.failures, 1)
    self.assertEmpty(res.errors)

  def test_short_description(self):
    ts = unittest.makeSuite(self.GoodAdditionParams)
    short_desc = list(ts)[0].shortDescription()

    location = unittest.util.strclass(self.GoodAdditionParams).replace(
        '__main__.', '')
    expected = ('{}.test_addition0 (1, 2, 3)\n'.format(location) +
                'test_addition(1, 2, 3)')
    self.assertEqual(expected, short_desc)

  def test_short_description_addresses_removed(self):
    ts = unittest.makeSuite(self.ArgumentsWithAddresses)
    short_desc = list(ts)[0].shortDescription().split('\n')
    self.assertEqual(
        'test_something(<object>)', short_desc[1])
    short_desc = list(ts)[1].shortDescription().split('\n')
    self.assertEqual(
        'test_something(<__main__.MyOwnClass>)', short_desc[1])

  def test_id(self):
    ts = unittest.makeSuite(self.ArgumentsWithAddresses)
    self.assertEqual(
        (unittest.util.strclass(self.ArgumentsWithAddresses) +
         '.test_something0 (<object>)'),
        list(ts)[0].id())
    ts = unittest.makeSuite(self.GoodAdditionParams)
    self.assertEqual(
        (unittest.util.strclass(self.GoodAdditionParams) +
         '.test_addition0 (1, 2, 3)'),
        list(ts)[0].id())

  def test_str(self):
    ts = unittest.makeSuite(self.GoodAdditionParams)
    test = list(ts)[0]

    expected = 'test_addition0 (1, 2, 3) ({})'.format(
        unittest.util.strclass(self.GoodAdditionParams))
    self.assertEqual(expected, str(test))

  def test_dict_parameters(self):
    ts = unittest.makeSuite(self.DictionaryArguments)
    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(2, res.testsRun)
    self.assertTrue(res.wasSuccessful())

  def test_no_parameterized_tests(self):
    ts = unittest.makeSuite(self.NoParameterizedTests)
    self.assertEqual(4, ts.countTestCases())
    short_descs = [x.shortDescription() for x in list(ts)]
    full_class_name = unittest.util.strclass(self.NoParameterizedTests)
    full_class_name = full_class_name.replace('__main__.', '')
    self.assertSameElements(
        [
            '{}.testGenerator'.format(full_class_name),
            '{}.test_generator'.format(full_class_name),
            '{}.testNormal'.format(full_class_name),
            '{}.test_normal'.format(full_class_name),
        ],
        short_descs)

  def test_successful_product_test_testgrid(self):

    class GoodProductTestCase(parameterized.TestCase):

      @parameterized.product(
          num=(0, 20, 80),
          modulo=(2, 4),
          expected=(0,)
      )
      def testModuloResult(self, num, modulo, expected):
        self.assertEqual(expected, num % modulo)

    ts = unittest.makeSuite(GoodProductTestCase)
    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(ts.countTestCases(), 6)
    self.assertEqual(res.testsRun, 6)
    self.assertTrue(res.wasSuccessful())

  def test_successful_product_test_kwarg_seqs(self):

    class GoodProductTestCase(parameterized.TestCase):

      @parameterized.product((dict(num=0), dict(num=20), dict(num=0)),
                             (dict(modulo=2), dict(modulo=4)),
                             (dict(expected=0),))
      def testModuloResult(self, num, modulo, expected):
        self.assertEqual(expected, num % modulo)

    ts = unittest.makeSuite(GoodProductTestCase)
    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(ts.countTestCases(), 6)
    self.assertEqual(res.testsRun, 6)
    self.assertTrue(res.wasSuccessful())

  def test_successful_product_test_kwarg_seq_and_testgrid(self):

    class GoodProductTestCase(parameterized.TestCase):

      @parameterized.product((dict(
          num=5, modulo=3, expected=2), dict(num=7, modulo=4, expected=3)),
                             dtype=(int, float))
      def testModuloResult(self, num, dtype, modulo, expected):
        self.assertEqual(expected, dtype(num) % modulo)

    ts = unittest.makeSuite(GoodProductTestCase)
    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(ts.countTestCases(), 4)
    self.assertEqual(res.testsRun, 4)
    self.assertTrue(res.wasSuccessful())

  def test_inconsistent_arg_names_in_kwargs_seq(self):
    with self.assertRaisesRegex(AssertionError, 'must all have the same keys'):

      class BadProductParams(parameterized.TestCase):  

        @parameterized.product((dict(num=5, modulo=3), dict(num=7, modula=2)),
                               dtype=(int, float))
        def test_something(self):
          pass  

  def test_duplicate_arg_names_in_kwargs_seqs(self):
    with self.assertRaisesRegex(AssertionError, 'must all have distinct'):

      class BadProductParams(parameterized.TestCase):  

        @parameterized.product((dict(num=5, modulo=3), dict(num=7, modulo=4)),
                               (dict(foo='bar', num=5), dict(foo='baz', num=7)),
                               dtype=(int, float))
        def test_something(self):
          pass  

  def test_duplicate_arg_names_in_kwargs_seq_and_testgrid(self):
    with self.assertRaisesRegex(AssertionError, 'duplicate argument'):

      class BadProductParams(parameterized.TestCase):  

        @parameterized.product(
            (dict(num=5, modulo=3), dict(num=7, modulo=4)),
            (dict(foo='bar'), dict(foo='baz')),
            dtype=(int, float),
            foo=('a', 'b'),
        )
        def test_something(self):
          pass  

  def test_product_recorded_failures(self):

    class MixedProductTestCase(parameterized.TestCase):

      @parameterized.product(
          num=(0, 10, 20),
          modulo=(2, 4),
          expected=(0,)
      )
      def testModuloResult(self, num, modulo, expected):
        self.assertEqual(expected, num % modulo)

    ts = unittest.makeSuite(MixedProductTestCase)
    self.assertEqual(6, ts.countTestCases())

    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(res.testsRun, 6)
    self.assertFalse(res.wasSuccessful())
    self.assertLen(res.failures, 1)
    self.assertEmpty(res.errors)

  def test_mismatched_product_parameter(self):

    class MismatchedProductParam(parameterized.TestCase):

      @parameterized.product(
          a=(1, 2),
          mismatch=(1, 2)
      )
      
      def test_something(self, a, b):
        pass

    ts = unittest.makeSuite(MismatchedProductParam)
    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(res.testsRun, 4)
    self.assertFalse(res.wasSuccessful())
    self.assertLen(res.errors, 4)

  def test_no_test_error_empty_product_parameter(self):
    with self.assertRaises(parameterized.NoTestsError):

      class EmptyProductParam(parameterized.TestCase):  

        @parameterized.product(arg1=[1, 2], arg2=[])
        def test_something(self, arg1, arg2):
          pass  

  def test_bad_product_parameters(self):
    with self.assertRaisesRegex(AssertionError, 'must be given as list or'):

      class BadProductParams(parameterized.TestCase):  

        @parameterized.product(arg1=[1, 2], arg2='abcd')
        def test_something(self, arg1, arg2):
          pass  

  def test_generator_tests_disallowed(self):
    with self.assertRaisesRegex(RuntimeError, 'generated.*without'):
      class GeneratorTests(parameterized.TestCase):  
        test_generator_method = (lambda self: None for _ in range(10))

  def test_named_parameters_run(self):
    ts = unittest.makeSuite(self.NamedTests)
    self.assertEqual(9, ts.countTestCases())
    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(9, res.testsRun)
    self.assertTrue(res.wasSuccessful())

  def test_named_parameters_id(self):
    ts = sorted(unittest.makeSuite(self.CamelCaseNamedTests),
                key=lambda t: t.id())
    self.assertLen(ts, 9)
    full_class_name = unittest.util.strclass(self.CamelCaseNamedTests)
    self.assertEqual(
        full_class_name + '.testDictSingleInteresting',
        ts[0].id())
    self.assertEqual(
        full_class_name + '.testDictSomethingBoring',
        ts[1].id())
    self.assertEqual(
        full_class_name + '.testDictSomethingInteresting',
        ts[2].id())
    self.assertEqual(
        full_class_name + '.testMixedSomethingBoring',
        ts[3].id())
    self.assertEqual(
        full_class_name + '.testMixedSomethingInteresting',
        ts[4].id())
    self.assertEqual(
        full_class_name + '.testSingleInteresting',
        ts[5].id())
    self.assertEqual(
        full_class_name + '.testSomethingBoring',
        ts[6].id())
    self.assertEqual(
        full_class_name + '.testSomethingInteresting',
        ts[7].id())
    self.assertEqual(
        full_class_name + '.testWithoutParameters',
        ts[8].id())

  def test_named_parameters_id_with_underscore_case(self):
    ts = sorted(unittest.makeSuite(self.NamedTests),
                key=lambda t: t.id())
    self.assertLen(ts, 9)
    full_class_name = unittest.util.strclass(self.NamedTests)
    self.assertEqual(
        full_class_name + '.test_dict_single_interesting',
        ts[0].id())
    self.assertEqual(
        full_class_name + '.test_dict_something_boring',
        ts[1].id())
    self.assertEqual(
        full_class_name + '.test_dict_something_interesting',
        ts[2].id())
    self.assertEqual(
        full_class_name + '.test_mixed_something_boring',
        ts[3].id())
    self.assertEqual(
        full_class_name + '.test_mixed_something_interesting',
        ts[4].id())
    self.assertEqual(
        full_class_name + '.test_single_interesting',
        ts[5].id())
    self.assertEqual(
        full_class_name + '.test_something_boring',
        ts[6].id())
    self.assertEqual(
        full_class_name + '.test_something_interesting',
        ts[7].id())
    self.assertEqual(
        full_class_name + '.test_without_parameters',
        ts[8].id())

  def test_named_parameters_short_description(self):
    ts = sorted(unittest.makeSuite(self.NamedTests),
                key=lambda t: t.id())
    actual = {t._testMethodName: t.shortDescription() for t in ts}
    expected = {
        'test_dict_single_interesting': 'case=0',
        'test_dict_something_boring': 'case=1',
        'test_dict_something_interesting': 'case=0',
        'test_mixed_something_boring': '1',
        'test_mixed_something_interesting': 'case=0',
        'test_something_boring': '1',
        'test_something_interesting': '0',
    }
    for test_name, param_repr in expected.items():
      short_desc = actual[test_name].split('\n')
      self.assertIn(test_name, short_desc[0])
      self.assertEqual('{}({})'.format(test_name, param_repr), short_desc[1])

  def test_load_tuple_named_test(self):
    loader = unittest.TestLoader()
    ts = list(loader.loadTestsFromName('NamedTests.test_something_interesting',
                                       module=self))
    self.assertLen(ts, 1)
    self.assertEndsWith(ts[0].id(), '.test_something_interesting')

  def test_load_dict_named_test(self):
    loader = unittest.TestLoader()
    ts = list(
        loader.loadTestsFromName(
            'NamedTests.test_dict_something_interesting', module=self))
    self.assertLen(ts, 1)
    self.assertEndsWith(ts[0].id(), '.test_dict_something_interesting')

  def test_load_mixed_named_test(self):
    loader = unittest.TestLoader()
    ts = list(
        loader.loadTestsFromName(
            'NamedTests.test_mixed_something_interesting', module=self))
    self.assertLen(ts, 1)
    self.assertEndsWith(ts[0].id(), '.test_mixed_something_interesting')

  def test_duplicate_named_test_fails(self):
    with self.assertRaises(parameterized.DuplicateTestNameError):

      class _(parameterized.TestCase):

        @parameterized.named_parameters(
            ('Interesting', 0),
            ('Interesting', 1),
        )
        def test_something(self, unused_obj):
          pass

  def test_duplicate_dict_named_test_fails(self):
    with self.assertRaises(parameterized.DuplicateTestNameError):

      class _(parameterized.TestCase):

        @parameterized.named_parameters(
            {'testcase_name': 'Interesting', 'unused_obj': 0},
            {'testcase_name': 'Interesting', 'unused_obj': 1},
        )
        def test_dict_something(self, unused_obj):
          pass

  def test_duplicate_mixed_named_test_fails(self):
    with self.assertRaises(parameterized.DuplicateTestNameError):

      class _(parameterized.TestCase):

        @parameterized.named_parameters(
            {'testcase_name': 'Interesting', 'unused_obj': 0},
            ('Interesting', 1),
        )
        def test_mixed_something(self, unused_obj):
          pass

  def test_named_test_with_no_name_fails(self):
    with self.assertRaises(RuntimeError):

      class _(parameterized.TestCase):

        @parameterized.named_parameters(
            (0,),
        )
        def test_something(self, unused_obj):
          pass

  def test_named_test_dict_with_no_name_fails(self):
    with self.assertRaises(RuntimeError):

      class _(parameterized.TestCase):

        @parameterized.named_parameters(
            {'unused_obj': 0},
        )
        def test_something(self, unused_obj):
          pass

  def test_parameterized_test_iter_has_testcases_property(self):
    @parameterized.parameters(1, 2, 3, 4, 5, 6)
    def test_something(unused_self, unused_obj):  
      pass

    expected_testcases = [1, 2, 3, 4, 5, 6]
    self.assertTrue(hasattr(test_something, 'testcases'))
    self.assertCountEqual(expected_testcases, test_something.testcases)

  def test_chained_decorator(self):
    ts = unittest.makeSuite(self.ChainedTests)
    self.assertEqual(1, ts.countTestCases())
    test = next(t for t in ts)
    self.assertTrue(hasattr(test, 'test_chained_flavor_strawberry_cone_waffle'))
    res = unittest.TestResult()

    ts.run(res)
    self.assertEqual(1, res.testsRun)
    self.assertTrue(res.wasSuccessful())

  def test_singleton_list_extraction(self):
    ts = unittest.makeSuite(self.SingletonListExtraction)
    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(10, res.testsRun)
    self.assertTrue(res.wasSuccessful())

  def test_singleton_argument_extraction(self):
    ts = unittest.makeSuite(self.SingletonArgumentExtraction)
    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(9, res.testsRun)
    self.assertTrue(res.wasSuccessful())

  def test_singleton_dict_argument(self):
    ts = unittest.makeSuite(self.SingletonDictArgument)
    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(1, res.testsRun)
    self.assertTrue(res.wasSuccessful())

  def test_decorated_bare_class(self):
    ts = unittest.makeSuite(self.DecoratedBareClass)
    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(2, res.testsRun)
    self.assertTrue(res.wasSuccessful(), msg=str(res.failures))

  def test_decorated_class(self):
    ts = unittest.makeSuite(self.DecoratedClass)
    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(4, res.testsRun)
    self.assertLen(res.failures, 2)

  def test_generator_decorated_class(self):
    ts = unittest.makeSuite(self.GeneratorDecoratedClass)
    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(32, res.testsRun)
    self.assertLen(res.failures, 16)

  def test_no_duplicate_decorations(self):
    with self.assertRaises(AssertionError):

      @parameterized.parameters(1, 2, 3, 4)
      class _(parameterized.TestCase):

        @parameterized.parameters(5, 6, 7, 8)
        def test_something(self, unused_obj):
          pass

  def test_double_class_decorations_not_supported(self):

    @parameterized.parameters('foo', 'bar')
    class SuperclassWithClassDecorator(parameterized.TestCase):

      def test_name(self, name):
        del name

    with self.assertRaises(AssertionError):

      @parameterized.parameters('foo', 'bar')
      class SubclassWithClassDecorator(SuperclassWithClassDecorator):
        pass

      del SubclassWithClassDecorator

  def test_other_decorator_ordering_unnamed(self):
    ts = unittest.makeSuite(self.OtherDecoratorUnnamed)
    res = unittest.TestResult()
    ts.run(res)
    
    
    self.assertEqual(3, res.testsRun)
    self.assertFalse(res.wasSuccessful())
    self.assertEmpty(res.failures)
    
    self.assertLen(res.errors, 1)

  def test_other_decorator_ordering_named(self):
    ts = unittest.makeSuite(self.OtherDecoratorNamed)
    
    for test in ts:  
      ts_attributes = dir(test)
      self.assertIn('test_parameterized_then_other_a', ts_attributes)
      self.assertIn('test_parameterized_then_other_b', ts_attributes)

    res = unittest.TestResult()
    ts.run(res)
    
    
    self.assertEqual(3, res.testsRun)
    self.assertFalse(res.wasSuccessful())
    self.assertEmpty(res.failures)
    
    self.assertLen(res.errors, 1)

  def test_other_decorator_ordering_named_with_dict(self):
    ts = unittest.makeSuite(self.OtherDecoratorNamedWithDict)
    
    for test in ts:  
      ts_attributes = dir(test)
      self.assertIn('test_parameterized_then_other_a', ts_attributes)
      self.assertIn('test_parameterized_then_other_b', ts_attributes)

    res = unittest.TestResult()
    ts.run(res)
    
    
    self.assertEqual(3, res.testsRun)
    self.assertFalse(res.wasSuccessful())
    self.assertEmpty(res.failures)
    
    self.assertLen(res.errors, 1)

  def test_no_test_error_empty_parameters(self):
    with self.assertRaises(parameterized.NoTestsError):

      @parameterized.parameters()
      def test_something():
        pass

      del test_something

  def test_no_test_error_empty_generator(self):
    with self.assertRaises(parameterized.NoTestsError):

      @parameterized.parameters((i for i in []))
      def test_something():
        pass

      del test_something

  def test_unique_descriptive_names(self):

    class RecordSuccessTestsResult(unittest.TestResult):

      def __init__(self, *args, **kwargs):
        super(RecordSuccessTestsResult, self).__init__(*args, **kwargs)
        self.successful_tests = []

      def addSuccess(self, test):
        self.successful_tests.append(test)

    ts = unittest.makeSuite(self.UniqueDescriptiveNamesTest)
    res = RecordSuccessTestsResult()
    ts.run(res)
    self.assertTrue(res.wasSuccessful())
    self.assertEqual(2, res.testsRun)
    test_ids = [test.id() for test in res.successful_tests]
    full_class_name = unittest.util.strclass(self.UniqueDescriptiveNamesTest)
    expected_test_ids = [
        full_class_name + '.test_normal0 (13)',
        full_class_name + '.test_normal1 (13)',
    ]
    self.assertTrue(test_ids)
    self.assertCountEqual(expected_test_ids, test_ids)

  def test_multi_generators(self):
    ts = unittest.makeSuite(self.MultiGeneratorsTestCase)
    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(2, res.testsRun)
    self.assertTrue(res.wasSuccessful(), msg=str(res.failures))

  def test_named_parameters_reusable(self):
    ts = unittest.makeSuite(self.NamedParametersReusableTestCase)
    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(8, res.testsRun)
    self.assertTrue(res.wasSuccessful(), msg=str(res.failures))

  def test_subclass_inherits_superclass_test_params_reprs(self):
    self.assertEqual(
        {'test_name0': "('foo')", 'test_name1': "('bar')"},
        self.SuperclassTestCase._test_params_reprs)
    self.assertEqual(
        {'test_name0': "('foo')", 'test_name1': "('bar')"},
        self.SubclassTestCase._test_params_reprs)


def _decorate_with_side_effects(func, self):
  self.sideeffect = True
  func(self)


class CoopMetaclassCreationTest(absltest.TestCase):

  class TestBase(absltest.TestCase):

    
    
    
    

    
    
    
    

    class __metaclass__(type):  

      def __init__(cls, name, bases, dct):
        type.__init__(cls, name, bases, dct)
        for member_name, obj in dct.items():
          if member_name.startswith('test'):
            setattr(cls, member_name,
                    lambda self, f=obj: _decorate_with_side_effects(f, self))

  class MyParams(parameterized.CoopTestCase(TestBase)):

    @parameterized.parameters(
        (1, 2, 3),
        (4, 5, 9))
    def test_addition(self, op1, op2, result):
      self.assertEqual(result, op1 + op2)

  class MySuite(unittest.TestSuite):
    
    
    
    _cleanup = False

  def test_successful_execution(self):
    ts = unittest.makeSuite(self.MyParams)

    res = unittest.TestResult()
    ts.run(res)
    self.assertEqual(2, res.testsRun)
    self.assertTrue(res.wasSuccessful())

  def test_metaclass_side_effects(self):
    ts = unittest.makeSuite(self.MyParams, suiteClass=self.MySuite)

    res = unittest.TestResult()
    ts.run(res)
    self.assertTrue(list(ts)[0].sideeffect)


if __name__ == '__main__':
  absltest.main()
