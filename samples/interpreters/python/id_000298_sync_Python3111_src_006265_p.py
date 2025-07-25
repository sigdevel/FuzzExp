
"""
    pygments.lexers._postgres_builtins
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Self-updating data files for PostgreSQL lexer.

    :copyright: Copyright 2006-2017 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""




KEYWORDS = (
    'ABORT',
    'ABSOLUTE',
    'ACCESS',
    'ACTION',
    'ADD',
    'ADMIN',
    'AFTER',
    'AGGREGATE',
    'ALL',
    'ALSO',
    'ALTER',
    'ALWAYS',
    'ANALYSE',
    'ANALYZE',
    'AND',
    'ANY',
    'ARRAY',
    'AS',
    'ASC',
    'ASSERTION',
    'ASSIGNMENT',
    'ASYMMETRIC',
    'AT',
    'ATTRIBUTE',
    'AUTHORIZATION',
    'BACKWARD',
    'BEFORE',
    'BEGIN',
    'BETWEEN',
    'BIGINT',
    'BINARY',
    'BIT',
    'BOOLEAN',
    'BOTH',
    'BY',
    'CACHE',
    'CALLED',
    'CASCADE',
    'CASCADED',
    'CASE',
    'CAST',
    'CATALOG',
    'CHAIN',
    'CHAR',
    'CHARACTER',
    'CHARACTERISTICS',
    'CHECK',
    'CHECKPOINT',
    'CLASS',
    'CLOSE',
    'CLUSTER',
    'COALESCE',
    'COLLATE',
    'COLLATION',
    'COLUMN',
    'COMMENT',
    'COMMENTS',
    'COMMIT',
    'COMMITTED',
    'CONCURRENTLY',
    'CONFIGURATION',
    'CONNECTION',
    'CONSTRAINT',
    'CONSTRAINTS',
    'CONTENT',
    'CONTINUE',
    'CONVERSION',
    'COPY',
    'COST',
    'CREATE',
    'CROSS',
    'CSV',
    'CURRENT',
    'CURRENT_CATALOG',
    'CURRENT_DATE',
    'CURRENT_ROLE',
    'CURRENT_SCHEMA',
    'CURRENT_TIME',
    'CURRENT_TIMESTAMP',
    'CURRENT_USER',
    'CURSOR',
    'CYCLE',
    'DATA',
    'DATABASE',
    'DAY',
    'DEALLOCATE',
    'DEC',
    'DECIMAL',
    'DECLARE',
    'DEFAULT',
    'DEFAULTS',
    'DEFERRABLE',
    'DEFERRED',
    'DEFINER',
    'DELETE',
    'DELIMITER',
    'DELIMITERS',
    'DESC',
    'DICTIONARY',
    'DISABLE',
    'DISCARD',
    'DISTINCT',
    'DO',
    'DOCUMENT',
    'DOMAIN',
    'DOUBLE',
    'DROP',
    'EACH',
    'ELSE',
    'ENABLE',
    'ENCODING',
    'ENCRYPTED',
    'END',
    'ENUM',
    'ESCAPE',
    'EVENT',
    'EXCEPT',
    'EXCLUDE',
    'EXCLUDING',
    'EXCLUSIVE',
    'EXECUTE',
    'EXISTS',
    'EXPLAIN',
    'EXTENSION',
    'EXTERNAL',
    'EXTRACT',
    'FALSE',
    'FAMILY',
    'FETCH',
    'FILTER',
    'FIRST',
    'FLOAT',
    'FOLLOWING',
    'FOR',
    'FORCE',
    'FOREIGN',
    'FORWARD',
    'FREEZE',
    'FROM',
    'FULL',
    'FUNCTION',
    'FUNCTIONS',
    'GLOBAL',
    'GRANT',
    'GRANTED',
    'GREATEST',
    'GROUP',
    'HANDLER',
    'HAVING',
    'HEADER',
    'HOLD',
    'HOUR',
    'IDENTITY',
    'IF',
    'ILIKE',
    'IMMEDIATE',
    'IMMUTABLE',
    'IMPLICIT',
    'IN',
    'INCLUDING',
    'INCREMENT',
    'INDEX',
    'INDEXES',
    'INHERIT',
    'INHERITS',
    'INITIALLY',
    'INLINE',
    'INNER',
    'INOUT',
    'INPUT',
    'INSENSITIVE',
    'INSERT',
    'INSTEAD',
    'INT',
    'INTEGER',
    'INTERSECT',
    'INTERVAL',
    'INTO',
    'INVOKER',
    'IS',
    'ISNULL',
    'ISOLATION',
    'JOIN',
    'KEY',
    'LABEL',
    'LANGUAGE',
    'LARGE',
    'LAST',
    'LATERAL',
    'LC_COLLATE',
    'LC_CTYPE',
    'LEADING',
    'LEAKPROOF',
    'LEAST',
    'LEFT',
    'LEVEL',
    'LIKE',
    'LIMIT',
    'LISTEN',
    'LOAD',
    'LOCAL',
    'LOCALTIME',
    'LOCALTIMESTAMP',
    'LOCATION',
    'LOCK',
    'MAPPING',
    'MATCH',
    'MATERIALIZED',
    'MAXVALUE',
    'MINUTE',
    'MINVALUE',
    'MODE',
    'MONTH',
    'MOVE',
    'NAME',
    'NAMES',
    'NATIONAL',
    'NATURAL',
    'NCHAR',
    'NEXT',
    'NO',
    'NONE',
    'NOT',
    'NOTHING',
    'NOTIFY',
    'NOTNULL',
    'NOWAIT',
    'NULL',
    'NULLIF',
    'NULLS',
    'NUMERIC',
    'OBJECT',
    'OF',
    'OFF',
    'OFFSET',
    'OIDS',
    'ON',
    'ONLY',
    'OPERATOR',
    'OPTION',
    'OPTIONS',
    'OR',
    'ORDER',
    'ORDINALITY',
    'OUT',
    'OUTER',
    'OVER',
    'OVERLAPS',
    'OVERLAY',
    'OWNED',
    'OWNER',
    'PARSER',
    'PARTIAL',
    'PARTITION',
    'PASSING',
    'PASSWORD',
    'PLACING',
    'PLANS',
    'POLICY',
    'POSITION',
    'PRECEDING',
    'PRECISION',
    'PREPARE',
    'PREPARED',
    'PRESERVE',
    'PRIMARY',
    'PRIOR',
    'PRIVILEGES',
    'PROCEDURAL',
    'PROCEDURE',
    'PROGRAM',
    'QUOTE',
    'RANGE',
    'READ',
    'REAL',
    'REASSIGN',
    'RECHECK',
    'RECURSIVE',
    'REF',
    'REFERENCES',
    'REFRESH',
    'REINDEX',
    'RELATIVE',
    'RELEASE',
    'RENAME',
    'REPEATABLE',
    'REPLACE',
    'REPLICA',
    'RESET',
    'RESTART',
    'RESTRICT',
    'RETURNING',
    'RETURNS',
    'REVOKE',
    'RIGHT',
    'ROLE',
    'ROLLBACK',
    'ROW',
    'ROWS',
    'RULE',
    'SAVEPOINT',
    'SCHEMA',
    'SCROLL',
    'SEARCH',
    'SECOND',
    'SECURITY',
    'SELECT',
    'SEQUENCE',
    'SEQUENCES',
    'SERIALIZABLE',
    'SERVER',
    'SESSION',
    'SESSION_USER',
    'SET',
    'SETOF',
    'SHARE',
    'SHOW',
    'SIMILAR',
    'SIMPLE',
    'SMALLINT',
    'SNAPSHOT',
    'SOME',
    'STABLE',
    'STANDALONE',
    'START',
    'STATEMENT',
    'STATISTICS',
    'STDIN',
    'STDOUT',
    'STORAGE',
    'STRICT',
    'STRIP',
    'SUBSTRING',
    'SYMMETRIC',
    'SYSID',
    'SYSTEM',
    'TABLE',
    'TABLES',
    'TABLESPACE',
    'TEMP',
    'TEMPLATE',
    'TEMPORARY',
    'TEXT',
    'THEN',
    'TIME',
    'TIMESTAMP',
    'TO',
    'TRAILING',
    'TRANSACTION',
    'TREAT',
    'TRIGGER',
    'TRIM',
    'TRUE',
    'TRUNCATE',
    'TRUSTED',
    'TYPE',
    'TYPES',
    'UNBOUNDED',
    'UNCOMMITTED',
    'UNENCRYPTED',
    'UNION',
    'UNIQUE',
    'UNKNOWN',
    'UNLISTEN',
    'UNLOGGED',
    'UNTIL',
    'UPDATE',
    'USER',
    'USING',
    'VACUUM',
    'VALID',
    'VALIDATE',
    'VALIDATOR',
    'VALUE',
    'VALUES',
    'VARCHAR',
    'VARIADIC',
    'VARYING',
    'VERBOSE',
    'VERSION',
    'VIEW',
    'VIEWS',
    'VOLATILE',
    'WHEN',
    'WHERE',
    'WHITESPACE',
    'WINDOW',
    'WITH',
    'WITHIN',
    'WITHOUT',
    'WORK',
    'WRAPPER',
    'WRITE',
    'XML',
    'XMLATTRIBUTES',
    'XMLCONCAT',
    'XMLELEMENT',
    'XMLEXISTS',
    'XMLFOREST',
    'XMLPARSE',
    'XMLPI',
    'XMLROOT',
    'XMLSERIALIZE',
    'YEAR',
    'YES',
    'ZONE',
)

DATATYPES = (
    'bigint',
    'bigserial',
    'bit',
    'bit varying',
    'bool',
    'boolean',
    'box',
    'bytea',
    'char',
    'character',
    'character varying',
    'cidr',
    'circle',
    'date',
    'decimal',
    'double precision',
    'float4',
    'float8',
    'inet',
    'int',
    'int2',
    'int4',
    'int8',
    'integer',
    'interval',
    'json',
    'jsonb',
    'line',
    'lseg',
    'macaddr',
    'money',
    'numeric',
    'path',
    'pg_lsn',
    'point',
    'polygon',
    'real',
    'serial',
    'serial2',
    'serial4',
    'serial8',
    'smallint',
    'smallserial',
    'text',
    'time',
    'timestamp',
    'timestamptz',
    'timetz',
    'tsquery',
    'tsvector',
    'txid_snapshot',
    'uuid',
    'varbit',
    'varchar',
    'with time zone',
    'without time zone',
    'xml',
)

PSEUDO_TYPES = (
    'any',
    'anyelement',
    'anyarray',
    'anynonarray',
    'anyenum',
    'anyrange',
    'cstring',
    'internal',
    'language_handler',
    'fdw_handler',
    'record',
    'trigger',
    'void',
    'opaque',
)


PSEUDO_TYPES = tuple(sorted(set(PSEUDO_TYPES) - set(map(str.lower, KEYWORDS))))

PLPGSQL_KEYWORDS = (
    'ALIAS', 'CONSTANT', 'DIAGNOSTICS', 'ELSIF', 'EXCEPTION', 'EXIT',
    'FOREACH', 'GET', 'LOOP', 'NOTICE', 'OPEN', 'PERFORM', 'QUERY', 'RAISE',
    'RETURN', 'REVERSE', 'SQLSTATE', 'WHILE',
)


if __name__ == '__main__':  
    import re
    try:
        from urllib import urlopen
    except ImportError:
        from urllib.request import urlopen

    from pygments.util import format_lines

    
    SOURCE_URL = 'https://github.com/postgres/postgres/raw/master'
    KEYWORDS_URL = SOURCE_URL + '/doc/src/sgml/keywords.sgml'
    DATATYPES_URL = SOURCE_URL + '/doc/src/sgml/datatype.sgml'

    def update_myself():
        data_file = list(urlopen(DATATYPES_URL))
        datatypes = parse_datatypes(data_file)
        pseudos = parse_pseudos(data_file)

        keywords = parse_keywords(urlopen(KEYWORDS_URL))
        update_consts(__file__, 'DATATYPES', datatypes)
        update_consts(__file__, 'PSEUDO_TYPES', pseudos)
        update_consts(__file__, 'KEYWORDS', keywords)

    def parse_keywords(f):
        kw = []
        for m in re.finditer(
                r'\s*<entry><token>([^<]+)</token></entry>\s*'
                r'<entry>([^<]+)</entry>', f.read()):
            kw.append(m.group(1))

        if not kw:
            raise ValueError('no keyword found')

        kw.sort()
        return kw

    def parse_datatypes(f):
        dt = set()
        for line in f:
            if '<sect1' in line:
                break
            if '<entry><type>' not in line:
                continue

            
            
            "time" and "without time zone"

            
            line = re.sub("<replaceable>[^<]+</replaceable>", "", line)
            line = re.sub("<[^>]+>", "", line)

            
            for tmp in [t for tmp in line.split('[')
                        for t in tmp.split(']') if "(" not in t]:
                for t in tmp.split(','):
                    t = t.strip()
                    if not t: continue
                    dt.add(" ".join(t.split()))

        dt = list(dt)
        dt.sort()
        return dt

    def parse_pseudos(f):
        dt = []
        re_start = re.compile(r'\s*<table id="datatype-pseudotypes-table">')
        re_entry = re.compile(r'\s*<entry><type>([^<]+)</></entry>')
        re_end = re.compile(r'\s*</table>')

        f = iter(f)
        for line in f:
            if re_start.match(line) is not None:
                break
        else:
            raise ValueError('pseudo datatypes table not found')

        for line in f:
            m = re_entry.match(line)
            if m is not None:
                dt.append(m.group(1))

            if re_end.match(line) is not None:
                break
        else:
            raise ValueError('end of pseudo datatypes table not found')

        if not dt:
            raise ValueError('pseudo datatypes not found')

        return dt

    def update_consts(filename, constname, content):
        with open(filename) as f:
            data = f.read()

        
        re_match = re.compile(r'^%s\s*=\s*\($.*?^\s*\)$' % constname, re.M | re.S)
        m = re_match.search(data)
        if not m:
            raise ValueError('Could not find existing definition for %s' %
                             (constname,))

        new_block = format_lines(constname, content)
        data = data[:m.start()] + new_block + data[m.end():]

        with open(filename, 'w') as f:
            f.write(data)

    update_myself()
