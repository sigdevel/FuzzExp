



















"""
Run all test suites
"""

import os
import unittest
import sys
import tempfile
import shutil


if __name__ == '__main__':
    testdir = tempfile.mkdtemp(prefix='TestAll '+__name__)
    os.environ['BLEACHBIT_TEST_OPTIONS_DIR'] = testdir
    
    print("""You should use the unittest discovery, it's much nicer:
    python -m unittest discover -p Test*.py                       
    python -m unittest tests.TestCLI                              
    python -m unittest tests.TestCLI.CLITestCase.test_encoding    """)
    suite = unittest.defaultTestLoader.discover(
        os.getcwd(), pattern='Test*.py')
    success = unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    
    del os.environ['BLEACHBIT_TEST_OPTIONS_DIR']
    if os.path.exists(testdir):
        shutil.rmtree(testdir)
    
    sys.exit(success == False)
