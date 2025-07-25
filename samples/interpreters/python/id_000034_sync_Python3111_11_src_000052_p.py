












from __future__ import print_function, division, absolute_import, unicode_literals

import sys

from tatsu.buffering import Buffer
from tatsu.parsing import Parser
from tatsu.parsing import tatsumasu
from tatsu.util import re, generic_main


KEYWORDS = {}  


class XFBuffer(Buffer):
    def __init__(
        self,
        text,
        whitespace=None,
        nameguard=None,
        comments_re='(?s)\\(:((?!(\\(:|:\\))).)*:\\)',
        eol_comments_re=None,
        ignorecase=None,
        namechars='-',
        **kwargs
    ):
        super(XFBuffer, self).__init__(
            text,
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            namechars=namechars,
            **kwargs
        )


class XFParser(Parser):
    def __init__(
        self,
        whitespace=None,
        nameguard=None,
        comments_re='(?s)\\(:((?!(\\(:|:\\))).)*:\\)',
        eol_comments_re=None,
        ignorecase=None,
        left_recursion=True,
        parseinfo=True,
        keywords=None,
        namechars='-',
        buffer_class=XFBuffer,
        **kwargs
    ):
        if keywords is None:
            keywords = KEYWORDS
        super(XFParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            parseinfo=parseinfo,
            keywords=keywords,
            namechars=namechars,
            buffer_class=buffer_class,
            **kwargs
        )

    @tatsumasu()
    def _module_(self):

        def block0():
            self._namespace_declaration_()
        self._closure(block0)

        def block1():
            self._default_()
        self._closure(block1)

        def block2():
            self._parameter_()
        self._closure(block2)

        def block3():
            with self._choice():
                with self._option():
                    self._filter_declaration_()
                with self._option():
                    self._fact_variable_()
                with self._option():
                    self._general_variable_()
                with self._option():
                    self._function_declaration_()
                self._error('no available options')
        self._closure(block3)

        def block5():
            self._assertion_()
        self._closure(block5)
        self._check_eof()

    @tatsumasu()
    def _separator_(self):
        self._token(';')

    @tatsumasu()
    def _namespace_declaration_(self):
        self._token('namespace')
        self._name_()
        self._token('=')
        self._quoted_url_()
        self._separator_()

    @tatsumasu()
    def _default_(self):
        with self._choice():
            with self._option():
                self._severity_()
            with self._option():
                self._token('default-language')
                self._language_()
                self._separator_()
            self._error('no available options')

    @tatsumasu()
    def _severity_(self):
        self._token('unsatisfied-severity')
        self._message_severity_()
        self._separator_()

    @tatsumasu()
    def _message_severity_(self):
        with self._choice():
            with self._option():
                self._token('ERROR')
            with self._option():
                self._token('WARNING')
            with self._option():
                self._token('INFO')
            self._error('no available options')

    @tatsumasu()
    def _parameter_(self):
        self._token('parameter')
        self._name_()
        with self._optional():
            self._token('required')
        self._token('{')
        with self._optional():
            self._token('select')
            self._enclosed_expression_()
        with self._optional():
            self._token('as')
            self._qname_()
        self._token('}')
        self._separator_()

    @tatsumasu()
    def _filter_declaration_(self):
        self._token('filter')
        self._name_()
        self._token('{')

        def block0():
            self._filter_()
        self._positive_closure(block0)
        self._token('}')
        self._separator_()

    @tatsumasu()
    def _filter_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._concept_filter_()
                with self._option():
                    self._general_filter_()
                with self._option():
                    self._period_filter_()
                with self._option():
                    self._dimension_filter_()
                with self._option():
                    self._unit_filter_()
                with self._option():
                    self._entity_filter_()
                with self._option():
                    self._match_filter_()
                with self._option():
                    self._relative_filter_()
                with self._option():
                    self._tuple_filter_()
                with self._option():
                    self._value_filter_()
                with self._option():
                    self._boolean_filter_()
                with self._option():
                    self._aspect_cover_filter_()
                with self._option():
                    self._concept_relation_filter_()
                with self._option():
                    self._declared_filter_reference_()
                self._error('no available options')

    @tatsumasu()
    def _concept_filter_(self):
        with self._optional():
            self._token('complemented')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('covering')
                with self._option():
                    self._constant('covering')
                with self._option():
                    self._token('non-covering')
                self._error('no available options')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('concept-name')
                    self._cut()

                    def block1():
                        with self._choice():
                            with self._option():
                                self._qname_()
                            with self._option():
                                self._localname_()
                            with self._option():
                                self._enclosed_expression_()
                            self._error('no available options')
                    self._positive_closure(block1)
                with self._option():
                    self._token('concept-period-type')
                    self._cut()
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token('instant')
                            with self._option():
                                self._token('duration')
                            self._error('no available options')
                with self._option():
                    self._token('concept-balance')
                    self._cut()
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token('credit')
                            with self._option():
                                self._token('debit')
                            with self._option():
                                self._token('none')
                            self._error('no available options')
                with self._option():
                    self._token('concept-data-type')
                    self._cut()
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token('strict')
                            with self._option():
                                self._token('non-strict')
                            self._error('no available options')
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._qname_()
                            with self._option():
                                self._enclosed_expression_()
                            self._error('no available options')
                with self._option():
                    self._token('concept-substitution-group')
                    self._cut()
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token('strict')
                            with self._option():
                                self._token('non-strict')
                            self._error('no available options')
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._qname_()
                            with self._option():
                                self._enclosed_expression_()
                            self._error('no available options')
                self._error('no available options')
        self._separator_()

    @tatsumasu()
    def _general_filter_(self):
        with self._optional():
            self._token('complemented')
        self._token('general')
        self._cut()
        self._enclosed_expression_()
        self._separator_()

    @tatsumasu()
    def _period_filter_(self):
        with self._optional():
            self._token('complemented')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('period-start')
                    self._cut()
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._date_constant_()
                            with self._option():
                                self._date_time_constant_()
                            with self._option():
                                with self._group():
                                    self._token('date')
                                    self._enclosed_expression_()
                                    with self._optional():
                                        self._token('time')
                                        self._enclosed_expression_()
                            self._error('no available options')
                with self._option():
                    self._token('period-end')
                    self._cut()
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._date_constant_()
                            with self._option():
                                self._date_time_constant_()
                            with self._option():
                                with self._group():
                                    self._token('date')
                                    self._enclosed_expression_()
                                    with self._optional():
                                        self._token('time')
                                        self._enclosed_expression_()
                            self._error('no available options')
                with self._option():
                    self._token('period-instant')
                    self._cut()
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._date_constant_()
                            with self._option():
                                self._date_time_constant_()
                            with self._option():
                                with self._group():
                                    self._token('date')
                                    self._enclosed_expression_()
                                    with self._optional():
                                        self._token('time')
                                        self._enclosed_expression_()
                            self._error('no available options')
                with self._option():
                    self._token('period')
                    self._cut()
                    self._enclosed_expression_()
                with self._option():
                    self._token('instant-duration')
                    self._cut()
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._token('start')
                            with self._option():
                                self._token('end')
                            self._error('no available options')
                    self._variable_ref_()
                self._error('no available options')
        self._separator_()

    @tatsumasu()
    def _dimension_filter_(self):
        with self._optional():
            self._token('complemented')
        with self._group():
            with self._choice():
                with self._option():
                    with self._group():
                        self._token('explicit-dimension')
                        self._cut()
                        with self._group():
                            with self._choice():
                                with self._option():
                                    self._variable_ref_()
                                with self._option():
                                    self._qname_()
                                with self._option():
                                    self._localname_()
                                with self._option():
                                    self._enclosed_expression_()
                                self._error('no available options')

                        def block1():
                            with self._choice():
                                with self._option():
                                    self._token('default-member')
                                with self._option():
                                    self._token('member')
                                    self._cut()
                                    with self._group():
                                        with self._choice():
                                            with self._option():
                                                self._variable_ref_()
                                            with self._option():
                                                self._qname_()
                                            with self._option():
                                                self._localname_()
                                            with self._option():
                                                self._enclosed_expression_()
                                            self._error('no available options')
                                    with self._optional():
                                        self._token('linkrole')
                                        self._quoted_anyURI_()
                                        self._token('arcrole')
                                        self._quoted_anyURI_()
                                        self._token('axis')
                                        self._dimension_axis_()
                                self._error('no available options')
                        self._closure(block1)
                with self._option():
                    with self._group():
                        self._token('typed-dimension')
                        self._cut()
                        with self._group():
                            with self._choice():
                                with self._option():
                                    self._variable_ref_()
                                with self._option():
                                    self._qname_()
                                with self._option():
                                    self._localname_()
                                with self._option():
                                    self._enclosed_expression_()
                                self._error('no available options')
                        with self._optional():
                            self._token('test')
                            self._enclosed_expression_()
                self._error('no available options')
        self._separator_()

    @tatsumasu()
    def _dimension_axis_(self):
        with self._choice():
            with self._option():
                self._token('child')
            with self._option():
                self._token('child-or-self')
            with self._option():
                self._token('descendant')
            with self._option():
                self._token('descendant-or-self')
            self._error('no available options')

    @tatsumasu()
    def _unit_filter_(self):
        with self._optional():
            self._token('complemented')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('unit-single-measure')
                    self._cut()
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._qname_()
                            with self._option():
                                self._enclosed_expression_()
                            self._error('no available options')
                with self._option():
                    self._token('unit-general-measures')
                    self._cut()
                    self._enclosed_expression_()
                self._error('no available options')
        self._separator_()

    @tatsumasu()
    def _entity_filter_(self):
        with self._optional():
            self._token('complemented')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('entity-scheme-pattern')
                    self._cut()
                    self._regexp_pattern_()
                with self._option():
                    self._token('entity-scheme')
                    self._cut()
                    self._enclosed_expression_()
                with self._option():
                    self._token('entity-identifier-pattern')
                    self._cut()
                    self._regexp_pattern_()
                with self._option():
                    self._token('entity-identifier')
                    self._cut()
                    self._enclosed_expression_()
                with self._option():
                    self._token('entity')
                    self._cut()
                    self._token('scheme')
                    self._enclosed_expression_()
                    self._token('value')
                    self._enclosed_expression_()
                self._error('no available options')
        self._separator_()

    @tatsumasu()
    def _match_filter_(self):
        with self._optional():
            self._token('complemented')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('match-concept')
                    self._cut()
                    self._variable_ref_()
                with self._option():
                    self._token('match-location')
                    self._cut()
                    self._variable_ref_()
                with self._option():
                    self._token('match-entity-identifier')
                    self._cut()
                    self._variable_ref_()
                with self._option():
                    self._token('match-period')
                    self._cut()
                    self._variable_ref_()
                with self._option():
                    self._token('match-unit')
                    self._cut()
                    self._variable_ref_()
                with self._option():
                    self._token('match-dimension')
                    self._cut()
                    self._variable_ref_()
                    self._token('dimension')
                    self._qname_()
                self._error('no available options')
        with self._optional():
            self._token('match-any')
        self._separator_()

    @tatsumasu()
    def _relative_filter_(self):
        with self._optional():
            self._token('complemented')
        self._token('relative')
        self._cut()
        self._variable_ref_()
        self._separator_()

    @tatsumasu()
    def _tuple_filter_(self):
        with self._optional():
            self._token('complemented')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('parent')
                    self._cut()
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._qname_()
                            with self._option():
                                self._enclosed_expression_()
                            self._error('no available options')
                with self._option():
                    self._token('ancestor')
                    self._cut()
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._qname_()
                            with self._option():
                                self._enclosed_expression_()
                            self._error('no available options')
                with self._option():
                    self._token('sibling')
                    self._cut()
                    self._variable_ref_()
                self._error('no available options')
        self._separator_()

    @tatsumasu()
    def _value_filter_(self):
        with self._optional():
            self._token('complemented')
        self._token('nilled')
        self._separator_()

    @tatsumasu()
    def _boolean_filter_(self):
        with self._optional():
            self._token('complemented')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('and')
                with self._option():
                    self._token('or')
                self._error('no available options')
        self._cut()
        self._token('{')

        def block1():
            self._filter_()
        self._positive_closure(block1)
        self._token('}')
        self._separator_()

    @tatsumasu()
    def _aspect_cover_filter_(self):
        with self._optional():
            self._token('complemented')
        self._token('aspect-cover')
        self._cut()

        def block0():
            with self._choice():
                with self._option():
                    self._token('all')
                with self._option():
                    self._token('concept')
                with self._option():
                    self._token('entity-identifier')
                with self._option():
                    self._token('location')
                with self._option():
                    self._token('period')
                with self._option():
                    self._token('unit')
                with self._option():
                    self._token('dimensions')
                with self._option():
                    self._token('dimension')
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._qname_()
                            with self._option():
                                self._localname_()
                            with self._option():
                                self._enclosed_expression_()
                            self._error('no available options')
                with self._option():
                    self._token('exclude-dimension')
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._qname_()
                            with self._option():
                                self._localname_()
                            with self._option():
                                self._enclosed_expression_()
                            self._error('no available options')
                self._error('no available options')
        self._positive_closure(block0)
        self._separator_()

    @tatsumasu()
    def _concept_relation_filter_(self):
        with self._optional():
            self._token('complemented')
        self._token('concept-relation')
        self._cut()
        with self._group():
            with self._choice():
                with self._option():
                    self._variable_ref_()
                with self._option():
                    self._qname_()
                with self._option():
                    self._localname_()
                with self._option():
                    self._enclosed_expression_()
                self._error('no available options')
        with self._optional():
            self._token('linkrole')
            with self._group():
                with self._choice():
                    with self._option():
                        self._quoted_anyURI_()
                    with self._option():
                        self._enclosed_expression_()
                    self._error('no available options')
        with self._optional():
            self._token('arcrole')
            with self._group():
                with self._choice():
                    with self._option():
                        self._quoted_anyURI_()
                    with self._option():
                        self._enclosed_expression_()
                    self._error('no available options')
        with self._optional():
            self._token('axis')
            self._relation_axis_()
        with self._optional():
            self._token('generations')
            self._non_negative_integer_()
        with self._optional():
            self._token('test')
            self._enclosed_expression_()
        self._separator_()

    @tatsumasu()
    def _relation_axis_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._token('child-or-self')
                with self._option():
                    self._token('child')
                with self._option():
                    self._token('descendant-or-self')
                with self._option():
                    self._token('descendant')
                with self._option():
                    self._token('parent-or-self')
                with self._option():
                    self._token('parent')
                with self._option():
                    self._token('ancestor-or-self')
                with self._option():
                    self._token('ancestor')
                with self._option():
                    self._token('sibling-or-self')
                with self._option():
                    self._token('sibling-or-descendant')
                with self._option():
                    self._token('sibling')
                self._error('no available options')
        self._separator_()

    @tatsumasu()
    def _declared_filter_reference_(self):
        self._token('filter')
        self._cut()
        self._variable_ref_()
        self._separator_()

    @tatsumasu()
    def _fact_variable_(self):
        self._token('variable')
        self._cut()
        self._variable_ref_()
        self._token('{')
        with self._optional():
            self._token('bind-as-sequence')
        with self._optional():
            self._token('nils')
        with self._optional():
            self._token('matches')
        with self._optional():
            self._token('fallback')
            self._enclosed_expression_()

        def block0():
            self._filter_()
        self._closure(block0)
        self._token('}')
        self._separator_()

    @tatsumasu()
    def _general_variable_(self):
        self._token('variable')
        self._cut()
        self._variable_ref_()
        self._token('{')
        with self._optional():
            self._token('bind-as-sequence')
        self._token('select')
        self._enclosed_expression_()
        self._token('}')
        self._separator_()

    @tatsumasu()
    def _function_declaration_(self):
        self._token('function')
        self._cut()
        self._qname_()
        self._token('(')

        def block0():
            self._NCNAME_FRAG_()
            self._token('as')
            self._qname_()
        self._closure(block0)
        self._token(')')
        self._token('as')
        self._qname_()
        with self._optional():
            self._token('{')
            self._token('return')
            self._enclosed_expression_()
            self._separator_()
            self._token('}')
        self._separator_()

    @tatsumasu()
    def _assertion_(self):
        self._token('assertion')
        self._name_()
        self._token('{')

        def block0():
            with self._choice():
                with self._option():
                    self._label_()
                with self._option():
                    self._message_()
                with self._option():
                    self._severity_()
                with self._option():
                    self._token('aspect-model-non-dimensional')
                    self._separator_()
                with self._option():
                    self._token('no-implicit-filtering')
                    self._separator_()
                self._error('no available options')
        self._closure(block0)

        def block2():
            self._filter_()
        self._closure(block2)

        def block3():
            with self._choice():
                with self._option():
                    self._fact_variable_()
                with self._option():
                    self._general_variable_()
                with self._option():
                    self._referenced_parameter_()
                self._error('no available options')
        self._closure(block3)

        def block5():
            self._precondition_()
        self._closure(block5)
        with self._group():
            with self._choice():
                with self._option():
                    self._value_expression_()
                with self._option():
                    self._existence_expression_()
                self._error('no available options')
        self._token('}')
        self._separator_()

    @tatsumasu()
    def _label_(self):
        self._token('label')
        with self._optional():
            self._token('(')
            self._language_()
            self._token(')')
        self._quoted_string_()
        self._separator_()

    @tatsumasu()
    def _message_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._token('satisfied-message')
                with self._option():
                    self._token('unsatisfied-message')
                self._error('no available options')
        self._cut()
        with self._optional():
            self._token('(')
            self._cut()
            self._language_()
            self._token(')')
        self._quoted_string_()
        self._separator_()

    @tatsumasu()
    def _referenced_parameter_(self):
        self._token('parameter')
        self._cut()
        self._variable_ref_()
        self._token('references')
        self._qname_()
        self._separator_()

    @tatsumasu()
    def _precondition_(self):
        self._token('precondition')
        self._enclosed_expression_()

    @tatsumasu()
    def _value_expression_(self):
        self._token('test')
        self._enclosed_expression_()
        self._separator_()

    @tatsumasu()
    def _existence_expression_(self):
        self._token('evaluation-count')
        self._enclosed_expression_()
        self._separator_()

    @tatsumasu()
    def _enclosed_expression_(self):
        self._token('{')
        self._xPath_()
        self._token('}')

    @tatsumasu()
    def _name_(self):
        self._NCNAME_FRAG_()

    @tatsumasu()
    def _language_(self):
        self._pattern(r'[A-Za-z]{2}(-[A-Za-z]{2})?')

    @tatsumasu()
    def _quoted_anyURI_(self):
        self._quoted_url_()

    @tatsumasu()
    def _quoted_url_(self):
        self._quoted_string_()

    @tatsumasu()
    def _localname_(self):
        self._name_()

    @tatsumasu()
    def _variable_ref_(self):
        self._token('$')
        self._variable_name_()

    @tatsumasu()
    def _variable_name_(self):
        self._name_()

    @tatsumasu()
    def _non_negative_integer_(self):
        self._pattern(r'[0-9]+')

    @tatsumasu()
    def _date_time_constant_(self):
        self._pattern(r'\b(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\\.[0-9]+)?(Z)?\b')

    @tatsumasu()
    def _date_constant_(self):
        self._pattern(r'\b(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])\b')

    @tatsumasu()
    def _quoted_string_(self):
        self._pattern(r'("([^\\"]|\\.)*"|\'([^\\\']|\\.)*\')')

    @tatsumasu()
    def _regexp_pattern_(self):
        self._pattern(r'\/([^\\\/]|\\.)*\/')

    @tatsumasu()
    def _xPath_(self):
        self._expr_()

    @tatsumasu()
    def _expr_(self):
        self._exprSingle_()

        def block0():
            self._token(',')
            self._exprSingle_()
        self._closure(block0)

    @tatsumasu()
    def _exprSingle_(self):
        with self._choice():
            with self._option():
                self._forExpr_()
            with self._option():
                self._quantifiedExpr_()
            with self._option():
                self._ifExpr_()
            with self._option():
                self._orExpr_()
            self._error('no available options')

    @tatsumasu()
    def _forExpr_(self):
        self._simpleForClause_()
        self._token('return')
        self._exprSingle_()

    @tatsumasu()
    def _simpleForClause_(self):
        self._token('for')
        self._token('$')
        self._varName_()
        self._token('in')
        self._exprSingle_()

        def block0():
            self._token(',')
            self._token('$')
            self._varName_()
            self._token('in')
            self._exprSingle_()
        self._closure(block0)

    @tatsumasu()
    def _quantifiedExpr_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._token('some')
                with self._option():
                    self._token('every')
                self._error('no available options')
        self._token('$')
        self._varName_()
        self._token('in')
        self._exprSingle_()

        def block1():
            self._token(',')
            self._token('$')
            self._varName_()
            self._token('in')
            self._exprSingle_()
        self._closure(block1)
        self._token('satisfies')
        self._exprSingle_()

    @tatsumasu()
    def _ifExpr_(self):
        self._token('if')
        self._token('(')
        self._expr_()
        self._token(')')
        self._token('then')
        self._exprSingle_()
        self._token('else')
        self._exprSingle_()

    @tatsumasu()
    def _orExpr_(self):
        self._andExpr_()

        def block0():
            self._token('or')
            self._andExpr_()
        self._closure(block0)

    @tatsumasu()
    def _andExpr_(self):
        self._comparisonExpr_()

        def block0():
            self._token('and')
            self._comparisonExpr_()
        self._closure(block0)

    @tatsumasu()
    def _comparisonExpr_(self):
        self._rangeExpr_()
        with self._optional():
            with self._group():
                with self._choice():
                    with self._option():
                        self._valueComp_()
                    with self._option():
                        self._nodeComp_()
                    with self._option():
                        self._generalComp_()
                    self._error('no available options')
            self._rangeExpr_()

    @tatsumasu()
    def _rangeExpr_(self):
        self._additiveExpr_()
        with self._optional():
            self._token('to')
            self._additiveExpr_()

    @tatsumasu()
    def _additiveExpr_(self):
        self._multiplicativeExpr_()

        def block0():
            with self._group():
                with self._choice():
                    with self._option():
                        self._token('+')
                    with self._option():
                        self._token('-')
                    self._error('no available options')
            self._multiplicativeExpr_()
        self._closure(block0)

    @tatsumasu()
    def _multiplicativeExpr_(self):
        self._unionExpr_()

        def block0():
            with self._group():
                with self._choice():
                    with self._option():
                        self._token('*')
                    with self._option():
                        self._token('div')
                    with self._option():
                        self._token('idiv')
                    with self._option():
                        self._token('mod')
                    self._error('no available options')
            self._unionExpr_()
        self._closure(block0)

    @tatsumasu()
    def _unionExpr_(self):
        self._intersectExceptExpr_()

        def block0():
            with self._group():
                with self._choice():
                    with self._option():
                        self._token('union')
                    with self._option():
                        self._token('|')
                    self._error('no available options')
            self._intersectExceptExpr_()
        self._closure(block0)

    @tatsumasu()
    def _intersectExceptExpr_(self):
        self._instanceofExpr_()

        def block0():
            with self._group():
                with self._choice():
                    with self._option():
                        self._token('intersect')
                    with self._option():
                        self._token('except')
                    self._error('no available options')
            self._instanceofExpr_()
        self._closure(block0)

    @tatsumasu()
    def _instanceofExpr_(self):
        self._treatExpr_()
        with self._optional():
            self._token('instance')
            self._token('of')
            self._sequenceType_()

    @tatsumasu()
    def _treatExpr_(self):
        self._castableExpr_()
        with self._optional():
            self._token('treat')
            self._token('as')
            self._sequenceType_()

    @tatsumasu()
    def _castableExpr_(self):
        self._castExpr_()
        with self._optional():
            self._token('castable')
            self._token('as')
            self._singleType_()

    @tatsumasu()
    def _castExpr_(self):
        self._unaryExpr_()
        with self._optional():
            self._token('cast')
            self._token('as')
            self._singleType_()

    @tatsumasu()
    def _unaryExpr_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._token('-')
                with self._option():
                    self._token('+')
                self._error('no available options')
        self._closure(block0)
        self._valueExpr_()

    @tatsumasu()
    def _valueExpr_(self):
        self._pathExpr_()

    @tatsumasu()
    def _generalComp_(self):
        with self._choice():
            with self._option():
                self._token('=')
            with self._option():
                self._token('!=')
            with self._option():
                self._token('<=')
            with self._option():
                self._token('<')
            with self._option():
                self._token('>=')
            with self._option():
                self._token('>')
            self._error('no available options')

    @tatsumasu()
    def _valueComp_(self):
        with self._choice():
            with self._option():
                self._token('eq')
            with self._option():
                self._token('ne')
            with self._option():
                self._token('lt')
            with self._option():
                self._token('le')
            with self._option():
                self._token('gt')
            with self._option():
                self._token('ge')
            self._error('no available options')

    @tatsumasu()
    def _nodeComp_(self):
        with self._choice():
            with self._option():
                self._token('is')
            with self._option():
                self._token('<<')
            with self._option():
                self._token('>>')
            self._error('no available options')

    @tatsumasu()
    def _pathExpr_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._token('//')
                    self._relativePathExpr_()
            with self._option():
                with self._group():
                    self._token('/')
                    with self._optional():
                        self._relativePathExpr_()
            with self._option():
                self._relativePathExpr_()
            self._error('no available options')

    @tatsumasu()
    def _relativePathExpr_(self):
        self._stepExpr_()

        def block0():
            with self._group():
                with self._choice():
                    with self._option():
                        self._token('/')
                    with self._option():
                        self._token('//')
                    self._error('no available options')
            self._stepExpr_()
        self._closure(block0)

    @tatsumasu()
    def _stepExpr_(self):
        with self._choice():
            with self._option():
                self._filterExpr_()
            with self._option():
                self._axisStep_()
            self._error('no available options')

    @tatsumasu()
    def _axisStep_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._reverseStep_()
                with self._option():
                    self._forwardStep_()
                self._error('no available options')
        self._predicateList_()

    @tatsumasu()
    def _forwardStep_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._forwardAxis_()
                    self._nodeTest_()
            with self._option():
                self._abbrevForwardStep_()
            self._error('no available options')

    @tatsumasu()
    def _forwardAxis_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._token('child')
                    self._token('::')
            with self._option():
                with self._group():
                    self._token('descendant')
                    self._token('::')
            with self._option():
                with self._group():
                    self._token('attribute')
                    self._token('::')
            with self._option():
                with self._group():
                    self._token('self')
                    self._token('::')
            with self._option():
                with self._group():
                    self._token('descendant-or-self')
                    self._token('::')
            with self._option():
                with self._group():
                    self._token('following-sibling')
                    self._token('::')
            with self._option():
                with self._group():
                    self._token('following')
                    self._token('::')
            with self._option():
                with self._group():
                    self._token('namespace')
                    self._token('::')
            self._error('no available options')

    @tatsumasu()
    def _abbrevForwardStep_(self):
        with self._optional():
            self._token('@')
        self._nodeTest_()

    @tatsumasu()
    def _reverseStep_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._reverseAxis_()
                    self._nodeTest_()
            with self._option():
                self._abbrevReverseStep_()
            self._error('no available options')

    @tatsumasu()
    def _reverseAxis_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._token('parent')
                    self._token('::')
            with self._option():
                with self._group():
                    self._token('ancestor')
                    self._token('::')
            with self._option():
                with self._group():
                    self._token('preceding-sibling')
                    self._token('::')
            with self._option():
                with self._group():
                    self._token('preceding')
                    self._token('::')
            with self._option():
                with self._group():
                    self._token('ancestor-or-self')
                    self._token('::')
            self._error('no available options')

    @tatsumasu()
    def _abbrevReverseStep_(self):
        self._token('..')

    @tatsumasu()
    def _nodeTest_(self):
        with self._choice():
            with self._option():
                self._kindTest_()
            with self._option():
                self._nameTest_()
            self._error('no available options')

    @tatsumasu()
    def _nameTest_(self):
        with self._choice():
            with self._option():
                self._qname_()
            with self._option():
                self._wildcard_()
            self._error('no available options')

    @tatsumasu()
    def _wildcard_(self):
        with self._choice():
            with self._option():
                self._token('*')
            with self._option():
                with self._group():
                    self._ncname_()
                    self._token(':')
                    self._token('*')
            with self._option():
                with self._group():
                    self._token('*')
                    self._token(':')
                    self._ncname_()
            self._error('no available options')

    @tatsumasu()
    def _filterExpr_(self):
        self._primaryExpr_()
        self._predicateList_()

    @tatsumasu()
    def _predicateList_(self):

        def block0():
            self._predicate_()
        self._closure(block0)

    @tatsumasu()
    def _predicate_(self):
        self._token('[')
        self._expr_()
        self._token(']')

    @tatsumasu()
    def _primaryExpr_(self):
        with self._choice():
            with self._option():
                self._literal_()
            with self._option():
                self._varRef_()
            with self._option():
                self._parenthesizedExpr_()
            with self._option():
                self._contextItemExpr_()
            with self._option():
                self._functionCall_()
            self._error('no available options')

    @tatsumasu()
    def _literal_(self):
        with self._choice():
            with self._option():
                self._numericLiteral_()
            with self._option():
                self._stringLiteral_()
            self._error('no available options')

    @tatsumasu()
    def _numericLiteral_(self):
        with self._choice():
            with self._option():
                self._integerLiteral_()
            with self._option():
                self._decimalLiteral_()
            with self._option():
                self._doubleLiteral_()
            self._error('no available options')

    @tatsumasu()
    def _varRef_(self):
        self._token('$')
        self._varName_()

    @tatsumasu()
    def _varName_(self):
        self._qname_()

    @tatsumasu()
    def _parenthesizedExpr_(self):
        self._token('(')
        with self._optional():
            self._expr_()
        self._token(')')

    @tatsumasu()
    def _contextItemExpr_(self):
        self._token('.')

    @tatsumasu()
    def _functionCall_(self):
        self._qname_()
        self._token('(')
        with self._optional():
            self._exprSingle_()

            def block0():
                self._token(',')
                self._exprSingle_()
            self._closure(block0)
        self._token(')')

    @tatsumasu()
    def _singleType_(self):
        self._atomicType_()
        with self._optional():
            self._token('?')

    @tatsumasu()
    def _sequenceType_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._token('empty-sequence')
                    self._token('(')
                    self._token(')')
            with self._option():
                with self._group():
                    self._itemType_()
                    with self._optional():
                        self._occurrenceIndicator_()
            self._error('no available options')

    @tatsumasu()
    def _occurrenceIndicator_(self):
        with self._choice():
            with self._option():
                self._token('?')
            with self._option():
                self._token('*')
            with self._option():
                self._token('+')
            self._error('no available options')

    @tatsumasu()
    def _itemType_(self):
        with self._choice():
            with self._option():
                self._kindTest_()
            with self._option():
                with self._group():
                    self._token('item')
                    self._token('(')
                    self._token(')')
            with self._option():
                self._atomicType_()
            self._error('no available options')

    @tatsumasu()
    def _atomicType_(self):
        self._qname_()

    @tatsumasu()
    def _kindTest_(self):
        with self._choice():
            with self._option():
                self._documentTest_()
            with self._option():
                self._elementTest_()
            with self._option():
                self._attributeTest_()
            with self._option():
                self._schemaElementTest_()
            with self._option():
                self._schemaAttributeTest_()
            with self._option():
                self._pITest_()
            with self._option():
                self._commentTest_()
            with self._option():
                self._textTest_()
            with self._option():
                self._anyKindTest_()
            self._error('no available options')

    @tatsumasu()
    def _anyKindTest_(self):
        self._token('node')
        self._token('(')
        self._token(')')

    @tatsumasu()
    def _documentTest_(self):
        self._token('document-node')
        self._token('(')
        with self._optional():
            with self._choice():
                with self._option():
                    self._elementTest_()
                with self._option():
                    self._schemaElementTest_()
                self._error('no available options')
        self._token(')')

    @tatsumasu()
    def _textTest_(self):
        self._token('text')
        self._token('(')
        self._token(')')

    @tatsumasu()
    def _commentTest_(self):
        self._token('comment')
        self._token('(')
        self._token(')')

    @tatsumasu()
    def _pITest_(self):
        self._token('processing-instruction')
        self._token('(')
        with self._optional():
            with self._choice():
                with self._option():
                    self._ncname_()
                with self._option():
                    self._stringLiteral_()
                self._error('no available options')
        self._token(')')

    @tatsumasu()
    def _attributeTest_(self):
        self._token('attribute')
        self._token('(')
        with self._optional():
            self._attribNameOrWildcard_()
            with self._optional():
                self._token(',')
                self._typeName_()
        self._token(')')

    @tatsumasu()
    def _attribNameOrWildcard_(self):
        with self._choice():
            with self._option():
                self._attributeName_()
            with self._option():
                self._token('*')
            self._error('no available options')

    @tatsumasu()
    def _schemaAttributeTest_(self):
        self._token('schema-attribute')
        self._token('(')
        self._attributeDeclaration_()
        self._token(')')

    @tatsumasu()
    def _attributeDeclaration_(self):
        self._attributeName_()

    @tatsumasu()
    def _elementTest_(self):
        self._token('element')
        self._token('(')
        with self._optional():
            self._elementNameOrWildcard_()
            with self._optional():
                self._token(',')
                self._typeName_()
                with self._optional():
                    self._token('?')
        self._token(')')

    @tatsumasu()
    def _elementNameOrWildcard_(self):
        with self._choice():
            with self._option():
                self._elementName_()
            with self._option():
                self._token('*')
            self._error('no available options')

    @tatsumasu()
    def _schemaElementTest_(self):
        self._token('schema-element')
        self._token('(')
        self._elementDeclaration_()
        self._token(')')

    @tatsumasu()
    def _elementDeclaration_(self):
        self._elementName_()

    @tatsumasu()
    def _attributeName_(self):
        self._qname_()

    @tatsumasu()
    def _elementName_(self):
        self._qname_()

    @tatsumasu()
    def _typeName_(self):
        self._qname_()

    @tatsumasu()
    def _integerLiteral_(self):
        self._DIGITS_()

    @tatsumasu()
    def _decimalLiteral_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._token('.')
                    self._DIGITS_()
            with self._option():
                with self._group():
                    self._DIGITS_()
                    self._pattern(r'\.[0-9]*')
            self._error('no available options')

    @tatsumasu()
    def _doubleLiteral_(self):
        with self._group():
            with self._choice():
                with self._option():
                    with self._group():
                        self._token('.')
                        self._DIGITS_()
                with self._option():
                    with self._group():
                        self._DIGITS_()
                        self._pattern(r'(\.[0-9]*)?')
                self._error('no available options')
        self._pattern(r'[eE][+-]?')
        self._DIGITS_()

    @tatsumasu()
    def _stringLiteral_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._pattern(r'"')

                    def block0():
                        with self._choice():
                            with self._option():
                                self._ESCAPEQUOT_()
                            with self._option():
                                self._pattern(r'[^"]')
                            self._error('no available options')
                    self._closure(block0)
                    self._pattern(r'"')
            with self._option():
                with self._group():
                    self._pattern(r"'")

                    def block2():
                        with self._choice():
                            with self._option():
                                self._ESCAPEAPOS_()
                            with self._option():
                                self._pattern(r"[^']")
                            self._error('no available options')
                    self._closure(block2)
                    self._pattern(r"'")
            self._error('no available options')

    @tatsumasu()
    def _ESCAPEQUOT_(self):
        self._token('""')

    @tatsumasu()
    def _ESCAPEAPOS_(self):
        self._token("''")

    @tatsumasu()
    def _qname_(self):
        with self._choice():
            with self._option():
                with self._group():
                    self._NCNAME_FRAG_()
                    self._pattern(r':')
                    self._NCNAME_FRAG_()
            with self._option():
                self._NCNAME_FRAG_()
            self._error('no available options')

    @tatsumasu()
    def _ncname_(self):
        self._NCNAME_FRAG_()

    @tatsumasu()
    def _NCNAME_FRAG_(self):
        self._pattern(r'([A-Z]|_|[a-z]|[\u00C0-\u00D6]|[\u00D8-\u00F6]|[\u00F8-\u02FF]|[\u0370-\u037D]|[\u037F-\u1FFF]|[\u200C-\u200D]|[\u2070-\u218F]|[\u2C00-\u2FEF]|[\u3001-\uD7FF]|[\uF900-\uFDCF]|[\uFDF0-\uFFFD]|[\U00010000-\U000EFFFF])([A-Z]|_|[a-z]|[\u00C0-\u00D6]|[\u00D8-\u00F6]|[\u00F8-\u02FF]|[\u0370-\u037D]|[\u037F-\u1FFF]|[\u200C-\u200D]|[\u2070-\u218F]|[\u2C00-\u2FEF]|[\u3001-\uD7FF]|[\uF900-\uFDCF]|[\uFDF0-\uFFFD]|[\U00010000-\U000EFFFF]|-|\.|[0-9]|\u00B7|[\u0300-\u036F]|[\u203F-\u2040])*')

    @tatsumasu()
    def _DIGITS_(self):
        self._pattern(r'[0-9]+')


class XFSemantics(object):
    def module(self, ast):
        return ast

    def separator(self, ast):
        return ast

    def namespace_declaration(self, ast):
        return ast

    def default(self, ast):
        return ast

    def severity(self, ast):
        return ast

    def message_severity(self, ast):
        return ast

    def parameter(self, ast):
        return ast

    def filter_declaration(self, ast):
        return ast

    def filter(self, ast):
        return ast

    def concept_filter(self, ast):
        return ast

    def general_filter(self, ast):
        return ast

    def period_filter(self, ast):
        return ast

    def dimension_filter(self, ast):
        return ast

    def dimension_axis(self, ast):
        return ast

    def unit_filter(self, ast):
        return ast

    def entity_filter(self, ast):
        return ast

    def match_filter(self, ast):
        return ast

    def relative_filter(self, ast):
        return ast

    def tuple_filter(self, ast):
        return ast

    def value_filter(self, ast):
        return ast

    def boolean_filter(self, ast):
        return ast

    def aspect_cover_filter(self, ast):
        return ast

    def concept_relation_filter(self, ast):
        return ast

    def relation_axis(self, ast):
        return ast

    def declared_filter_reference(self, ast):
        return ast

    def fact_variable(self, ast):
        return ast

    def general_variable(self, ast):
        return ast

    def function_declaration(self, ast):
        return ast

    def assertion(self, ast):
        return ast

    def label(self, ast):
        return ast

    def message(self, ast):
        return ast

    def referenced_parameter(self, ast):
        return ast

    def precondition(self, ast):
        return ast

    def value_expression(self, ast):
        return ast

    def existence_expression(self, ast):
        return ast

    def enclosed_expression(self, ast):
        return ast

    def name(self, ast):
        return ast

    def language(self, ast):
        return ast

    def quoted_anyURI(self, ast):
        return ast

    def quoted_url(self, ast):
        return ast

    def localname(self, ast):
        return ast

    def variable_ref(self, ast):
        return ast

    def variable_name(self, ast):
        return ast

    def non_negative_integer(self, ast):
        return ast

    def date_time_constant(self, ast):
        return ast

    def date_constant(self, ast):
        return ast

    def quoted_string(self, ast):
        return ast

    def regexp_pattern(self, ast):
        return ast

    def xPath(self, ast):
        return ast

    def expr(self, ast):
        return ast

    def exprSingle(self, ast):
        return ast

    def forExpr(self, ast):
        return ast

    def simpleForClause(self, ast):
        return ast

    def quantifiedExpr(self, ast):
        return ast

    def ifExpr(self, ast):
        return ast

    def orExpr(self, ast):
        return ast

    def andExpr(self, ast):
        return ast

    def comparisonExpr(self, ast):
        return ast

    def rangeExpr(self, ast):
        return ast

    def additiveExpr(self, ast):
        return ast

    def multiplicativeExpr(self, ast):
        return ast

    def unionExpr(self, ast):
        return ast

    def intersectExceptExpr(self, ast):
        return ast

    def instanceofExpr(self, ast):
        return ast

    def treatExpr(self, ast):
        return ast

    def castableExpr(self, ast):
        return ast

    def castExpr(self, ast):
        return ast

    def unaryExpr(self, ast):
        return ast

    def valueExpr(self, ast):
        return ast

    def generalComp(self, ast):
        return ast

    def valueComp(self, ast):
        return ast

    def nodeComp(self, ast):
        return ast

    def pathExpr(self, ast):
        return ast

    def relativePathExpr(self, ast):
        return ast

    def stepExpr(self, ast):
        return ast

    def axisStep(self, ast):
        return ast

    def forwardStep(self, ast):
        return ast

    def forwardAxis(self, ast):
        return ast

    def abbrevForwardStep(self, ast):
        return ast

    def reverseStep(self, ast):
        return ast

    def reverseAxis(self, ast):
        return ast

    def abbrevReverseStep(self, ast):
        return ast

    def nodeTest(self, ast):
        return ast

    def nameTest(self, ast):
        return ast

    def wildcard(self, ast):
        return ast

    def filterExpr(self, ast):
        return ast

    def predicateList(self, ast):
        return ast

    def predicate(self, ast):
        return ast

    def primaryExpr(self, ast):
        return ast

    def literal(self, ast):
        return ast

    def numericLiteral(self, ast):
        return ast

    def varRef(self, ast):
        return ast

    def varName(self, ast):
        return ast

    def parenthesizedExpr(self, ast):
        return ast

    def contextItemExpr(self, ast):
        return ast

    def functionCall(self, ast):
        return ast

    def singleType(self, ast):
        return ast

    def sequenceType(self, ast):
        return ast

    def occurrenceIndicator(self, ast):
        return ast

    def itemType(self, ast):
        return ast

    def atomicType(self, ast):
        return ast

    def kindTest(self, ast):
        return ast

    def anyKindTest(self, ast):
        return ast

    def documentTest(self, ast):
        return ast

    def textTest(self, ast):
        return ast

    def commentTest(self, ast):
        return ast

    def pITest(self, ast):
        return ast

    def attributeTest(self, ast):
        return ast

    def attribNameOrWildcard(self, ast):
        return ast

    def schemaAttributeTest(self, ast):
        return ast

    def attributeDeclaration(self, ast):
        return ast

    def elementTest(self, ast):
        return ast

    def elementNameOrWildcard(self, ast):
        return ast

    def schemaElementTest(self, ast):
        return ast

    def elementDeclaration(self, ast):
        return ast

    def attributeName(self, ast):
        return ast

    def elementName(self, ast):
        return ast

    def typeName(self, ast):
        return ast

    def integerLiteral(self, ast):
        return ast

    def decimalLiteral(self, ast):
        return ast

    def doubleLiteral(self, ast):
        return ast

    def stringLiteral(self, ast):
        return ast

    def ESCAPEQUOT(self, ast):
        return ast

    def ESCAPEAPOS(self, ast):
        return ast

    def qname(self, ast):
        return ast

    def ncname(self, ast):
        return ast

    def NCNAME_FRAG(self, ast):
        return ast

    def DIGITS(self, ast):
        return ast


def main(filename, start=None, **kwargs):
    if start is None:
        start = 'module'
    if not filename or filename == '-':
        text = sys.stdin.read()
    else:
        with open(filename) as f:
            text = f.read()
    parser = XFParser()
    return parser.parse(text, rule_name=start, filename=filename, **kwargs)


if __name__ == '__main__':
    import json
    from tatsu.util import asjson

    ast = generic_main(main, XFParser, name='XF')
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(asjson(ast), indent=2))
    print()
