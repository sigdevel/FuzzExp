import ast
import types
import decimal
import unittest

a_global = 'global variable'








class TestCase(unittest.TestCase):
    def assertAllRaise(self, exception_type, regex, error_strings):
        for str in error_strings:
            with self.subTest(str=str):
                with self.assertRaisesRegex(exception_type, regex):
                    eval(str)

    def test__format__lookup(self):
        
        class X:
            def __format__(self, spec):
                return 'class'

        x = X()

        
        
        y = X()
        y.__format__ = types.MethodType(lambda self, spec: 'instance', y)

        self.assertEqual(f'{y}', format(y))
        self.assertEqual(f'{y}', 'class')
        self.assertEqual(format(x), format(y))

        
        
        
        self.assertEqual(x.__format__(''), 'class')
        self.assertEqual(y.__format__(''), 'instance')

        
        self.assertEqual(type(x).__format__(x, ''), 'class')
        self.assertEqual(type(y).__format__(y, ''), 'class')

    def test_ast(self):
        
        class X:
            def __init__(self):
                self.called = False
            def __call__(self):
                self.called = True
                return 4
        x = X()
        expr = """
a = 10
f'{a * x()}'"""
        t = ast.parse(expr)
        c = compile(t, '', 'exec')

        
        self.assertFalse(x.called)

        
        exec(c)

        
        self.assertTrue(x.called)

    def test_ast_line_numbers(self):
        expr = """
a = 10
f'{a * x()}'"""
        t = ast.parse(expr)
        self.assertEqual(type(t), ast.Module)
        self.assertEqual(len(t.body), 2)
        
        self.assertEqual(type(t.body[0]), ast.Assign)
        self.assertEqual(t.body[0].lineno, 2)
        
        self.assertEqual(type(t.body[1]), ast.Expr)
        self.assertEqual(type(t.body[1].value), ast.JoinedStr)
        self.assertEqual(len(t.body[1].value.values), 1)
        self.assertEqual(type(t.body[1].value.values[0]), ast.FormattedValue)
        self.assertEqual(t.body[1].lineno, 3)
        self.assertEqual(t.body[1].value.lineno, 3)
        self.assertEqual(t.body[1].value.values[0].lineno, 3)
        
        binop = t.body[1].value.values[0].value
        self.assertEqual(type(binop), ast.BinOp)
        self.assertEqual(type(binop.left), ast.Name)
        self.assertEqual(type(binop.op), ast.Mult)
        self.assertEqual(type(binop.right), ast.Call)
        self.assertEqual(binop.lineno, 3)
        self.assertEqual(binop.left.lineno, 3)
        self.assertEqual(binop.right.lineno, 3)
        self.assertEqual(binop.col_offset, 3)
        self.assertEqual(binop.left.col_offset, 3)
        self.assertEqual(binop.right.col_offset, 7)

    def test_ast_line_numbers_multiple_formattedvalues(self):
        expr = """
f'no formatted values'
f'eggs {a * x()} spam {b + y()}'"""
        t = ast.parse(expr)
        self.assertEqual(type(t), ast.Module)
        self.assertEqual(len(t.body), 2)
        
        self.assertEqual(type(t.body[0]), ast.Expr)
        self.assertEqual(type(t.body[0].value), ast.JoinedStr)
        self.assertEqual(t.body[0].lineno, 2)
        
        self.assertEqual(type(t.body[1]), ast.Expr)
        self.assertEqual(type(t.body[1].value), ast.JoinedStr)
        self.assertEqual(len(t.body[1].value.values), 4)
        self.assertEqual(type(t.body[1].value.values[0]), ast.Str)
        self.assertEqual(type(t.body[1].value.values[1]), ast.FormattedValue)
        self.assertEqual(type(t.body[1].value.values[2]), ast.Str)
        self.assertEqual(type(t.body[1].value.values[3]), ast.FormattedValue)
        self.assertEqual(t.body[1].lineno, 3)
        self.assertEqual(t.body[1].value.lineno, 3)
        self.assertEqual(t.body[1].value.values[0].lineno, 3)
        self.assertEqual(t.body[1].value.values[1].lineno, 3)
        self.assertEqual(t.body[1].value.values[2].lineno, 3)
        self.assertEqual(t.body[1].value.values[3].lineno, 3)
        
        binop1 = t.body[1].value.values[1].value
        self.assertEqual(type(binop1), ast.BinOp)
        self.assertEqual(type(binop1.left), ast.Name)
        self.assertEqual(type(binop1.op), ast.Mult)
        self.assertEqual(type(binop1.right), ast.Call)
        self.assertEqual(binop1.lineno, 3)
        self.assertEqual(binop1.left.lineno, 3)
        self.assertEqual(binop1.right.lineno, 3)
        self.assertEqual(binop1.col_offset, 8)
        self.assertEqual(binop1.left.col_offset, 8)
        self.assertEqual(binop1.right.col_offset, 12)
        
        binop2 = t.body[1].value.values[3].value
        self.assertEqual(type(binop2), ast.BinOp)
        self.assertEqual(type(binop2.left), ast.Name)
        self.assertEqual(type(binop2.op), ast.Add)
        self.assertEqual(type(binop2.right), ast.Call)
        self.assertEqual(binop2.lineno, 3)
        self.assertEqual(binop2.left.lineno, 3)
        self.assertEqual(binop2.right.lineno, 3)
        self.assertEqual(binop2.col_offset, 23)
        self.assertEqual(binop2.left.col_offset, 23)
        self.assertEqual(binop2.right.col_offset, 27)

    def test_ast_line_numbers_nested(self):
        expr = """
a = 10
f'{a * f"-{x()}-"}'"""
        t = ast.parse(expr)
        self.assertEqual(type(t), ast.Module)
        self.assertEqual(len(t.body), 2)
        
        self.assertEqual(type(t.body[0]), ast.Assign)
        self.assertEqual(t.body[0].lineno, 2)
        
        self.assertEqual(type(t.body[1]), ast.Expr)
        self.assertEqual(type(t.body[1].value), ast.JoinedStr)
        self.assertEqual(len(t.body[1].value.values), 1)
        self.assertEqual(type(t.body[1].value.values[0]), ast.FormattedValue)
        self.assertEqual(t.body[1].lineno, 3)
        self.assertEqual(t.body[1].value.lineno, 3)
        self.assertEqual(t.body[1].value.values[0].lineno, 3)
        
        binop = t.body[1].value.values[0].value
        self.assertEqual(type(binop), ast.BinOp)
        self.assertEqual(type(binop.left), ast.Name)
        self.assertEqual(type(binop.op), ast.Mult)
        self.assertEqual(type(binop.right), ast.JoinedStr)
        self.assertEqual(binop.lineno, 3)
        self.assertEqual(binop.left.lineno, 3)
        self.assertEqual(binop.right.lineno, 3)
        self.assertEqual(binop.col_offset, 3)
        self.assertEqual(binop.left.col_offset, 3)
        self.assertEqual(binop.right.col_offset, 7)
        
        self.assertEqual(len(binop.right.values), 3)
        self.assertEqual(type(binop.right.values[0]), ast.Str)
        self.assertEqual(type(binop.right.values[1]), ast.FormattedValue)
        self.assertEqual(type(binop.right.values[2]), ast.Str)
        self.assertEqual(binop.right.values[0].lineno, 3)
        self.assertEqual(binop.right.values[1].lineno, 3)
        self.assertEqual(binop.right.values[2].lineno, 3)
        call = binop.right.values[1].value
        self.assertEqual(type(call), ast.Call)
        self.assertEqual(call.lineno, 3)
        self.assertEqual(call.col_offset, 11)

    def test_ast_line_numbers_duplicate_expression(self):
        """Duplicate expression

        NOTE: this is currently broken, always sets location of the first
        expression.
        """
        expr = """
a = 10
f'{a * x()} {a * x()} {a * x()}'
"""
        t = ast.parse(expr)
        self.assertEqual(type(t), ast.Module)
        self.assertEqual(len(t.body), 2)
        
        self.assertEqual(type(t.body[0]), ast.Assign)
        self.assertEqual(t.body[0].lineno, 2)
        
        self.assertEqual(type(t.body[1]), ast.Expr)
        self.assertEqual(type(t.body[1].value), ast.JoinedStr)
        self.assertEqual(len(t.body[1].value.values), 5)
        self.assertEqual(type(t.body[1].value.values[0]), ast.FormattedValue)
        self.assertEqual(type(t.body[1].value.values[1]), ast.Str)
        self.assertEqual(type(t.body[1].value.values[2]), ast.FormattedValue)
        self.assertEqual(type(t.body[1].value.values[3]), ast.Str)
        self.assertEqual(type(t.body[1].value.values[4]), ast.FormattedValue)
        self.assertEqual(t.body[1].lineno, 3)
        self.assertEqual(t.body[1].value.lineno, 3)
        self.assertEqual(t.body[1].value.values[0].lineno, 3)
        self.assertEqual(t.body[1].value.values[1].lineno, 3)
        self.assertEqual(t.body[1].value.values[2].lineno, 3)
        self.assertEqual(t.body[1].value.values[3].lineno, 3)
        self.assertEqual(t.body[1].value.values[4].lineno, 3)
        
        binop = t.body[1].value.values[0].value
        self.assertEqual(type(binop), ast.BinOp)
        self.assertEqual(type(binop.left), ast.Name)
        self.assertEqual(type(binop.op), ast.Mult)
        self.assertEqual(type(binop.right), ast.Call)
        self.assertEqual(binop.lineno, 3)
        self.assertEqual(binop.left.lineno, 3)
        self.assertEqual(binop.right.lineno, 3)
        self.assertEqual(binop.col_offset, 3)
        self.assertEqual(binop.left.col_offset, 3)
        self.assertEqual(binop.right.col_offset, 7)
        
        binop = t.body[1].value.values[2].value
        self.assertEqual(type(binop), ast.BinOp)
        self.assertEqual(type(binop.left), ast.Name)
        self.assertEqual(type(binop.op), ast.Mult)
        self.assertEqual(type(binop.right), ast.Call)
        self.assertEqual(binop.lineno, 3)
        self.assertEqual(binop.left.lineno, 3)
        self.assertEqual(binop.right.lineno, 3)
        self.assertEqual(binop.col_offset, 3)  
        self.assertEqual(binop.left.col_offset, 3)  
        self.assertEqual(binop.right.col_offset, 7)  
        
        binop = t.body[1].value.values[4].value
        self.assertEqual(type(binop), ast.BinOp)
        self.assertEqual(type(binop.left), ast.Name)
        self.assertEqual(type(binop.op), ast.Mult)
        self.assertEqual(type(binop.right), ast.Call)
        self.assertEqual(binop.lineno, 3)
        self.assertEqual(binop.left.lineno, 3)
        self.assertEqual(binop.right.lineno, 3)
        self.assertEqual(binop.col_offset, 3)  
        self.assertEqual(binop.left.col_offset, 3)  
        self.assertEqual(binop.right.col_offset, 7)  

    def test_ast_line_numbers_multiline_fstring(self):
        
        
        
        
        expr = """
a = 10
f'''
  {a
     *
       x()}
non-important content
'''
"""
        t = ast.parse(expr)
        self.assertEqual(type(t), ast.Module)
        self.assertEqual(len(t.body), 2)
        
        self.assertEqual(type(t.body[0]), ast.Assign)
        self.assertEqual(t.body[0].lineno, 2)
        
        self.assertEqual(type(t.body[1]), ast.Expr)
        self.assertEqual(type(t.body[1].value), ast.JoinedStr)
        self.assertEqual(len(t.body[1].value.values), 3)
        self.assertEqual(type(t.body[1].value.values[0]), ast.Str)
        self.assertEqual(type(t.body[1].value.values[1]), ast.FormattedValue)
        self.assertEqual(type(t.body[1].value.values[2]), ast.Str)
        
        
        
        self.assertEqual(t.body[1].lineno, 8)
        self.assertEqual(t.body[1].value.lineno, 8)
        self.assertEqual(t.body[1].value.values[0].lineno, 8)
        self.assertEqual(t.body[1].value.values[1].lineno, 8)
        self.assertEqual(t.body[1].value.values[2].lineno, 8)
        self.assertEqual(t.body[1].col_offset, -1)
        self.assertEqual(t.body[1].value.col_offset, -1)
        self.assertEqual(t.body[1].value.values[0].col_offset, -1)
        self.assertEqual(t.body[1].value.values[1].col_offset, -1)
        self.assertEqual(t.body[1].value.values[2].col_offset, -1)
        
        
        binop = t.body[1].value.values[1].value
        self.assertEqual(type(binop), ast.BinOp)
        self.assertEqual(type(binop.left), ast.Name)
        self.assertEqual(type(binop.op), ast.Mult)
        self.assertEqual(type(binop.right), ast.Call)
        self.assertEqual(binop.lineno, 4)
        self.assertEqual(binop.left.lineno, 4)
        self.assertEqual(binop.right.lineno, 6)
        self.assertEqual(binop.col_offset, 3)
        self.assertEqual(binop.left.col_offset, 3)
        self.assertEqual(binop.right.col_offset, 7)

    def test_docstring(self):
        def f():
            f'''Not a docstring'''
        self.assertIsNone(f.__doc__)
        def g():
            '''Not a docstring''' \
            f''
        self.assertIsNone(g.__doc__)

    def test_literal_eval(self):
        with self.assertRaisesRegex(ValueError, 'malformed node or string'):
            ast.literal_eval("f'x'")

    def test_ast_compile_time_concat(self):
        x = ['']

        expr = """x[0] = 'foo' f'{3}'"""
        t = ast.parse(expr)
        c = compile(t, '', 'exec')
        exec(c)
        self.assertEqual(x[0], 'foo3')

    def test_compile_time_concat_errors(self):
        self.assertAllRaise(SyntaxError,
                            'cannot mix bytes and nonbytes literals',
                            [r"""f'' b''""",
                             r"""b'' f''""",
                             ])

    def test_literal(self):
        self.assertEqual(f'', '')
        self.assertEqual(f'a', 'a')
        self.assertEqual(f' ', ' ')

    def test_unterminated_string(self):
        self.assertAllRaise(SyntaxError, 'f-string: unterminated string',
                            [r"""f'{"x'""",
                             r"""f'{"x}'""",
                             r"""f'{("x'""",
                             r"""f'{("x}'""",
                             ])

    def test_mismatched_parens(self):
        self.assertAllRaise(SyntaxError, 'f-string: mismatched',
                            ["f'{((}'",
                             ])

    def test_double_braces(self):
        self.assertEqual(f'{{', '{')
        self.assertEqual(f'a{{', 'a{')
        self.assertEqual(f'{{b', '{b')
        self.assertEqual(f'a{{b', 'a{b')
        self.assertEqual(f'}}', '}')
        self.assertEqual(f'a}}', 'a}')
        self.assertEqual(f'}}b', '}b')
        self.assertEqual(f'a}}b', 'a}b')
        self.assertEqual(f'{{}}', '{}')
        self.assertEqual(f'a{{}}', 'a{}')
        self.assertEqual(f'{{b}}', '{b}')
        self.assertEqual(f'{{}}c', '{}c')
        self.assertEqual(f'a{{b}}', 'a{b}')
        self.assertEqual(f'a{{}}c', 'a{}c')
        self.assertEqual(f'{{b}}c', '{b}c')
        self.assertEqual(f'a{{b}}c', 'a{b}c')

        self.assertEqual(f'{{{10}', '{10')
        self.assertEqual(f'}}{10}', '}10')
        self.assertEqual(f'}}{{{10}', '}{10')
        self.assertEqual(f'}}a{{{10}', '}a{10')

        self.assertEqual(f'{10}{{', '10{')
        self.assertEqual(f'{10}}}', '10}')
        self.assertEqual(f'{10}}}{{', '10}{')
        self.assertEqual(f'{10}}}a{{' '}', '10}a{}')

        
        self.assertEqual(f'{"{{}}"}', '{{}}')

        self.assertAllRaise(TypeError, 'unhashable type',
                            ["f'{ {{}} }'", 
                             ])

    def test_compile_time_concat(self):
        x = 'def'
        self.assertEqual('abc' f'
        self.assertEqual('abc' f'{x}' 'ghi', 'abcdefghi')
        self.assertEqual('abc' f'{x}' 'gh' f'i{x:4}', 'abcdefghidef ')
        self.assertEqual('{x}' f'{x}', '{x}def')
        self.assertEqual('{x' f'{x}', '{xdef')
        self.assertEqual('{x}' f'{x}', '{x}def')
        self.assertEqual('{{x}}' f'{x}', '{{x}}def')
        self.assertEqual('{{x' f'{x}', '{{xdef')
        self.assertEqual('x}}' f'{x}', 'x}}def')
        self.assertEqual(f'{x}' 'x}}', 'defx}}')
        self.assertEqual(f'{x}' '', 'def')
        self.assertEqual('' f'{x}' '', 'def')
        self.assertEqual('' f'{x}', 'def')
        self.assertEqual(f'{x}' '2', 'def2')
        self.assertEqual('1' f'{x}' '2', '1def2')
        self.assertEqual('1' f'{x}', '1def')
        self.assertEqual(f'{x}' f'-{x}', 'def-def')
        self.assertEqual('' f'', '')
        self.assertEqual('' f'' '', '')
        self.assertEqual('' f'' '' f'', '')
        self.assertEqual(f'', '')
        self.assertEqual(f'' '', '')
        self.assertEqual(f'' '' f'', '')
        self.assertEqual(f'' '' f'' '', '')

        self.assertAllRaise(SyntaxError, "f-string: expecting '}'",
                            ["f'{3' f'}'",  
                             ])

    def test_comments(self):
        
        d = {'
        self.assertEqual(f'{""}', '
        self.assertEqual(f'{d[""]}', 'hash')

        self.assertAllRaise(SyntaxError, "f-string expression part cannot include '",
                            ["f'{1",   "(1"
                             "f'{3(",
                             "f'{",
                             "f'{)",   
                                          
                             ])

    def test_many_expressions(self):
        
        
        
        
        def build_fstr(n, extra=''):
            return "f'" + ('{x} ' * n) + extra + "'"

        x = 'X'
        width = 1

        
        for i in range(250, 260):
            self.assertEqual(eval(build_fstr(i)), (x+' ')*i)

        
        self.assertEqual(eval(build_fstr(255)*256), (x+' ')*(255*256))

        s = build_fstr(253, '{x:{width}} ')
        self.assertEqual(eval(s), (x+' ')*254)

        
        s = "f'{1}' 'x' 'y'" * 1024
        self.assertEqual(eval(s), '1xy' * 1024)

    def test_format_specifier_expressions(self):
        width = 10
        precision = 4
        value = decimal.Decimal('12.34567')
        self.assertEqual(f'result: {value:{width}.{precision}}', 'result:      12.35')
        self.assertEqual(f'result: {value:{width!r}.{precision}}', 'result:      12.35')
        self.assertEqual(f'result: {value:{width:0}.{precision:1}}', 'result:      12.35')
        self.assertEqual(f'result: {value:{1}{0:0}.{precision:1}}', 'result:      12.35')
        self.assertEqual(f'result: {value:{ 1}{ 0:0}.{ precision:1}}', 'result:      12.35')
        self.assertEqual(f'{10:
        self.assertEqual(f'{10:{""}1{0}{"x"}}', '       0xa')
        self.assertEqual(f'{-10:-{""}1{0}x}', '      -0xa')
        self.assertEqual(f'{-10:{"-"}"x"}}', '      -0xa')
        self.assertEqual(f'{10:

        self.assertAllRaise(SyntaxError, "f-string: expecting '}'",
                            ["""f'{"s"!r{":10"}}'""",

                             
                             ])

        self.assertAllRaise(SyntaxError, "invalid syntax",
                            [
                             "f'{4:{/5}}'",
                             ])

        self.assertAllRaise(SyntaxError, "f-string: expressions nested too deeply",
                            [
                             "f'result: {value:{width:{0}}.{precision:1}}'",
                             ])

        self.assertAllRaise(SyntaxError, 'f-string: invalid conversion character',
                            [
                             
                             """f'{"s"!{"r"}}'""",
                             ])

    def test_side_effect_order(self):
        class X:
            def __init__(self):
                self.i = 0
            def __format__(self, spec):
                self.i += 1
                return str(self.i)

        x = X()
        self.assertEqual(f'{x} {x}', '1 2')

    def test_missing_expression(self):
        self.assertAllRaise(SyntaxError, 'f-string: empty expression not allowed',
                            ["f'{}'",
                             "f'{ }'"
                             "f' {} '",
                             "f'{!r}'",
                             "f'{ !r}'",
                             "f'{10:{ }}'",
                             "f' { } '",

                             
                             
                             "f'''{\t\f\r\n}'''",

                             
                             
                             "f'{!x}'",
                             "f'{ !xr}'",
                             "f'{!x:}'",
                             "f'{!x:a}'",
                             "f'{ !xr:}'",
                             "f'{ !xr:a}'",

                             "f'{!}'",
                             "f'{:}'",

                             
                             
                             "f'{!'",
                             "f'{!s:'",
                             "f'{:'",
                             "f'{:x'",
                             ])

        
        self.assertAllRaise(SyntaxError, 'invalid character in identifier',
                            ["f'''{\xa0}'''",
                             "\xa0",
                             ])

    def test_parens_in_expressions(self):
        self.assertEqual(f'{3,}', '(3,)')

        
        
        
        
        self.assertAllRaise(SyntaxError, 'invalid syntax',
                            ["f'{,}'",
                             "f'{,}'",  
                             ])

        self.assertAllRaise(SyntaxError, "f-string: expecting '}'",
                            ["f'{3)+(4}'",
                             ])

        self.assertAllRaise(SyntaxError, 'EOL while scanning string literal',
                            ["f'{\n}'",
                             ])

    def test_backslashes_in_string_part(self):
        self.assertEqual(f'\t', '\t')
        self.assertEqual(r'\t', '\\t')
        self.assertEqual(rf'\t', '\\t')
        self.assertEqual(f'{2}\t', '2\t')
        self.assertEqual(f'{2}\t{3}', '2\t3')
        self.assertEqual(f'\t{3}', '\t3')

        self.assertEqual(f'\u0394', '\u0394')
        self.assertEqual(r'\u0394', '\\u0394')
        self.assertEqual(rf'\u0394', '\\u0394')
        self.assertEqual(f'{2}\u0394', '2\u0394')
        self.assertEqual(f'{2}\u0394{3}', '2\u03943')
        self.assertEqual(f'\u0394{3}', '\u03943')

        self.assertEqual(f'\U00000394', '\u0394')
        self.assertEqual(r'\U00000394', '\\U00000394')
        self.assertEqual(rf'\U00000394', '\\U00000394')
        self.assertEqual(f'{2}\U00000394', '2\u0394')
        self.assertEqual(f'{2}\U00000394{3}', '2\u03943')
        self.assertEqual(f'\U00000394{3}', '\u03943')

        self.assertEqual(f'\N{GREEK CAPITAL LETTER DELTA}', '\u0394')
        self.assertEqual(f'{2}\N{GREEK CAPITAL LETTER DELTA}', '2\u0394')
        self.assertEqual(f'{2}\N{GREEK CAPITAL LETTER DELTA}{3}', '2\u03943')
        self.assertEqual(f'\N{GREEK CAPITAL LETTER DELTA}{3}', '\u03943')
        self.assertEqual(f'2\N{GREEK CAPITAL LETTER DELTA}', '2\u0394')
        self.assertEqual(f'2\N{GREEK CAPITAL LETTER DELTA}3', '2\u03943')
        self.assertEqual(f'\N{GREEK CAPITAL LETTER DELTA}3', '\u03943')

        self.assertEqual(f'\x20', ' ')
        self.assertEqual(r'\x20', '\\x20')
        self.assertEqual(rf'\x20', '\\x20')
        self.assertEqual(f'{2}\x20', '2 ')
        self.assertEqual(f'{2}\x20{3}', '2 3')
        self.assertEqual(f'\x20{3}', ' 3')

        self.assertEqual(f'2\x20', '2 ')
        self.assertEqual(f'2\x203', '2 3')
        self.assertEqual(f'\x203', ' 3')

        with self.assertWarns(DeprecationWarning):  
            value = eval(r"f'\{6*7}'")
        self.assertEqual(value, '\\42')
        self.assertEqual(f'\\{6*7}', '\\42')
        self.assertEqual(fr'\{6*7}', '\\42')

        AMPERSAND = 'spam'
        
        
        self.assertEqual(f'\N{AMPERSAND}', '&')
        self.assertEqual(f'\\N{AMPERSAND}', '\\Nspam')
        self.assertEqual(fr'\N{AMPERSAND}', '\\Nspam')
        self.assertEqual(f'\\\N{AMPERSAND}', '\\&')

    def test_misformed_unicode_character_name(self):
        
        
        self.assertAllRaise(SyntaxError, r"\(unicode error\) 'unicodeescape' codec can't decode bytes in position .*: malformed \\N character escape",
                            [r"f'\N'",
                             r"f'\N{'",
                             r"f'\N{GREEK CAPITAL LETTER DELTA'",

                             
                             
                             r"'\N'",
                             r"'\N{'",
                             r"'\N{GREEK CAPITAL LETTER DELTA'",
                             ])

    def test_no_backslashes_in_expression_part(self):
        self.assertAllRaise(SyntaxError, 'f-string expression part cannot include a backslash',
                            [r"f'{\'a\'}'",
                             r"f'{\t3}'",
                             r"f'{\}'",
                             r"rf'{\'a\'}'",
                             r"rf'{\t3}'",
                             r"rf'{\}'",
                             r"""rf'{"\N{LEFT CURLY BRACKET}"}'""",
                             r"f'{\n}'",
                             ])

    def test_no_escapes_for_braces(self):
        """
        Only literal curly braces begin an expression.
        """
        
        self.assertEqual(f'\x7b1+1}}', '{1+1}')
        self.assertEqual(f'\x7b1+1', '{1+1')
        self.assertEqual(f'\u007b1+1', '{1+1')
        self.assertEqual(f'\N{LEFT CURLY BRACKET}1+1\N{RIGHT CURLY BRACKET}', '{1+1}')

    def test_newlines_in_expressions(self):
        self.assertEqual(f'{0}', '0')
        self.assertEqual(rf'''{3+
4}''', '7')

    def test_lambda(self):
        x = 5
        self.assertEqual(f'{(lambda y:x*y)("8")!r}', "'88888'")
        self.assertEqual(f'{(lambda y:x*y)("8")!r:10}', "'88888'   ")
        self.assertEqual(f'{(lambda y:x*y)("8"):10}', "88888     ")

        
        
        self.assertAllRaise(SyntaxError, 'unexpected EOF while parsing',
                            ["f'{lambda x:x}'",
                             ])

    def test_yield(self):
        
        
        def fn(y):
            f'y:{yield y*2}'

        g = fn(4)
        self.assertEqual(next(g), 8)

    def test_yield_send(self):
        def fn(x):
            yield f'x:{yield (lambda i: x * i)}'

        g = fn(10)
        the_lambda = next(g)
        self.assertEqual(the_lambda(4), 40)
        self.assertEqual(g.send('string'), 'x:string')

    def test_expressions_with_triple_quoted_strings(self):
        self.assertEqual(f"{'''x'''}", 'x')
        self.assertEqual(f"{'''eric's'''}", "eric's")

        
        self.assertEqual(f'{"x" """eric"s""" "y"}', 'xeric"sy')
        self.assertEqual(f'{"x" """eric"s"""}', 'xeric"s')
        self.assertEqual(f'{"""eric"s""" "y"}', 'eric"sy')
        self.assertEqual(f'{"""x""" """eric"s""" "y"}', 'xeric"sy')
        self.assertEqual(f'{"""x""" """eric"s""" """y"""}', 'xeric"sy')
        self.assertEqual(f'{r"""x""" """eric"s""" """y"""}', 'xeric"sy')

    def test_multiple_vars(self):
        x = 98
        y = 'abc'
        self.assertEqual(f'{x}{y}', '98abc')

        self.assertEqual(f'X{x}{y}', 'X98abc')
        self.assertEqual(f'{x}X{y}', '98Xabc')
        self.assertEqual(f'{x}{y}X', '98abcX')

        self.assertEqual(f'X{x}Y{y}', 'X98Yabc')
        self.assertEqual(f'X{x}{y}Y', 'X98abcY')
        self.assertEqual(f'{x}X{y}Y', '98XabcY')

        self.assertEqual(f'X{x}Y{y}Z', 'X98YabcZ')

    def test_closure(self):
        def outer(x):
            def inner():
                return f'x:{x}'
            return inner

        self.assertEqual(outer('987')(), 'x:987')
        self.assertEqual(outer(7)(), 'x:7')

    def test_arguments(self):
        y = 2
        def f(x, width):
            return f'x={x*y:{width}}'

        self.assertEqual(f('foo', 10), 'x=foofoo    ')
        x = 'bar'
        self.assertEqual(f(10, 10), 'x=        20')

    def test_locals(self):
        value = 123
        self.assertEqual(f'v:{value}', 'v:123')

    def test_missing_variable(self):
        with self.assertRaises(NameError):
            f'v:{value}'

    def test_missing_format_spec(self):
        class O:
            def __format__(self, spec):
                if not spec:
                    return '*'
                return spec

        self.assertEqual(f'{O():x}', 'x')
        self.assertEqual(f'{O()}', '*')
        self.assertEqual(f'{O():}', '*')

        self.assertEqual(f'{3:}', '3')
        self.assertEqual(f'{3!s:}', '3')

    def test_global(self):
        self.assertEqual(f'g:{a_global}', 'g:global variable')
        self.assertEqual(f'g:{a_global!r}', "g:'global variable'")

        a_local = 'local variable'
        self.assertEqual(f'g:{a_global} l:{a_local}',
                         'g:global variable l:local variable')
        self.assertEqual(f'g:{a_global!r}',
                         "g:'global variable'")
        self.assertEqual(f'g:{a_global} l:{a_local!r}',
                         "g:global variable l:'local variable'")

        self.assertIn("module 'unittest' from", f'{unittest}')

    def test_shadowed_global(self):
        a_global = 'really a local'
        self.assertEqual(f'g:{a_global}', 'g:really a local')
        self.assertEqual(f'g:{a_global!r}', "g:'really a local'")

        a_local = 'local variable'
        self.assertEqual(f'g:{a_global} l:{a_local}',
                         'g:really a local l:local variable')
        self.assertEqual(f'g:{a_global!r}',
                         "g:'really a local'")
        self.assertEqual(f'g:{a_global} l:{a_local!r}',
                         "g:really a local l:'local variable'")

    def test_call(self):
        def foo(x):
            return 'x=' + str(x)

        self.assertEqual(f'{foo(10)}', 'x=10')

    def test_nested_fstrings(self):
        y = 5
        self.assertEqual(f'{f"{0}"*3}', '000')
        self.assertEqual(f'{f"{y}"*3}', '555')

    def test_invalid_string_prefixes(self):
        self.assertAllRaise(SyntaxError, 'unexpected EOF while parsing',
                            ["fu''",
                             "uf''",
                             "Fu''",
                             "fU''",
                             "Uf''",
                             "uF''",
                             "ufr''",
                             "urf''",
                             "fur''",
                             "fru''",
                             "rfu''",
                             "ruf''",
                             "FUR''",
                             "Fur''",
                             "fb''",
                             "fB''",
                             "Fb''",
                             "FB''",
                             "bf''",
                             "bF''",
                             "Bf''",
                             "BF''",
                             ])

    def test_leading_trailing_spaces(self):
        self.assertEqual(f'{ 3}', '3')
        self.assertEqual(f'{  3}', '3')
        self.assertEqual(f'{3 }', '3')
        self.assertEqual(f'{3  }', '3')

        self.assertEqual(f'expr={ {x: y for x, y in [(1, 2), ]}}',
                         'expr={1: 2}')
        self.assertEqual(f'expr={ {x: y for x, y in [(1, 2), ]} }',
                         'expr={1: 2}')

    def test_not_equal(self):
        
        
        

        self.assertEqual(f'{3!=4}', 'True')
        self.assertEqual(f'{3!=4:}', 'True')
        self.assertEqual(f'{3!=4!s}', 'True')
        self.assertEqual(f'{3!=4!s:.3}', 'Tru')

    def test_conversions(self):
        self.assertEqual(f'{3.14:10.10}', '      3.14')
        self.assertEqual(f'{3.14!s:10.10}', '3.14      ')
        self.assertEqual(f'{3.14!r:10.10}', '3.14      ')
        self.assertEqual(f'{3.14!a:10.10}', '3.14      ')

        self.assertEqual(f'{"a"}', 'a')
        self.assertEqual(f'{"a"!r}', "'a'")
        self.assertEqual(f'{"a"!a}', "'a'")

        
        self.assertEqual(f'{"a!r"}', "a!r")

        
        self.assertEqual(f'{3.14:!<10.10}', '3.14!!!!!!')

        self.assertAllRaise(SyntaxError, 'f-string: invalid conversion character',
                            ["f'{3!g}'",
                             "f'{3!A}'",
                             "f'{3!3}'",
                             "f'{3!G}'",
                             "f'{3!!}'",
                             "f'{3!:}'",
                             "f'{3! s}'",  
                             ])

        self.assertAllRaise(SyntaxError, "f-string: expecting '}'",
                            ["f'{x!s{y}}'",
                             "f'{3!ss}'",
                             "f'{3!ss:}'",
                             "f'{3!ss:s}'",
                             ])

    def test_assignment(self):
        self.assertAllRaise(SyntaxError, 'invalid syntax',
                            ["f'' = 3",
                             "f'{0}' = x",
                             "f'{x}' = x",
                             ])

    def test_del(self):
        self.assertAllRaise(SyntaxError, 'invalid syntax',
                            ["del f''",
                             "del '' f''",
                             ])

    def test_mismatched_braces(self):
        self.assertAllRaise(SyntaxError, "f-string: single '}' is not allowed",
                            ["f'{{}'",
                             "f'{{}}}'",
                             "f'}'",
                             "f'x}'",
                             "f'x}x'",
                             r"f'\u007b}'",

                             
                             "f'{3:}>10}'",
                             "f'{3:}}>10}'",
                             ])

        self.assertAllRaise(SyntaxError, "f-string: expecting '}'",
                            ["f'{3:{{>10}'",
                             "f'{3'",
                             "f'{3!'",
                             "f'{3:'",
                             "f'{3!s'",
                             "f'{3!s:'",
                             "f'{3!s:3'",
                             "f'x{'",
                             "f'x{x'",
                             "f'{x'",
                             "f'{3:s'",
                             "f'{{{'",
                             "f'{{}}{'",
                             "f'{'",
                             ])

        
        self.assertEqual(f'{"{"}', '{')
        self.assertEqual(f'{"}"}', '}')
        self.assertEqual(f'{3:{"}"}>10}', '}}}}}}}}}3')
        self.assertEqual(f'{2:{"{"}>10}', '{{{{{{{{{2')

    def test_if_conditional(self):
        
        
        

        def test_fstring(x, expected):
            flag = 0
            if f'{x}':
                flag = 1
            else:
                flag = 2
            self.assertEqual(flag, expected)

        def test_concat_empty(x, expected):
            flag = 0
            if '' f'{x}':
                flag = 1
            else:
                flag = 2
            self.assertEqual(flag, expected)

        def test_concat_non_empty(x, expected):
            flag = 0
            if ' ' f'{x}':
                flag = 1
            else:
                flag = 2
            self.assertEqual(flag, expected)

        test_fstring('', 2)
        test_fstring(' ', 1)

        test_concat_empty('', 2)
        test_concat_empty(' ', 1)

        test_concat_non_empty('', 1)
        test_concat_non_empty(' ', 1)

    def test_empty_format_specifier(self):
        x = 'test'
        self.assertEqual(f'{x}', 'test')
        self.assertEqual(f'{x:}', 'test')
        self.assertEqual(f'{x!s:}', 'test')
        self.assertEqual(f'{x!r:}', "'test'")

    def test_str_format_differences(self):
        d = {'a': 'string',
             0: 'integer',
             }
        a = 0
        self.assertEqual(f'{d[0]}', 'integer')
        self.assertEqual(f'{d["a"]}', 'string')
        self.assertEqual(f'{d[a]}', 'integer')
        self.assertEqual('{d[a]}'.format(d=d), 'string')
        self.assertEqual('{d[0]}'.format(d=d), 'integer')

    def test_invalid_expressions(self):
        self.assertAllRaise(SyntaxError, 'invalid syntax',
                            [r"f'{a[4)}'",
                             r"f'{a(4]}'",
                            ])

    def test_errors(self):
        
        self.assertAllRaise(TypeError, 'unsupported',
                            [r"f'{(lambda: 0):x}'",
                             r"f'{(0,):x}'",
                             ])
        self.assertAllRaise(ValueError, 'Unknown format code',
                            [r"f'{1000:j}'",
                             r"f'{1000:j}'",
                            ])

    def test_loop(self):
        for i in range(1000):
            self.assertEqual(f'i:{i}', 'i:' + str(i))

    def test_dict(self):
        d = {'"': 'dquote',
             "'": 'squote',
             'foo': 'bar',
             }
        self.assertEqual(f'''{d["'"]}''', 'squote')
        self.assertEqual(f"""{d['"']}""", 'dquote')

        self.assertEqual(f'{d["foo"]}', 'bar')
        self.assertEqual(f"{d['foo']}", 'bar')

    def test_backslash_char(self):
        
        
        self.assertEqual(eval('f"\\\n"'), '')
        self.assertEqual(eval('f"\\\r"'), '')


if __name__ == '__main__':
    unittest.main()
