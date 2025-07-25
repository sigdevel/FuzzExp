




"License");






"AS IS" BASIS,





import asyncio
import decimal
import http
import json
import uuid
import unittest

import edgedb

from edb.common import devmode
from edb.common import taskgroup as tg
from edb.testbase import server as tb
from edb.server.compiler import enums
from edb.tools import test


class TestServerProto(tb.QueryTestCase):

    TRANSACTION_ISOLATION = False

    SETUP = '''
        CREATE TYPE Tmp {
            CREATE REQUIRED PROPERTY tmp -> std::str;
        };

        CREATE MODULE test;
        CREATE TYPE test::Tmp2 {
            CREATE REQUIRED PROPERTY tmp -> std::str;
        };

        CREATE TYPE TransactionTest EXTENDING std::Object {
            CREATE PROPERTY name -> std::str;
        };

        CREATE SCALAR TYPE RGB
            EXTENDING enum<'RED', 'BLUE', 'GREEN'>;

        CREATE GLOBAL glob -> int64;

        
        
        
        CONFIGURE SESSION SET __internal_testmode := true;

    '''

    TEARDOWN = '''
        DROP TYPE Tmp;
    '''

    def setUp(self):
        super().setUp()
        
        
        
        self.con._clear_codecs_cache()

    async def is_testmode_on(self):
        
        "true") then this script fails.
        try:
            await self.con.execute('''
                CREATE FUNCTION testconf() -> bool
                    USING SQL $$ SELECT true; $$;
                DROP FUNCTION testconf();
            ''')
        except edgedb.InvalidFunctionDefinitionError:
            return False

        return await self.con.query_single('''
            SELECT cfg::Config.__internal_testmode LIMIT 1
        ''')

    async def test_server_proto_parse_redirect_data_01(self):
        
        
        
        for power in range(10, 20):
            base = 2 ** power
            for i in range(base - 100, base + 100):
                v = await self.con.query_single(
                    'select str_repeat(".", <int64>$i)', i=i)
                self.assertEqual(len(v), i)

    async def test_server_proto_parse_error_recover_01(self):
        for _ in range(2):
            with self.assertRaises(edgedb.EdgeQLSyntaxError):
                await self.con.query('select syntax error')

            with self.assertRaises(edgedb.EdgeQLSyntaxError):
                await self.con.query('select syntax error')

            with self.assertRaisesRegex(edgedb.EdgeQLSyntaxError,
                                        'Unexpected end of line'):
                await self.con.query('select (')

            with self.assertRaisesRegex(edgedb.EdgeQLSyntaxError,
                                        'Unexpected end of line'):
                await self.con.query_json('select (')

            for _ in range(10):
                self.assertEqual(
                    await self.con.query('select 1;'),
                    edgedb.Set((1,)))

            self.assertTrue(await self.is_testmode_on())

    async def test_server_proto_parse_error_recover_02(self):
        for _ in range(2):
            with self.assertRaises(edgedb.EdgeQLSyntaxError):
                await self.con.execute('select syntax error')

            with self.assertRaises(edgedb.EdgeQLSyntaxError):
                await self.con.execute('select syntax error')

            for _ in range(10):
                await self.con.execute('select 1; select 2;'),

    async def test_server_proto_exec_error_recover_01(self):
        for _ in range(2):
            with self.assertRaises(edgedb.DivisionByZeroError):
                await self.con.query('select 1 / 0;')

            with self.assertRaises(edgedb.DivisionByZeroError):
                await self.con.query('select 1 / 0;')
            self.assertEqual(self.con._get_last_status(), None)

            for _ in range(10):
                self.assertEqual(
                    await self.con.query('select 1;'),
                    edgedb.Set((1,)))
                self.assertEqual(self.con._get_last_status(), 'SELECT')

    async def test_server_proto_exec_error_recover_02(self):
        for _ in range(2):
            with self.assertRaises(edgedb.DivisionByZeroError):
                await self.con.execute('select 1 / 0;')

            with self.assertRaises(edgedb.DivisionByZeroError):
                await self.con.execute('select 1 / 0;')

            for _ in range(10):
                await self.con.execute('select 1;')

    async def test_server_proto_exec_error_recover_03(self):
        query = 'select 10 // <int64>$0;'
        for i in [1, 2, 0, 3, 1, 0, 1]:
            if i:
                self.assertEqual(
                    await self.con.query(query, i),
                    edgedb.Set([10 // i]))
            else:
                with self.assertRaises(edgedb.DivisionByZeroError):
                    await self.con.query(query, i)

    async def test_server_proto_exec_error_recover_04(self):
        for i in [1, 2, 0, 3, 1, 0, 1]:
            if i:
                await self.con.execute(f'select 10 // {i};')
            else:
                with self.assertRaises(edgedb.DivisionByZeroError):
                    await self.con.query(f'select 10 // {i};')

    async def test_server_proto_exec_error_recover_05(self):
        with self.assertRaisesRegex(edgedb.QueryArgumentError,
                                    "missed {'0'}"):
            await self.con.execute(f'select <int64>$0')
        self.assertEqual(
            await self.con.query('SELECT "HELLO"'),
            ["HELLO"])

    async def test_server_proto_fetch_single_command_01(self):
        r = await self.con.query('''
            CREATE TYPE server_fetch_single_command_01 {
                CREATE REQUIRED PROPERTY server_fetch_single_command_01 ->
                    std::str;
            };
        ''')
        self.assertEqual(r, [])
        self.assertEqual(self.con._get_last_status(), 'CREATE TYPE')

        r = await self.con.query('''
            DROP TYPE server_fetch_single_command_01;
        ''')
        self.assertEqual(r, [])
        self.assertEqual(self.con._get_last_status(), 'DROP TYPE')

        r = await self.con.query('''
            CREATE TYPE server_fetch_single_command_01 {
                CREATE REQUIRED PROPERTY server_fetch_single_command_01 ->
                    std::str;
            };
        ''')
        self.assertEqual(len(r), 0)

        r = await self.con.query('''
            DROP TYPE server_fetch_single_command_01;
        ''')
        self.assertEqual(len(r), 0)

        r = await self.con.query_json('''
            CREATE TYPE server_fetch_single_command_01 {
                CREATE REQUIRED PROPERTY server_fetch_single_command_01 ->
                    std::str;
            };
        ''')
        self.assertEqual(r, '[]')

        r = await self.con.query_json('''
            DROP TYPE server_fetch_single_command_01;
        ''')
        self.assertEqual(r, '[]')

    async def test_server_proto_fetch_single_command_02(self):
        r = await self.con.query('''
            SET MODULE default;
        ''')
        self.assertEqual(r, [])
        self.assertEqual(self.con._get_last_status(), 'SET ALIAS')

        r = await self.con.query('''
            SET ALIAS foo AS MODULE default;
        ''')
        self.assertEqual(r, [])

        r = await self.con.query('''
            SET MODULE default;
        ''')
        self.assertEqual(len(r), 0)

        r = await self.con.query_json('''
            SET ALIAS foo AS MODULE default;
        ''')
        self.assertEqual(r, '[]')

        r = await self.con.query_json('''
            SET MODULE default;
        ''')
        self.assertEqual(r, '[]')

        r = await self.con.query_json('''
            SET ALIAS foo AS MODULE default;
        ''')
        self.assertEqual(r, '[]')

    async def test_server_proto_fetch_single_command_03(self):
        qs = [
            'START TRANSACTION',
            'DECLARE SAVEPOINT t0',
            'ROLLBACK TO SAVEPOINT t0',
            'RELEASE SAVEPOINT t0',
            'ROLLBACK',
            'START TRANSACTION',
            'COMMIT',
        ]

        for _ in range(3):
            for q in qs:
                r = await self.con.query(q)
                self.assertEqual(r, [])

            for q in qs:
                r = await self.con.query_json(q)
                self.assertEqual(r, '[]')

        with self.assertRaisesRegex(
                edgedb.InterfaceError,
                r'it does not return any data'):
            await self.con.query_required_single('START TRANSACTION')

        with self.assertRaisesRegex(
                edgedb.InterfaceError,
                r'it does not return any data'):
            await self.con.query_required_single_json('START TRANSACTION')

    async def test_server_proto_query_script_01(self):
        self.assertEqual(
            await self.con.query('''
                SET MODULE test;
                SELECT 1;
            '''),
            [1],
        )

        self.assertEqual(
            await self.con.query_json('''
                SET MODULE test;
                SELECT 1;
            '''),
            '[1]',
        )

        with self.assertRaisesRegex(
                edgedb.InterfaceError,
                r'it does not return any data'):
            await self.con.query_required_single('''
                SELECT 1;
                SET MODULE test;
            ''')

        with self.assertRaisesRegex(
                edgedb.InterfaceError,
                r'it does not return any data'):
            await self.con.query_required_single_json('''
                SELECT 1;
                SET MODULE test;
            ''')

    async def test_server_proto_set_reset_alias_01(self):
        await self.con.execute('''
            SET ALIAS foo AS MODULE std;
            SET ALIAS bar AS MODULE std;
            SET MODULE test;
        ''')

        self.assertEqual(
            await self.con.query('SELECT foo::min({1}) + bar::min({0})'),
            [1])

        self.assertEqual(
            await self.con.query('''
                SELECT count(
                    Tmp2 FILTER Tmp2.tmp = "test_server_set_reset_alias_01");
            '''),
            [0])

        await self.con.execute('''
            RESET ALIAS bar;
        ''')

        self.assertEqual(
            await self.con.query('SELECT foo::min({1})'),
            [1])

        with self.assertRaisesRegex(
                edgedb.InvalidReferenceError,
                "function 'bar::min' does not exist"):
            await self.con.query('SELECT bar::min({1})')

        await self.con.query('''
            RESET ALIAS *;
        ''')

        with self.assertRaisesRegex(
                edgedb.InvalidReferenceError,
                "function 'foo::min' does not exist"):
            await self.con.query('SELECT foo::min({3})')

        self.assertEqual(
            await self.con.query('SELECT min({4})'),
            [4])

        with self.assertRaisesRegex(
                edgedb.InvalidReferenceError,
                "object type or alias 'default::Tmp2' does not exist"):
            await self.con.query('''
                SELECT count(
                    Tmp2 FILTER Tmp2.tmp = "test_server_set_reset_alias_01");
            ''')

    async def test_server_proto_set_reset_alias_02(self):
        await self.con.execute('''
            SET ALIAS foo AS MODULE std;
            SET ALIAS bar AS MODULE std;
            SET MODULE test;
        ''')

        self.assertEqual(
            await self.con.query('''
                SELECT count(
                    Tmp2 FILTER Tmp2.tmp = "test_server_set_reset_alias_01");
            '''),
            [0])

        await self.con.execute('''
            RESET MODULE;
        ''')

        with self.assertRaisesRegex(
                edgedb.InvalidReferenceError,
                "object type or alias 'default::Tmp2' does not exist"):
            await self.con.query('''
                SELECT count(
                    Tmp2 FILTER Tmp2.tmp = "test_server_set_reset_alias_01");
            ''')

    async def test_server_proto_set_reset_alias_03(self):
        with self.assertRaisesRegex(
                edgedb.UnknownModuleError, "module 'blahhhh' does not exist"):
            await self.con.execute('''
                SET ALIAS foo AS MODULE blahhhh;
            ''')

        with self.assertRaisesRegex(
                edgedb.UnknownModuleError, "module 'blahhhh' does not exist"):
            await self.con.execute('''
                SET MODULE blahhhh;
            ''')

        
        await self.con.execute('''
            SET MODULE default;
        ''')

        self.assertEqual(
            await self.con.query('''
                SELECT count(
                    Tmp FILTER Tmp.tmp = "test_server_set_reset_alias_01");
            '''),
            [0])

    async def test_server_proto_set_reset_alias_04(self):
        with self.assertRaisesRegex(
                edgedb.ConfigurationError,
                "unrecognized configuration parameter 'blahhhhhh'"):

            await self.con.execute('''
                SET ALIAS foo AS MODULE std;
                CONFIGURE SESSION SET blahhhhhh := 123;
            ''')

        with self.assertRaisesRegex(
                edgedb.InvalidReferenceError,
                "function 'foo::min' does not exist"):
            await self.con.query('SELECT foo::min({3})')

    async def test_server_proto_set_reset_alias_05(self):
        
        "DECLARE SAVEPOINT a1; ROLLBACK TO SAVEPOINT a1;" commands
        
        

        await self.con.query('START TRANSACTION')

        await self.con.execute('''
            SET ALIAS foo AS MODULE std;
        ''')
        await self.con.query('DECLARE SAVEPOINT a1')
        await self.con.query('ROLLBACK TO SAVEPOINT a1')

        with self.assertRaises(edgedb.DivisionByZeroError):
            await self.con.execute('''
                SELECT 1/0;
            ''')

        await self.con.query('ROLLBACK')

        with self.assertRaises(edgedb.InvalidReferenceError):
            await self.con.execute('''
                SELECT foo::len('aaa')
            ''')

    async def test_server_proto_set_reset_alias_06(self):
        await self.con.query('START TRANSACTION')

        await self.con.execute('''
            SET MODULE test;
        ''')
        await self.con.query('select Tmp2')
        await self.con.query('ROLLBACK')

        with self.assertRaises(edgedb.InvalidReferenceError):
            await self.con.query('select Tmp2')

    async def test_server_proto_set_reset_alias_07(self):
        await self.con.query('START TRANSACTION')

        await self.con.execute('''
            SET MODULE test;
        ''')
        await self.con.query('select Tmp2')

        await self.con.execute('''
            SET MODULE default;
        ''')

        with self.assertRaises(edgedb.InvalidReferenceError):
            await self.con.query('select Tmp2')

        await self.con.query('ROLLBACK')

    async def test_server_proto_set_global_01(self):
        await self.con.query('set global glob := 0')
        self.assertEqual(await self.con.query_single('select global glob'), 0)

        await self.con.query('START TRANSACTION')
        self.assertEqual(await self.con.query_single('select global glob'), 0)
        await self.con.query('set global glob := 1')
        self.assertEqual(await self.con.query_single('select global glob'), 1)

        await self.con.query('DECLARE SAVEPOINT a1')
        await self.con.query('set global glob := 2')
        self.assertEqual(await self.con.query_single('select global glob'), 2)
        await self.con.query('ROLLBACK TO SAVEPOINT a1')

        self.assertEqual(await self.con.query_single('select global glob'), 1)

        await self.con.query('ROLLBACK')

        self.assertEqual(await self.con.query_single('select global glob'), 0)

        await self.con.query('reset global glob')

    async def test_server_proto_set_global_02(self):
        await self.con.execute('START TRANSACTION')
        await self.con.execute('set global glob := 1')
        await self.con.execute('COMMIT')
        self.assertEqual(await self.con.query_single('select global glob'), 1)

    async def test_server_proto_basic_datatypes_01(self):
        for _ in range(10):
            self.assertEqual(
                await self.con.query_single(
                    'select ()'),
                ())

            self.assertEqual(
                await self.con.query(
                    'select (1,)'),
                edgedb.Set([(1,)]))

            async with self.con.transaction():
                self.assertEqual(
                    await self.con.query_single(
                        'select <array<int64>>[]'),
                    [])

            self.assertEqual(
                await self.con.query(
                    'select ["a", "b"]'),
                edgedb.Set([["a", "b"]]))

            self.assertEqual(
                await self.con.query('''
                    SELECT {(a := 1 + 1 + 40, world := ("hello", 32)),
                            (a:=1, world := ("yo", 10))};
                '''),
                edgedb.Set([
                    edgedb.NamedTuple(a=42, world=("hello", 32)),
                    edgedb.NamedTuple(a=1, world=("yo", 10)),
                ]))

            with self.assertRaisesRegex(
                edgedb.InterfaceError,
                r'query_single\(\) as it may return more than one element'
            ):
                await self.con.query_single('SELECT {1, 2}')

            await self.con.query_single('SELECT <int64>{}')

            with self.assertRaisesRegex(
                edgedb.NoDataError,
                r'returned no data',
            ):
                await self.con.query_required_single('SELECT <int64>{}')

    async def test_server_proto_basic_datatypes_02(self):
        self.assertEqual(
            await self.con.query(
                r'''select [b"\x00a", b"b", b'', b'\na', b'=A0']'''),
            edgedb.Set([[b"\x00a", b"b", b'', b'\na', b'=A0']]))

        self.assertEqual(
            await self.con.query(
                r'select <bytes>$0', b'he\x00llo'),
            edgedb.Set([b'he\x00llo']))

    async def test_server_proto_basic_datatypes_03(self):
        for _ in range(10):
            self.assertEqual(
                await self.con.query_json(
                    'select ()'),
                '[[]]')

            self.assertEqual(
                await self.con.query_json(
                    'select (1,)'),
                '[[1]]')

            self.assertEqual(
                await self.con.query_json(
                    'select <array<int64>>[]'),
                '[[]]')

            self.assertEqual(
                json.loads(
                    await self.con.query_json(
                        'select ["a", "b"]')),
                [["a", "b"]])

            self.assertEqual(
                json.loads(
                    await self.con.query_single_json(
                        'select ["a", "b"]')),
                ["a", "b"])

            self.assertEqual(
                json.loads(
                    await self.con.query_json('''
                        SELECT {(a := 1 + 1 + 40, world := ("hello", 32)),
                                (a:=1, world := ("yo", 10))};
                    ''')),
                [
                    {"a": 42, "world": ["hello", 32]},
                    {"a": 1, "world": ["yo", 10]}
                ])

            self.assertEqual(
                json.loads(
                    await self.con.query_json('SELECT {1, 2}')),
                [1, 2])

            self.assertEqual(
                json.loads(await self.con.query_json('SELECT <int64>{}')),
                [])

            with self.assertRaises(edgedb.NoDataError):
                await self.con.query_required_single_json('SELECT <int64>{}')

        self.assertEqual(self.con._get_last_status(), 'SELECT')

    async def test_server_proto_basic_datatypes_04(self):
        
        
        d = await self.con.query_single('''
            SELECT (<RGB>"RED", <RGB>"GREEN", [1], [<RGB>"GREEN"], [2])
        ''')
        self.assertEqual(d[2], [1])

    async def test_server_proto_basic_datatypes_05(self):
        
        
        "@foo" vs "foo"; before fixing the
        "@foo" key, not "foo")

        for _ in range(5):
            await self.assert_query_result(
                r"""
                    WITH MODULE schema
                    SELECT ObjectType {
                        name,
                        properties: {
                            name,
                            @foo := 1
                        } ORDER BY .name LIMIT 1,
                    }
                    FILTER .name = 'default::Tmp';
                """,
                [{
                    'name': 'default::Tmp',
                    'properties': [{
                        'name': 'id',
                        '@foo': 1
                    }],
                }]
            )

        for _ in range(5):
            await self.assert_query_result(
                r"""
                    WITH MODULE schema
                    SELECT ObjectType {
                        name,
                        properties: {
                            name,
                            foo := 1
                        } ORDER BY .name LIMIT 1,
                    }
                    FILTER .name = 'default::Tmp';
                """,
                [{
                    'name': 'default::Tmp',
                    'properties': [{
                        'name': 'id',
                        'foo': 1
                    }],
                }]
            )

    async def test_server_proto_basic_datatypes_06(self):
        
        
        for _ in range(5):
            await self.assert_query_result(
                r"""
                    WITH MODULE schema
                    SELECT ObjectType {
                        name,
                        properties: {
                            name,
                            foo1 := 1
                        } ORDER BY .name LIMIT 1,
                    }
                    FILTER .name = 'default::Tmp';
                """,
                [{
                    'name': 'default::Tmp',
                    'properties': [{
                        'name': 'id',
                        'foo1': 1
                    }],
                }]
            )

        for _ in range(5):
            await self.assert_query_result(
                r"""
                    WITH MODULE schema
                    SELECT ObjectType {
                        name,
                        properties: {
                            name,
                            foo2 := 1
                        } ORDER BY .name LIMIT 1,
                    }
                    FILTER .name = 'default::Tmp';
                """,
                [{
                    'name': 'default::Tmp',
                    'properties': [{
                        'name': 'id',
                        'foo2': 1
                    }],
                }]
            )

    async def test_server_proto_args_01(self):
        self.assertEqual(
            await self.con.query(
                'select (<array<str>>$foo)[0] ++ (<array<str>>$bar)[0];',
                foo=['aaa'], bar=['bbb']),
            edgedb.Set(('aaabbb',)))

    async def test_server_proto_args_02(self):
        self.assertEqual(
            await self.con.query(
                'select (<array<str>>$0)[0] ++ (<array<str>>$1)[0];',
                ['aaa'], ['bbb']),
            edgedb.Set(('aaabbb',)))

    async def test_server_proto_args_03(self):
        with self.assertRaisesRegex(edgedb.QueryError, r'missing \$0'):
            await self.con.query('select <int64>$1;')

        with self.assertRaisesRegex(edgedb.QueryError, r'missing \$1'):
            await self.con.query('select <int64>$0 + <int64>$2;')

        with self.assertRaisesRegex(edgedb.QueryError,
                                    'combine positional and named parameters'):
            await self.con.query('select <int64>$0 + <int64>$bar;')

    async def test_server_proto_args_04(self):
        self.assertEqual(
            await self.con.query_json(
                'select (<array<str>>$0)[0] ++ (<array<str>>$1)[0];',
                ['aaa'], ['bbb']),
            '["aaabbb"]')

    async def test_server_proto_args_05(self):
        self.assertEqual(
            await self.con.query_json(
                'select (<array<str>>$foo)[0] ++ (<array<str>>$bar)[0];',
                foo=['aaa'], bar=['bbb']),
            '["aaabbb"]')

    async def test_server_proto_args_06(self):
        for _ in range(10):
            self.assertEqual(
                await self.con.query_single(
                    'select <int64>$你好 + 10',
                    你好=32),
                42)

    async def test_server_proto_args_07(self):
        with self.assertRaisesRegex(edgedb.QueryError,
                                    r'missing a type cast.*parameter'):
            await self.con.query_single(
                'select schema::Object {name} filter .id=$id', id='asd')

    async def test_server_proto_args_08(self):
        async with self._run_and_rollback():
            await self.con.execute(
                '''
                CREATE TYPE str;
                CREATE TYPE int64;
                CREATE TYPE float64;
                CREATE TYPE decimal;
                CREATE TYPE bigint;
                '''
            )

            self.assertEqual(
                await self.con.query_single('select ("1", 1, 1.1, 1.1n, 1n)'),
                ('1', 1, 1.1, decimal.Decimal('1.1'), 1)
            )

    async def test_server_proto_args_09(self):
        async with self._run_and_rollback():
            self.assertEqual(
                await self.con.query_single(
                    'WITH std AS MODULE math SELECT ("1", 1, 1.1, 1.1n, 1n)'
                ),
                ('1', 1, 1.1, decimal.Decimal('1.1'), 1)
            )

    async def test_server_proto_args_10(self):
        self.assertEqual(
            await self.con.query(
                '''
                    select 1;
                    select '!' ++ <str>$arg;
                ''',
                arg='?'
            ),
            edgedb.Set(('!?',)))

    async def test_server_proto_args_11(self):
        async with self._run_and_rollback():
            self.assertEqual(
                await self.con.query(
                    '''
                        insert Tmp { tmp := <str>$0 };
                        select Tmp.tmp ++ <str>$1;
                    ''',
                    "?", "!"),
                edgedb.Set(["?!"]),
            )

        async with self._run_and_rollback():
            self.assertEqual(
                await self.con.query(
                    '''
                        insert Tmp { tmp := <str>$foo };
                        select Tmp.tmp ++ <str>$bar;
                    ''',
                    foo="?", bar="!"),
                edgedb.Set(["?!"]),
            )

    async def test_server_proto_wait_cancel_01(self):
        
        
        lock_key = tb.gen_lock_key()

        con2 = await self.connect(database=self.con.dbname)

        await self.con.query('START TRANSACTION')
        await self.con.query(
            'select sys::_advisory_lock(<int64>$0)', lock_key)

        try:
            async with tg.TaskGroup() as g:

                async def exec_to_fail():
                    with self.assertRaises(edgedb.ClientConnectionClosedError):
                        await con2.query(
                            'select sys::_advisory_lock(<int64>$0)', lock_key)

                g.create_task(exec_to_fail())

                await asyncio.sleep(0.1)
                con2.terminate()

            
            await asyncio.sleep(2)

        finally:
            k = await self.con.query(
                'select sys::_advisory_unlock(<int64>$0)', lock_key)
            await self.con.query('ROLLBACK')
            self.assertEqual(k, [True])

    async def test_server_proto_log_message_01(self):
        msgs = []

        def on_log(con, msg):
            msgs.append(msg)

        self.con.add_log_listener(on_log)
        try:
            await self.con.query(
                'configure system set __internal_restart := true;')
            await asyncio.sleep(0.01)  
        finally:
            self.con.remove_log_listener(on_log)

        for msg in msgs:
            if (msg.get_severity_name() == 'NOTICE' and
                    'server restart is required' in str(msg)):
                break
        else:
            raise AssertionError('a notice message was not delivered')

    async def test_server_proto_tx_savepoint_01(self):
        

        typename = 'Savepoint_01'
        query = f'SELECT {typename}.prop1'
        con = self.con

        
        self.assertTrue(await self.is_testmode_on())

        await con.query('START TRANSACTION')
        await con.execute(f'''
            CONFIGURE SESSION SET __internal_testmode := false;
        ''')
        await con.query('DECLARE SAVEPOINT t1')
        await con.execute(f'''
            CREATE TYPE {typename} {{
                CREATE REQUIRED PROPERTY prop1 -> std::str;
            }};
        ''')
        await con.query('DECLARE SAVEPOINT t1')

        self.assertEqual(self.con._get_last_status(), 'DECLARE SAVEPOINT')

        
        self.assertFalse(await self.is_testmode_on())
        
        await con.query('ROLLBACK TO SAVEPOINT t1')

        try:
            await con.execute(f'''
                INSERT {typename} {{
                    prop1 := 'aaa'
                }};
            ''')
            await self.con.query('DECLARE SAVEPOINT t1')

            await con.execute(f'''
                INSERT {typename} {{
                    prop1 := 'bbb'
                }};
            ''')

            await self.con.query('DECLARE SAVEPOINT t2')

            await con.execute(f'''
                INSERT {typename} {{
                    prop1 := 'ccc'
                }};
            ''')

            await self.con.query('DECLARE SAVEPOINT t1')

            await con.execute(f'''
                INSERT {typename} {{
                    prop1 := 'ddd'
                }};
            ''')

            await self.con.query('DECLARE SAVEPOINT t3')

            self.assertEqual(
                await con.query(query),
                edgedb.Set(('aaa', 'bbb', 'ccc', 'ddd')))

            for _ in range(10):
                await con.query('ROLLBACK TO SAVEPOINT t1')

                self.assertEqual(
                    await con.query(query),
                    edgedb.Set(('aaa', 'bbb', 'ccc')))

            await con.query('RELEASE SAVEPOINT t1')
            self.assertEqual(
                await con.query(query),
                edgedb.Set(('aaa', 'bbb', 'ccc')))

            for _ in range(5):
                await con.query('ROLLBACK TO SAVEPOINT t1')
                self.assertEqual(
                    await con.query(query),
                    edgedb.Set(('aaa',)))

            await con.query('RELEASE SAVEPOINT t1')
            await con.query('RELEASE SAVEPOINT t1')
            await con.query('ROLLBACK TO SAVEPOINT t1')

            with self.assertRaisesRegex(
                    edgedb.InvalidReferenceError,
                    ".*Savepoint.*does not exist"):
                await con.query(query)

        finally:
            await con.query('ROLLBACK')

        
        
        self.assertTrue(await self.is_testmode_on())

    async def test_server_proto_tx_savepoint_02(self):
        with self.assertRaisesRegex(
                edgedb.TransactionError, 'savepoints can only be used in tra'):
            await self.con.query('DECLARE SAVEPOINT t1')

        with self.assertRaisesRegex(
                edgedb.TransactionError, 'savepoints can only be used in tra'):
            await self.con.query('DECLARE SAVEPOINT t1')

    async def test_server_proto_tx_savepoint_03(self):
        
        

        await self.con.query('START TRANSACTION')
        await self.con.query('DECLARE SAVEPOINT t0')

        try:
            self.assertEqual(
                await self.con.query('SELECT 1;'),
                [1])

            with self.assertRaisesRegex(
                    edgedb.TransactionError, "there is no 't1' savepoint"):
                await self.con.query('''
                    RELEASE SAVEPOINT t1;
                ''')

            with self.assertRaisesRegex(
                    edgedb.TransactionError, "current transaction is aborted"):
                await self.con.query('SELECT 1;')

            with self.assertRaisesRegex(
                    edgedb.TransactionError, "current transaction is aborted"):
                await self.con.query_single('''
                    RELEASE SAVEPOINT t1;
                ''')

            await self.con.query('''
                ROLLBACK TO SAVEPOINT t0;
            ''')

            self.assertEqual(
                await self.con.query('SELECT 1;'),
                [1])

            with self.assertRaisesRegex(
                    edgedb.TransactionError, "there is no 't1' savepoint"):
                await self.con.query('''
                    RELEASE SAVEPOINT t1;
                ''')

            with self.assertRaisesRegex(
                    edgedb.TransactionError, "current transaction is aborted"):
                await self.con.query('SELECT 1;')

            with self.assertRaisesRegex(
                    edgedb.TransactionError, "current transaction is aborted"):
                await self.con.query('''
                    RELEASE SAVEPOINT t1;
                ''')

        finally:
            await self.con.query('ROLLBACK')

            self.assertEqual(
                await self.con.query('SELECT 1;'),
                [1])

    async def test_server_proto_tx_savepoint_04(self):
        
        

        await self.con.query('START TRANSACTION')
        await self.con.query('DECLARE SAVEPOINT t0')

        try:
            self.assertEqual(
                await self.con.query('SELECT 1;'),
                [1])

            with self.assertRaises(edgedb.DivisionByZeroError):
                await self.con.query('''
                    SELECT 1 / 0;
                ''')

            with self.assertRaisesRegex(
                    edgedb.TransactionError, "current transaction is aborted"):
                await self.con.query('SELECT 1;')

            await self.con.query('''
                ROLLBACK TO SAVEPOINT t0;
            ''')

            self.assertEqual(
                await self.con.query('SELECT 1;'),
                [1])

            with self.assertRaises(edgedb.DivisionByZeroError):
                await self.con.query_single('''
                    SELECT 1 / 0;
                ''')

            with self.assertRaisesRegex(
                    edgedb.TransactionError, "current transaction is aborted"):
                await self.con.query('SELECT 1;')

        finally:
            await self.con.query('ROLLBACK')

            self.assertEqual(
                await self.con.query('SELECT 1;'),
                [1])

    async def test_server_proto_tx_savepoint_05(self):
        

        await self.con.query('START TRANSACTION')
        await self.con.query('DECLARE SAVEPOINT t0')

        try:
            await self.con.execute('SELECT 1;')

            with self.assertRaisesRegex(
                    edgedb.TransactionError, "there is no 't1' savepoint"):
                await self.con.execute('''
                    RELEASE SAVEPOINT t1;
                ''')

            with self.assertRaisesRegex(
                    edgedb.TransactionError, "current transaction is aborted"):
                await self.con.execute('SELECT 1;')

            with self.assertRaisesRegex(
                    edgedb.TransactionError, "current transaction is aborted"):
                await self.con.execute('''
                    RELEASE SAVEPOINT t1;
                ''')

            await self.con.query('''
                ROLLBACK TO SAVEPOINT t0;
            ''')

            await self.con.execute('SELECT 1;')

            with self.assertRaisesRegex(
                    edgedb.TransactionError, "there is no 't1' savepoint"):
                await self.con.query('''
                    RELEASE SAVEPOINT t1;
                ''')

            with self.assertRaisesRegex(
                    edgedb.TransactionError, "current transaction is aborted"):
                await self.con.execute('SELECT 1;')

            with self.assertRaisesRegex(
                    edgedb.TransactionError, "current transaction is aborted"):
                await self.con.query('''
                    RELEASE SAVEPOINT t1;
                ''')

        finally:
            await self.con.query('ROLLBACK')

            await self.con.execute('SELECT 1;')

    async def test_server_proto_tx_savepoint_06(self):
        
        
        

        await self.con.query('START TRANSACTION')
        await self.con.query('DECLARE SAVEPOINT t0')

        try:
            await self.con.execute('SELECT 1;')

            with self.assertRaises(edgedb.DivisionByZeroError):
                await self.con.execute('''
                    SELECT 1 / 0;
                ''')

            with self.assertRaisesRegex(
                    edgedb.TransactionError, "current transaction is aborted"):
                await self.con.execute('SELECT 1;')

            await self.con.query('''
                ROLLBACK TO SAVEPOINT t0;
            ''')

            await self.con.execute('SELECT 1;')

            with self.assertRaises(edgedb.DivisionByZeroError):
                await self.con.execute('''
                    SELECT 1 / 0;
                ''')

            with self.assertRaisesRegex(
                    edgedb.TransactionError, "current transaction is aborted"):
                await self.con.execute('SELECT 1;')

        finally:
            await self.con.query('ROLLBACK')

            await self.con.execute('SELECT 1;')

    async def test_server_proto_tx_savepoint_07(self):
        con = self.con

        await con.query('START TRANSACTION')
        await con.query('DECLARE SAVEPOINT t1')
        await con.execute(f'''
            SET ALIAS t1 AS MODULE std;
            SET ALIAS t1 AS MODULE std;
        ''')
        await con.query('DECLARE SAVEPOINT t2')
        await con.execute(f'''
            SET ALIAS t2 AS MODULE std;
        ''')

        self.assertEqual(self.con._get_last_status(), 'SET ALIAS')

        try:

            for _ in range(5):
                self.assertEqual(
                    await con.query('SELECT t1::min({1}) + t2::min({2})'),
                    [3])

            await self.con.query('ROLLBACK TO SAVEPOINT t2')

            for _ in range(5):
                self.assertEqual(
                    await con.query(
                        'SELECT t1::min({1}) + std::min({100})'),
                    [101])

            with self.assertRaisesRegex(
                    edgedb.InvalidReferenceError,
                    "function 't2::min' does not exist"):
                await con.query('SELECT t1::min({1}) + t2::min({2})')

            await self.con.query('''
                ROLLBACK TO SAVEPOINT t1;
            ''')

            self.assertEqual(
                await con.query('SELECT std::min({100})'),
                [100])

            with self.assertRaisesRegex(
                    edgedb.InvalidReferenceError,
                    "function 't1::min' does not exist"):
                await con.query('SELECT t1::min({1})')

        finally:
            await con.query('ROLLBACK')

        with self.assertRaisesRegex(
                edgedb.InvalidReferenceError,
                "function 't1::min' does not exist"):
            await con.query('SELECT t1::min({1})')

    async def test_server_proto_tx_savepoint_08(self):
        con = self.con

        with self.assertRaises(edgedb.DivisionByZeroError):
            await con.query('START TRANSACTION')
            await con.query('DECLARE SAVEPOINT t1')
            await con.query('SET ALIAS t1 AS MODULE std')
            await con.query('SELECT 1 / 0')

        await con.query('ROLLBACK')
        self.assertEqual(self.con._get_last_status(), 'ROLLBACK TRANSACTION')

        with self.assertRaisesRegex(
                edgedb.InvalidReferenceError,
                "function 't1::min' does not exist"):
            await con.query_single('SELECT t1::min({1})')

    async def test_server_proto_tx_savepoint_09(self):
        
        
        

        con = self.con

        with self.assertRaises(edgedb.DivisionByZeroError):
            await con.query('START TRANSACTION')
            await con.query('DECLARE SAVEPOINT t1')
            await con.query('SET ALIAS t1 AS MODULE std')
            await con.query('SELECT 1 / 0')

        try:
            await con.query('ROLLBACK TO SAVEPOINT t1')
            await con.query('SET ALIAS t2 AS MODULE std')
            self.assertEqual(self.con._get_last_status(), 'SET ALIAS')

            self.assertEqual(
                await con.query('SELECT t2::min({2})'),
                [2])

            with self.assertRaisesRegex(
                    edgedb.InvalidReferenceError,
                    "function 't1::min' does not exist"):
                await con.query('SELECT t1::min({1})')

        finally:
            await con.query('ROLLBACK')

    async def test_server_proto_tx_savepoint_10(self):
        con = self.con

        with self.assertRaises(edgedb.DivisionByZeroError):
            await con.query('START TRANSACTION')
            await con.query('DECLARE SAVEPOINT t1')
            await con.query('DECLARE SAVEPOINT t2')
            await con.query('SELECT 1/0')

        try:
            with self.assertRaises(edgedb.DivisionByZeroError):
                await con.query('ROLLBACK TO SAVEPOINT t2')
                await self.con.query('SELECT 1/0')

            await con.query('''
                ROLLBACK TO SAVEPOINT t1;
            ''')

            self.assertEqual(
                await con.query('SELECT 42+1+1+1'),
                [45])
        finally:
            await con.query('ROLLBACK')

    async def test_server_proto_tx_savepoint_11(self):
        con = self.con

        with self.assertRaises(edgedb.DivisionByZeroError):
            await con.query('START TRANSACTION')
            await con.query('DECLARE SAVEPOINT t1')
            await con.query('DECLARE SAVEPOINT t2')
            await con.query('SELECT 1/0')

        try:
            await con.query('ROLLBACK TO SAVEPOINT t2')

            self.assertEqual(
                await con.query_single('SELECT 42+1+1+1+1'),
                46)
        finally:
            await con.query('ROLLBACK')

    async def test_server_proto_tx_savepoint_12(self):
        con = self.con

        await con.query('START TRANSACTION')
        await con.query('DECLARE SAVEPOINT p1')
        await con.query('DECLARE SAVEPOINT p2')
        await con.query('ROLLBACK TO SAVEPOINT p1')

        try:
            with self.assertRaises(edgedb.TransactionError):
                await con.query('ROLLBACK TO SAVEPOINT p2')
        finally:
            await con.query('ROLLBACK')

    async def test_server_proto_tx_savepoint_13(self):
        con = self.con

        await con.query('START TRANSACTION')
        await con.query('DECLARE SAVEPOINT p1')
        await con.query('DECLARE SAVEPOINT p2')
        await con.query('RELEASE SAVEPOINT p1')

        try:
            with self.assertRaises(edgedb.TransactionError):
                await con.query('ROLLBACK TO SAVEPOINT p2')
        finally:
            await con.query('ROLLBACK')

    async def test_server_proto_tx_01(self):
        await self.con.query('START TRANSACTION')

        try:
            await self.con.execute('SELECT 1;')

            with self.assertRaises(edgedb.DivisionByZeroError):
                await self.con.execute('''
                    SELECT 1 / 0;
                ''')

            with self.assertRaisesRegex(
                    edgedb.TransactionError, "current transaction is aborted"):
                await self.con.execute('SELECT 1;')

            
            
            with self.assertRaisesRegex(
                    edgedb.EdgeQLSyntaxError, "Unexpected 'ROLLBA'"):
                await self.con.execute('ROLLBA;')

        finally:
            await self.con.query('ROLLBACK')

        await self.con.execute('SELECT 1;')

    async def test_server_proto_tx_02(self):
        
        

        con2 = await self.connect(database=self.con.dbname)

        try:
            with self.assertRaises(edgedb.DivisionByZeroError):
                await con2.query('START TRANSACTION')
                await con2.execute('''
                    SELECT 1;
                    SELECT 1 / 0;
                ''')

            with self.assertRaisesRegex(
                    edgedb.TransactionError,
                    "current transaction is aborted"):
                await con2.query('SELECT 1;')

            await con2.query('ROLLBACK')

            self.assertEqual(
                await con2.query('SELECT 1;'),
                [1])

            with self.assertRaisesRegex(
                    edgedb.TransactionError,
                    'savepoints can only be used in tra'):
                await con2.query('DECLARE SAVEPOINT t1')
        finally:
            await con2.aclose()

    async def test_server_proto_tx_03(self):
        
        "ROLLBACK" is cached.

        con2 = await self.connect(database=self.con.dbname)

        try:
            for _ in range(5):
                await con2.query('START TRANSACTION')
                await con2.query('ROLLBACK')

            with self.assertRaises(edgedb.DivisionByZeroError):
                await con2.query('START TRANSACTION')
                await con2.execute('''
                    SELECT 1;
                    SELECT 1 / 0;
                ''')

            with self.assertRaisesRegex(
                    edgedb.TransactionError,
                    "current transaction is aborted"):
                await con2.query('SELECT 1;')

            await con2.query('ROLLBACK')

            self.assertEqual(
                await con2.query('SELECT 1;'),
                [1])

            with self.assertRaisesRegex(
                    edgedb.TransactionError,
                    'savepoints can only be used in tra'):
                await con2.query('DECLARE SAVEPOINT t1')
        finally:
            await con2.aclose()

    async def test_server_proto_tx_04(self):
        await self.con.query('START TRANSACTION')

        try:
            with self.assertRaisesRegex(
                    edgedb.TransactionError, 'already in transaction'):

                await self.con.query('START TRANSACTION')
        finally:
            await self.con.query('ROLLBACK')

    async def test_server_proto_tx_05(self):
        
        

        query = 'SELECT "test_server_proto_tx_04"'

        for _ in range(5):
            self.assertEqual(
                await self.con.query(query),
                ['test_server_proto_tx_04'])

        await self.con.query('START TRANSACTION')

        for i in range(5):
            self.assertEqual(
                await self.con.query(query),
                ['test_server_proto_tx_04'])

            self.assertEqual(
                await self.con.query('SELECT <int64>$0', i),
                [i])

        await self.con.query('ROLLBACK')

    async def test_server_proto_tx_06(self):
        
        

        query = 'SELECT 1'

        con2 = await self.connect(database=self.con.dbname)
        try:
            for _ in range(5):
                self.assertEqual(
                    await self.con.query(query),
                    [1])
        finally:
            await con2.aclose()

        await self.con.query('START TRANSACTION')

        try:
            for _ in range(5):
                self.assertEqual(
                    await self.con.query(query),
                    [1])
        finally:
            await self.con.query('ROLLBACK')

    async def test_server_proto_tx_07(self):
        

        try:
            await self.con.query('''
                START TRANSACTION ISOLATION SERIALIZABLE, READ ONLY,
                    DEFERRABLE;
            ''')

            with self.assertRaisesRegex(
                    edgedb.TransactionError,
                    'read-only transaction'):

                await self.con.query('''
                    INSERT Tmp {
                        tmp := 'aaa'
                    };
                ''')
        finally:
            await self.con.query(f'''
                ROLLBACK;
            ''')

        self.assertEqual(
            await self.con.query('SELECT 42'),
            [42])

    async def test_server_proto_tx_10(self):
        

        with self.assertRaises(edgedb.DivisionByZeroError):
            await self.con.query('START TRANSACTION')
            await self.con.query('DECLARE SAVEPOINT c0')
            await self.con.query('SET ALIAS f1 AS MODULE std')
            await self.con.query('DECLARE SAVEPOINT c1')
            await self.con.query('''
                CONFIGURE SESSION SET __internal_testmode := false
            ''')
            await self.con.query('COMMIT')

            await self.con.query('START TRANSACTION')
            await self.con.query('SET ALIAS f2 AS MODULE std')

            await self.con.query('DECLARE SAVEPOINT a0')
            await self.con.query('SET ALIAS f3 AS MODULE std')
            await self.con.query('DECLARE SAVEPOINT a1')
            await self.con.query('SELECT 1 / 0')
            await self.con.query('COMMIT')

            await self.con.query('START TRANSACTION')
            await self.con.query('SET ALIAS f4 AS MODULE std')
            await self.con.query('COMMIT')

        await self.con.query('ROLLBACK')

        self.assertFalse(await self.is_testmode_on())

        self.assertEqual(
            await self.con.query('SELECT f1::min({1})'),
            [1])

        for n in ['f2', 'f3', 'f4']:
            with self.assertRaises(edgedb.errors.InvalidReferenceError):
                async with self.con.transaction():
                    await self.con.query(f'SELECT {n}::min({{1}})')

        await self.con.query(
            'CONFIGURE SESSION SET __internal_testmode := true')
        self.assertTrue(await self.is_testmode_on())

    async def test_server_proto_tx_11(self):
        
        
        

        async def test_funcs(*, count, working, not_working):
            for ns in working:
                self.assertEqual(
                    await self.con.query(f'SELECT {ns}::min({{1}})'),
                    [1])

            await self.con.query('DECLARE SAVEPOINT _')
            for ns in not_working:
                with self.assertRaises(edgedb.errors.InvalidReferenceError):
                    try:
                        await self.con.query(f'SELECT {ns}::min({{1}})')
                    finally:
                        await self.con.query('ROLLBACK TO SAVEPOINT _;')
            await self.con.query('RELEASE SAVEPOINT _')

            actual_count = await self.con.query_single(
                '''SELECT count(
                    Tmp11
                    FILTER Tmp11.tmp = "test_server_proto_tx_11")
                ''')
            self.assertEqual(actual_count, count)

        await self.con.execute('''
            CREATE TYPE Tmp11 {
                CREATE REQUIRED PROPERTY tmp -> std::str;
            };
        ''')

        await self.con.query('START TRANSACTION')
        await self.con.query('DECLARE SAVEPOINT c0')
        await self.con.query('SET ALIAS f1 AS MODULE std')
        await self.con.execute('''
            INSERT Tmp11 {
                tmp := 'test_server_proto_tx_11'
            };
        ''')
        await self.con.query('DECLARE SAVEPOINT c1')
        await self.con.query('COMMIT')

        await self.con.query('START TRANSACTION')
        await self.con.query('SET ALIAS f2 AS MODULE std')
        await self.con.execute('''
            INSERT Tmp11 {
                tmp := 'test_server_proto_tx_11'
            };
        ''')

        await self.con.query('DECLARE SAVEPOINT a0')
        await self.con.query('SET ALIAS f3 AS MODULE std')
        await self.con.execute('''
            INSERT Tmp11 {
                tmp := 'test_server_proto_tx_11'
            };
        ''')

        await self.con.query('DECLARE SAVEPOINT a1')
        await self.con.query('SET ALIAS f4 AS MODULE std')
        await self.con.execute('''
            INSERT Tmp11 {
                tmp := 'test_server_proto_tx_11'
            };
        ''')
        with self.assertRaises(edgedb.DivisionByZeroError):
            await self.con.query('SELECT 1 / 0')

        await self.con.query('ROLLBACK TO SAVEPOINT a1')
        await test_funcs(
            count=3,
            working=['f1', 'f2', 'f3'], not_working=['f4', 'f5'])

        await self.con.query('ROLLBACK TO SAVEPOINT a0')
        await test_funcs(
            count=2,
            working=['f1', 'f2'], not_working=['f3', 'f4', 'f5'])

        await self.con.query('ROLLBACK')
        await self.con.query('START TRANSACTION')

        await test_funcs(
            count=1,
            working=['f1'], not_working=['f2', 'f3', 'f4', 'f5'])
        await self.con.query('COMMIT')

    async def test_server_proto_tx_12(self):
        
        

        await self.con.query('START TRANSACTION')
        await self.con.query('DECLARE SAVEPOINT c0')
        await self.con.query('SET ALIAS z1 AS MODULE std')
        await self.con.query('DECLARE SAVEPOINT c1')

        for _ in range(3):
            with self.assertRaises(edgedb.DivisionByZeroError):
                await self.con.execute('''
                    SET ALIAS z2 AS MODULE std;
                    SELECT 1 / 0;
                ''')
            await self.con.query('ROLLBACK TO SAVEPOINT c1')

            await self.con.query('''
                SET ALIAS z3 AS MODULE std;
            ''')
            await self.con.query('ROLLBACK TO SAVEPOINT c1')

        self.assertEqual(
            await self.con.query('SELECT z1::min({1})'),
            [1])

        await self.con.query('DECLARE SAVEPOINT _;')
        for ns in ['z2', 'z3']:
            with self.assertRaises(edgedb.errors.InvalidReferenceError):
                try:
                    await self.con.query(f'SELECT {ns}::min({{1}})')
                finally:
                    await self.con.query('ROLLBACK TO SAVEPOINT _;')
        await self.con.query('RELEASE SAVEPOINT _;')

        self.assertEqual(
            await self.con.query('SELECT z1::min({1})'),
            [1])

        await self.con.query('ROLLBACK')

    async def test_server_proto_tx_13(self):
        

        async def test_funcs(*, working, not_working):
            for ns in working:
                self.assertEqual(
                    await self.con.query(f'SELECT {ns}::min({{1}})'),
                    [1])

            for ns in not_working:
                with self.assertRaises(edgedb.errors.InvalidReferenceError):
                    await self.con.query(f'SELECT {ns}::min({{1}})')

        self.assertTrue(await self.is_testmode_on())

        try:
            await self.con.execute('''
                CREATE TYPE Tmp_tx_13 {
                    CREATE PROPERTY tmp_tx_13_1 -> int64;
                };

                ALTER TYPE Tmp_tx_13 {
                    CREATE LINK tmp_tx_13_2 -> Tmp_tx_13 {
                        ON TARGET DELETE DEFERRED RESTRICT;
                    };
                };

                INSERT Tmp_tx_13 {
                    tmp_tx_13_1 := 1
                };

                INSERT Tmp_tx_13 {
                    tmp_tx_13_1 := 2,
                    tmp_tx_13_2 := DETACHED (
                        SELECT Tmp_tx_13
                        FILTER Tmp_tx_13.tmp_tx_13_1 = 1
                        LIMIT 1
                    )
                };

                SET ALIAS f1 AS MODULE std;
            ''')

            await self.con.query('START TRANSACTION')
            await self.con.execute('''
                SET ALIAS f2 AS MODULE std;
                CONFIGURE SESSION SET __internal_testmode := false;
            ''')
            await self.con.query('SET ALIAS f3 AS MODULE std')
            await self.con.execute('''
                DELETE (SELECT Tmp_tx_13
                        FILTER Tmp_tx_13.tmp_tx_13_1 = 1);
                SET ALIAS f4 AS MODULE std;
            ''')

            self.assertFalse(
                await self.con.query_single('''
                    SELECT cfg::Config.__internal_testmode LIMIT 1
                ''')
            )

            with self.assertRaises(edgedb.ConstraintViolationError):
                await self.con.query('COMMIT')

            await test_funcs(working=['f1'],
                             not_working=['f2', 'f3', 'f4'])

        finally:
            await self.con.execute('''
                DROP TYPE Tmp_tx_13;
            ''')

        self.assertTrue(await self.is_testmode_on())

    async def test_server_proto_tx_14(self):
        await self.con.query('ROLLBACK')
        await self.con.query('ROLLBACK')
        await self.con.query('ROLLBACK')

        self.assertEqual(
            await self.con.query_single('SELECT 1;'),
            1)

        await self.con.query('START TRANSACTION')
        await self.con.query('ROLLBACK')
        await self.con.query('ROLLBACK')
        await self.con.query('ROLLBACK')

        self.assertEqual(
            await self.con.query_single('SELECT 1;'),
            1)

        await self.con.query('START TRANSACTION')

        await self.con.query('ROLLBACK')
        await self.con.query('ROLLBACK')

        self.assertEqual(
            await self.con.query_single('SELECT 1;'),
            1)

    @test.xfail("... we currently always use serializable")
    async def test_server_proto_tx_16(self):
        try:
            for isol, expected in [
                ('', 'RepeatableRead'),
                ('SERIALIZABLE', 'Serializable'),
                ('REPEATABLE READ', 'RepeatableRead')
            ]:
                stmt = 'START TRANSACTION'

                if isol:
                    stmt += f' ISOLATION {isol}'

                await self.con.query(stmt)
                result = await self.con.query_single(
                    'SELECT sys::get_transaction_isolation()')
                
                
                
                self.assertIsInstance(result, edgedb.EnumValue)
                self.assertEqual(str(result), expected)
                await self.con.query('ROLLBACK')
        finally:
            await self.con.query('ROLLBACK')

    async def test_server_proto_tx_17(self):
        con1 = self.con
        con2 = await self.connect(database=con1.dbname)

        tx1 = con1.transaction()
        tx2 = con2.transaction()
        await tx1.start()
        await tx2.start()

        try:
            async def worker(con, tx, n):
                await con.query_single(f'''
                    SELECT count(TransactionTest FILTER .name LIKE 'tx_17_{n}')
                ''')

                n2 = 1 if n == 2 else 2

                await con.query(f'''
                    INSERT TransactionTest {{
                        name := 'tx_17_{n2}'
                    }}
                ''')

            await asyncio.gather(
                worker(con1, tx1, 1), worker(con2, tx2, 2)
            )

            await tx1.commit()

            with self.assertRaises(edgedb.TransactionSerializationError):
                await tx2.commit()

        finally:
            if tx1.is_active():
                await tx1.rollback()
            if tx2.is_active():
                await tx2.rollback()
            await con2.aclose()

    async def test_server_proto_tx_18(self):
        
        
        
        with self.assertRaisesRegex(edgedb.ConstraintViolationError,
                                    'upper_str is not in upper case'):
            async with self.con.transaction():
                await self.con.execute(r"""

                    CREATE ABSTRACT CONSTRAINT uppercase {
                        CREATE ANNOTATION title := "Upper case constraint";
                        USING (str_upper(__subject__) = __subject__);
                        SET errmessage := "{__subject__} is not in upper case";
                    };

                    CREATE SCALAR TYPE upper_str EXTENDING str {
                        CREATE CONSTRAINT uppercase
                    };

                    SELECT <upper_str>'123_hello';
                """)

    async def test_server_proto_tx_19(self):
        
        
        
        
        

        
        

        
        

        typename = f'test_{uuid.uuid4().hex}'

        await self.con.execute(f'''
            CREATE SCALAR TYPE {typename} EXTENDING int64;
        ''')

        for _ in range(10):
            result = await self.con.query_single(f'''
                SELECT <{typename}>100000
            ''')
            self.assertEqual(result, 100000)

            result = await self.con.query_single('''
                SELECT "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            ''')
            self.assertEqual(
                result, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    async def test_server_proto_tx_20(self):
        await self.con.query('START TRANSACTION')
        try:
            with self.assertRaisesRegex(
                edgedb.QueryError,
                'cannot execute CREATE DATABASE in a transaction'
            ):
                await self.con.execute('CREATE DATABASE t1;')
        finally:
            await self.con.query('ROLLBACK')

        with self.assertRaisesRegex(
            edgedb.QueryError,
            'cannot execute CREATE DATABASE with other commands'
        ):
            await self.con.execute('''
                SELECT 1;
                CREATE DATABASE t1;
            ''')

    async def test_server_proto_tx_21(self):
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        "default". If it fails to inject
        "SYNC" between state reset and "START TRANSACTION" this
        

        async with tb.start_edgedb_server(max_allowed_connections=4) as sd:
            for _ in range(8):
                con1 = await sd.connect()
                try:
                    await con1.query('SET ALIAS foo AS MODULE default')
                finally:
                    await con1.aclose()

            con2 = await sd.connect()
            try:
                await con2.query('START TRANSACTION READ ONLY, DEFERRABLE')
            finally:
                await con2.aclose()

            con2 = await sd.connect()
            try:
                await con2.execute('START TRANSACTION READ ONLY, DEFERRABLE')
            finally:
                await con2.aclose()

    async def test_server_proto_tx_22(self):
        await self.con.query('START TRANSACTION')
        try:
            with self.assertRaises(edgedb.DivisionByZeroError):
                await self.con.execute('SELECT 1/0')
            
            with self.assertRaises(edgedb.TransactionError):
                await self.con.query('COMMIT')
        finally:
            await self.con.query('ROLLBACK')

        self.assertEqual(await self.con.query_single('SELECT 42'), 42)


class TestServerProtoMigration(tb.QueryTestCase):

    TRANSACTION_ISOLATION = False

    async def test_server_proto_mig_01(self):
        "test_edgeql_tutorial" test that might
        
        
        

        typename = f'test_{uuid.uuid4().hex}'

        await self.con.execute(f'''
            START MIGRATION TO {{
                module default {{
                    type {typename} {{
                        required property foo -> str;
                    }}
                }}
            }};
            POPULATE MIGRATION;
            COMMIT MIGRATION;

            INSERT {typename} {{
                foo := '123'
            }};
        ''')

        await self.assert_query_result(
            f'SELECT {typename}.foo',
            ['123']
        )


class TestServerProtoDdlPropagation(tb.QueryTestCase):

    TRANSACTION_ISOLATION = False

    @unittest.skipUnless(devmode.is_in_dev_mode(),
                         'the test requires devmode')
    async def test_server_proto_ddlprop_01(self):
        if not self.has_create_role:
            self.skipTest('create role is not supported by the backend')

        conargs = self.get_connect_args()

        await self.con.execute('''
            CREATE TYPE Test {
                CREATE PROPERTY foo -> int16;
            };

            INSERT Test { foo := 123 };
        ''')

        self.assertEqual(
            await self.con.query_single('SELECT Test.foo LIMIT 1'),
            123
        )

        server_args = {}
        if self.backend_dsn:
            server_args['backend_dsn'] = self.backend_dsn
        else:
            server_args['adjacent_to'] = self.con
        async with tb.start_edgedb_server(**server_args) as sd:

            con2 = await sd.connect(
                user=conargs.get('user'),
                password=conargs.get('password'),
                database=self.get_database_name(),
            )

            try:
                self.assertEqual(
                    await con2.query_single('SELECT Test.foo LIMIT 1'),
                    123
                )

                await self.con.execute('''
                    CREATE TYPE Test2 {
                        CREATE PROPERTY foo -> str;
                    };

                    INSERT Test2 { foo := 'text' };
                ''')

                self.assertEqual(
                    await self.con.query_single('SELECT Test2.foo LIMIT 1'),
                    'text'
                )

                
                
                
                async for tr in self.try_until_succeeds(
                    ignore=edgedb.InvalidReferenceError, timeout=30,
                ):
                    async with tr:
                        self.assertEqual(
                            await con2.query_single(
                                'SELECT Test2.foo LIMIT 1',
                            ),
                            'text',
                        )

            finally:
                await con2.aclose()

            
            async for tr in self.try_until_succeeds(
                ignore=edgedb.TransactionSerializationError
            ):
                async with tr:
                    await self.con.execute('''
                        CREATE SUPERUSER ROLE ddlprop01 {
                            SET password := 'aaaa';
                        }
                    ''')

            
            
            
            async for tr in self.try_until_succeeds(
                ignore=edgedb.AuthenticationError
            ):
                async with tr:
                    con3 = await sd.connect(
                        user='ddlprop01',
                        password='aaaa',
                        database=self.get_database_name(),
                    )

            try:
                self.assertEqual(
                    await con3.query_single('SELECT 42'),
                    42
                )
            finally:
                await con3.aclose()

                
                async for tr in self.try_until_succeeds(
                    ignore=edgedb.TransactionSerializationError
                ):
                    async with tr:
                        await self.con.execute('''
                            DROP ROLE ddlprop01;
                        ''')

    @unittest.skipUnless(devmode.is_in_dev_mode(),
                         'the test requires devmode')
    async def test_server_adjacent_database_propagation(self):
        if not self.has_create_database:
            self.skipTest('create database is not supported by the backend')

        conargs = self.get_connect_args()

        server_args = {}
        if self.backend_dsn:
            server_args['backend_dsn'] = self.backend_dsn
        else:
            server_args['adjacent_to'] = self.con
        async with tb.start_edgedb_server(**server_args) as sd:

            await self.con.execute('''
                CREATE DATABASE test_db_prop;
            ''')

            
            async for tr in self.try_until_succeeds(
                ignore=edgedb.UnknownDatabaseError,
                timeout=30,
            ):
                async with tr:
                    con2 = await sd.connect(
                        user=conargs.get('user'),
                        password=conargs.get('password'),
                        database="test_db_prop",
                    )

                    await con2.query("select 1")
                    await con2.aclose()

            await tb.drop_db(self.con, 'test_db_prop')

            
            con2 = await sd.connect(
                user=conargs.get('user'),
                password=conargs.get('password'),
                database=self.get_database_name(),
            )

            await con2.execute('''
                CREATE DATABASE test_db_prop;
            ''')

            async for tr in self.try_until_succeeds(
                ignore=edgedb.UnknownDatabaseError,
                timeout=30,
            ):
                async with tr:
                    con1 = await self.connect(database="test_db_prop")
                    await con1.query("select 1")
                    await con1.aclose()

            await tb.drop_db(con2, 'test_db_prop')

            await con2.aclose()

    @unittest.skipUnless(devmode.is_in_dev_mode(),
                         'the test requires devmode')
    async def test_server_adjacent_extension_propagation(self):
        server_args = {}
        if self.backend_dsn:
            server_args['backend_dsn'] = self.backend_dsn
        else:
            server_args['adjacent_to'] = self.con

        async with tb.start_edgedb_server(**server_args) as sd:

            await self.con.execute("CREATE EXTENSION notebook;")

            
            async for tr in self.try_until_succeeds(
                ignore=self.failureException,
            ):
                async with tr:
                    with self.http_con(server=self) as http_con:
                        response, _, status = self.http_con_json_request(
                            http_con,
                            path="notebook",
                            body={"queries": ["SELECT 1"]},
                        )

                        self.assertEqual(status, http.HTTPStatus.OK)
                        self.assertEqual(
                            response,
                            {
                                'kind': 'results',
                                'results': [
                                    {
                                        'kind': 'data',
                                        'data': [
                                            'AAAAAAAAAAAAAAAAAAABBQ==',
                                            'AgAAAAAAAAAAAAAAAAAAAQU=',
                                            'RAAAABIAAQAAAAgAAAAAAAAAAQ==',
                                            'U0VMRUNU'
                                        ]
                                    },
                                ],
                            },
                        )

            
            async for tr in self.try_until_succeeds(
                ignore=self.failureException,
            ):
                async with tr:
                    with self.http_con(server=sd) as http_con:
                        response, _, status = self.http_con_json_request(
                            http_con,
                            path="notebook",
                            body={"queries": ["SELECT 1"]},
                        )

                        self.assertEqual(status, http.HTTPStatus.OK)
                        self.assertEqual(
                            response,
                            {
                                'kind': 'results',
                                'results': [
                                    {
                                        'kind': 'data',
                                        'data': [
                                            'AAAAAAAAAAAAAAAAAAABBQ==',
                                            'AgAAAAAAAAAAAAAAAAAAAQU=',
                                            'RAAAABIAAQAAAAgAAAAAAAAAAQ==',
                                            'U0VMRUNU'
                                        ]
                                    },
                                ],
                            },
                        )

            
            await self.con.execute("DROP EXTENSION notebook;")

            
            async for tr in self.try_until_succeeds(
                ignore=self.failureException,
            ):
                async with tr:
                    with self.http_con(server=self) as http_con:
                        response, _, status = self.http_con_json_request(
                            http_con,
                            path="notebook",
                            body={"queries": ["SELECT 1"]},
                        )

                        self.assertEqual(status, http.HTTPStatus.NOT_FOUND)

            
            async for tr in self.try_until_succeeds(
                ignore=self.failureException,
            ):
                async with tr:
                    with self.http_con(server=sd) as http_con:
                        response, _, status = self.http_con_json_request(
                            http_con,
                            path="notebook",
                            body={"queries": ["SELECT 1"]},
                        )

                        self.assertEqual(status, http.HTTPStatus.NOT_FOUND)


class TestServerProtoDDL(tb.DDLTestCase):

    TRANSACTION_ISOLATION = False

    async def test_server_proto_create_db_01(self):
        if not self.has_create_database:
            self.skipTest('create database is not supported by the backend')

        db = 'test_server_proto_create_db_01'

        con1 = self.con

        cleanup = False
        try:
            for _ in range(3):
                await con1.execute(f'''
                    CREATE DATABASE {db};
                ''')
                cleanup = True

                con2 = await self.connect(database=db)
                try:
                    self.assertEqual(
                        await con2.query_single('SELECT 1'),
                        1
                    )
                finally:
                    await con2.aclose()

                await tb.drop_db(con1, db)
                cleanup = False
        finally:
            if cleanup:
                await tb.drop_db(con1, db)

    async def test_server_proto_query_cache_invalidate_01(self):
        typename = 'CacheInv_01'

        con1 = self.con
        con2 = await self.connect(database=con1.dbname)
        try:
            await con2.execute(f'''
                CREATE TYPE {typename} {{
                    CREATE REQUIRED PROPERTY prop1 -> std::str;
                }};

                INSERT {typename} {{
                    prop1 := 'aaa'
                }};
            ''')

            query = f'SELECT {typename}.prop1'

            for _ in range(5):
                self.assertEqual(
                    await con1.query(query),
                    edgedb.Set(['aaa']))

            await con2.execute(f'''
                DELETE (SELECT {typename});

                ALTER TYPE {typename} {{
                    DROP PROPERTY prop1;
                }};

                ALTER TYPE {typename} {{
                    CREATE REQUIRED PROPERTY prop1 -> std::int64;
                }};

                INSERT {typename} {{
                    prop1 := 123
                }};
            ''')

            for _ in range(5):
                self.assertEqual(
                    await con1.query(query),
                    edgedb.Set([123]))

        finally:
            await con2.aclose()

    async def test_server_proto_query_cache_invalidate_02(self):
        typename = 'CacheInv_02'

        con1 = self.con
        con2 = await self.connect(database=con1.dbname)
        try:
            await con2.query(f'''
                CREATE TYPE {typename} {{
                    CREATE REQUIRED PROPERTY prop1 -> std::str;
                }};
            ''')

            await con2.query(f'''
                INSERT {typename} {{
                    prop1 := 'aaa'
                }};
            ''')

            query = f'SELECT {typename}.prop1'

            for _ in range(5):
                self.assertEqual(
                    await con1.query(query),
                    edgedb.Set(['aaa']))

            await con2.query(f'''
                DELETE (SELECT {typename});
            ''')

            await con2.query(f'''
                ALTER TYPE {typename} {{
                    DROP PROPERTY prop1;
                }};
            ''')

            await con2.query(f'''
                ALTER TYPE {typename} {{
                    CREATE REQUIRED PROPERTY prop1 -> std::int64;
                }};
            ''')

            await con2.query(f'''
                INSERT {typename} {{
                    prop1 := 123
                }};
            ''')

            for _ in range(5):
                self.assertEqual(
                    await con1.query(query),
                    edgedb.Set([123]))

        finally:
            await con2.aclose()

    async def test_server_proto_query_cache_invalidate_03(self):
        typename = 'CacheInv_03'

        con1 = self.con
        con2 = await self.connect(database=con1.dbname)
        try:
            await con2.execute(f'''
                CREATE TYPE {typename} {{
                    CREATE REQUIRED PROPERTY prop1 -> array<std::str>;
                }};

                INSERT {typename} {{
                    prop1 := ['a', 'aa']
                }};
            ''')

            query = f'SELECT {typename}.prop1'

            for _ in range(5):
                self.assertEqual(
                    await con1.query(query),
                    edgedb.Set([['a', 'aa']]))

            await con2.execute(f'''
                DELETE (SELECT {typename});

                ALTER TYPE {typename} {{
                    DROP PROPERTY prop1;
                }};

                ALTER TYPE {typename} {{
                    CREATE REQUIRED PROPERTY prop1 -> array<std::int64>;
                }};

                INSERT {typename} {{
                    prop1 := [1, 23]
                }};
            ''')

            for _ in range(5):
                self.assertEqual(
                    await con1.query(query),
                    edgedb.Set([[1, 23]]))

        finally:
            await con2.aclose()

    async def test_server_proto_query_cache_invalidate_04(self):
        typename = 'CacheInv_04'

        con1 = self.con
        con2 = await self.connect(database=con1.dbname)
        try:
            await con2.execute(f'''
                CREATE TYPE {typename} {{
                    CREATE REQUIRED PROPERTY prop1 -> std::str;
                }};

                INSERT {typename} {{
                    prop1 := 'aaa'
                }};
            ''')

            query = f'SELECT {typename}.prop1'

            for _ in range(5):
                self.assertEqual(
                    await con1.query(query),
                    edgedb.Set(['aaa']))

            await con2.execute(f'''
                DELETE (SELECT {typename});

                ALTER TYPE {typename} {{
                    DROP PROPERTY prop1;
                }};

                ALTER TYPE {typename} {{
                    CREATE REQUIRED MULTI PROPERTY prop1 -> std::str;
                }};

                INSERT {typename} {{
                    prop1 := {{'bbb', 'ccc'}}
                }};
            ''')

            for _ in range(5):
                self.assertEqual(
                    await con1.query(query),
                    edgedb.Set(['bbb', 'ccc']))

        finally:
            await con2.aclose()

    async def test_server_proto_query_cache_invalidate_05(self):
        typename = 'CacheInv_05'

        con1 = self.con
        con2 = await self.connect(database=con1.dbname)
        try:
            await con2.execute(f'''
                CREATE TYPE {typename} {{
                    CREATE REQUIRED PROPERTY prop1 -> std::str;
                }};

                CREATE TYPE Other{typename} {{
                    CREATE REQUIRED PROPERTY prop2 -> std::str;
                }};

                INSERT {typename} {{
                    prop1 := 'aaa'
                }};

                INSERT Other{typename} {{
                    prop2 := 'bbb'
                }};
            ''')

            query = f'SELECT {typename}.prop1'

            for _ in range(5):
                self.assertEqual(
                    await con1.query(query),
                    edgedb.Set(['aaa']))

            await con2.execute(f'''
                DELETE (SELECT {typename});

                ALTER TYPE {typename} {{
                    DROP PROPERTY prop1;
                }};

                ALTER TYPE {typename} {{
                    CREATE REQUIRED LINK prop1 -> Other{typename};
                }};

                INSERT {typename} {{
                    prop1 := (SELECT Other{typename} LIMIT 1)
                }};
            ''')

            other = await con1.query(f'SELECT Other{typename}')

            for _ in range(5):
                self.assertEqual(
                    [x.id for x in await con1.query(query)],
                    [x.id for x in other],
                )

        finally:
            await con2.aclose()

    async def test_server_proto_query_cache_invalidate_06(self):
        typename = 'CacheInv_06'

        con1 = self.con
        con2 = await self.connect(database=con1.dbname)
        try:
            await con2.execute(f'''
                CREATE TYPE Foo{typename};

                CREATE TYPE Bar{typename};

                CREATE TYPE {typename} {{
                    CREATE REQUIRED LINK link1 -> Foo{typename};
                }};

                INSERT Foo{typename};
                INSERT Bar{typename};

                INSERT {typename} {{
                    link1 := (SELECT Foo{typename} LIMIT 1)
                }};
            ''')

            foo = await con1.query(f'SELECT Foo{typename}')
            bar = await con1.query(f'SELECT Bar{typename}')

            query = f'SELECT {typename}.link1'

            for _ in range(5):
                self.assertEqual(
                    [x.id for x in await con1.query(query)],
                    [x.id for x in foo],
                )

            await con2.execute(f'''
                DELETE (SELECT {typename});

                ALTER TYPE {typename} {{
                    DROP LINK link1;
                }};

                ALTER TYPE {typename} {{
                    CREATE REQUIRED LINK link1 -> Bar{typename};
                }};

                INSERT {typename} {{
                    link1 := (SELECT Bar{typename} LIMIT 1)
                }};
            ''')

            for _ in range(5):
                self.assertEqual(
                    [x.id for x in await con1.query(query)],
                    [x.id for x in bar],
                )

        finally:
            await con2.aclose()

    async def test_server_proto_query_cache_invalidate_07(self):
        typename = 'CacheInv_07'

        con1 = self.con
        con2 = await self.connect(database=con1.dbname)
        try:
            await con2.execute(f'''
                CREATE TYPE Foo{typename};

                CREATE ABSTRACT LINK link1 {{
                    CREATE PROPERTY prop1 -> std::str;
                }};

                CREATE TYPE {typename} {{
                    CREATE REQUIRED LINK link1 EXTENDING link1
                        -> Foo{typename};
                }};

                INSERT Foo{typename};

                INSERT {typename} {{
                    link1 := (
                        SELECT assert_single(Foo{typename}) {{@prop1 := 'aaa'}}
                    )
                }};
            ''')

            query = f'SELECT {typename}.link1@prop1'

            for _ in range(5):
                self.assertEqual(
                    await con1.query(query),
                    edgedb.Set(['aaa']))

            await con2.execute(f'''
                DELETE (SELECT {typename});

                ALTER ABSTRACT LINK link1 {{
                    DROP PROPERTY prop1;
                }};

                ALTER ABSTRACT LINK link1 {{
                    CREATE PROPERTY prop1 -> std::int64;
                }};

                INSERT {typename} {{
                    link1 := (
                        (SELECT Foo{typename} LIMIT 1)
                        {{@prop1 := 123}}
                    )
                }};
            ''')

            for _ in range(5):
                self.assertEqual(
                    await con1.query(query),
                    edgedb.Set([123]))

        finally:
            await con2.aclose()

    async def test_server_proto_query_cache_invalidate_09(self):
        typename = 'CacheInv_09'

        await self.con.query('START TRANSACTION')
        try:
            await self.con.execute(f'''
                CREATE TYPE {typename} {{
                    CREATE REQUIRED PROPERTY prop1 -> std::str;
                }};

                INSERT {typename} {{
                    prop1 := 'aaa'
                }};
            ''')

            query = f'SELECT {typename}.prop1'

            for _ in range(5):
                self.assertEqual(
                    await self.con.query(query),
                    edgedb.Set(['aaa']))

            await self.con.execute(f'''
                DELETE (SELECT {typename});

                ALTER TYPE {typename} {{
                    DROP PROPERTY prop1;
                }};

                ALTER TYPE {typename} {{
                    CREATE REQUIRED PROPERTY prop1 -> std::int64;
                }};

                INSERT {typename} {{
                    prop1 := 123
                }};
            ''')

            for _ in range(5):
                self.assertEqual(
                    await self.con.query(query),
                    edgedb.Set([123]))

        finally:
            await self.con.query('ROLLBACK')

    async def test_server_proto_backend_tid_propagation_01(self):
        async with self._run_and_rollback():
            await self.con.execute('''
                CREATE SCALAR TYPE tid_prop_01 EXTENDING str;
            ''')

            result = await self.con.query_single('''
                select 1;
                SELECT (<array<tid_prop_01>>$input)[1]
            ''', input=['a', 'b'])

            self.assertEqual(result, 'b')

    async def test_server_proto_backend_tid_propagation_02(self):
        try:
            await self.con.execute('''
                CREATE SCALAR TYPE tid_prop_02 EXTENDING str;
            ''')

            result = await self.con.query_single('''
                SELECT (<array<tid_prop_02>>$input)[1]
            ''', input=['a', 'b'])

            self.assertEqual(result, 'b')
        finally:
            await self.con.execute('''
                DROP SCALAR TYPE tid_prop_02;
            ''')

    async def test_server_proto_backend_tid_propagation_03(self):
        try:
            await self.con.execute('''
                START MIGRATION TO {
                    module default {
                        scalar type tid_prop_03 extending str;
                    }
                };
                POPULATE MIGRATION;
                COMMIT MIGRATION;
            ''')

            result = await self.con.query_single('''
                SELECT (<array<tid_prop_03>>$input)[1]
            ''', input=['A', 'B'])

            self.assertEqual(result, 'B')

        finally:
            await self.con.execute('''
                DROP SCALAR TYPE tid_prop_03;
            ''')

    async def test_server_proto_backend_tid_propagation_04(self):
        try:
            await self.con.query('START TRANSACTION;')
            await self.con.execute(f'''
                CREATE SCALAR TYPE tid_prop_04 EXTENDING str;
            ''')

            result = await self.con.query_single('''
                SELECT (<array<tid_prop_04>>$input)[1]
            ''', input=['A', 'B'])

            self.assertEqual(result, 'B')

        finally:
            await self.con.query('ROLLBACK')

    async def test_server_proto_backend_tid_propagation_05(self):
        try:
            await self.con.query('START TRANSACTION')
            await self.con.query('DECLARE SAVEPOINT s1')
            await self.con.execute('''
                CREATE SCALAR TYPE tid_prop_051 EXTENDING str;
            ''')
            await self.con.query('ROLLBACK TO SAVEPOINT s1')
            await self.con.execute('''
                CREATE SCALAR TYPE tid_prop_051 EXTENDING str;
                CREATE SCALAR TYPE tid_prop_052 EXTENDING str;
            ''')

            result = await self.con.query_single('''
                SELECT (<array<tid_prop_052>>$input)[1]
            ''', input=['A', 'C'])

            self.assertEqual(result, 'C')

        finally:
            await self.con.query('ROLLBACK')

    async def test_server_proto_backend_tid_propagation_06(self):
        async with self._run_and_rollback():
            await self.con.query('''
                CREATE SCALAR TYPE tid_prop_06 EXTENDING str;
            ''')

            result = await self.con.query_single('''
                SELECT (<array<tid_prop_06>>$input)[1]
            ''', input=['a', 'b'])

            self.assertEqual(result, 'b')

    async def test_server_proto_backend_tid_propagation_07(self):
        try:
            await self.con.query('''
                CREATE SCALAR TYPE tid_prop_07 EXTENDING str;
            ''')

            result = await self.con.query_single('''
                SELECT (<array<tid_prop_07>>$input)[1]
            ''', input=['a', 'b'])

            self.assertEqual(result, 'b')
        finally:
            await self.con.execute('''
                DROP SCALAR TYPE tid_prop_07;
            ''')

    async def test_server_proto_backend_tid_propagation_08(self):
        try:
            await self.con.query('START TRANSACTION')
            await self.con.execute('''
                CREATE SCALAR TYPE tid_prop_081 EXTENDING str;
            ''')
            await self.con.query('COMMIT')
            await self.con.query('START TRANSACTION')
            await self.con.execute('''
                CREATE SCALAR TYPE tid_prop_082 EXTENDING str;
            ''')

            await self.con.execute('''
                CREATE SCALAR TYPE tid_prop_083 EXTENDING str;
            ''')

            result = await self.con.query_single('''
                SELECT (<array<tid_prop_081>>$input)[0]
            ''', input=['A', 'C'])
            self.assertEqual(result, 'A')

            result = await self.con.query_single('''
                SELECT (<array<tid_prop_082>>$input)[1]
            ''', input=['A', 'C'])
            self.assertEqual(result, 'C')

            result = await self.con.query_single('''
                SELECT (<array<tid_prop_083>>$input)[1]
            ''', input=['A', 'Z'])
            self.assertEqual(result, 'Z')

        finally:
            await self.con.query('ROLLBACK')
            await self.con.execute('''
                DROP SCALAR TYPE tid_prop_081;
            ''')

    async def test_server_proto_backend_tid_propagation_09(self):
        try:
            await self.con.query('START TRANSACTION')
            await self.con.execute('''
                CREATE SCALAR TYPE tid_prop_091 EXTENDING str;
            ''')
            await self.con.query('COMMIT')
            await self.con.query('START TRANSACTION')
            await self.con.execute('''
                CREATE SCALAR TYPE tid_prop_092 EXTENDING str;
            ''')

            await self.con.execute('''
                CREATE SCALAR TYPE tid_prop_093 EXTENDING str;
            ''')

            await self.con.query('COMMIT')

            result = await self.con.query_single('''
                SELECT (<array<tid_prop_091>>$input)[0]
            ''', input=['A', 'C'])
            self.assertEqual(result, 'A')

            result = await self.con.query_single('''
                SELECT (<array<tid_prop_092>>$input)[1]
            ''', input=['A', 'C'])
            self.assertEqual(result, 'C')

            result = await self.con.query_single('''
                SELECT (<array<tid_prop_093>>$input)[1]
            ''', input=['A', 'Z'])
            self.assertEqual(result, 'Z')

        finally:
            await self.con.execute('''
                DROP SCALAR TYPE tid_prop_091;
                DROP SCALAR TYPE tid_prop_092;
                DROP SCALAR TYPE tid_prop_093;
            ''')

    async def test_server_proto_fetch_limit_01(self):
        try:
            await self.con.execute('''
                CREATE TYPE FL_A {
                    CREATE PROPERTY n -> int64;
                };
                CREATE TYPE FL_B {
                    CREATE PROPERTY n -> int64;
                    CREATE MULTI LINK a -> FL_A;
                };

                FOR i IN {1, 2, 3, 4, 5}
                UNION (
                    INSERT FL_A {
                        n := i
                    }
                );

                FOR i IN {1, 2, 3, 4, 5}
                UNION (
                    INSERT FL_B {
                        n := i,
                        a := FL_A,
                    }
                );
            ''')

            result = await self.con._fetchall(
                r"""
                    SELECT FL_B {
                        id,
                        __type__,
                        a,
                    } ORDER BY .n
                """,
                __limit__=2
            )

            self.assertEqual(len(result), 2)
            self.assertEqual(len(result[0].a), 2)

            result = await self.con._fetchall(
                r"""
                    SELECT FL_B {
                        a ORDER BY .n,
                        a_arr := array_agg(.a)
                    } ORDER BY .n
                """,
                __limit__=2
            )

            self.assertEqual(len(result), 2)
            self.assertEqual(len(result[0].a), 2)
            self.assertEqual(len(result[0].a_arr), 2)

            
            result = await self.con._fetchall(
                r"""
                    SELECT FL_B {
                        a ORDER BY .n,
                        a_arr := array_agg(.a)
                    } ORDER BY .n
                """,
                __limit__=3
            )

            self.assertEqual(len(result), 3)
            self.assertEqual(len(result[0].a), 3)
            self.assertEqual(len(result[0].a_arr), 3)

            
            result = await self.con._fetchall(
                r"""
                    SELECT FL_B {
                        a ORDER BY .n LIMIT 3,
                        a_arr := array_agg((SELECT .a LIMIT 3)),
                        a_count := count(.a),
                        a_comp := (SELECT .a LIMIT 3),
                    }
                    ORDER BY .n
                    LIMIT 3
                """,
                __limit__=4
            )

            self.assertEqual(len(result), 3)
            self.assertEqual(len(result[0].a), 3)
            self.assertEqual(len(result[0].a_arr), 3)
            self.assertEqual(len(result[0].a_comp), 3)
            self.assertEqual(result[0].a_count, 5)

            
            result = await self.con._fetchall(
                r"""
                    WITH a := {11, 12, 13}
                    SELECT _ := {9, 1, 13}
                    FILTER _ IN a;
                """,
                __limit__=1
            )

            self.assertEqual(result, edgedb.Set([13]))

            
            result = await self.con._fetchall(
                r"""
                    WITH a := {11, 12, 13}
                    SELECT <json>array_agg(a);
                """,
                __limit__=1
            )

            self.assertEqual(result, edgedb.Set(['[11, 12, 13]']))

            
            result = await self.con._fetchall(
                r"""
                    WITH a := {11, 12, 13}
                    SELECT max(a);
                """,
                __limit__=1
            )

            self.assertEqual(result, edgedb.Set([13]))

        finally:
            await self.con.execute('''
                DROP TYPE FL_B;
                DROP TYPE FL_A;
            ''')

    async def test_server_proto_fetch_limit_02(self):
        with self.assertRaises(edgedb.ProtocolError):
            await self.con._fetchall(
                'SELECT {1, 2, 3}',
                __limit__=-2,
            )

    async def test_server_proto_fetch_limit_03(self):
        await self.con._fetchall(
            'SELECT {1, 2, 3}',
            __limit__=1,
        )

        with self.assertRaises(edgedb.ProtocolError):
            await self.con._fetchall(
                'SELECT {1, 2, 3}',
                __limit__=-2,
            )

    async def test_fetch_elements(self):
        result = await self.con._fetchall_json_elements('''
            SELECT {"test1", "test2"}
        ''')
        self.assertEqual(result, ['"test1"', '"test2"'])

    async def test_query_single_script(self):
        
        
        result = await self.con.query_single('''
            select {1, 2};
            select 1;
        ''')
        self.assertEqual(result, 1)


class TestServerProtoConcurrentDDL(tb.DDLTestCase):

    TRANSACTION_ISOLATION = False

    async def test_server_proto_concurrent_ddl(self):
        typename_prefix = 'ConcurrentDDL'
        ntasks = 5

        async with tg.TaskGroup() as g:
            cons_tasks = [
                g.create_task(self.connect(database=self.con.dbname))
                for _ in range(ntasks)
            ]

        cons = [c.result() for c in cons_tasks]

        try:
            async with tg.TaskGroup() as g:
                for i, con in enumerate(cons):
                    g.create_task(con.execute(f'''
                        CREATE TYPE {typename_prefix}{i} {{
                            CREATE REQUIRED PROPERTY prop1 -> std::int64;
                        }};

                        INSERT {typename_prefix}{i} {{
                            prop1 := {i}
                        }};
                    '''))
        except tg.TaskGroupError as e:
            self.assertIn(
                edgedb.TransactionSerializationError,
                e.get_error_types(),
            )
        else:
            self.fail("TransactionSerializationError not raised")
        finally:
            async with tg.TaskGroup() as g:
                for con in cons:
                    g.create_task(con.aclose())


class TestServerProtoConcurrentGlobalDDL(tb.DDLTestCase):

    TRANSACTION_ISOLATION = False

    async def test_server_proto_concurrent_global_ddl(self):
        if not self.has_create_role:
            self.skipTest('create role is not supported by the backend')

        ntasks = 5

        async with tg.TaskGroup() as g:
            cons_tasks = [
                g.create_task(self.connect(database=self.con.dbname))
                for _ in range(ntasks)
            ]

        cons = [c.result() for c in cons_tasks]

        try:
            async with tg.TaskGroup() as g:
                for i, con in enumerate(cons):
                    g.create_task(con.execute(f'''
                        CREATE SUPERUSER ROLE concurrent_{i}
                    '''))
        except tg.TaskGroupError as e:
            self.assertIn(
                edgedb.TransactionSerializationError,
                e.get_error_types(),
            )
        else:
            self.fail("TransactionSerializationError not raised")
        finally:
            async with tg.TaskGroup() as g:
                for con in cons:
                    g.create_task(con.aclose())


class TestServerCapabilities(tb.QueryTestCase):

    TRANSACTION_ISOLATION = False

    SETUP = '''
        CREATE TYPE Modify {
            CREATE REQUIRED PROPERTY prop1 -> std::str;
        };
    '''

    TEARDOWN = '''
        DROP TYPE Modify;
    '''

    async def test_server_capabilities_01(self):
        await self.con._fetchall(
            'SELECT {1, 2, 3}',
        )
        self.assertEqual(
            self.con._get_last_capabilities(),
            enums.Capability(0),
        )

        
        await self.con._fetchall(
            'SELECT {1, 2, 3}',
            __allow_capabilities__=0,
        )
        self.assertEqual(
            self.con._get_last_capabilities(),
            enums.Capability(0),
        )

        
        await self.con._fetchall(
            'DESCRIBE OBJECT cfg::Config',
            __allow_capabilities__=0,
        )
        self.assertEqual(
            self.con._get_last_capabilities(),
            enums.Capability(0),
        )

    async def test_server_capabilities_02(self):
        await self.con._fetchall(
            'INSERT Modify { prop1 := "xx" }',
        )
        self.assertEqual(
            self.con._get_last_capabilities(),
            enums.Capability.MODIFICATIONS,
        )
        with self.assertRaises(edgedb.ProtocolError):
            await self.con._fetchall(
                'INSERT Modify { prop1 := "xx" }',
                __allow_capabilities__=0,
            )
        await self.con._fetchall(
            'INSERT Modify { prop1 := "xx" }',
            __allow_capabilities__=enums.Capability.MODIFICATIONS,
        )

    async def test_server_capabilities_03(self):
        with self.assertRaises(edgedb.ProtocolError):
            await self.con._fetchall(
                'CREATE TYPE Type1',
                __allow_capabilities__=0,
            )
        try:
            await self.con._fetchall(
                'CREATE TYPE Type1',
                __allow_capabilities__=enums.Capability.DDL,
            )
            self.assertEqual(
                self.con._get_last_capabilities(),
                enums.Capability.DDL,
            )
        finally:
            await self.con._fetchall(
                'DROP TYPE Type1',
            )
            self.assertEqual(
                self.con._get_last_capabilities(),
                enums.Capability.DDL,
            )

    async def test_server_capabilities_04(self):
        caps = enums.Capability.ALL & ~enums.Capability.SESSION_CONFIG
        with self.assertRaises(edgedb.ProtocolError):
            await self.con._fetchall(
                'CONFIGURE SESSION SET singleprop := "42"',
                __allow_capabilities__=caps,
            )

    async def test_server_capabilities_05(self):
        caps = enums.Capability.ALL & ~enums.Capability.PERSISTENT_CONFIG
        with self.assertRaises(edgedb.ProtocolError):
            await self.con._fetchall(
                'CONFIGURE INSTANCE SET singleprop := "42"',
                __allow_capabilities__=caps,
            )

    async def test_server_capabilities_06(self):
        caps = enums.Capability.ALL & ~enums.Capability.TRANSACTION
        with self.assertRaises(edgedb.DisabledCapabilityError):
            await self.con._fetchall(
                'START MIGRATION TO {}',
                __allow_capabilities__=caps,
            )

    async def test_server_capabilities_07(self):
        caps = enums.Capability.ALL & ~enums.Capability.TRANSACTION
        await self.con._fetchall(
            'START MIGRATION TO {};'
            'POPULATE MIGRATION;'
            'ABORT MIGRATION;',
            __allow_capabilities__=caps,
        )
