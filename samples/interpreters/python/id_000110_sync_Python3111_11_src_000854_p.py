from test.support import verbose, run_unittest, gc_collect, bigmemtest, _2G, \
        cpython_only, captured_stdout
import io
import locale
import re
from re import Scanner
import sre_compile
import sre_constants
import sys
import string
import traceback
import unittest
from weakref import proxy







class S(str):
    def __getitem__(self, index):
        return S(super().__getitem__(index))

class B(bytes):
    def __getitem__(self, index):
        return B(super().__getitem__(index))

class ReTests(unittest.TestCase):

    def assertTypedEqual(self, actual, expect, msg=None):
        self.assertEqual(actual, expect, msg)
        def recurse(actual, expect):
            if isinstance(expect, (tuple, list)):
                for x, y in zip(actual, expect):
                    recurse(x, y)
            else:
                self.assertIs(type(actual), type(expect), msg)
        recurse(actual, expect)

    def test_keep_buffer(self):
        
        b = bytearray(b'x')
        it = re.finditer(b'a', b)
        with self.assertRaises(BufferError):
            b.extend(b'x'*400)
        list(it)
        del it
        gc_collect()
        b.extend(b'x'*400)

    def test_weakref(self):
        s = 'QabbbcR'
        x = re.compile('ab+c')
        y = proxy(x)
        self.assertEqual(x.findall('QabbbcR'), y.findall('QabbbcR'))

    def test_search_star_plus(self):
        self.assertEqual(re.search('x*', 'axx').span(0), (0, 0))
        self.assertEqual(re.search('x*', 'axx').span(), (0, 0))
        self.assertEqual(re.search('x+', 'axx').span(0), (1, 3))
        self.assertEqual(re.search('x+', 'axx').span(), (1, 3))
        self.assertIsNone(re.search('x', 'aaa'))
        self.assertEqual(re.match('a*', 'xxx').span(0), (0, 0))
        self.assertEqual(re.match('a*', 'xxx').span(), (0, 0))
        self.assertEqual(re.match('x*', 'xxxa').span(0), (0, 3))
        self.assertEqual(re.match('x*', 'xxxa').span(), (0, 3))
        self.assertIsNone(re.match('a+', 'xxx'))

    def bump_num(self, matchobj):
        int_value = int(matchobj.group(0))
        return str(int_value + 1)

    def test_basic_re_sub(self):
        self.assertTypedEqual(re.sub('y', 'a', 'xyz'), 'xaz')
        self.assertTypedEqual(re.sub('y', S('a'), S('xyz')), 'xaz')
        self.assertTypedEqual(re.sub(b'y', b'a', b'xyz'), b'xaz')
        self.assertTypedEqual(re.sub(b'y', B(b'a'), B(b'xyz')), b'xaz')
        self.assertTypedEqual(re.sub(b'y', bytearray(b'a'), bytearray(b'xyz')), b'xaz')
        self.assertTypedEqual(re.sub(b'y', memoryview(b'a'), memoryview(b'xyz')), b'xaz')
        for y in ("\xe0", "\u0430", "\U0001d49c"):
            self.assertEqual(re.sub(y, 'a', 'x%sz' % y), 'xaz')

        self.assertEqual(re.sub("(?i)b+", "x", "bbbb BBBB"), 'x x')
        self.assertEqual(re.sub(r'\d+', self.bump_num, '08.2 -2 23x99y'),
                         '9.3 -3 24x100y')
        self.assertEqual(re.sub(r'\d+', self.bump_num, '08.2 -2 23x99y', 3),
                         '9.3 -3 23x99y')

        self.assertEqual(re.sub('.', lambda m: r"\n", 'x'), '\\n')
        self.assertEqual(re.sub('.', r"\n", 'x'), '\n')

        s = r"\1\1"
        self.assertEqual(re.sub('(.)', s, 'x'), 'xx')
        self.assertEqual(re.sub('(.)', re.escape(s), 'x'), s)
        self.assertEqual(re.sub('(.)', lambda m: s, 'x'), s)

        self.assertEqual(re.sub('(?P<a>x)', '\g<a>\g<a>', 'xx'), 'xxxx')
        self.assertEqual(re.sub('(?P<a>x)', '\g<a>\g<1>', 'xx'), 'xxxx')
        self.assertEqual(re.sub('(?P<unk>x)', '\g<unk>\g<unk>', 'xx'), 'xxxx')
        self.assertEqual(re.sub('(?P<unk>x)', '\g<1>\g<1>', 'xx'), 'xxxx')

        self.assertEqual(re.sub('a',r'\t\n\v\r\f\a\b\B\Z\a\A\w\W\s\S\d\D','a'),
                         '\t\n\v\r\f\a\b\\B\\Z\a\\A\\w\\W\\s\\S\\d\\D')
        self.assertEqual(re.sub('a', '\t\n\v\r\f\a', 'a'), '\t\n\v\r\f\a')
        self.assertEqual(re.sub('a', '\t\n\v\r\f\a', 'a'),
                         (chr(9)+chr(10)+chr(11)+chr(13)+chr(12)+chr(7)))

        self.assertEqual(re.sub('^\s*', 'X', 'test'), 'Xtest')

    def test_bug_449964(self):
        
        self.assertEqual(re.sub(r'(?P<unk>x)', '\g<1>\g<1>\\b', 'xx'),
                         'xx\bxx\b')

    def test_bug_449000(self):
        
        self.assertEqual(re.sub(r'\r\n', r'\n', 'abc\r\ndef\r\n'),
                         'abc\ndef\n')
        self.assertEqual(re.sub('\r\n', r'\n', 'abc\r\ndef\r\n'),
                         'abc\ndef\n')
        self.assertEqual(re.sub(r'\r\n', '\n', 'abc\r\ndef\r\n'),
                         'abc\ndef\n')
        self.assertEqual(re.sub('\r\n', '\n', 'abc\r\ndef\r\n'),
                         'abc\ndef\n')

    def test_bug_1661(self):
        
        pattern = re.compile('.')
        self.assertRaises(ValueError, re.match, pattern, 'A', re.I)
        self.assertRaises(ValueError, re.search, pattern, 'A', re.I)
        self.assertRaises(ValueError, re.findall, pattern, 'A', re.I)
        self.assertRaises(ValueError, re.compile, pattern, re.I)

    def test_bug_3629(self):
        
        re.compile("(?P<quote>)(?(quote))")

    def test_sub_template_numeric_escape(self):
        
        self.assertEqual(re.sub('x', r'\0', 'x'), '\0')
        self.assertEqual(re.sub('x', r'\000', 'x'), '\000')
        self.assertEqual(re.sub('x', r'\001', 'x'), '\001')
        self.assertEqual(re.sub('x', r'\008', 'x'), '\0' + '8')
        self.assertEqual(re.sub('x', r'\009', 'x'), '\0' + '9')
        self.assertEqual(re.sub('x', r'\111', 'x'), '\111')
        self.assertEqual(re.sub('x', r'\117', 'x'), '\117')

        self.assertEqual(re.sub('x', r'\1111', 'x'), '\1111')
        self.assertEqual(re.sub('x', r'\1111', 'x'), '\111' + '1')

        self.assertEqual(re.sub('x', r'\00', 'x'), '\x00')
        self.assertEqual(re.sub('x', r'\07', 'x'), '\x07')
        self.assertEqual(re.sub('x', r'\08', 'x'), '\0' + '8')
        self.assertEqual(re.sub('x', r'\09', 'x'), '\0' + '9')
        self.assertEqual(re.sub('x', r'\0a', 'x'), '\0' + 'a')

        self.assertEqual(re.sub('x', r'\400', 'x'), '\0')
        self.assertEqual(re.sub('x', r'\777', 'x'), '\377')

        self.assertRaises(re.error, re.sub, 'x', r'\1', 'x')
        self.assertRaises(re.error, re.sub, 'x', r'\8', 'x')
        self.assertRaises(re.error, re.sub, 'x', r'\9', 'x')
        self.assertRaises(re.error, re.sub, 'x', r'\11', 'x')
        self.assertRaises(re.error, re.sub, 'x', r'\18', 'x')
        self.assertRaises(re.error, re.sub, 'x', r'\1a', 'x')
        self.assertRaises(re.error, re.sub, 'x', r'\90', 'x')
        self.assertRaises(re.error, re.sub, 'x', r'\99', 'x')
        self.assertRaises(re.error, re.sub, 'x', r'\118', 'x') 
        self.assertRaises(re.error, re.sub, 'x', r'\11a', 'x')
        self.assertRaises(re.error, re.sub, 'x', r'\181', 'x') 
        self.assertRaises(re.error, re.sub, 'x', r'\800', 'x') 

        
        self.assertEqual(re.sub('(((((((((((x)))))))))))', r'\11', 'x'), 'x')
        self.assertEqual(re.sub('((((((((((y))))))))))(.)', r'\118', 'xyz'),
                         'xz8')
        self.assertEqual(re.sub('((((((((((y))))))))))(.)', r'\11a', 'xyz'),
                         'xza')

    def test_qualified_re_sub(self):
        self.assertEqual(re.sub('a', 'b', 'aaaaa'), 'bbbbb')
        self.assertEqual(re.sub('a', 'b', 'aaaaa', 1), 'baaaa')

    def test_bug_114660(self):
        self.assertEqual(re.sub(r'(\S)\s+(\S)', r'\1 \2', 'hello  there'),
                         'hello there')

    def test_bug_462270(self):
        
        self.assertEqual(re.sub('x*', '-', 'abxd'), '-a-b-d-')
        self.assertEqual(re.sub('x+', '-', 'abxd'), 'ab-d')

    def test_symbolic_groups(self):
        re.compile('(?P<a>x)(?P=a)(?(a)y)')
        re.compile('(?P<a1>x)(?P=a1)(?(a1)y)')
        self.assertRaises(re.error, re.compile, '(?P<a>)(?P<a>)')
        self.assertRaises(re.error, re.compile, '(?Px)')
        self.assertRaises(re.error, re.compile, '(?P=)')
        self.assertRaises(re.error, re.compile, '(?P=1)')
        self.assertRaises(re.error, re.compile, '(?P=a)')
        self.assertRaises(re.error, re.compile, '(?P=a1)')
        self.assertRaises(re.error, re.compile, '(?P=a.)')
        self.assertRaises(re.error, re.compile, '(?P<)')
        self.assertRaises(re.error, re.compile, '(?P<>)')
        self.assertRaises(re.error, re.compile, '(?P<1>)')
        self.assertRaises(re.error, re.compile, '(?P<a.>)')
        self.assertRaises(re.error, re.compile, '(?())')
        self.assertRaises(re.error, re.compile, '(?(a))')
        self.assertRaises(re.error, re.compile, '(?(1a))')
        self.assertRaises(re.error, re.compile, '(?(a.))')
        
        re.compile('(?P<µ>x)(?P=µ)(?(µ)y)')
        re.compile('(?P<𝔘𝔫𝔦𝔠𝔬𝔡𝔢>x)(?P=𝔘𝔫𝔦𝔠𝔬𝔡𝔢)(?(𝔘𝔫𝔦𝔠𝔬𝔡𝔢)y)')
        self.assertRaises(re.error, re.compile, '(?P<©>x)')

    def test_symbolic_refs(self):
        self.assertRaises(re.error, re.sub, '(?P<a>x)', '\g<a', 'xx')
        self.assertRaises(re.error, re.sub, '(?P<a>x)', '\g<', 'xx')
        self.assertRaises(re.error, re.sub, '(?P<a>x)', '\g', 'xx')
        self.assertRaises(re.error, re.sub, '(?P<a>x)', '\g<a a>', 'xx')
        self.assertRaises(re.error, re.sub, '(?P<a>x)', '\g<>', 'xx')
        self.assertRaises(re.error, re.sub, '(?P<a>x)', '\g<1a1>', 'xx')
        self.assertRaises(IndexError, re.sub, '(?P<a>x)', '\g<ab>', 'xx')
        self.assertRaises(re.error, re.sub, '(?P<a>x)|(?P<b>y)', '\g<b>', 'xx')
        self.assertRaises(re.error, re.sub, '(?P<a>x)|(?P<b>y)', '\\2', 'xx')
        self.assertRaises(re.error, re.sub, '(?P<a>x)', '\g<-1>', 'xx')
        
        self.assertEqual(re.sub('(?P<µ>x)', r'\g<µ>', 'xx'), 'xx')
        self.assertEqual(re.sub('(?P<𝔘𝔫𝔦𝔠𝔬𝔡𝔢>x)', r'\g<𝔘𝔫𝔦𝔠𝔬𝔡𝔢>', 'xx'), 'xx')
        self.assertRaises(re.error, re.sub, '(?P<a>x)', r'\g<©>', 'xx')

    def test_re_subn(self):
        self.assertEqual(re.subn("(?i)b+", "x", "bbbb BBBB"), ('x x', 2))
        self.assertEqual(re.subn("b+", "x", "bbbb BBBB"), ('x BBBB', 1))
        self.assertEqual(re.subn("b+", "x", "xyz"), ('xyz', 0))
        self.assertEqual(re.subn("b*", "x", "xyz"), ('xxxyxzx', 4))
        self.assertEqual(re.subn("b*", "x", "xyz", 2), ('xxxyz', 2))

    def test_re_split(self):
        for string in ":a:b::c", S(":a:b::c"):
            self.assertTypedEqual(re.split(":", string),
                                  ['', 'a', 'b', '', 'c'])
            self.assertTypedEqual(re.split(":*", string),
                                  ['', 'a', 'b', 'c'])
            self.assertTypedEqual(re.split("(:*)", string),
                                  ['', ':', 'a', ':', 'b', '::', 'c'])
        for string in (b":a:b::c", B(b":a:b::c"), bytearray(b":a:b::c"),
                       memoryview(b":a:b::c")):
            self.assertTypedEqual(re.split(b":", string),
                                  [b'', b'a', b'b', b'', b'c'])
            self.assertTypedEqual(re.split(b":*", string),
                                  [b'', b'a', b'b', b'c'])
            self.assertTypedEqual(re.split(b"(:*)", string),
                                  [b'', b':', b'a', b':', b'b', b'::', b'c'])
        for a, b, c in ("\xe0\xdf\xe7", "\u0430\u0431\u0432",
                        "\U0001d49c\U0001d49e\U0001d4b5"):
            string = ":%s:%s::%s" % (a, b, c)
            self.assertEqual(re.split(":", string), ['', a, b, '', c])
            self.assertEqual(re.split(":*", string), ['', a, b, c])
            self.assertEqual(re.split("(:*)", string),
                             ['', ':', a, ':', b, '::', c])

        self.assertEqual(re.split("(?::*)", ":a:b::c"), ['', 'a', 'b', 'c'])
        self.assertEqual(re.split("(:)*", ":a:b::c"),
                         ['', ':', 'a', ':', 'b', ':', 'c'])
        self.assertEqual(re.split("([b:]+)", ":a:b::c"),
                         ['', ':', 'a', ':b::', 'c'])
        self.assertEqual(re.split("(b)|(:+)", ":a:b::c"),
                         ['', None, ':', 'a', None, ':', '', 'b', None, '',
                          None, '::', 'c'])
        self.assertEqual(re.split("(?:b)|(?::+)", ":a:b::c"),
                         ['', 'a', '', '', 'c'])

    def test_qualified_re_split(self):
        self.assertEqual(re.split(":", ":a:b::c", 2), ['', 'a', 'b::c'])
        self.assertEqual(re.split(':', 'a:b:c:d', 2), ['a', 'b', 'c:d'])
        self.assertEqual(re.split("(:)", ":a:b::c", 2),
                         ['', ':', 'a', ':', 'b::c'])
        self.assertEqual(re.split("(:*)", ":a:b::c", 2),
                         ['', ':', 'a', ':', 'b::c'])

    def test_re_findall(self):
        self.assertEqual(re.findall(":+", "abc"), [])
        for string in "a:b::c:::d", S("a:b::c:::d"):
            self.assertTypedEqual(re.findall(":+", string),
                                  [":", "::", ":::"])
            self.assertTypedEqual(re.findall("(:+)", string),
                                  [":", "::", ":::"])
            self.assertTypedEqual(re.findall("(:)(:*)", string),
                                  [(":", ""), (":", ":"), (":", "::")])
        for string in (b"a:b::c:::d", B(b"a:b::c:::d"), bytearray(b"a:b::c:::d"),
                       memoryview(b"a:b::c:::d")):
            self.assertTypedEqual(re.findall(b":+", string),
                                  [b":", b"::", b":::"])
            self.assertTypedEqual(re.findall(b"(:+)", string),
                                  [b":", b"::", b":::"])
            self.assertTypedEqual(re.findall(b"(:)(:*)", string),
                                  [(b":", b""), (b":", b":"), (b":", b"::")])
        for x in ("\xe0", "\u0430", "\U0001d49c"):
            xx = x * 2
            xxx = x * 3
            string = "a%sb%sc%sd" % (x, xx, xxx)
            self.assertEqual(re.findall("%s+" % x, string), [x, xx, xxx])
            self.assertEqual(re.findall("(%s+)" % x, string), [x, xx, xxx])
            self.assertEqual(re.findall("(%s)(%s*)" % (x, x), string),
                             [(x, ""), (x, x), (x, xx)])

    def test_bug_117612(self):
        self.assertEqual(re.findall(r"(a|(b))", "aba"),
                         [("a", ""),("b", "b"),("a", "")])

    def test_re_match(self):
        for string in 'a', S('a'):
            self.assertEqual(re.match('a', string).groups(), ())
            self.assertEqual(re.match('(a)', string).groups(), ('a',))
            self.assertEqual(re.match('(a)', string).group(0), 'a')
            self.assertEqual(re.match('(a)', string).group(1), 'a')
            self.assertEqual(re.match('(a)', string).group(1, 1), ('a', 'a'))
        for string in b'a', B(b'a'), bytearray(b'a'), memoryview(b'a'):
            self.assertEqual(re.match(b'a', string).groups(), ())
            self.assertEqual(re.match(b'(a)', string).groups(), (b'a',))
            self.assertEqual(re.match(b'(a)', string).group(0), b'a')
            self.assertEqual(re.match(b'(a)', string).group(1), b'a')
            self.assertEqual(re.match(b'(a)', string).group(1, 1), (b'a', b'a'))
        for a in ("\xe0", "\u0430", "\U0001d49c"):
            self.assertEqual(re.match(a, a).groups(), ())
            self.assertEqual(re.match('(%s)' % a, a).groups(), (a,))
            self.assertEqual(re.match('(%s)' % a, a).group(0), a)
            self.assertEqual(re.match('(%s)' % a, a).group(1), a)
            self.assertEqual(re.match('(%s)' % a, a).group(1, 1), (a, a))

        pat = re.compile('((a)|(b))(c)?')
        self.assertEqual(pat.match('a').groups(), ('a', 'a', None, None))
        self.assertEqual(pat.match('b').groups(), ('b', None, 'b', None))
        self.assertEqual(pat.match('ac').groups(), ('a', 'a', None, 'c'))
        self.assertEqual(pat.match('bc').groups(), ('b', None, 'b', 'c'))
        self.assertEqual(pat.match('bc').groups(""), ('b', "", 'b', 'c'))

        
        m = re.match('(a)', 'a')
        self.assertEqual(m.group(0), 'a')
        self.assertEqual(m.group(0), 'a')
        self.assertEqual(m.group(1), 'a')
        self.assertEqual(m.group(1, 1), ('a', 'a'))

        pat = re.compile('(?:(?P<a1>a)|(?P<b2>b))(?P<c3>c)?')
        self.assertEqual(pat.match('a').group(1, 2, 3), ('a', None, None))
        self.assertEqual(pat.match('b').group('a1', 'b2', 'c3'),
                         (None, 'b', None))
        self.assertEqual(pat.match('ac').group(1, 'b2', 3), ('a', None, 'c'))

    def test_re_fullmatch(self):
        
        self.assertEqual(re.fullmatch(r"a", "a").span(), (0, 1))
        for string in "ab", S("ab"):
            self.assertEqual(re.fullmatch(r"a|ab", string).span(), (0, 2))
        for string in b"ab", B(b"ab"), bytearray(b"ab"), memoryview(b"ab"):
            self.assertEqual(re.fullmatch(br"a|ab", string).span(), (0, 2))
        for a, b in "\xe0\xdf", "\u0430\u0431", "\U0001d49c\U0001d49e":
            r = r"%s|%s" % (a, a + b)
            self.assertEqual(re.fullmatch(r, a + b).span(), (0, 2))
        self.assertEqual(re.fullmatch(r".*?$", "abc").span(), (0, 3))
        self.assertEqual(re.fullmatch(r".*?", "abc").span(), (0, 3))
        self.assertEqual(re.fullmatch(r"a.*?b", "ab").span(), (0, 2))
        self.assertEqual(re.fullmatch(r"a.*?b", "abb").span(), (0, 3))
        self.assertEqual(re.fullmatch(r"a.*?b", "axxb").span(), (0, 4))
        self.assertIsNone(re.fullmatch(r"a+", "ab"))
        self.assertIsNone(re.fullmatch(r"abc$", "abc\n"))
        self.assertIsNone(re.fullmatch(r"abc\Z", "abc\n"))
        self.assertIsNone(re.fullmatch(r"(?m)abc$", "abc\n"))
        self.assertEqual(re.fullmatch(r"ab(?=c)cd", "abcd").span(), (0, 4))
        self.assertEqual(re.fullmatch(r"ab(?<=b)cd", "abcd").span(), (0, 4))
        self.assertEqual(re.fullmatch(r"(?=a|ab)ab", "ab").span(), (0, 2))

        self.assertEqual(
            re.compile(r"bc").fullmatch("abcd", pos=1, endpos=3).span(), (1, 3))
        self.assertEqual(
            re.compile(r".*?$").fullmatch("abcd", pos=1, endpos=3).span(), (1, 3))
        self.assertEqual(
            re.compile(r".*?").fullmatch("abcd", pos=1, endpos=3).span(), (1, 3))

    def test_re_groupref_exists(self):
        self.assertEqual(re.match('^(\()?([^()]+)(?(1)\))$', '(a)').groups(),
                         ('(', 'a'))
        self.assertEqual(re.match('^(\()?([^()]+)(?(1)\))$', 'a').groups(),
                         (None, 'a'))
        self.assertIsNone(re.match('^(\()?([^()]+)(?(1)\))$', 'a)'))
        self.assertIsNone(re.match('^(\()?([^()]+)(?(1)\))$', '(a'))
        self.assertEqual(re.match('^(?:(a)|c)((?(1)b|d))$', 'ab').groups(),
                         ('a', 'b'))
        self.assertEqual(re.match('^(?:(a)|c)((?(1)b|d))$', 'cd').groups(),
                         (None, 'd'))
        self.assertEqual(re.match('^(?:(a)|c)((?(1)|d))$', 'cd').groups(),
                         (None, 'd'))
        self.assertEqual(re.match('^(?:(a)|c)((?(1)|d))$', 'a').groups(),
                         ('a', ''))

        
        p = re.compile('(?P<g1>a)(?P<g2>b)?((?(g2)c|d))')
        self.assertEqual(p.match('abc').groups(),
                         ('a', 'b', 'c'))
        self.assertEqual(p.match('ad').groups(),
                         ('a', None, 'd'))
        self.assertIsNone(p.match('abd'))
        self.assertIsNone(p.match('ac'))


    def test_re_groupref(self):
        self.assertEqual(re.match(r'^(\|)?([^()]+)\1$', '|a|').groups(),
                         ('|', 'a'))
        self.assertEqual(re.match(r'^(\|)?([^()]+)\1?$', 'a').groups(),
                         (None, 'a'))
        self.assertIsNone(re.match(r'^(\|)?([^()]+)\1$', 'a|'))
        self.assertIsNone(re.match(r'^(\|)?([^()]+)\1$', '|a'))
        self.assertEqual(re.match(r'^(?:(a)|c)(\1)$', 'aa').groups(),
                         ('a', 'a'))
        self.assertEqual(re.match(r'^(?:(a)|c)(\1)?$', 'c').groups(),
                         (None, None))

    def test_groupdict(self):
        self.assertEqual(re.match('(?P<first>first) (?P<second>second)',
                                  'first second').groupdict(),
                         {'first':'first', 'second':'second'})

    def test_expand(self):
        self.assertEqual(re.match("(?P<first>first) (?P<second>second)",
                                  "first second")
                                  .expand(r"\2 \1 \g<second> \g<first>"),
                         "second first second first")

    def test_repeat_minmax(self):
        self.assertIsNone(re.match("^(\w){1}$", "abc"))
        self.assertIsNone(re.match("^(\w){1}?$", "abc"))
        self.assertIsNone(re.match("^(\w){1,2}$", "abc"))
        self.assertIsNone(re.match("^(\w){1,2}?$", "abc"))

        self.assertEqual(re.match("^(\w){3}$", "abc").group(1), "c")
        self.assertEqual(re.match("^(\w){1,3}$", "abc").group(1), "c")
        self.assertEqual(re.match("^(\w){1,4}$", "abc").group(1), "c")
        self.assertEqual(re.match("^(\w){3,4}?$", "abc").group(1), "c")
        self.assertEqual(re.match("^(\w){3}?$", "abc").group(1), "c")
        self.assertEqual(re.match("^(\w){1,3}?$", "abc").group(1), "c")
        self.assertEqual(re.match("^(\w){1,4}?$", "abc").group(1), "c")
        self.assertEqual(re.match("^(\w){3,4}?$", "abc").group(1), "c")

        self.assertIsNone(re.match("^x{1}$", "xxx"))
        self.assertIsNone(re.match("^x{1}?$", "xxx"))
        self.assertIsNone(re.match("^x{1,2}$", "xxx"))
        self.assertIsNone(re.match("^x{1,2}?$", "xxx"))

        self.assertTrue(re.match("^x{3}$", "xxx"))
        self.assertTrue(re.match("^x{1,3}$", "xxx"))
        self.assertTrue(re.match("^x{1,4}$", "xxx"))
        self.assertTrue(re.match("^x{3,4}?$", "xxx"))
        self.assertTrue(re.match("^x{3}?$", "xxx"))
        self.assertTrue(re.match("^x{1,3}?$", "xxx"))
        self.assertTrue(re.match("^x{1,4}?$", "xxx"))
        self.assertTrue(re.match("^x{3,4}?$", "xxx"))

        self.assertIsNone(re.match("^x{}$", "xxx"))
        self.assertTrue(re.match("^x{}$", "x{}"))

    def test_getattr(self):
        self.assertEqual(re.compile("(?i)(a)(b)").pattern, "(?i)(a)(b)")
        self.assertEqual(re.compile("(?i)(a)(b)").flags, re.I | re.U)
        self.assertEqual(re.compile("(?i)(a)(b)").groups, 2)
        self.assertEqual(re.compile("(?i)(a)(b)").groupindex, {})
        self.assertEqual(re.compile("(?i)(?P<first>a)(?P<other>b)").groupindex,
                         {'first': 1, 'other': 2})

        self.assertEqual(re.match("(a)", "a").pos, 0)
        self.assertEqual(re.match("(a)", "a").endpos, 1)
        self.assertEqual(re.match("(a)", "a").string, "a")
        self.assertEqual(re.match("(a)", "a").regs, ((0, 1), (0, 1)))
        self.assertTrue(re.match("(a)", "a").re)

    def test_special_escapes(self):
        self.assertEqual(re.search(r"\b(b.)\b",
                                   "abcd abc bcd bx").group(1), "bx")
        self.assertEqual(re.search(r"\B(b.)\B",
                                   "abc bcd bc abxd").group(1), "bx")
        self.assertEqual(re.search(r"\b(b.)\b",
                                   "abcd abc bcd bx", re.ASCII).group(1), "bx")
        self.assertEqual(re.search(r"\B(b.)\B",
                                   "abc bcd bc abxd", re.ASCII).group(1), "bx")
        self.assertEqual(re.search(r"\b(b.)\b",
                                   "abcd abc bcd bx", re.LOCALE).group(1), "bx")
        self.assertEqual(re.search(r"\B(b.)\B",
                                   "abc bcd bc abxd", re.LOCALE).group(1), "bx")
        self.assertEqual(re.search(r"^abc$", "\nabc\n", re.M).group(0), "abc")
        self.assertEqual(re.search(r"^\Aabc\Z$", "abc", re.M).group(0), "abc")
        self.assertIsNone(re.search(r"^\Aabc\Z$", "\nabc\n", re.M))
        self.assertEqual(re.search(br"\b(b.)\b",
                                   b"abcd abc bcd bx").group(1), b"bx")
        self.assertEqual(re.search(br"\B(b.)\B",
                                   b"abc bcd bc abxd").group(1), b"bx")
        self.assertEqual(re.search(br"\b(b.)\b",
                                   b"abcd abc bcd bx", re.LOCALE).group(1), b"bx")
        self.assertEqual(re.search(br"\B(b.)\B",
                                   b"abc bcd bc abxd", re.LOCALE).group(1), b"bx")
        self.assertEqual(re.search(br"^abc$", b"\nabc\n", re.M).group(0), b"abc")
        self.assertEqual(re.search(br"^\Aabc\Z$", b"abc", re.M).group(0), b"abc")
        self.assertIsNone(re.search(br"^\Aabc\Z$", b"\nabc\n", re.M))
        self.assertEqual(re.search(r"\d\D\w\W\s\S",
                                   "1aa! a").group(0), "1aa! a")
        self.assertEqual(re.search(br"\d\D\w\W\s\S",
                                   b"1aa! a").group(0), b"1aa! a")
        self.assertEqual(re.search(r"\d\D\w\W\s\S",
                                   "1aa! a", re.ASCII).group(0), "1aa! a")
        self.assertEqual(re.search(r"\d\D\w\W\s\S",
                                   "1aa! a", re.LOCALE).group(0), "1aa! a")
        self.assertEqual(re.search(br"\d\D\w\W\s\S",
                                   b"1aa! a", re.LOCALE).group(0), b"1aa! a")

    def test_string_boundaries(self):
        
        self.assertEqual(re.search(r"\b(abc)\b", "abc").group(1),
                         "abc")
        
        self.assertTrue(re.match(r"\b", "abc"))
        
        self.assertTrue(re.search(r"\B", "abc"))
        
        self.assertFalse(re.match(r"\B", "abc"))
        
        
        self.assertIsNone(re.search(r"\B", ""))
        
        
        self.assertIsNone(re.search(r"\b", ""))
        
        
        self.assertEqual(len(re.findall(r"\b", "a")), 2)
        self.assertEqual(len(re.findall(r"\B", "a")), 0)
        
        self.assertEqual(len(re.findall(r"\b", " ")), 0)
        self.assertEqual(len(re.findall(r"\b", "   ")), 0)
        
        self.assertEqual(len(re.findall(r"\B", " ")), 2)

    def test_bigcharset(self):
        self.assertEqual(re.match("([\u2222\u2223])",
                                  "\u2222").group(1), "\u2222")
        r = '[%s]' % ''.join(map(chr, range(256, 2**16, 255)))
        self.assertEqual(re.match(r, "\uff01").group(), "\uff01")

    def test_big_codesize(self):
        
        r = re.compile('|'.join(('%d'%x for x in range(10000))))
        self.assertTrue(r.match('1000'))
        self.assertTrue(r.match('9999'))

    def test_anyall(self):
        self.assertEqual(re.match("a.b", "a\nb", re.DOTALL).group(0),
                         "a\nb")
        self.assertEqual(re.match("a.*b", "a\n\nb", re.DOTALL).group(0),
                         "a\n\nb")

    def test_lookahead(self):
        self.assertEqual(re.match("(a(?=\s[^a]))", "a b").group(1), "a")
        self.assertEqual(re.match("(a(?=\s[^a]*))", "a b").group(1), "a")
        self.assertEqual(re.match("(a(?=\s[abc]))", "a b").group(1), "a")
        self.assertEqual(re.match("(a(?=\s[abc]*))", "a bc").group(1), "a")
        self.assertEqual(re.match(r"(a)(?=\s\1)", "a a").group(1), "a")
        self.assertEqual(re.match(r"(a)(?=\s\1*)", "a aa").group(1), "a")
        self.assertEqual(re.match(r"(a)(?=\s(abc|a))", "a a").group(1), "a")

        self.assertEqual(re.match(r"(a(?!\s[^a]))", "a a").group(1), "a")
        self.assertEqual(re.match(r"(a(?!\s[abc]))", "a d").group(1), "a")
        self.assertEqual(re.match(r"(a)(?!\s\1)", "a b").group(1), "a")
        self.assertEqual(re.match(r"(a)(?!\s(abc|a))", "a b").group(1), "a")

        
        self.assertTrue(re.match(r'(a)b(?=\1)a', 'aba'))
        self.assertIsNone(re.match(r'(a)b(?=\1)c', 'abac'))
        
        self.assertTrue(re.match(r'(?P<g>a)b(?=(?P=g))a', 'aba'))
        self.assertIsNone(re.match(r'(?P<g>a)b(?=(?P=g))c', 'abac'))
        
        self.assertTrue(re.match(r'(?:(a)|(x))b(?=(?(2)x|c))c', 'abc'))
        self.assertIsNone(re.match(r'(?:(a)|(x))b(?=(?(2)c|x))c', 'abc'))
        self.assertTrue(re.match(r'(?:(a)|(x))b(?=(?(2)x|c))c', 'abc'))
        self.assertIsNone(re.match(r'(?:(a)|(x))b(?=(?(1)b|x))c', 'abc'))
        self.assertTrue(re.match(r'(?:(a)|(x))b(?=(?(1)c|x))c', 'abc'))
        
        self.assertTrue(re.match(r'(a)b(?=(?(2)x|c))(c)', 'abc'))
        self.assertIsNone(re.match(r'(a)b(?=(?(2)b|x))(c)', 'abc'))
        self.assertTrue(re.match(r'(a)b(?=(?(1)c|x))(c)', 'abc'))

    def test_lookbehind(self):
        self.assertTrue(re.match(r'ab(?<=b)c', 'abc'))
        self.assertIsNone(re.match(r'ab(?<=c)c', 'abc'))
        self.assertIsNone(re.match(r'ab(?<!b)c', 'abc'))
        self.assertTrue(re.match(r'ab(?<!c)c', 'abc'))
        
        self.assertWarns(RuntimeWarning, re.compile, r'(a)a(?<=\1)c')
        
        self.assertWarns(RuntimeWarning, re.compile, r'(?P<g>a)a(?<=(?P=g))c')
        
        self.assertWarns(RuntimeWarning, re.compile, r'(a)b(?<=(?(1)b|x))c')
        
        self.assertWarns(RuntimeWarning, re.compile, r'(a)b(?<=(?(2)b|x))(c)')

    def test_ignore_case(self):
        self.assertEqual(re.match("abc", "ABC", re.I).group(0), "ABC")
        self.assertEqual(re.match(b"abc", b"ABC", re.I).group(0), b"ABC")
        self.assertEqual(re.match(r"(a\s[^a])", "a b", re.I).group(1), "a b")
        self.assertEqual(re.match(r"(a\s[^a]*)", "a bb", re.I).group(1), "a bb")
        self.assertEqual(re.match(r"(a\s[abc])", "a b", re.I).group(1), "a b")
        self.assertEqual(re.match(r"(a\s[abc]*)", "a bb", re.I).group(1), "a bb")
        self.assertEqual(re.match(r"((a)\s\2)", "a a", re.I).group(1), "a a")
        self.assertEqual(re.match(r"((a)\s\2*)", "a aa", re.I).group(1), "a aa")
        self.assertEqual(re.match(r"((a)\s(abc|a))", "a a", re.I).group(1), "a a")
        self.assertEqual(re.match(r"((a)\s(abc|a)*)", "a aa", re.I).group(1), "a aa")

        assert '\u212a'.lower() == 'k' 
        self.assertTrue(re.match(r'K', '\u212a', re.I))
        self.assertTrue(re.match(r'k', '\u212a', re.I))
        self.assertTrue(re.match(r'\u212a', 'K', re.I))
        self.assertTrue(re.match(r'\u212a', 'k', re.I))
        assert '\u017f'.upper() == 'S' 
        self.assertTrue(re.match(r'S', '\u017f', re.I))
        self.assertTrue(re.match(r's', '\u017f', re.I))
        self.assertTrue(re.match(r'\u017f', 'S', re.I))
        self.assertTrue(re.match(r'\u017f', 's', re.I))
        assert '\ufb05'.upper() == '\ufb06'.upper() == 'ST' 
        self.assertTrue(re.match(r'\ufb05', '\ufb06', re.I))
        self.assertTrue(re.match(r'\ufb06', '\ufb05', re.I))

    def test_ignore_case_set(self):
        self.assertTrue(re.match(r'[19A]', 'A', re.I))
        self.assertTrue(re.match(r'[19a]', 'a', re.I))
        self.assertTrue(re.match(r'[19a]', 'A', re.I))
        self.assertTrue(re.match(r'[19A]', 'a', re.I))
        self.assertTrue(re.match(br'[19A]', b'A', re.I))
        self.assertTrue(re.match(br'[19a]', b'a', re.I))
        self.assertTrue(re.match(br'[19a]', b'A', re.I))
        self.assertTrue(re.match(br'[19A]', b'a', re.I))
        assert '\u212a'.lower() == 'k' 
        self.assertTrue(re.match(r'[19K]', '\u212a', re.I))
        self.assertTrue(re.match(r'[19k]', '\u212a', re.I))
        self.assertTrue(re.match(r'[19\u212a]', 'K', re.I))
        self.assertTrue(re.match(r'[19\u212a]', 'k', re.I))
        assert '\u017f'.upper() == 'S' 
        self.assertTrue(re.match(r'[19S]', '\u017f', re.I))
        self.assertTrue(re.match(r'[19s]', '\u017f', re.I))
        self.assertTrue(re.match(r'[19\u017f]', 'S', re.I))
        self.assertTrue(re.match(r'[19\u017f]', 's', re.I))
        assert '\ufb05'.upper() == '\ufb06'.upper() == 'ST' 
        self.assertTrue(re.match(r'[19\ufb05]', '\ufb06', re.I))
        self.assertTrue(re.match(r'[19\ufb06]', '\ufb05', re.I))

    def test_ignore_case_range(self):
        
        self.assertTrue(re.match(r'[9-a]', '_', re.I))
        self.assertIsNone(re.match(r'[9-A]', '_', re.I))
        self.assertTrue(re.match(br'[9-a]', b'_', re.I))
        self.assertIsNone(re.match(br'[9-A]', b'_', re.I))
        self.assertTrue(re.match(r'[\xc0-\xde]', '\xd7', re.I))
        self.assertIsNone(re.match(r'[\xc0-\xde]', '\xf7', re.I))
        self.assertTrue(re.match(r'[\xe0-\xfe]', '\xf7', re.I))
        self.assertIsNone(re.match(r'[\xe0-\xfe]', '\xd7', re.I))
        self.assertTrue(re.match(r'[\u0430-\u045f]', '\u0450', re.I))
        self.assertTrue(re.match(r'[\u0430-\u045f]', '\u0400', re.I))
        self.assertTrue(re.match(r'[\u0400-\u042f]', '\u0450', re.I))
        self.assertTrue(re.match(r'[\u0400-\u042f]', '\u0400', re.I))
        self.assertTrue(re.match(r'[\U00010428-\U0001044f]', '\U00010428', re.I))
        self.assertTrue(re.match(r'[\U00010428-\U0001044f]', '\U00010400', re.I))
        self.assertTrue(re.match(r'[\U00010400-\U00010427]', '\U00010428', re.I))
        self.assertTrue(re.match(r'[\U00010400-\U00010427]', '\U00010400', re.I))

        assert '\u212a'.lower() == 'k' 
        self.assertTrue(re.match(r'[J-M]', '\u212a', re.I))
        self.assertTrue(re.match(r'[j-m]', '\u212a', re.I))
        self.assertTrue(re.match(r'[\u2129-\u212b]', 'K', re.I))
        self.assertTrue(re.match(r'[\u2129-\u212b]', 'k', re.I))
        assert '\u017f'.upper() == 'S' 
        self.assertTrue(re.match(r'[R-T]', '\u017f', re.I))
        self.assertTrue(re.match(r'[r-t]', '\u017f', re.I))
        self.assertTrue(re.match(r'[\u017e-\u0180]', 'S', re.I))
        self.assertTrue(re.match(r'[\u017e-\u0180]', 's', re.I))
        assert '\ufb05'.upper() == '\ufb06'.upper() == 'ST' 
        self.assertTrue(re.match(r'[\ufb04-\ufb05]', '\ufb06', re.I))
        self.assertTrue(re.match(r'[\ufb06-\ufb07]', '\ufb05', re.I))

    def test_category(self):
        self.assertEqual(re.match(r"(\s)", " ").group(1), " ")

    def test_getlower(self):
        import _sre
        self.assertEqual(_sre.getlower(ord('A'), 0), ord('a'))
        self.assertEqual(_sre.getlower(ord('A'), re.LOCALE), ord('a'))
        self.assertEqual(_sre.getlower(ord('A'), re.UNICODE), ord('a'))

        self.assertEqual(re.match("abc", "ABC", re.I).group(0), "ABC")
        self.assertEqual(re.match(b"abc", b"ABC", re.I).group(0), b"ABC")

    def test_not_literal(self):
        self.assertEqual(re.search("\s([^a])", " b").group(1), "b")
        self.assertEqual(re.search("\s([^a]*)", " bb").group(1), "bb")

    def test_search_coverage(self):
        self.assertEqual(re.search("\s(b)", " b").group(1), "b")
        self.assertEqual(re.search("a\s", "a ").group(0), "a ")

    def assertMatch(self, pattern, text, match=None, span=None,
                    matcher=re.match):
        if match is None and span is None:
            
            match = text
            span = (0, len(text))
        elif match is None or span is None:
            raise ValueError('If match is not None, span should be specified '
                             '(and vice versa).')
        m = matcher(pattern, text)
        self.assertTrue(m)
        self.assertEqual(m.group(), match)
        self.assertEqual(m.span(), span)

    def test_re_escape(self):
        alnum_chars = string.ascii_letters + string.digits + '_'
        p = ''.join(chr(i) for i in range(256))
        for c in p:
            if c in alnum_chars:
                self.assertEqual(re.escape(c), c)
            elif c == '\x00':
                self.assertEqual(re.escape(c), '\\000')
            else:
                self.assertEqual(re.escape(c), '\\' + c)
            self.assertMatch(re.escape(c), c)
        self.assertMatch(re.escape(p), p)

    def test_re_escape_byte(self):
        alnum_chars = (string.ascii_letters + string.digits + '_').encode('ascii')
        p = bytes(range(256))
        for i in p:
            b = bytes([i])
            if b in alnum_chars:
                self.assertEqual(re.escape(b), b)
            elif i == 0:
                self.assertEqual(re.escape(b), b'\\000')
            else:
                self.assertEqual(re.escape(b), b'\\' + b)
            self.assertMatch(re.escape(b), b)
        self.assertMatch(re.escape(p), p)

    def test_re_escape_non_ascii(self):
        s = 'xxx\u2620\u2620\u2620xxx'
        s_escaped = re.escape(s)
        self.assertEqual(s_escaped, 'xxx\\\u2620\\\u2620\\\u2620xxx')
        self.assertMatch(s_escaped, s)
        self.assertMatch('.%s+.' % re.escape('\u2620'), s,
                         'x\u2620\u2620\u2620x', (2, 7), re.search)

    def test_re_escape_non_ascii_bytes(self):
        b = 'y\u2620y\u2620y'.encode('utf-8')
        b_escaped = re.escape(b)
        self.assertEqual(b_escaped, b'y\\\xe2\\\x98\\\xa0y\\\xe2\\\x98\\\xa0y')
        self.assertMatch(b_escaped, b)
        res = re.findall(re.escape('\u2620'.encode('utf-8')), b)
        self.assertEqual(len(res), 2)

    def test_pickling(self):
        import pickle
        oldpat = re.compile('a(?:b|(c|e){1,2}?|d)+?(.)', re.UNICODE)
        for proto in range(pickle.HIGHEST_PROTOCOL + 1):
            pickled = pickle.dumps(oldpat, proto)
            newpat = pickle.loads(pickled)
            self.assertEqual(newpat, oldpat)
        
        from re import _compile

    def test_constants(self):
        self.assertEqual(re.I, re.IGNORECASE)
        self.assertEqual(re.L, re.LOCALE)
        self.assertEqual(re.M, re.MULTILINE)
        self.assertEqual(re.S, re.DOTALL)
        self.assertEqual(re.X, re.VERBOSE)

    def test_flags(self):
        for flag in [re.I, re.M, re.X, re.S, re.L]:
            self.assertTrue(re.compile('^pattern$', flag))

    def test_sre_character_literals(self):
        for i in [0, 8, 16, 32, 64, 127, 128, 255, 256, 0xFFFF, 0x10000, 0x10FFFF]:
            if i < 256:
                self.assertTrue(re.match(r"\%03o" % i, chr(i)))
                self.assertTrue(re.match(r"\%03o0" % i, chr(i)+"0"))
                self.assertTrue(re.match(r"\%03o8" % i, chr(i)+"8"))
                self.assertTrue(re.match(r"\x%02x" % i, chr(i)))
                self.assertTrue(re.match(r"\x%02x0" % i, chr(i)+"0"))
                self.assertTrue(re.match(r"\x%02xz" % i, chr(i)+"z"))
            if i < 0x10000:
                self.assertTrue(re.match(r"\u%04x" % i, chr(i)))
                self.assertTrue(re.match(r"\u%04x0" % i, chr(i)+"0"))
                self.assertTrue(re.match(r"\u%04xz" % i, chr(i)+"z"))
            self.assertTrue(re.match(r"\U%08x" % i, chr(i)))
            self.assertTrue(re.match(r"\U%08x0" % i, chr(i)+"0"))
            self.assertTrue(re.match(r"\U%08xz" % i, chr(i)+"z"))
        self.assertTrue(re.match(r"\0", "\000"))
        self.assertTrue(re.match(r"\08", "\0008"))
        self.assertTrue(re.match(r"\01", "\001"))
        self.assertTrue(re.match(r"\018", "\0018"))
        self.assertTrue(re.match(r"\567", chr(0o167)))
        self.assertRaises(re.error, re.match, r"\911", "")
        self.assertRaises(re.error, re.match, r"\x1", "")
        self.assertRaises(re.error, re.match, r"\x1z", "")
        self.assertRaises(re.error, re.match, r"\u123", "")
        self.assertRaises(re.error, re.match, r"\u123z", "")
        self.assertRaises(re.error, re.match, r"\U0001234", "")
        self.assertRaises(re.error, re.match, r"\U0001234z", "")
        self.assertRaises(re.error, re.match, r"\U00110000", "")

    def test_sre_character_class_literals(self):
        for i in [0, 8, 16, 32, 64, 127, 128, 255, 256, 0xFFFF, 0x10000, 0x10FFFF]:
            if i < 256:
                self.assertTrue(re.match(r"[\%o]" % i, chr(i)))
                self.assertTrue(re.match(r"[\%o8]" % i, chr(i)))
                self.assertTrue(re.match(r"[\%03o]" % i, chr(i)))
                self.assertTrue(re.match(r"[\%03o0]" % i, chr(i)))
                self.assertTrue(re.match(r"[\%03o8]" % i, chr(i)))
                self.assertTrue(re.match(r"[\x%02x]" % i, chr(i)))
                self.assertTrue(re.match(r"[\x%02x0]" % i, chr(i)))
                self.assertTrue(re.match(r"[\x%02xz]" % i, chr(i)))
            if i < 0x10000:
                self.assertTrue(re.match(r"[\u%04x]" % i, chr(i)))
                self.assertTrue(re.match(r"[\u%04x0]" % i, chr(i)))
                self.assertTrue(re.match(r"[\u%04xz]" % i, chr(i)))
            self.assertTrue(re.match(r"[\U%08x]" % i, chr(i)))
            self.assertTrue(re.match(r"[\U%08x0]" % i, chr(i)+"0"))
            self.assertTrue(re.match(r"[\U%08xz]" % i, chr(i)+"z"))
        self.assertTrue(re.match(r"[\U0001d49c-\U0001d4b5]", "\U0001d49e"))
        self.assertRaises(re.error, re.match, r"[\911]", "")
        self.assertRaises(re.error, re.match, r"[\x1z]", "")
        self.assertRaises(re.error, re.match, r"[\u123z]", "")
        self.assertRaises(re.error, re.match, r"[\U0001234z]", "")
        self.assertRaises(re.error, re.match, r"[\U00110000]", "")

    def test_sre_byte_literals(self):
        for i in [0, 8, 16, 32, 64, 127, 128, 255]:
            self.assertTrue(re.match((r"\%03o" % i).encode(), bytes([i])))
            self.assertTrue(re.match((r"\%03o0" % i).encode(), bytes([i])+b"0"))
            self.assertTrue(re.match((r"\%03o8" % i).encode(), bytes([i])+b"8"))
            self.assertTrue(re.match((r"\x%02x" % i).encode(), bytes([i])))
            self.assertTrue(re.match((r"\x%02x0" % i).encode(), bytes([i])+b"0"))
            self.assertTrue(re.match((r"\x%02xz" % i).encode(), bytes([i])+b"z"))
        self.assertTrue(re.match(br"\u", b'u'))
        self.assertTrue(re.match(br"\U", b'U'))
        self.assertTrue(re.match(br"\0", b"\000"))
        self.assertTrue(re.match(br"\08", b"\0008"))
        self.assertTrue(re.match(br"\01", b"\001"))
        self.assertTrue(re.match(br"\018", b"\0018"))
        self.assertTrue(re.match(br"\567", bytes([0o167])))
        self.assertRaises(re.error, re.match, br"\911", b"")
        self.assertRaises(re.error, re.match, br"\x1", b"")
        self.assertRaises(re.error, re.match, br"\x1z", b"")

    def test_sre_byte_class_literals(self):
        for i in [0, 8, 16, 32, 64, 127, 128, 255]:
            self.assertTrue(re.match((r"[\%o]" % i).encode(), bytes([i])))
            self.assertTrue(re.match((r"[\%o8]" % i).encode(), bytes([i])))
            self.assertTrue(re.match((r"[\%03o]" % i).encode(), bytes([i])))
            self.assertTrue(re.match((r"[\%03o0]" % i).encode(), bytes([i])))
            self.assertTrue(re.match((r"[\%03o8]" % i).encode(), bytes([i])))
            self.assertTrue(re.match((r"[\x%02x]" % i).encode(), bytes([i])))
            self.assertTrue(re.match((r"[\x%02x0]" % i).encode(), bytes([i])))
            self.assertTrue(re.match((r"[\x%02xz]" % i).encode(), bytes([i])))
        self.assertTrue(re.match(br"[\u]", b'u'))
        self.assertTrue(re.match(br"[\U]", b'U'))
        self.assertRaises(re.error, re.match, br"[\911]", b"")
        self.assertRaises(re.error, re.match, br"[\x1z]", b"")

    def test_bug_113254(self):
        self.assertEqual(re.match(r'(a)|(b)', 'b').start(1), -1)
        self.assertEqual(re.match(r'(a)|(b)', 'b').end(1), -1)
        self.assertEqual(re.match(r'(a)|(b)', 'b').span(1), (-1, -1))

    def test_bug_527371(self):
        
        self.assertIsNone(re.match(r'(a)?a','a').lastindex)
        self.assertEqual(re.match(r'(a)(b)?b','ab').lastindex, 1)
        self.assertEqual(re.match(r'(?P<a>a)(?P<b>b)?b','ab').lastgroup, 'a')
        self.assertEqual(re.match("(?P<a>a(b))", "ab").lastgroup, 'a')
        self.assertEqual(re.match("((a))", "a").lastindex, 1)

    def test_bug_545855(self):
        
        
        self.assertRaises(re.error, re.compile, 'foo[a-')

    def test_bug_418626(self):
        
        
        
        self.assertEqual(re.match('.*?c', 10000*'ab'+'cd').end(0), 20001)
        self.assertEqual(re.match('.*?cd', 5000*'ab'+'c'+5000*'ab'+'cde').end(0),
                         20003)
        self.assertEqual(re.match('.*?cd', 20000*'abc'+'de').end(0), 60001)
        
        
        self.assertEqual(re.search('(a|b)*?c', 10000*'ab'+'cd').end(0), 20001)

    def test_bug_612074(self):
        pat="["+re.escape("\u2039")+"]"
        self.assertEqual(re.compile(pat) and 1, 1)

    def test_stack_overflow(self):
        
        
        self.assertEqual(re.match('(x)*', 50000*'x').group(1), 'x')
        self.assertEqual(re.match('(x)*y', 50000*'x'+'y').group(1), 'x')
        self.assertEqual(re.match('(x)*?y', 50000*'x'+'y').group(1), 'x')

    def test_unlimited_zero_width_repeat(self):
        
        self.assertIsNone(re.match(r'(?:a?)*y', 'z'))
        self.assertIsNone(re.match(r'(?:a?)+y', 'z'))
        self.assertIsNone(re.match(r'(?:a?){2,}y', 'z'))
        self.assertIsNone(re.match(r'(?:a?)*?y', 'z'))
        self.assertIsNone(re.match(r'(?:a?)+?y', 'z'))
        self.assertIsNone(re.match(r'(?:a?){2,}?y', 'z'))

    def test_scanner(self):
        def s_ident(scanner, token): return token
        def s_operator(scanner, token): return "op%s" % token
        def s_float(scanner, token): return float(token)
        def s_int(scanner, token): return int(token)

        scanner = Scanner([
            (r"[a-zA-Z_]\w*", s_ident),
            (r"\d+\.\d*", s_float),
            (r"\d+", s_int),
            (r"=|\+|-|\*|/", s_operator),
            (r"\s+", None),
            ])

        self.assertTrue(scanner.scanner.scanner("").pattern)

        self.assertEqual(scanner.scan("sum = 3*foo + 312.50 + bar"),
                         (['sum', 'op=', 3, 'op*', 'foo', 'op+', 312.5,
                           'op+', 'bar'], ''))

    def test_bug_448951(self):
        
        
        for op in '','?','*':
            self.assertEqual(re.match(r'((.%s):)?z'%op, 'z').groups(),
                             (None, None))
            self.assertEqual(re.match(r'((.%s):)?z'%op, 'a:z').groups(),
                             ('a:', 'a'))

    def test_bug_725106(self):
        
        self.assertEqual(re.match('^((a)|b)*', 'abc').groups(),
                         ('b', 'a'))
        self.assertEqual(re.match('^(([ab])|c)*', 'abc').groups(),
                         ('c', 'b'))
        self.assertEqual(re.match('^((d)|[ab])*', 'abc').groups(),
                         ('b', None))
        self.assertEqual(re.match('^((a)c|[ab])*', 'abc').groups(),
                         ('b', None))
        self.assertEqual(re.match('^((a)|b)*?c', 'abc').groups(),
                         ('b', 'a'))
        self.assertEqual(re.match('^(([ab])|c)*?d', 'abcd').groups(),
                         ('c', 'b'))
        self.assertEqual(re.match('^((d)|[ab])*?c', 'abc').groups(),
                         ('b', None))
        self.assertEqual(re.match('^((a)c|[ab])*?c', 'abc').groups(),
                         ('b', None))

    def test_bug_725149(self):
        
        self.assertEqual(re.match('(a)(?:(?=(b)*)c)*', 'abb').groups(),
                         ('a', None))
        self.assertEqual(re.match('(a)((?!(b)*))*', 'abb').groups(),
                         ('a', None, None))

    def test_bug_764548(self):
        
        class my_unicode(str): pass
        pat = re.compile(my_unicode("abc"))
        self.assertIsNone(pat.match("xyz"))

    def test_finditer(self):
        iter = re.finditer(r":+", "a:b::c:::d")
        self.assertEqual([item.group(0) for item in iter],
                         [":", "::", ":::"])

        pat = re.compile(r":+")
        iter = pat.finditer("a:b::c:::d", 1, 10)
        self.assertEqual([item.group(0) for item in iter],
                         [":", "::", ":::"])

        pat = re.compile(r":+")
        iter = pat.finditer("a:b::c:::d", pos=1, endpos=10)
        self.assertEqual([item.group(0) for item in iter],
                         [":", "::", ":::"])

        pat = re.compile(r":+")
        iter = pat.finditer("a:b::c:::d", endpos=10, pos=1)
        self.assertEqual([item.group(0) for item in iter],
                         [":", "::", ":::"])

        pat = re.compile(r":+")
        iter = pat.finditer("a:b::c:::d", pos=3, endpos=8)
        self.assertEqual([item.group(0) for item in iter],
                         ["::", "::"])

    def test_bug_926075(self):
        self.assertIsNot(re.compile('bug_926075'),
                         re.compile(b'bug_926075'))

    def test_bug_931848(self):
        pattern = "[\u002E\u3002\uFF0E\uFF61]"
        self.assertEqual(re.compile(pattern).split("a.b.c"),
                         ['a','b','c'])

    def test_bug_581080(self):
        iter = re.finditer(r"\s", "a b")
        self.assertEqual(next(iter).span(), (1,2))
        self.assertRaises(StopIteration, next, iter)

        scanner = re.compile(r"\s").scanner("a b")
        self.assertEqual(scanner.search().span(), (1, 2))
        self.assertIsNone(scanner.search())

    def test_bug_817234(self):
        iter = re.finditer(r".*", "asdf")
        self.assertEqual(next(iter).span(), (0, 4))
        self.assertEqual(next(iter).span(), (4, 4))
        self.assertRaises(StopIteration, next, iter)

    def test_bug_6561(self):
        
        
        
        decimal_digits = [
            '\u0037', 
            '\u0e58', 
            '\uff10', 
            ]
        for x in decimal_digits:
            self.assertEqual(re.match('^\d$', x).group(0), x)

        not_decimal_digits = [
            '\u2165', 
            '\u3039', 
            '\u2082', 
            '\u32b4', 
            ]
        for x in not_decimal_digits:
            self.assertIsNone(re.match('^\d$', x))

    def test_empty_array(self):
        
        import array
        for typecode in 'bBuhHiIlLfd':
            a = array.array(typecode)
            self.assertIsNone(re.compile(b"bla").match(a))
            self.assertEqual(re.compile(b"").match(a).groups(), ())

    def test_inline_flags(self):
        
        upper_char = chr(0x1ea0) 
        lower_char = chr(0x1ea1) 

        p = re.compile(upper_char, re.I | re.U)
        q = p.match(lower_char)
        self.assertTrue(q)

        p = re.compile(lower_char, re.I | re.U)
        q = p.match(upper_char)
        self.assertTrue(q)

        p = re.compile('(?i)' + upper_char, re.U)
        q = p.match(lower_char)
        self.assertTrue(q)

        p = re.compile('(?i)' + lower_char, re.U)
        q = p.match(upper_char)
        self.assertTrue(q)

        p = re.compile('(?iu)' + upper_char)
        q = p.match(lower_char)
        self.assertTrue(q)

        p = re.compile('(?iu)' + lower_char)
        q = p.match(upper_char)
        self.assertTrue(q)

    def test_dollar_matches_twice(self):
        "$ matches the end of string, and just before the terminating \n"
        pattern = re.compile('$')
        self.assertEqual(pattern.sub('
        self.assertEqual(pattern.sub('
        self.assertEqual(pattern.sub('

        pattern = re.compile('$', re.MULTILINE)
        self.assertEqual(pattern.sub('
        self.assertEqual(pattern.sub('
        self.assertEqual(pattern.sub('

    def test_bytes_str_mixing(self):
        
        pat = re.compile('.')
        bpat = re.compile(b'.')
        self.assertRaises(TypeError, pat.match, b'b')
        self.assertRaises(TypeError, bpat.match, 'b')
        self.assertRaises(TypeError, pat.sub, b'b', 'c')
        self.assertRaises(TypeError, pat.sub, 'b', b'c')
        self.assertRaises(TypeError, pat.sub, b'b', b'c')
        self.assertRaises(TypeError, bpat.sub, b'b', 'c')
        self.assertRaises(TypeError, bpat.sub, 'b', b'c')
        self.assertRaises(TypeError, bpat.sub, 'b', 'c')

    def test_ascii_and_unicode_flag(self):
        
        for flags in (0, re.UNICODE):
            pat = re.compile('\xc0', flags | re.IGNORECASE)
            self.assertTrue(pat.match('\xe0'))
            pat = re.compile('\w', flags)
            self.assertTrue(pat.match('\xe0'))
        pat = re.compile('\xc0', re.ASCII | re.IGNORECASE)
        self.assertIsNone(pat.match('\xe0'))
        pat = re.compile('(?a)\xc0', re.IGNORECASE)
        self.assertIsNone(pat.match('\xe0'))
        pat = re.compile('\w', re.ASCII)
        self.assertIsNone(pat.match('\xe0'))
        pat = re.compile('(?a)\w')
        self.assertIsNone(pat.match('\xe0'))
        
        for flags in (0, re.ASCII):
            pat = re.compile(b'\xc0', flags | re.IGNORECASE)
            self.assertIsNone(pat.match(b'\xe0'))
            pat = re.compile(b'\w', flags)
            self.assertIsNone(pat.match(b'\xe0'))
        
        self.assertRaises(ValueError, re.compile, b'\w', re.UNICODE)
        self.assertRaises(ValueError, re.compile, b'(?u)\w')
        self.assertRaises(ValueError, re.compile, '\w', re.UNICODE | re.ASCII)
        self.assertRaises(ValueError, re.compile, '(?u)\w', re.ASCII)
        self.assertRaises(ValueError, re.compile, '(?a)\w', re.UNICODE)
        self.assertRaises(ValueError, re.compile, '(?au)\w')

    def test_bug_6509(self):
        
        
        pat = re.compile('a(\w)')
        self.assertEqual(pat.sub('b\\1', 'ac'), 'bc')
        pat = re.compile('a(.)')
        self.assertEqual(pat.sub('b\\1', 'a\u1234'), 'b\u1234')
        pat = re.compile('..')
        self.assertEqual(pat.sub(lambda m: 'str', 'a5'), 'str')

        
        pat = re.compile(b'a(\w)')
        self.assertEqual(pat.sub(b'b\\1', b'ac'), b'bc')
        pat = re.compile(b'a(.)')
        self.assertEqual(pat.sub(b'b\\1', b'a\xCD'), b'b\xCD')
        pat = re.compile(b'..')
        self.assertEqual(pat.sub(lambda m: b'bytes', b'a5'), b'bytes')

    def test_dealloc(self):
        
        import _sre
        
        
        
        
        long_overflow = 2**128
        self.assertRaises(TypeError, re.finditer, "a", {})
        self.assertRaises(OverflowError, _sre.compile, "abc", 0, [long_overflow])
        self.assertRaises(TypeError, _sre.compile, {}, 0, [])

    def test_search_dot_unicode(self):
        self.assertTrue(re.search("123.*-", '123abc-'))
        self.assertTrue(re.search("123.*-", '123\xe9-'))
        self.assertTrue(re.search("123.*-", '123\u20ac-'))
        self.assertTrue(re.search("123.*-", '123\U0010ffff-'))
        self.assertTrue(re.search("123.*-", '123\xe9\u20ac\U0010ffff-'))

    def test_compile(self):
        
        pattern = re.compile('random pattern')
        self.assertIsInstance(pattern, re._pattern_type)
        same_pattern = re.compile(pattern)
        self.assertIsInstance(same_pattern, re._pattern_type)
        self.assertIs(same_pattern, pattern)
        
        self.assertRaises(TypeError, re.compile, 0)

    def test_bug_13899(self):
        "[\A]" should work like "A" but matches
        
        self.assertEqual(re.findall(r'[\A\B\b\C\Z]', 'AB\bCZ'),
                         ['A', 'B', '\b', 'C', 'Z'])

    @bigmemtest(size=_2G, memuse=1)
    def test_large_search(self, size):
        
        s = 'a' * size
        m = re.search('$', s)
        self.assertIsNotNone(m)
        self.assertEqual(m.start(), size)
        self.assertEqual(m.end(), size)

    
    
    @bigmemtest(size=_2G, memuse=16 + 2)
    def test_large_subn(self, size):
        
        s = 'a' * size
        r, n = re.subn('', '', s)
        self.assertEqual(r, s)
        self.assertEqual(n, size + 1)

    def test_bug_16688(self):
        
        
        self.assertEqual(re.findall(r"(?i)(a)\1", "aa \u0100"), ['a'])
        self.assertEqual(re.match(r"(?s).{1,3}", "\u0100\u0100").span(), (0, 2))

    def test_repeat_minmax_overflow(self):
        
        string = "x" * 100000
        self.assertEqual(re.match(r".{65535}", string).span(), (0, 65535))
        self.assertEqual(re.match(r".{,65535}", string).span(), (0, 65535))
        self.assertEqual(re.match(r".{65535,}?", string).span(), (0, 65535))
        self.assertEqual(re.match(r".{65536}", string).span(), (0, 65536))
        self.assertEqual(re.match(r".{,65536}", string).span(), (0, 65536))
        self.assertEqual(re.match(r".{65536,}?", string).span(), (0, 65536))
        
        self.assertRaises(OverflowError, re.compile, r".{%d}" % 2**128)
        self.assertRaises(OverflowError, re.compile, r".{,%d}" % 2**128)
        self.assertRaises(OverflowError, re.compile, r".{%d,}?" % 2**128)
        self.assertRaises(OverflowError, re.compile, r".{%d,%d}" % (2**129, 2**128))

    @cpython_only
    def test_repeat_minmax_overflow_maxrepeat(self):
        try:
            from _sre import MAXREPEAT
        except ImportError:
            self.skipTest('requires _sre.MAXREPEAT constant')
        string = "x" * 100000
        self.assertIsNone(re.match(r".{%d}" % (MAXREPEAT - 1), string))
        self.assertEqual(re.match(r".{,%d}" % (MAXREPEAT - 1), string).span(),
                         (0, 100000))
        self.assertIsNone(re.match(r".{%d,}?" % (MAXREPEAT - 1), string))
        self.assertRaises(OverflowError, re.compile, r".{%d}" % MAXREPEAT)
        self.assertRaises(OverflowError, re.compile, r".{,%d}" % MAXREPEAT)
        self.assertRaises(OverflowError, re.compile, r".{%d,}?" % MAXREPEAT)

    def test_backref_group_name_in_exception(self):
        
        with self.assertRaisesRegex(sre_constants.error, '<foo>'):
            re.compile('(?P=<foo>)')

    def test_group_name_in_exception(self):
        
        with self.assertRaisesRegex(sre_constants.error, '\?foo'):
            re.compile('(?P<?foo>)')

    def test_issue17998(self):
        for reps in '*', '+', '?', '{1}':
            for mod in '', '?':
                pattern = '.' + reps + mod + 'yz'
                self.assertEqual(re.compile(pattern, re.S).findall('xyz'),
                                 ['xyz'], msg=pattern)
                pattern = pattern.encode()
                self.assertEqual(re.compile(pattern, re.S).findall(b'xyz'),
                                 [b'xyz'], msg=pattern)

    def test_match_repr(self):
        for string in '[abracadabra]', S('[abracadabra]'):
            m = re.search(r'(.+)(.*?)\1', string)
            self.assertEqual(repr(m), "<%s.%s object; "
                             "span=(1, 12), match='abracadabra'>" %
                             (type(m).__module__, type(m).__qualname__))
        for string in (b'[abracadabra]', B(b'[abracadabra]'),
                       bytearray(b'[abracadabra]'),
                       memoryview(b'[abracadabra]')):
            m = re.search(rb'(.+)(.*?)\1', string)
            self.assertEqual(repr(m), "<%s.%s object; "
                             "span=(1, 12), match=b'abracadabra'>" %
                             (type(m).__module__, type(m).__qualname__))

        first, second = list(re.finditer("(aa)|(bb)", "aa bb"))
        self.assertEqual(repr(first), "<%s.%s object; "
                         "span=(0, 2), match='aa'>" %
                         (type(second).__module__, type(first).__qualname__))
        self.assertEqual(repr(second), "<%s.%s object; "
                         "span=(3, 5), match='bb'>" %
                         (type(second).__module__, type(second).__qualname__))


    def test_bug_2537(self):
        
        for outer_op in ('{0,}', '*', '+', '{1,187}'):
            for inner_op in ('{0,}', '*', '?'):
                r = re.compile("^((x|y)%s)%s" % (inner_op, outer_op))
                m = r.match("xyyzy")
                self.assertEqual(m.group(0), "xyy")
                self.assertEqual(m.group(1), "")
                self.assertEqual(m.group(2), "y")

    def test_debug_flag(self):
        pat = r'(\.)(?:[ch]|py)(?(1)$|: )'
        with captured_stdout() as out:
            re.compile(pat, re.DEBUG)
        dump = '''\
subpattern 1
  literal 46
subpattern None
  branch
    in
      literal 99
      literal 104
  or
    literal 112
    literal 121
subpattern None
  groupref_exists 1
    at at_end
  else
    literal 58
    literal 32
'''
        self.assertEqual(out.getvalue(), dump)
        
        
        with captured_stdout() as out:
            re.compile(pat, re.DEBUG)
        self.assertEqual(out.getvalue(), dump)

    def test_keyword_parameters(self):
        
        pat = re.compile(r'(ab)')
        self.assertEqual(
            pat.match(string='abracadabra', pos=7, endpos=10).span(), (7, 9))
        self.assertEqual(
            pat.fullmatch(string='abracadabra', pos=7, endpos=9).span(), (7, 9))
        self.assertEqual(
            pat.search(string='abracadabra', pos=3, endpos=10).span(), (7, 9))
        self.assertEqual(
            pat.findall(string='abracadabra', pos=3, endpos=10), ['ab'])
        self.assertEqual(
            pat.split(string='abracadabra', maxsplit=1),
            ['', 'ab', 'racadabra'])
        self.assertEqual(
            pat.scanner(string='abracadabra', pos=3, endpos=10).search().span(),
            (7, 9))

    def test_bug_20998(self):
        
        
        self.assertEqual(re.fullmatch('[a-c]+', 'ABC', re.I).span(), (0, 3))

    def test_locale_caching(self):
        
        oldlocale = locale.setlocale(locale.LC_CTYPE)
        self.addCleanup(locale.setlocale, locale.LC_CTYPE, oldlocale)
        for loc in 'en_US.iso88591', 'en_US.utf8':
            try:
                locale.setlocale(locale.LC_CTYPE, loc)
            except locale.Error:
                
                self.skipTest('test needs %s locale' % loc)

        re.purge()
        self.check_en_US_iso88591()
        self.check_en_US_utf8()
        re.purge()
        self.check_en_US_utf8()
        self.check_en_US_iso88591()

    def check_en_US_iso88591(self):
        locale.setlocale(locale.LC_CTYPE, 'en_US.iso88591')
        self.assertTrue(re.match(b'\xc5\xe5', b'\xc5\xe5', re.L|re.I))
        self.assertTrue(re.match(b'\xc5', b'\xe5', re.L|re.I))
        self.assertTrue(re.match(b'\xe5', b'\xc5', re.L|re.I))
        self.assertTrue(re.match(b'(?Li)\xc5\xe5', b'\xc5\xe5'))
        self.assertTrue(re.match(b'(?Li)\xc5', b'\xe5'))
        self.assertTrue(re.match(b'(?Li)\xe5', b'\xc5'))

    def check_en_US_utf8(self):
        locale.setlocale(locale.LC_CTYPE, 'en_US.utf8')
        self.assertTrue(re.match(b'\xc5\xe5', b'\xc5\xe5', re.L|re.I))
        self.assertIsNone(re.match(b'\xc5', b'\xe5', re.L|re.I))
        self.assertIsNone(re.match(b'\xe5', b'\xc5', re.L|re.I))
        self.assertTrue(re.match(b'(?Li)\xc5\xe5', b'\xc5\xe5'))
        self.assertIsNone(re.match(b'(?Li)\xc5', b'\xe5'))
        self.assertIsNone(re.match(b'(?Li)\xe5', b'\xc5'))


class PatternReprTests(unittest.TestCase):
    def check(self, pattern, expected):
        self.assertEqual(repr(re.compile(pattern)), expected)

    def check_flags(self, pattern, flags, expected):
        self.assertEqual(repr(re.compile(pattern, flags)), expected)

    def test_without_flags(self):
        self.check('random pattern',
                   "re.compile('random pattern')")

    def test_single_flag(self):
        self.check_flags('random pattern', re.IGNORECASE,
            "re.compile('random pattern', re.IGNORECASE)")

    def test_multiple_flags(self):
        self.check_flags('random pattern', re.I|re.S|re.X,
            "re.compile('random pattern', "
            "re.IGNORECASE|re.DOTALL|re.VERBOSE)")

    def test_unicode_flag(self):
        self.check_flags('random pattern', re.U,
                         "re.compile('random pattern')")
        self.check_flags('random pattern', re.I|re.S|re.U,
                         "re.compile('random pattern', "
                         "re.IGNORECASE|re.DOTALL)")

    def test_inline_flags(self):
        self.check('(?i)pattern',
                   "re.compile('(?i)pattern', re.IGNORECASE)")

    def test_unknown_flags(self):
        self.check_flags('random pattern', 0x123000,
                         "re.compile('random pattern', 0x123000)")
        self.check_flags('random pattern', 0x123000|re.I,
            "re.compile('random pattern', re.IGNORECASE|0x123000)")

    def test_bytes(self):
        self.check(b'bytes pattern',
                   "re.compile(b'bytes pattern')")
        self.check_flags(b'bytes pattern', re.A,
                         "re.compile(b'bytes pattern', re.ASCII)")

    def test_quotes(self):
        self.check('random "double quoted" pattern',
            '''re.compile('random "double quoted" pattern')''')
        self.check("random 'single quoted' pattern",
            '''re.compile("random 'single quoted' pattern")''')
        self.check('''both 'single' and "double" quotes''',
            '''re.compile('both \\'single\\' and "double" quotes')''')

    def test_long_pattern(self):
        pattern = 'Very %spattern' % ('long ' * 1000)
        r = repr(re.compile(pattern))
        self.assertLess(len(r), 300)
        self.assertEqual(r[:30], "re.compile('Very long long lon")
        r = repr(re.compile(pattern, re.I))
        self.assertLess(len(r), 300)
        self.assertEqual(r[:30], "re.compile('Very long long lon")
        self.assertEqual(r[-16:], ", re.IGNORECASE)")


class ImplementationTest(unittest.TestCase):
    """
    Test implementation details of the re module.
    """

    def test_overlap_table(self):
        f = sre_compile._generate_overlap_table
        self.assertEqual(f(""), [])
        self.assertEqual(f("a"), [0])
        self.assertEqual(f("abcd"), [0, 0, 0, 0])
        self.assertEqual(f("aaaa"), [0, 1, 2, 3])
        self.assertEqual(f("ababba"), [0, 0, 1, 2, 0, 1])
        self.assertEqual(f("abcabdac"), [0, 0, 0, 1, 2, 0, 1, 0])


class ExternalTests(unittest.TestCase):

    def test_re_benchmarks(self):
        're_tests benchmarks'
        from test.re_tests import benchmarks
        for pattern, s in benchmarks:
            with self.subTest(pattern=pattern, string=s):
                p = re.compile(pattern)
                self.assertTrue(p.search(s))
                self.assertTrue(p.match(s))
                self.assertTrue(p.fullmatch(s))
                s2 = ' '*10000 + s + ' '*10000
                self.assertTrue(p.search(s2))
                self.assertTrue(p.match(s2, 10000))
                self.assertTrue(p.match(s2, 10000, 10000 + len(s)))
                self.assertTrue(p.fullmatch(s2, 10000, 10000 + len(s)))

    def test_re_tests(self):
        're_tests test suite'
        from test.re_tests import tests, SUCCEED, FAIL, SYNTAX_ERROR
        for t in tests:
            pattern = s = outcome = repl = expected = None
            if len(t) == 5:
                pattern, s, outcome, repl, expected = t
            elif len(t) == 3:
                pattern, s, outcome = t
            else:
                raise ValueError('Test tuples should have 3 or 5 fields', t)

            with self.subTest(pattern=pattern, string=s):
                if outcome == SYNTAX_ERROR:  
                    with self.assertRaises(re.error):
                        re.compile(pattern)
                    continue

                obj = re.compile(pattern)
                result = obj.search(s)
                if outcome == FAIL:
                    self.assertIsNone(result, 'Succeeded incorrectly')
                    continue

                with self.subTest():
                    self.assertTrue(result, 'Failed incorrectly')
                    
                    
                    start, end = result.span(0)
                    vardict = {'found': result.group(0),
                               'groups': result.group(),
                               'flags': result.re.flags}
                    for i in range(1, 100):
                        try:
                            gi = result.group(i)
                            
                            if gi is None:
                                gi = "None"
                        except IndexError:
                            gi = "Error"
                        vardict['g%d' % i] = gi
                    for i in result.re.groupindex.keys():
                        try:
                            gi = result.group(i)
                            if gi is None:
                                gi = "None"
                        except IndexError:
                            gi = "Error"
                        vardict[i] = gi
                    self.assertEqual(eval(repl, vardict), expected,
                                     'grouping error')

                
                
                try:
                    bpat = bytes(pattern, "ascii")
                    bs = bytes(s, "ascii")
                except UnicodeEncodeError:
                    
                    pass
                else:
                    with self.subTest('bytes pattern match'):
                        bpat = re.compile(bpat)
                        self.assertTrue(bpat.search(bs))

                
                
                
                
                if (pattern[:2] != r'\B' and pattern[-2:] != r'\B'
                            and result is not None):
                    with self.subTest('range-limited match'):
                        obj = re.compile(pattern)
                        self.assertTrue(obj.search(s, start, end + 1))

                
                
                with self.subTest('case-insensitive match'):
                    obj = re.compile(pattern, re.IGNORECASE)
                    self.assertTrue(obj.search(s))

                
                
                if '(?u)' not in pattern:
                    with self.subTest('locale-sensitive match'):
                        obj = re.compile(pattern, re.LOCALE)
                        self.assertTrue(obj.search(s))

                
                
                with self.subTest('unicode-sensitive match'):
                    obj = re.compile(pattern, re.UNICODE)
                    self.assertTrue(obj.search(s))


if __name__ == "__main__":
    unittest.main()
