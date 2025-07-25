


"""This file runs the test suite against several versions of SQLite
and Python to make sure everything is ok in the various combinations.
It only runs on a UNIX like environment.

All the work is done in parallel rather than serially.  This allows
for it to finish a lot sooner.

"""

import os
import sys
import argparse
import subprocess
import re
import shutil
import time
import concurrent.futures
import random

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


os.putenv("APSWTESTPREFIX", "")
try:
    del os.environ["APSWTESTPREFIX"]
except KeyError:
    pass


def run(cmd):
    subprocess.run(cmd, shell=True, check=True)


def dotest(pyver, logdir, pybin, pylib, workdir, sqlitever, debug, sysconfig):
    pyflags = "-X warn_default_encoding  -X dev" if debug else ""
    
    pyflags += " -W ignore::DeprecationWarning:setuptools"
    if "3.6" in pybin:
        
        pyflags+=" -W ignore::DeprecationWarning"
    if "3.10" in pybin:
        
        pyflags+=" -W ignore::EncodingWarning"
    extdebug = "--debug" if debug else ""
    logf = os.path.abspath(os.path.join(logdir, "buildruntests.txt"))
    
    build_ext_flags="--definevalues SQLITE_ENABLE_COLUMN_METADATA,SQLITE_DEFAULT_CACHE_SIZE=-1" if random.choice((False, True)) else ""
    if pyver == "system" or sysconfig:
        build_ext_flags += " --use-system-sqlite-config"

    run(f"""set -e ; cd { workdir } ; ( env LD_LIBRARY_PATH={ pylib } { pybin } -bb -Werror { pyflags } setup.py fetch \
             --version={ sqlitever } --all build_test_extension build_ext --inplace --force --enable-all-extensions \
             { extdebug } { build_ext_flags } test -v ) >{ logf }  2>&1""")


def runtest(workdir, pyver, bits, sqlitever, logdir, debug, sysconfig):
    pybin, pylib = buildpython(workdir, pyver, bits, os.path.abspath(os.path.join(logdir, "pybuild.txt")))
    dotest(pyver, logdir, pybin, pylib, workdir, sqlitever, debug, sysconfig)


def main(PYVERS, SQLITEVERS, BITS, concurrency):
    try:
        del os.environ["APSWTESTPREFIX"]
    except KeyError:
        pass
    print("Test starting")
    os.system("rm -rf apsw/.*so megatestresults 2>/dev/null ; mkdir megatestresults")
    print("  ... removing old work directory")
    topworkdir = os.path.abspath("../apsw-test")
    os.system(f"rm -rf { topworkdir }/* 2>/dev/null ; mkdir -p { topworkdir }")
    os.system('rm -rf $HOME/.local/lib/python*/site-packages/apsw* 2>/dev/null')
    print("      done")

    jobs = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        for pyver in PYVERS:
            for sqlitever in SQLITEVERS:
                for debug in False, True:
                    for sysconfig in False, True:
                        for bits in BITS:
                            if pyver == "system" and bits != 64: continue
                            if sysconfig and bits != 64: continue
                            print(f"Python { pyver } { bits }bit  SQLite { sqlitever }  debug { debug } sysconfig { sysconfig }")
                            workdir = os.path.abspath(
                                os.path.join(topworkdir,
                                            "py%s-%d-sq%s%s%s" % (pyver, bits, sqlitever, "-debug" if debug else "", "-sysconfig" if sysconfig else "")))
                            logdir = os.path.abspath(
                                os.path.join("megatestresults",
                                            "py%s-%d-sq%s%s%s" % (pyver, bits, sqlitever, "-debug" if debug else "", "-sysconfig" if sysconfig else "")))
                            os.makedirs(logdir)
                            os.makedirs(workdir)
                            copy_git_files(workdir)
                            job = executor.submit(runtest,
                                                workdir=workdir,
                                                bits=bits,
                                                pyver=pyver,
                                                sqlitever=sqlitever,
                                                logdir=logdir,
                                                debug=debug,
                                                sysconfig=sysconfig)
                            job.info = f"py { pyver } sqlite { sqlitever } debug { debug } bits { bits } sysconfig { sysconfig }"
                            jobs.append(job)

        print(f"\nAll { len(jobs) } builds started, now waiting for them to finish ({ concurrency } concurrency)\n")
        start= time.time()
        for job in concurrent.futures.as_completed(jobs):
            print(job.info, "-> ", end="", flush=True)
            try:
                job.result()
                print("\t OK", flush=True)
            except Exception as e:
                print("\t FAIL", e, flush=True)

        print(f"\nFinished in { int(time.time() - start) } seconds")


def copy_git_files(destdir):
    for line in subprocess.run(["git", "ls-files"], text=True, capture_output=True, check=True).stdout.split("\n"):
        if not line:
            continue
        fn = line.split("/")
        if fn[0] in {".github", "doc"}:
            continue
        if len(fn) > 1:
            os.makedirs(os.path.join(destdir, "/".join(fn[:-1])), exist_ok=True)
        shutil.copyfile(line, os.path.join(destdir, line))


def getpyurl(pyver):
    dirver = pyver
    if 'a' in dirver:
        dirver = dirver.split('a')[0]
    elif 'b' in dirver:
        dirver = dirver.split('b')[0]
    elif 'rc' in dirver:
        dirver = dirver.split('rc')[0]

    
    p = 'P'
    ext = "xz"
    return "https://www.python.org/ftp/python/%s/%sython-%s.tar.%s" % (dirver, p, pyver, ext)


def buildpython(workdir, pyver, bits, logfilename):
    if pyver == "system": return "/usr/bin/python3", ""
    url = getpyurl(pyver)
    tarx = "J"
    run("set -e ; cd %s ; mkdir pyinst ; ( echo \"Getting %s\"; wget -q %s -O - | tar xf%s -  ) > %s 2>&1" %
        (workdir, url, url, tarx, logfilename))
    full = ""
    if sys.platform.startswith("linux"):
        ldflags = "LDFLAGS=\"-L/usr/lib/$(dpkg-architecture -qDEB_HOST_MULTIARCH)\"; export LDFLAGS;"
    else:
        ldflags = ""
    run(f"set -e ; cd { workdir } ; cd Python-{ pyver } ; env CC='gcc -m{ bits }' ./configure --prefix={ workdir }/pyinst  >> { logfilename } 2>&1; make >>{ logfilename } 2>&1; make  install >>{ logfilename } 2>&1 ; make clean >/dev/null"
        )
    suf = "3"
    pybin = os.path.join(workdir, "pyinst", "bin", "python" + suf)
    return pybin, os.path.join(workdir, "pyinst", "lib")


def natural_compare(a, b):
    
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]

    return cmp(alphanum_key(a), alphanum_key(b))


def cmp(a, b):
    if a < b:
        return -1
    if a > b:
        return +1
    assert a == b
    return 0



PYVERS = (
    '3.12.0a2',
    '3.11.0',
    '3.10.8',
    '3.9.14',
    '3.8.14',
    '3.7.14',
    '3.6.15',
    'system',
)

SQLITEVERS = ('3.39.0', '3.39.1', '3.39.2', '3.39.3', '3.39.4', '3.40.0')

BITS = (64, 32)

if __name__ == '__main__':
    nprocs = 0
    try:
        
        for line in open("/proc/cpuinfo", "rt"):
            line = line.split()
            if line and line[0] == "processor":
                nprocs += 1
    except:
        pass
    
    if nprocs == 0:
        nprocs = 1

    concurrency = nprocs * 2
    if concurrency > 24:
        concurrency = 24

    parser = argparse.ArgumentParser()
    parser.add_argument("--pyvers",
                        help="Which Python versions to test against [%(default)s]",
                        default=",".join(PYVERS))
    parser.add_argument("--sqlitevers",
                        dest="sqlitevers",
                        help="Which SQLite versions to test against [%(default)s]",
                        default=",".join(SQLITEVERS))
    parser.add_argument("--bits", default=",".join(str(b) for b in BITS), help="Bits [%(default)s]")
    parser.add_argument("--tasks",
                        type=int,
                        dest="concurrency",
                        help="Number of simultaneous builds/tests to run [%(default)s]",
                        default=concurrency)

    options = parser.parse_args()

    pyvers = options.pyvers.split(",")
    sqlitevers = options.sqlitevers.split(",")
    bits = tuple(int(b.strip()) for b in options.bits.split(","))
    concurrency = options.concurrency
    sqlitevers = [x for x in sqlitevers if x]
    main(pyvers, sqlitevers, bits, concurrency)
