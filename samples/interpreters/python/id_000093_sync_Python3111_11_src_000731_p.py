import signal
import sys
import unittest
import warnings
from unittest import mock

import asyncio
from asyncio import base_subprocess
from asyncio import subprocess
from asyncio import test_utils
try:
    from test import support
except ImportError:
    from asyncio import test_support as support
if sys.platform != 'win32':
    from asyncio import unix_events


PROGRAM_BLOCKED = [sys.executable, '-c', 'import time; time.sleep(3600)']


PROGRAM_CAT = [
    sys.executable, '-c',
    ';'.join(('import sys',
              'data = sys.stdin.buffer.read()',
              'sys.stdout.buffer.write(data)'))]

class TestSubprocessTransport(base_subprocess.BaseSubprocessTransport):
    def _start(self, *args, **kwargs):
        self._proc = mock.Mock()
        self._proc.stdin = None
        self._proc.stdout = None
        self._proc.stderr = None


class SubprocessTransportTests(test_utils.TestCase):
    def setUp(self):
        self.loop = self.new_test_loop()
        self.set_event_loop(self.loop)


    def create_transport(self, waiter=None):
        protocol = mock.Mock()
        protocol.connection_made._is_coroutine = False
        protocol.process_exited._is_coroutine = False
        transport = TestSubprocessTransport(
                        self.loop, protocol, ['test'], False,
                        None, None, None, 0, waiter=waiter)
        return (transport, protocol)

    def test_proc_exited(self):
        waiter = asyncio.Future(loop=self.loop)
        transport, protocol = self.create_transport(waiter)
        transport._process_exited(6)
        self.loop.run_until_complete(waiter)

        self.assertEqual(transport.get_returncode(), 6)

        self.assertTrue(protocol.connection_made.called)
        self.assertTrue(protocol.process_exited.called)
        self.assertTrue(protocol.connection_lost.called)
        self.assertEqual(protocol.connection_lost.call_args[0], (None,))

        self.assertFalse(transport.is_closing())
        self.assertIsNone(transport._loop)
        self.assertIsNone(transport._proc)
        self.assertIsNone(transport._protocol)

        
        self.assertRaises(ProcessLookupError,
                          transport.send_signal, signal.SIGTERM)
        self.assertRaises(ProcessLookupError, transport.terminate)
        self.assertRaises(ProcessLookupError, transport.kill)

        transport.close()


class SubprocessMixin:

    def test_stdin_stdout(self):
        args = PROGRAM_CAT

        @asyncio.coroutine
        def run(data):
            proc = yield from asyncio.create_subprocess_exec(
                                          *args,
                                          stdin=subprocess.PIPE,
                                          stdout=subprocess.PIPE,
                                          loop=self.loop)

            
            proc.stdin.write(data)
            yield from proc.stdin.drain()
            proc.stdin.close()

            
            data = yield from proc.stdout.read()
            exitcode = yield from proc.wait()
            return (exitcode, data)

        task = run(b'some data')
        task = asyncio.wait_for(task, 60.0, loop=self.loop)
        exitcode, stdout = self.loop.run_until_complete(task)
        self.assertEqual(exitcode, 0)
        self.assertEqual(stdout, b'some data')

    def test_communicate(self):
        args = PROGRAM_CAT

        @asyncio.coroutine
        def run(data):
            proc = yield from asyncio.create_subprocess_exec(
                                          *args,
                                          stdin=subprocess.PIPE,
                                          stdout=subprocess.PIPE,
                                          loop=self.loop)
            stdout, stderr = yield from proc.communicate(data)
            return proc.returncode, stdout

        task = run(b'some data')
        task = asyncio.wait_for(task, 60.0, loop=self.loop)
        exitcode, stdout = self.loop.run_until_complete(task)
        self.assertEqual(exitcode, 0)
        self.assertEqual(stdout, b'some data')

    def test_shell(self):
        create = asyncio.create_subprocess_shell('exit 7',
                                                 loop=self.loop)
        proc = self.loop.run_until_complete(create)
        exitcode = self.loop.run_until_complete(proc.wait())
        self.assertEqual(exitcode, 7)

    def test_start_new_session(self):
        
        create = asyncio.create_subprocess_shell('exit 8',
                                                 start_new_session=True,
                                                 loop=self.loop)
        proc = self.loop.run_until_complete(create)
        exitcode = self.loop.run_until_complete(proc.wait())
        self.assertEqual(exitcode, 8)

    def test_kill(self):
        args = PROGRAM_BLOCKED
        create = asyncio.create_subprocess_exec(*args, loop=self.loop)
        proc = self.loop.run_until_complete(create)
        proc.kill()
        returncode = self.loop.run_until_complete(proc.wait())
        if sys.platform == 'win32':
            self.assertIsInstance(returncode, int)
            
        else:
            self.assertEqual(-signal.SIGKILL, returncode)

    def test_terminate(self):
        args = PROGRAM_BLOCKED
        create = asyncio.create_subprocess_exec(*args, loop=self.loop)
        proc = self.loop.run_until_complete(create)
        proc.terminate()
        returncode = self.loop.run_until_complete(proc.wait())
        if sys.platform == 'win32':
            self.assertIsInstance(returncode, int)
            
        else:
            self.assertEqual(-signal.SIGTERM, returncode)

    @unittest.skipIf(sys.platform == 'win32', "Don't have SIGHUP")
    def test_send_signal(self):
        code = 'import time; print("sleeping", flush=True); time.sleep(3600)'
        args = [sys.executable, '-c', code]
        create = asyncio.create_subprocess_exec(*args,
                                                stdout=subprocess.PIPE,
                                                loop=self.loop)
        proc = self.loop.run_until_complete(create)

        @asyncio.coroutine
        def send_signal(proc):
            
            line = yield from proc.stdout.readline()
            self.assertEqual(line, b'sleeping\n')

            proc.send_signal(signal.SIGHUP)
            returncode = (yield from proc.wait())
            return returncode

        returncode = self.loop.run_until_complete(send_signal(proc))
        self.assertEqual(-signal.SIGHUP, returncode)

    def prepare_broken_pipe_test(self):
        
        large_data = b'x' * support.PIPE_MAX_SIZE

        
        create = asyncio.create_subprocess_exec(
                             sys.executable, '-c', 'pass',
                             stdin=subprocess.PIPE,
                             loop=self.loop)
        proc = self.loop.run_until_complete(create)
        return (proc, large_data)

    def test_stdin_broken_pipe(self):
        proc, large_data = self.prepare_broken_pipe_test()

        @asyncio.coroutine
        def write_stdin(proc, data):
            proc.stdin.write(data)
            yield from proc.stdin.drain()

        coro = write_stdin(proc, large_data)
        
        with test_utils.disable_logger():
            self.assertRaises((BrokenPipeError, ConnectionResetError),
                              self.loop.run_until_complete, coro)
        self.loop.run_until_complete(proc.wait())

    def test_communicate_ignore_broken_pipe(self):
        proc, large_data = self.prepare_broken_pipe_test()

        
        with test_utils.disable_logger():
            self.loop.run_until_complete(proc.communicate(large_data))
        self.loop.run_until_complete(proc.wait())

    def test_pause_reading(self):
        limit = 10
        size = (limit * 2 + 1)

        @asyncio.coroutine
        def test_pause_reading():
            code = '\n'.join((
                'import sys',
                'sys.stdout.write("x" * %s)' % size,
                'sys.stdout.flush()',
            ))

            connect_read_pipe = self.loop.connect_read_pipe

            @asyncio.coroutine
            def connect_read_pipe_mock(*args, **kw):
                transport, protocol = yield from connect_read_pipe(*args, **kw)
                transport.pause_reading = mock.Mock()
                transport.resume_reading = mock.Mock()
                return (transport, protocol)

            self.loop.connect_read_pipe = connect_read_pipe_mock

            proc = yield from asyncio.create_subprocess_exec(
                                         sys.executable, '-c', code,
                                         stdin=asyncio.subprocess.PIPE,
                                         stdout=asyncio.subprocess.PIPE,
                                         limit=limit,
                                         loop=self.loop)
            stdout_transport = proc._transport.get_pipe_transport(1)

            stdout, stderr = yield from proc.communicate()

            
            
            
            return (stdout, stdout_transport)

        
        
        stdout, transport = self.loop.run_until_complete(test_pause_reading())

        self.assertEqual(stdout, b'x' * size)
        self.assertTrue(transport.pause_reading.called)
        self.assertTrue(transport.resume_reading.called)

    def test_stdin_not_inheritable(self):
        
        
        @asyncio.coroutine
        def len_message(message):
            code = 'import sys; data = sys.stdin.read(); print(len(data))'
            proc = yield from asyncio.create_subprocess_exec(
                                          sys.executable, '-c', code,
                                          stdin=asyncio.subprocess.PIPE,
                                          stdout=asyncio.subprocess.PIPE,
                                          stderr=asyncio.subprocess.PIPE,
                                          close_fds=False,
                                          loop=self.loop)
            stdout, stderr = yield from proc.communicate(message)
            exitcode = yield from proc.wait()
            return (stdout, exitcode)

        output, exitcode = self.loop.run_until_complete(len_message(b'abc'))
        self.assertEqual(output.rstrip(), b'3')
        self.assertEqual(exitcode, 0)

    def test_cancel_process_wait(self):
        

        @asyncio.coroutine
        def cancel_wait():
            proc = yield from asyncio.create_subprocess_exec(
                                          *PROGRAM_BLOCKED,
                                          loop=self.loop)

            
            task = self.loop.create_task(proc.wait())
            self.loop.call_soon(task.cancel)
            try:
                yield from task
            except asyncio.CancelledError:
                pass

            
            task.cancel()

            
            proc.kill()
            yield from proc.wait()

        self.loop.run_until_complete(cancel_wait())

    def test_cancel_make_subprocess_transport_exec(self):
        @asyncio.coroutine
        def cancel_make_transport():
            coro = asyncio.create_subprocess_exec(*PROGRAM_BLOCKED,
                                                  loop=self.loop)
            task = self.loop.create_task(coro)

            self.loop.call_soon(task.cancel)
            try:
                yield from task
            except asyncio.CancelledError:
                pass

        
        "Exception during subprocess creation, kill the subprocess"
        with test_utils.disable_logger():
            self.loop.run_until_complete(cancel_make_transport())

    def test_cancel_post_init(self):
        @asyncio.coroutine
        def cancel_make_transport():
            coro = self.loop.subprocess_exec(asyncio.SubprocessProtocol,
                                             *PROGRAM_BLOCKED)
            task = self.loop.create_task(coro)

            self.loop.call_soon(task.cancel)
            try:
                yield from task
            except asyncio.CancelledError:
                pass

        
        "Exception during subprocess creation, kill the subprocess"
        with test_utils.disable_logger():
            self.loop.run_until_complete(cancel_make_transport())
            test_utils.run_briefly(self.loop)

    def test_close_kill_running(self):
        @asyncio.coroutine
        def kill_running():
            create = self.loop.subprocess_exec(asyncio.SubprocessProtocol,
                                               *PROGRAM_BLOCKED)
            transport, protocol = yield from create

            kill_called = False
            def kill():
                nonlocal kill_called
                kill_called = True
                orig_kill()

            proc = transport.get_extra_info('subprocess')
            orig_kill = proc.kill
            proc.kill = kill
            returncode = transport.get_returncode()
            transport.close()
            yield from transport._wait()
            return (returncode, kill_called)

        "Close running child process: kill ..." log
        with test_utils.disable_logger():
            returncode, killed = self.loop.run_until_complete(kill_running())
        self.assertIsNone(returncode)

        
        self.assertTrue(killed)
        test_utils.run_briefly(self.loop)

    def test_close_dont_kill_finished(self):
        @asyncio.coroutine
        def kill_running():
            create = self.loop.subprocess_exec(asyncio.SubprocessProtocol,
                                               *PROGRAM_BLOCKED)
            transport, protocol = yield from create
            proc = transport.get_extra_info('subprocess')

            
            proc.kill()
            proc.wait()

            proc.kill = mock.Mock()
            proc_returncode = proc.poll()
            transport_returncode = transport.get_returncode()
            transport.close()
            return (proc_returncode, transport_returncode, proc.kill.called)

        "Unknown child process pid ..." log of SafeChildWatcher,
        
        
        with test_utils.disable_logger():
            result = self.loop.run_until_complete(kill_running())
            test_utils.run_briefly(self.loop)

        proc_returncode, transport_return_code, killed = result

        self.assertIsNotNone(proc_returncode)
        self.assertIsNone(transport_return_code)

        
        
        self.assertFalse(killed)

    def test_popen_error(self):
        
        
        if sys.platform == 'win32':
            target = 'asyncio.windows_utils.Popen'
        else:
            target = 'subprocess.Popen'
        with mock.patch(target) as popen:
            exc = ZeroDivisionError
            popen.side_effect = exc

            create = asyncio.create_subprocess_exec(sys.executable, '-c',
                                                    'pass', loop=self.loop)
            with warnings.catch_warnings(record=True) as warns:
                with self.assertRaises(exc):
                    self.loop.run_until_complete(create)
                self.assertEqual(warns, [])


if sys.platform != 'win32':
    
    class SubprocessWatcherMixin(SubprocessMixin):

        Watcher = None

        def setUp(self):
            policy = asyncio.get_event_loop_policy()
            self.loop = policy.new_event_loop()
            self.set_event_loop(self.loop)

            watcher = self.Watcher()
            watcher.attach_loop(self.loop)
            policy.set_child_watcher(watcher)
            self.addCleanup(policy.set_child_watcher, None)

    class SubprocessSafeWatcherTests(SubprocessWatcherMixin,
                                     test_utils.TestCase):

        Watcher = unix_events.SafeChildWatcher

    class SubprocessFastWatcherTests(SubprocessWatcherMixin,
                                     test_utils.TestCase):

        Watcher = unix_events.FastChildWatcher

else:
    
    class SubprocessProactorTests(SubprocessMixin, test_utils.TestCase):

        def setUp(self):
            self.loop = asyncio.ProactorEventLoop()
            self.set_event_loop(self.loop)


if __name__ == '__main__':
    unittest.main()
