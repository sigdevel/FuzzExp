"""Scalene: a scripting-language aware profiler for Python.

    https://github.com/plasma-umass/scalene

    See the paper "docs/scalene-paper.pdf" in this repository for technical
    details on an earlier version of Scalene's design; note that a
    number of these details have changed.

    by Emery Berger
    https://emeryberger.com

    usage: scalene test/testme.py
    usage help: scalene --help

"""
import argparse
import atexit
import builtins
import contextlib
from copy import copy
import functools
import gc
import http.server
import inspect
import json
import math
import multiprocessing
import os
import pathlib
import platform
import random
import re
import signal
import socketserver
import stat
import sys
import tempfile
import threading
import time
import traceback
import webbrowser
from collections import defaultdict
from functools import lru_cache
from signal import Handlers, Signals
from types import FrameType
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union, cast

from scalene.scalene_arguments import ScaleneArguments
from scalene.scalene_client_timer import ScaleneClientTimer
from scalene.scalene_funcutils import ScaleneFuncUtils
from scalene.scalene_json import ScaleneJSON
from scalene.scalene_mapfile import ScaleneMapFile
from scalene.scalene_output import ScaleneOutput
from scalene.scalene_preload import ScalenePreload
from scalene.scalene_signals import ScaleneSignals
from scalene.scalene_statistics import (
    Address,
    ByteCodeIndex,
    Filename,
    LineNumber,
    ScaleneStatistics,
)

if sys.platform != "win32":
    import resource

if platform.system() == "Darwin":
    from scalene.scalene_apple_gpu import ScaleneAppleGPU as ScaleneGPU
else:
    from scalene.scalene_gpu import ScaleneGPU  

from scalene.scalene_parseargs import ScaleneParseArgs, StopJupyterExecution
from scalene.scalene_sigqueue import ScaleneSigQueue


def require_python(version: Tuple[int, int]) -> None:
    assert (
        sys.version_info >= version
    ), f"Scalene requires Python version {version[0]}.{version[1]} or above."


require_python((3, 8))









def scalene_redirect_profile(func: Any) -> Any:
    return Scalene.profile(func)


builtins.profile = scalene_redirect_profile  


NEWLINE_TRIGGER_LENGTH = 98820  


def start() -> None:
    Scalene.start()


def stop() -> None:
    Scalene.stop()


class Scalene:
    """The Scalene profiler itself."""

    __in_jupyter = False  
    __start_time = 0  

    
    __is_child = -1
    
    __parent_pid = -1
    __initialized: bool = False
    __last_profiled = (Filename("NADA"), LineNumber(0), ByteCodeIndex(0))
    __last_profiled_invalidated = False

    
    
    __files_to_profile: Dict[Filename, bool] = defaultdict(bool)
    
    __functions_to_profile: Dict[Filename, Dict[Any, bool]] = defaultdict(
        lambda: {}
    )

    
    __original_thread_join = threading.Thread.join

    
    __original_lock = threading.Lock

    __args = ScaleneArguments()
    __signals = ScaleneSignals()
    __stats = ScaleneStatistics()
    __output = ScaleneOutput()
    __json = ScaleneJSON()
    __gpu = ScaleneGPU()

    __output.gpu = __gpu.has_gpu()
    __json.gpu = __gpu.has_gpu()

    @staticmethod
    def get_original_lock() -> threading.Lock:
        return Scalene.__original_lock()

    
    __all_python_names = [
        os.path.basename(sys.executable),
        os.path.basename(sys.executable) + str(sys.version_info.major),
        os.path.basename(sys.executable)
        + str(sys.version_info.major)
        + "."
        + str(sys.version_info.minor),
    ]

    
    __last_signal_time_virtual: float = 0
    __last_signal_time_wallclock: float = 0
    __last_signal_time_sys: float = 0
    __last_signal_time_user: float = 0

    
    __program_path: str = ""
    

    __python_alias_dir: pathlib.Path

    

    
    __next_output_time: float = float("inf")
    
    __pid: int = 0

    __malloc_mapfile: ScaleneMapFile
    __memcpy_mapfile: ScaleneMapFile

    
    
    __program_being_profiled = Filename("")

    
    __is_thread_sleeping: Dict[int, bool] = defaultdict(
        bool
    )  

    child_pids: Set[
        int
    ] = set()  

    
    __cpu_sigq: ScaleneSigQueue[Any]
    __alloc_sigq: ScaleneSigQueue[Any]
    __memcpy_sigq: ScaleneSigQueue[Any]
    __sigqueues: List[ScaleneSigQueue[Any]]

    client_timer: ScaleneClientTimer = ScaleneClientTimer()

    __orig_signal = signal.signal

    if sys.version_info < (3, 8):
        __orig_raise_signal = lambda s: os.kill(os.getpid(), s)
    else:
        __orig_raise_signal = signal.raise_signal

    __orig_kill = os.kill
    if sys.platform != "win32":
        __orig_setitimer = signal.setitimer
        __orig_siginterrupt = signal.siginterrupt

    @staticmethod
    def get_all_signals_set() -> Set[int]:
        return set(Scalene.__signals.get_all_signals())

    @staticmethod
    def get_timer_signals() -> Tuple[int, signal.Signals]:
        return Scalene.__signals.get_timer_signals()

    @staticmethod
    def set_in_jupyter() -> None:
        Scalene.__in_jupyter = True

    @staticmethod
    def in_jupyter() -> bool:
        return Scalene.__in_jupyter

    @staticmethod
    def interruption_handler(
        signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        this_frame: Optional[FrameType],
    ) -> None:
        raise KeyboardInterrupt

    @staticmethod
    def on_stack(
        frame: FrameType, fname: Filename, lineno: LineNumber
    ) -> Optional[FrameType]:
        """Returns true iff the given filename and line number are anywhere on the stack starting at frame."""
        found_frame = None
        f = frame
        while f:
            if (f.f_code.co_filename, f.f_lineno) == (fname, lineno):
                found_frame = f
                break
            f = cast(FrameType, f.f_back)
        return found_frame

    @staticmethod
    def update_line() -> None:
        
        bytearray(NEWLINE_TRIGGER_LENGTH)

    @staticmethod
    def invalidate_lines(frame: FrameType, _event: str, _arg: str) -> Any:
        """Mark the last_profiled information as invalid as soon as we execute a different line of code."""
        try:
            
            ff = frame.f_code.co_filename
            fl = frame.f_lineno
            (fname, lineno, lasti) = Scalene.__last_profiled
            if (ff == fname) and (fl == lineno):
                return None
            
            frame.f_trace = None
            frame.f_trace_lines = False
            
            if not Scalene.should_trace(ff):
                return None
            
            
            f = Scalene.on_stack(frame, fname, lineno)
            if f:
                
                
                
                return None
            
            sys.settrace(None)
            Scalene.update_line()
            Scalene.__last_profiled_invalidated = False
            Scalene.__last_profiled = (
                Filename(ff),
                LineNumber(fl),
                ByteCodeIndex(frame.f_lasti),
            )
            return None
        except AttributeError:
            
            return None
        except Exception as e:
            print("Error in program being profiled:\n", e)
            traceback.print_exc()
            return None

    @classmethod
    def clear_metrics(cls) -> None:
        """
        Clears the various states so that each forked process
        can start with a clean slate
        """
        cls.__stats.clear()
        cls.child_pids.clear()

    @classmethod
    def add_child_pid(cls, pid: int) -> None:
        cls.child_pids.add(pid)

    @classmethod
    def remove_child_pid(cls, pid: int) -> None:
        try:
            cls.child_pids.remove(pid)
        except KeyError:
            
            pass

    
    
    
    @staticmethod
    def profile(func: Any) -> Any:
        
        Scalene.__files_to_profile[func.__code__.co_filename] = True
        Scalene.__functions_to_profile[func.__code__.co_filename][func] = True

        @functools.wraps(func)
        def wrapper_profile(*args: Any, **kwargs: Any) -> Any:
            value = func(*args, **kwargs)
            return value

        return wrapper_profile

    @staticmethod
    def shim(func: Callable[[Any], Any]) -> Any:
        """
        Provides a decorator that, when used, calls the wrapped function with the Scalene type

        Wrapped function must be of type (s: Scalene) -> Any

        This decorator allows for marking a function in a separate file as a drop-in replacement for an existing
        library function. The intention is for these functions to replace a function that indefinitely blocks (which
        interferes with Scalene) with a function that awakens periodically to allow for signals to be delivered
        """
        func(Scalene)
        
        
        

        @functools.wraps(func)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        return wrapped

    @staticmethod
    def cleanup_files() -> None:
        Scalene.__malloc_mapfile.cleanup()
        Scalene.__memcpy_mapfile.cleanup()

    @staticmethod
    def set_thread_sleeping(tid: int) -> None:
        Scalene.__is_thread_sleeping[tid] = True

    @staticmethod
    def reset_thread_sleeping(tid: int) -> None:
        Scalene.__is_thread_sleeping[tid] = False

    timer_signals = True

    @staticmethod
    def windows_timer_loop() -> None:
        """For Windows, send periodic timer signals; launch as a background thread."""
        Scalene.timer_signals = True
        while Scalene.timer_signals:
            time.sleep(Scalene.__args.cpu_sampling_rate)
            Scalene.__orig_raise_signal(Scalene.__signals.cpu_signal)

    @staticmethod
    def start_signal_queues() -> None:
        """Starts the signal processing queues (i.e., their threads)"""
        for sigq in Scalene.__sigqueues:
            sigq.start()

    @staticmethod
    def stop_signal_queues() -> None:
        """Stops the signal processing queues (i.e., their threads)"""
        for sigq in Scalene.__sigqueues:
            sigq.stop()

    @staticmethod
    def malloc_signal_handler(
        signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        this_frame: Optional[FrameType],
    ) -> None:
        invalidated = Scalene.__last_profiled_invalidated
        (fname, lineno, lasti) = Scalene.__last_profiled
        if this_frame:
            Scalene.enter_function_meta(this_frame, Scalene.__stats)
        
        found_frame = False
        f = this_frame
        while f:
            if Scalene.should_trace(f.f_code.co_filename):
                found_frame = True
                break
            f = cast(FrameType, f.f_back)
        if not found_frame:
            return
        assert f
        
        
        
        
        if invalidated or not (
            fname == Filename(f.f_code.co_filename)
            and lineno == LineNumber(f.f_lineno)
        ):
            Scalene.update_line()
        Scalene.__last_profiled_invalidated = False
        Scalene.__last_profiled = (
            Filename(f.f_code.co_filename),
            LineNumber(f.f_lineno),
            ByteCodeIndex(f.f_lasti),
        )
        Scalene.__alloc_sigq.put([0])
        
        sys.settrace(Scalene.invalidate_lines)
        f.f_trace = Scalene.invalidate_lines
        f.f_trace_lines = True
        del this_frame

    @staticmethod
    def free_signal_handler(
        signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        this_frame: Optional[FrameType],
    ) -> None:
        if this_frame:
            Scalene.enter_function_meta(this_frame, Scalene.__stats)
        Scalene.__alloc_sigq.put([0])
        del this_frame

    @staticmethod
    def memcpy_signal_handler(
        signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        this_frame: Optional[FrameType],
    ) -> None:
        Scalene.__memcpy_sigq.put((signum, this_frame))
        del this_frame

    @staticmethod
    def enable_signals() -> None:
        """Set up the signal handlers to handle interrupts for profiling and start the
        timer interrupts."""
        if sys.platform == "win32":
            Scalene.timer_signals = True
            Scalene.__orig_signal(
                Scalene.__signals.cpu_signal,
                Scalene.cpu_signal_handler,
            )
            
            Scalene.timer_signals = True
            t = threading.Thread(target=Scalene.windows_timer_loop)
            t.start()
            Scalene.start_signal_queues()
            return
        Scalene.start_signal_queues()
        
        Scalene.__orig_signal(
            Scalene.__signals.malloc_signal, Scalene.malloc_signal_handler
        )
        Scalene.__orig_signal(
            Scalene.__signals.free_signal, Scalene.free_signal_handler
        )
        Scalene.__orig_signal(
            Scalene.__signals.memcpy_signal, Scalene.memcpy_signal_handler
        )
        
        for s in Scalene.__signals.get_all_signals():
            Scalene.__orig_siginterrupt(s, False)
        
        Scalene.__orig_signal(
            Scalene.__signals.cpu_signal,
            Scalene.cpu_signal_handler,
        )
        if sys.platform != "win32":
            Scalene.__orig_setitimer(
                Scalene.__signals.cpu_timer_signal,
                Scalene.__args.cpu_sampling_rate,
            )

    def __init__(
        self,
        arguments: argparse.Namespace,
        program_being_profiled: Optional[Filename] = None,
    ) -> None:
        import scalene.replacement_exit
        import scalene.replacement_get_context

        
        import scalene.replacement_lock
        import scalene.replacement_mp_lock
        import scalene.replacement_pjoin
        import scalene.replacement_signal_fns
        import scalene.replacement_thread_join

        if sys.platform != "win32":
            import scalene.replacement_fork
            import scalene.replacement_poll_selector

        Scalene.__args = cast(ScaleneArguments, arguments)
        Scalene.__cpu_sigq = ScaleneSigQueue(Scalene.cpu_sigqueue_processor)
        Scalene.__alloc_sigq = ScaleneSigQueue(
            Scalene.alloc_sigqueue_processor
        )
        Scalene.__memcpy_sigq = ScaleneSigQueue(
            Scalene.memcpy_sigqueue_processor
        )
        Scalene.__sigqueues = [
            Scalene.__cpu_sigq,
            Scalene.__alloc_sigq,
            Scalene.__memcpy_sigq,
        ]

        
        
        
        try:
            Scalene.__malloc_mapfile = ScaleneMapFile("malloc")
            Scalene.__memcpy_mapfile = ScaleneMapFile("memcpy")
        except:
            
            if not arguments.cpu_only:
                sys.exit(1)

        Scalene.__signals.set_timer_signals(arguments.use_virtual_time)
        if arguments.pid:
            
            
            
            
            dirname = os.environ["PATH"].split(os.pathsep)[0]
            Scalene.__python_alias_dir = pathlib.Path(dirname)
            Scalene.__pid = arguments.pid

        else:
            
            Scalene.__python_alias_dir = pathlib.Path(
                tempfile.mkdtemp(prefix="scalene")
            )
            
            
            
            Scalene.__pid = 0
            cmdline = ""
            
            cmdline += f" --cpu-sampling-rate={arguments.cpu_sampling_rate}"
            if arguments.use_virtual_time:
                cmdline += " --use-virtual-time"
            if "off" in arguments and arguments.off:
                cmdline += " --off"
            if arguments.cpu_only:
                cmdline += " --cpu-only"

            environ = ScalenePreload.get_preload_environ(arguments)
            preface = " ".join(
                "=".join((k, str(v))) for (k, v) in environ.items()
            )

            
            cmdline += f" --pid={os.getpid()} ---"
            payload = """
    echo $$
    %s %s -m scalene %s $@
    """ % (
                preface,
                sys.executable,
                cmdline,
            )
            
            for name in Scalene.__all_python_names:
                fname = os.path.join(Scalene.__python_alias_dir, name)
                with open(fname, "w") as file:
                    file.write(payload)
                os.chmod(fname, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)
            
            sys.path.insert(0, str(Scalene.__python_alias_dir))
            os.environ["PATH"] = (
                str(Scalene.__python_alias_dir)
                + os.pathsep
                + os.environ["PATH"]
            )
            
            sys.executable = Scalene.__all_python_names[0]

        
        atexit.register(Scalene.exit_handler)
        
        if program_being_profiled:
            Scalene.__program_being_profiled = Filename(
                
                program_being_profiled
            )

    @staticmethod
    def cpu_signal_handler(
        signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        this_frame: Optional[FrameType],
    ) -> None:
        """Wrapper for CPU signal handlers."""
        
        if sys.platform != "win32":
            
            
            ru = resource.getrusage(resource.RUSAGE_SELF)
            now_sys = ru.ru_stime
            now_user = ru.ru_utime
        else:
            time_info = os.times()
            now_sys = time_info.system
            now_user = time_info.user
        now_virtual = time.process_time()
        now_wallclock = time.perf_counter()
        if (
            Scalene.__last_signal_time_virtual == 0
            or Scalene.__last_signal_time_wallclock == 0
        ):
            
            Scalene.__last_signal_time_virtual = now_virtual
            Scalene.__last_signal_time_wallclock = now_wallclock
            Scalene.__last_signal_time_sys = now_sys
            Scalene.__last_signal_time_user = now_user
            if sys.platform != "win32":
                Scalene.__orig_setitimer(
                    Scalene.__signals.cpu_timer_signal,
                    Scalene.__args.cpu_sampling_rate,
                )
            return

        
        if random.randint(0, 9) == 0:
            (gpu_load, gpu_mem_used) = Scalene.__gpu.get_stats()
        else:
            (gpu_load, gpu_mem_used) = (0.0, 0.0)

        
        Scalene.__cpu_sigq.put(
            (
                signum,
                this_frame,
                now_virtual,
                now_wallclock,
                now_sys,
                now_user,
                gpu_load,
                gpu_mem_used,
                Scalene.__last_signal_time_virtual,
                Scalene.__last_signal_time_wallclock,
                Scalene.__last_signal_time_sys,
                Scalene.__last_signal_time_user,
                copy(Scalene.__is_thread_sleeping),
            )
        )
        elapsed = now_wallclock - Scalene.__last_signal_time_wallclock
        
        Scalene.__last_signal_time_virtual = now_virtual
        Scalene.__last_signal_time_wallclock = now_wallclock
        Scalene.__last_signal_time_sys = now_sys
        Scalene.__last_signal_time_user = now_user
        if sys.platform != "win32":
            if Scalene.client_timer.is_set:

                (
                    should_raise,
                    remaining_time,
                ) = Scalene.client_timer.yield_next_delay(elapsed)
                if should_raise:
                    Scalene.__orig_raise_signal(signal.SIGUSR1)
                
                
                if remaining_time > 0:
                    to_wait = min(
                        remaining_time, Scalene.__args.cpu_sampling_rate
                    )
                else:
                    to_wait = Scalene.__args.cpu_sampling_rate
                    Scalene.client_timer.reset()
                Scalene.__orig_setitimer(
                    Scalene.__signals.cpu_timer_signal,
                    to_wait,
                )
            else:
                Scalene.__orig_setitimer(
                    Scalene.__signals.cpu_timer_signal,
                    Scalene.__args.cpu_sampling_rate,
                )

    @staticmethod
    def output_profile() -> bool:
        if Scalene.__args.json:
            json_output = Scalene.__json.output_profiles(
                Scalene.__program_being_profiled,
                Scalene.__stats,
                Scalene.__pid,
                Scalene.profile_this_code,
                Scalene.__python_alias_dir,
                profile_memory=not Scalene.__args.cpu_only,
            )
            if json_output:
                if not Scalene.__output.output_file:
                    Scalene.__output.output_file = "/dev/stdout"
                with open(Scalene.__output.output_file, "w") as f:
                    f.write(
                        json.dumps(json_output, sort_keys=True, indent=4)
                        + "\n"
                    )
                return True
            else:
                return False
        else:
            output = Scalene.__output
            column_width = Scalene.__args.column_width
            if not Scalene.__args.html:
                
                try:
                    
                    if "ipykernel" in sys.modules:
                        column_width = 132
                    else:
                        import shutil

                        column_width = shutil.get_terminal_size().columns
                except:
                    pass

            did_output: bool = output.output_profiles(
                column_width,
                Scalene.__stats,
                Scalene.__pid,
                Scalene.profile_this_code,
                Scalene.__python_alias_dir,
                profile_memory=not Scalene.__args.cpu_only,
                reduced_profile=Scalene.__args.reduced_profile,
            )
            return did_output

    @staticmethod
    def profile_this_code(fname: Filename, lineno: LineNumber) -> bool:
        """When using @profile, only profile files & lines that have been decorated."""
        if not Scalene.__files_to_profile:
            return True
        if fname not in Scalene.__files_to_profile:
            return False
        
        line_info = (
            inspect.getsourcelines(fn)
            for fn in Scalene.__functions_to_profile[fname]
        )
        found_function = any(
            line_start <= lineno < line_start + len(lines)
            for (lines, line_start) in line_info
        )
        return found_function

    @staticmethod
    def cpu_sigqueue_processor(
        _signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        this_frame: FrameType,
        now_virtual: float,
        now_wallclock: float,
        now_sys: float,
        now_user: float,
        gpu_load: float,
        gpu_mem_used: float,
        prev_virtual: float,
        prev_wallclock: float,
        _prev_sys: float,
        prev_user: float,
        is_thread_sleeping: Dict[int, bool],
    ) -> None:
        """Handle interrupts for CPU profiling."""
        
        
        

        if now_wallclock >= Scalene.__next_output_time:
            
            
            
            Scalene.__next_output_time += Scalene.__args.profile_interval
            stats = Scalene.__stats
            
            with contextlib.ExitStack() as stack:
                locks = [
                    stack.enter_context(s.lock) for s in Scalene.__sigqueues
                ]
                stats.stop_clock()
                Scalene.output_profile()
                stats.start_clock()

        
        
        
        
        
        
        
        
        "problem" is in fact
        
        "for free"!  If we get
        
        
        
        
        
        
        
        elapsed_virtual = now_virtual - prev_virtual
        elapsed_wallclock = now_wallclock - prev_wallclock
        
        
        elapsed_user = now_user - prev_user
        try:
            cpu_utilization = elapsed_user / elapsed_wallclock
        except ZeroDivisionError:
            cpu_utilization = 0.0
        
        
        
        
        if cpu_utilization > 1.0:
            cpu_utilization = 1.0
            elapsed_wallclock = elapsed_user
        
        
        
        if math.isnan(gpu_load):
            gpu_load = 0.0
        gpu_time = gpu_load * Scalene.__args.cpu_sampling_rate
        Scalene.__stats.total_gpu_samples += gpu_time
        python_time = Scalene.__args.cpu_sampling_rate
        c_time = elapsed_virtual - python_time
        if c_time < 0:
            c_time = 0

        

        new_frames = Scalene.compute_frames_to_record(this_frame)

        
        total_time = python_time + c_time

        
        
        
        total_frames = sum(
            1
            for (frame, tident, orig_frame) in new_frames
            if not is_thread_sleeping[tident]
        )

        if total_frames == 0:
            normalized_time = total_time
        else:
            normalized_time = total_time / total_frames

        
        for (frame, tident, orig_frame) in new_frames:
            fname = Filename(frame.f_code.co_filename)
            lineno = LineNumber(frame.f_lineno)
            Scalene.enter_function_meta(frame, Scalene.__stats)
            if frame == new_frames[0][0]:
                
                if not is_thread_sleeping[tident]:

                    Scalene.__stats.cpu_samples_python[fname][lineno] += (
                        python_time / total_frames
                    )
                    Scalene.__stats.cpu_samples_c[fname][lineno] += (
                        c_time / total_frames
                    )
                    Scalene.__stats.cpu_samples[fname] += (
                        python_time + c_time
                    ) / total_frames
                    Scalene.__stats.cpu_utilization[fname][lineno].push(
                        cpu_utilization
                    )
                    Scalene.__stats.gpu_samples[fname][lineno] += (
                        gpu_time / total_frames
                    )
                    Scalene.__stats.gpu_mem_samples[fname][lineno].push(
                        gpu_mem_used
                    )

            else:
                
                
                
                
                
                
                if not is_thread_sleeping[tident]:
                    
                    if ScaleneFuncUtils.is_call_function(
                        orig_frame.f_code,
                        ByteCodeIndex(orig_frame.f_lasti),
                    ):
                        
                        Scalene.__stats.cpu_samples_c[fname][
                            lineno
                        ] += normalized_time
                    else:
                        
                        Scalene.__stats.cpu_samples_python[fname][
                            lineno
                        ] += normalized_time
                    Scalene.__stats.cpu_samples[fname] += normalized_time
                    Scalene.__stats.cpu_utilization[fname][lineno].push(
                        cpu_utilization
                    )

        
        del new_frames[:]
        del new_frames
        del this_frame
        del is_thread_sleeping
        Scalene.__stats.total_cpu_samples += total_time

    
    @staticmethod
    def compute_frames_to_record(
        _this_frame: FrameType,
    ) -> List[Tuple[FrameType, int, FrameType]]:
        """Collects all stack frames that Scalene actually processes."""
        frames: List[Tuple[FrameType, int]] = [
            (
                cast(
                    FrameType,
                    sys._current_frames().get(cast(int, t.ident), None),
                ),
                cast(int, t.ident),
            )
            for t in threading.enumerate()
            if t != threading.main_thread()
        ]
        

        tid = cast(int, threading.main_thread().ident)
        frames.insert(
            0,
            (
                sys._current_frames().get(tid, cast(FrameType, None)),
                tid,
            ),
        )

        
        new_frames: List[Tuple[FrameType, int, FrameType]] = []
        for (frame, tident) in frames:
            orig_frame = frame
            if not frame:
                continue
            fname = frame.f_code.co_filename
            
            if not fname:
                
                
                
                back = cast(FrameType, frame.f_back)
                fname = Filename(back.f_code.co_filename)
            while not Scalene.should_trace(fname):
                
                
                
                
                if frame:
                    frame = cast(FrameType, frame.f_back)
                    if frame:
                        fname = frame.f_code.co_filename
                else:
                    break
            if frame:
                new_frames.append((frame, tident, orig_frame))
        del frames[:]
        return new_frames

    @staticmethod
    def enter_function_meta(
        frame: FrameType, stats: ScaleneStatistics
    ) -> None:
        """Update tracking info so we can correctly report line number info later."""
        fname = Filename(frame.f_code.co_filename)
        lineno = LineNumber(frame.f_lineno)

        f = frame
        try:
            while "<" in Filename(f.f_code.co_name):
                f = cast(FrameType, f.f_back)
                
                if f is None:
                    return
        except:
            return
        if not Scalene.should_trace(f.f_code.co_filename):
            return

        fn_name = Filename(f.f_code.co_name)
        firstline = f.f_code.co_firstlineno
        
        while (
            f
            and f.f_back
            and f.f_back.f_code
            
            
        ):
            if "self" in f.f_locals:
                prepend_name = f.f_locals["self"].__class__.__name__
                if "Scalene" not in prepend_name:
                    fn_name = prepend_name + "." + fn_name
                break
            if "cls" in f.f_locals:
                prepend_name = getattr(f.f_locals["cls"], "__name__", None)
                if not prepend_name or "Scalene" in prepend_name:
                    break
                fn_name = prepend_name + "." + fn_name
                break
            f = f.f_back

        stats.function_map[fname][lineno] = fn_name
        stats.firstline_map[fn_name] = LineNumber(firstline)

    @staticmethod
    def alloc_sigqueue_processor(x: Optional[List[int]]) -> None:
        """Handle interrupts for memory profiling (mallocs and frees)."""
        stats = Scalene.__stats
        curr_pid = os.getpid()
        
        arr: List[
            Tuple[
                int,
                str,
                float,
                float,
                str,
                Filename,
                LineNumber,
                ByteCodeIndex,
            ]
        ] = []
        with contextlib.suppress(FileNotFoundError):
            while Scalene.__malloc_mapfile.read():
                count_str = Scalene.__malloc_mapfile.get_str()
                if count_str.strip() == "":
                    break
                (
                    action,
                    alloc_time_str,
                    count_str,
                    python_fraction_str,
                    pid,
                    pointer,
                    reported_fname,
                    reported_lineno,
                    bytei_str,
                ) = count_str.split(",")
                if int(curr_pid) == int(pid):
                    arr.append(
                        (
                            int(alloc_time_str),
                            action,
                            float(count_str),
                            float(python_fraction_str),
                            pointer,
                            Filename(reported_fname),
                            LineNumber(int(reported_lineno)),
                            ByteCodeIndex(int(bytei_str)),
                        )
                    )

        
        
        
        before = max(stats.current_footprint, 0)
        prevmax = stats.max_footprint
        freed_last_trigger = 0
        for (index, item) in enumerate(arr):
            (
                _alloc_time,
                action,
                count,
                _python_fraction,
                pointer,
                fname,
                lineno,
                bytei,
            ) = item
            is_malloc = action == "M"
            count /= 1024 * 1024
            if is_malloc:
                stats.current_footprint += count
                stats.max_footprint = max(
                    stats.current_footprint, stats.max_footprint
                )
            else:
                assert action == "f" or action == "F"
                stats.current_footprint -= count
                
                
                
                stats.current_footprint = max(0, stats.current_footprint)
                if action == "f":
                    
                    if stats.last_malloc_triggered[2] == pointer:
                        freed_last_trigger += 1
            timestamp = time.monotonic_ns() - Scalene.__start_time
            if len(stats.memory_footprint_samples) > 2:
                
                
                
                
                
                (t1, prior_y) = stats.memory_footprint_samples[-2]
                (t2, last_y) = stats.memory_footprint_samples[-1]
                y = stats.current_footprint
                if (prior_y < last_y and last_y < y) or (
                    prior_y > last_y and last_y > y
                ):
                    
                    
                    stats.memory_footprint_samples[-1] = [timestamp, y]
                else:
                    stats.memory_footprint_samples.append([timestamp, y])
            else:
                stats.memory_footprint_samples.append(
                    [
                        timestamp,
                        stats.current_footprint,
                    ]
                )
        after = stats.current_footprint

        if freed_last_trigger:
            if freed_last_trigger > 1:
                
                
                pass
            else:
                
                this_fn, this_ln, _this_ptr = stats.last_malloc_triggered
                if this_ln != 0:
                    mallocs, frees = stats.leak_score[this_fn][this_ln]
                    stats.leak_score[this_fn][this_ln] = (
                        mallocs,
                        frees + 1,
                    )
            stats.last_malloc_triggered = (
                Filename(""),
                LineNumber(0),
                Address("0x0"),
            )

        allocs = 0.0
        last_malloc = (Filename(""), LineNumber(0), Address("0x0"))
        malloc_pointer = "0x0"
        curr = before

        
        for item in arr:
            (
                _alloc_time,
                action,
                count,
                python_fraction,
                pointer,
                fname,
                lineno,
                bytei,
            ) = item

            is_malloc = action == "M"
            if is_malloc and count == NEWLINE_TRIGGER_LENGTH + 1:
                stats.memory_malloc_count[fname][lineno] += 1
                stats.memory_aggregate_footprint[fname][
                    lineno
                ] += stats.memory_current_highwater_mark[fname][lineno]
                stats.memory_current_footprint[fname][lineno] = 0
                stats.memory_current_highwater_mark[fname][lineno] = 0
                continue

            
            stats.bytei_map[fname][lineno].add(bytei)
            count /= 1024 * 1024
            if is_malloc:
                allocs += count
                curr += count
                malloc_pointer = pointer
                stats.memory_malloc_samples[fname][lineno] += count
                stats.memory_python_samples[fname][lineno] += (
                    python_fraction * count
                )
                stats.malloc_samples[fname] += 1
                stats.total_memory_malloc_samples += count
                
                stats.memory_current_footprint[fname][lineno] += count
                if (
                    stats.memory_current_footprint[fname][lineno]
                    > stats.memory_current_highwater_mark[fname][lineno]
                ):
                    stats.memory_current_highwater_mark[fname][
                        lineno
                    ] = stats.memory_current_footprint[fname][lineno]
                stats.memory_current_highwater_mark[fname][lineno] = max(
                    stats.memory_current_highwater_mark[fname][lineno],
                    stats.memory_current_footprint[fname][lineno],
                )
                stats.memory_max_footprint[fname][lineno] = max(
                    stats.memory_current_footprint[fname][lineno],
                    stats.memory_max_footprint[fname][lineno],
                )
            else:
                assert action == "f" or action == "F"
                curr -= count
                stats.memory_free_samples[fname][lineno] += count
                stats.memory_free_count[fname][lineno] += 1
                stats.total_memory_free_samples += count
                stats.memory_current_footprint[fname][lineno] -= count
                
                stats.memory_current_footprint[fname][lineno] = max(
                    0, stats.memory_current_footprint[fname][lineno]
                )

            stats.per_line_footprint_samples[fname][lineno].append(
                [time.monotonic_ns() - Scalene.__start_time, curr]
            )
            
            if allocs > 0:
                last_malloc = (
                    Filename(fname),
                    LineNumber(lineno),
                    Address(malloc_pointer),
                )
        stats.allocation_velocity = (
            stats.allocation_velocity[0] + (after - before),
            stats.allocation_velocity[1] + allocs,
        )
        if Scalene.__args.memory_leak_detector:
            
            if prevmax < stats.max_footprint and stats.max_footprint > 100:
                stats.last_malloc_triggered = last_malloc
                fname, lineno, _ = last_malloc
                mallocs, frees = stats.leak_score[fname][lineno]
                stats.leak_score[fname][lineno] = (mallocs + 1, frees)

    @staticmethod
    def before_fork() -> None:
        """Executed just before a fork."""
        Scalene.stop_signal_queues()

    @staticmethod
    def after_fork_in_parent(child_pid: int) -> None:
        """Executed by the parent process after a fork."""
        Scalene.add_child_pid(child_pid)
        Scalene.start_signal_queues()

    @staticmethod
    def after_fork_in_child() -> None:
        """
        Executed by a child process after a fork and mutates the
        current profiler into a child.
        """
        Scalene.__is_child = True

        Scalene.clear_metrics()
        if Scalene.__gpu.has_gpu():
            Scalene.__gpu.nvml_reinit()
        
        Scalene.__pid = Scalene.__parent_pid
        if not "off" in Scalene.__args or not Scalene.__args.off:
            Scalene.enable_signals()

    @staticmethod
    def memcpy_sigqueue_processor(
        _signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        frame: FrameType,
    ) -> None:
        curr_pid = os.getpid()
        arr: List[Tuple[str, int, int, int, int]] = []
        
        with contextlib.suppress(ValueError):
            while Scalene.__memcpy_mapfile.read():
                count_str = Scalene.__memcpy_mapfile.get_str()
                (
                    memcpy_time_str,
                    count_str2,
                    pid,
                    filename,
                    lineno,
                    bytei,
                ) = count_str.split(",")
                if int(curr_pid) == int(pid):
                    arr.append(
                        (
                            filename,
                            int(lineno),
                            int(bytei),
                            int(memcpy_time_str),
                            int(count_str2),
                        )
                    )
        arr.sort()

        for item in arr:
            filename, linenum, byteindex, _memcpy_time, count = item
            fname = Filename(filename)
            line_no = LineNumber(linenum)
            byteidx = ByteCodeIndex(byteindex)
            
            Scalene.__stats.bytei_map[fname][line_no].add(byteidx)
            Scalene.__stats.memcpy_samples[fname][line_no] += int(count)

    @staticmethod
    @lru_cache(None)
    def should_trace(filename: str) -> bool:
        """Return true if the filename is one we should trace."""
        if not filename:
            return False
        if "scalene/scalene" in filename:
            
            return False
        if "site-packages" in filename or "/lib/python" in filename:
            
            if not Scalene.__args.profile_all:
                return False
        
        profile_exclude_list = Scalene.__args.profile_exclude.split(",")
        if any(
            prof in filename for prof in profile_exclude_list if prof != ""
        ):
            return False
        if filename[0] == "<":
            if "<ipython" in filename:
                
                
                import re

                import IPython

                
                
                result = re.match("<ipython-input-([0-9]+)-.*>", filename)
                if result:
                    
                    with open(filename, "w+") as f:
                        f.write(
                            IPython.get_ipython().history_manager.input_hist_raw[
                                int(result.group(1))
                            ]
                        )
                return True
            else:
                
                return False
        
        
        profile_only_set = set(Scalene.__args.profile_only.split(","))
        not_found_in_profile_only = profile_only_set and not any(
            prof in filename for prof in profile_only_set
        )
        if not_found_in_profile_only:
            return False
        
        
        if Scalene.__args.profile_all:
            return True
        
        
        filename = os.path.abspath(filename)
        return Scalene.__program_path in filename

    @staticmethod
    def clear_mmap_data() -> None:
        if not Scalene.__args.cpu_only:
            while Scalene.__malloc_mapfile.read():
                pass
            while Scalene.__memcpy_mapfile.read():
                pass

    __done = False

    @staticmethod
    def start() -> None:
        """Initiate profiling."""
        
        if not Scalene.__initialized:
            print(
                "ERROR: Do not try to invoke `start` when you have not called Scalene using one of the methods "
                "in https://github.com/plasma-umass/scalene"
            )
            sys.exit(1)
        Scalene.__stats.start_clock()
        Scalene.enable_signals()
        Scalene.__start_time = time.monotonic_ns()
        Scalene.__done = False

    @staticmethod
    def stop() -> None:
        """Complete profiling."""
        Scalene.__done = True
        Scalene.disable_signals()
        Scalene.__stats.stop_clock()
        if Scalene.__args.web and not Scalene.__args.cli:
            if Scalene.in_jupyter():
                
                Scalene.__args.json = True
                Scalene.__output.html = False
                Scalene.__output.output_file = "profile.json"
            else:
                
                try:
                    if (
                        not webbrowser.get()
                        or type(webbrowser.get()).__name__ == "GenericBrowser"
                    ):
                        
                        
                        
                        Scalene.__args.web = False
                    else:
                        
                        Scalene.__args.json = True
                        Scalene.__output.html = False
                        Scalene.__output.output_file = "profile.json"
                except:
                    
                    Scalene.__args.web = False

    @staticmethod
    def is_done() -> bool:
        return Scalene.__done

    @staticmethod
    def start_signal_handler(
        _signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        _this_frame: Optional[FrameType],
    ) -> None:
        for pid in Scalene.child_pids:
            Scalene.__orig_kill(pid, Scalene.__signals.start_profiling_signal)
        Scalene.start()

    @staticmethod
    def stop_signal_handler(
        _signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        _this_frame: Optional[FrameType],
    ) -> None:
        for pid in Scalene.child_pids:
            Scalene.__orig_kill(pid, Scalene.__signals.stop_profiling_signal)
        Scalene.stop()

    @staticmethod
    def disable_signals(retry: bool = True) -> None:
        """Turn off the profiling signals."""
        if sys.platform == "win32":
            Scalene.timer_signals = False
            return
        try:
            Scalene.__orig_setitimer(Scalene.__signals.cpu_timer_signal, 0)
            Scalene.__orig_signal(
                Scalene.__signals.malloc_signal, signal.SIG_IGN
            )
            Scalene.__orig_signal(
                Scalene.__signals.free_signal, signal.SIG_IGN
            )
            Scalene.__orig_signal(
                Scalene.__signals.memcpy_signal, signal.SIG_IGN
            )
            Scalene.stop_signal_queues()
        except:
            
            if retry:
                Scalene.disable_signals(retry=False)

    @staticmethod
    def exit_handler() -> None:
        """When we exit, disable all signals."""
        Scalene.disable_signals()
        
        with contextlib.suppress(Exception):
            if not Scalene.__pid:
                Scalene.__python_alias_dir.cleanup()  
        with contextlib.suppress(Exception):
            os.remove(f"/tmp/scalene-malloc-lock{os.getpid()}")

    @staticmethod
    def termination_handler(
        _signum: Union[
            Callable[[Signals, FrameType], None], int, Handlers, None
        ],
        _this_frame: FrameType,
    ) -> None:
        sys.exit(1)

    def profile_code(
        self,
        code: str,
        the_globals: Dict[str, str],
        the_locals: Dict[str, str],
    ) -> int:
        
        if "off" not in Scalene.__args or not Scalene.__args.off:
            self.start()
        
        exit_status = 0
        try:
            exec(code, the_globals, the_locals)
        except SystemExit as se:
            
            exit_status = se.code
        except KeyboardInterrupt:
            
            print("Scalene execution interrupted.")
        except Exception as e:
            print("Error in program being profiled:\n", e)
            traceback.print_exc()
            exit_status = 1
        finally:
            self.stop()
            sys.settrace(None)
            
            if not Scalene.output_profile():
                print(
                    "Scalene: Program did not run for long enough to profile."
                )

            if Scalene.__args.web and not Scalene.__args.cli:
                
                
                

                try:
                    PORT = Scalene.__args.port

                    
                    class NoLogs(http.server.SimpleHTTPRequestHandler):
                        def log_message(
                            self, format: str, *args: List[Any]
                        ) -> None:
                            return

                        def log_request(
                            self,
                            code: Union[int, str] = 0,
                            size: Union[int, str] = 0,
                        ) -> None:
                            return

                    Handler = NoLogs
                    socketserver.TCPServer.allow_reuse_address = True
                    with socketserver.TCPServer(("", PORT), Handler) as httpd:
                        import threading

                        t = threading.Thread(target=httpd.serve_forever)
                        
                        import shutil

                        webgui_dir = pathlib.Path(
                            tempfile.mkdtemp(prefix="scalene-gui")
                        )
                        shutil.copytree(
                            os.path.join(os.path.dirname(__file__), "scalene-gui"),
                            os.path.join(webgui_dir, "scalene-gui"),
                        )
                        shutil.copy(
                            "profile.json", os.path.join(webgui_dir, "scalene-gui")
                        )
                        os.chdir(os.path.join(webgui_dir, "scalene-gui"))
                        t.start()
                        if Scalene.in_jupyter():
                            from IPython.core.display import HTML, display
                            from IPython.display import IFrame

                            display(
                                IFrame(
                                    src=f"http://localhost:{PORT}/profiler.html",
                                    width=700,
                                    height=600,
                                )
                            )
                        else:
                            webbrowser.open_new_tab(
                                f"http://localhost:{PORT}/profiler.html"
                            )
                        
                        time.sleep(5)
                        httpd.shutdown()
                except OSError:
                    print(f"Scalene: unable to run the Scalene GUI on port {PORT}.")
                    print("Possible solutions:")
                    print("(1) Use a different port (with --port)")
                    print("(2) Use the text version (with --cli)")
                    print("(3) Upload a generated profile.json file to the web GUI: https://plasma-umass.org/scalene-gui/.")

        return exit_status

    @staticmethod
    def process_args(args: argparse.Namespace) -> None:
        Scalene.__args = cast(ScaleneArguments, args)
        Scalene.__next_output_time = (
            time.perf_counter() + Scalene.__args.profile_interval
        )
        Scalene.__output.html = args.html
        Scalene.__output.output_file = args.outfile
        Scalene.__is_child = args.pid != 0
        
        Scalene.__parent_pid = args.pid if Scalene.__is_child else os.getpid()

    @staticmethod
    def set_initialized() -> None:
        Scalene.__initialized = True

    @staticmethod
    def main() -> None:
        (
            args,
            left,
        ) = ScaleneParseArgs.parse_args()
        Scalene.set_initialized()
        Scalene.run_profiler(args, left)

    @staticmethod
    def run_profiler(
        args: argparse.Namespace, left: List[str], is_jupyter: bool = False
    ) -> None:
        
        if is_jupyter:
            Scalene.set_in_jupyter()
        if not Scalene.__initialized:
            print(
                "ERROR: Do not try to manually invoke `run_profiler`.\n"
                "To invoke Scalene programmatically, see the usage noted in https://github.com/plasma-umass/scalene"
            )
            sys.exit(1)
        Scalene.__orig_signal(
            Scalene.__signals.start_profiling_signal,
            Scalene.start_signal_handler,
        )
        Scalene.__orig_signal(
            Scalene.__signals.stop_profiling_signal,
            Scalene.stop_signal_handler,
        )
        if sys.platform != "win32":
            Scalene.__orig_siginterrupt(
                Scalene.__signals.start_profiling_signal, False
            )
            Scalene.__orig_siginterrupt(
                Scalene.__signals.stop_profiling_signal, False
            )

        Scalene.__orig_signal(signal.SIGINT, Scalene.interruption_handler)
        if not is_jupyter:
            did_preload = ScalenePreload.setup_preload(args)
        else:
            did_preload = False
        if not did_preload:
            with contextlib.suppress(Exception):
                
                if os.getpgrp() != os.tcgetpgrp(sys.stdout.fileno()):
                    
                    print(f"Scalene now profiling process {os.getpid()}")
                    print(
                        f"  to disable profiling: python3 -m scalene.profile --off --pid {os.getpid()}"
                    )
                    print(
                        f"  to resume profiling:  python3 -m scalene.profile --on  --pid {os.getpid()}"
                    )
        Scalene.__stats.clear_all()
        sys.argv = left
        with contextlib.suppress(Exception):
            if not is_jupyter:
                multiprocessing.set_start_method("fork")
        try:
            Scalene.process_args(args)
            progs = None
            exit_status = 0
            try:
                
                progs = [x for x in sys.argv if re.match(".*\.py$", x)]
                
                with contextlib.suppress(Exception):
                    progs.append(sys.argv[0])
                    progs.append(__file__)
                if not progs:
                    raise FileNotFoundError
                with open(progs[0], "rb") as prog_being_profiled:
                    
                    try:
                        code = compile(
                            prog_being_profiled.read(),
                            progs[0],
                            "exec",
                        )
                    except SyntaxError:
                        traceback.print_exc()
                        sys.exit(1)
                    
                    program_path = os.path.dirname(os.path.abspath(progs[0]))
                    sys.path.insert(0, program_path)
                    if len(args.program_path) > 0:
                        Scalene.__program_path = os.path.abspath(
                            args.program_path
                        )
                    else:
                        Scalene.__program_path = program_path
                    
                    if not Scalene.__args.cpu_only:
                        from scalene import pywhere  

                        pywhere.register_files_to_profile(
                            list(Scalene.__files_to_profile.keys()),
                            Scalene.__program_path,
                            Scalene.__args.profile_all,
                        )

                    import __main__

                    the_locals = __main__.__dict__
                    the_globals = __main__.__dict__
                    
                    the_globals["__file__"] = os.path.abspath(progs[0])
                    
                    the_globals["__spec__"] = None
                    
                    gc.collect()
                    
                    profiler = Scalene(args, Filename(progs[0]))
                    try:
                        
                        exit_status = profiler.profile_code(
                            code, the_locals, the_globals
                        )
                        sys.exit(exit_status)
                    except StopJupyterExecution:
                        
                        pass
                    except AttributeError:
                        
                        raise
                    except Exception as ex:
                        template = "Scalene: An exception of type {0} occurred. Arguments:\n{1!r}"
                        message = template.format(type(ex).__name__, ex.args)
                        print(message)
                        print(traceback.format_exc())
            except (FileNotFoundError, IOError):
                if progs:
                    print("Scalene: could not find input file " + progs[0])
                else:
                    print("Scalene: no input file specified.")
                sys.exit(1)
        except SystemExit:
            pass
        except StopJupyterExecution:
            pass
        except Exception:
            print("Scalene failed to initialize.\n" + traceback.format_exc())
            sys.exit(1)
        finally:
            with contextlib.suppress(Exception):
                Scalene.__malloc_mapfile.close()
                Scalene.__memcpy_mapfile.close()
                if not Scalene.__is_child:
                    Scalene.cleanup_files()
            sys.exit(exit_status)


if __name__ == "__main__":
    Scalene.main()
