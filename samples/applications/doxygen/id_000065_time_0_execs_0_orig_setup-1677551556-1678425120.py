# Copyright 2018 The trfl Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or  implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Setup for pip package."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ['six', 'absl-py', 'numpy', 'wrapt', 'dm-tree']
EXTRA_PACKAGES = {
    'tensorflow': [
        'tensorflow>=1.15', 'tensorflow-probability>=0.8'
    ],
    'tensorflow with gpu': [
        'tensorflow-gpu>=1.15', 'tensorflow-probability>=0.8'
    ],
}

setup(
    name='trfl',
    version='1.2.0',
    description=('trfl is a library of building blocks for '
                 'reinforcement learning algorithms.'),
    long_description='',
    url='http://www.github.com/deepmind/trfl/',
    author='DeepMind',
    author_email='trfl-steering@google.com',
    # Contained modules and scripts.
    packages=find_packages(),
    install_requires=REQUIRED_PACKAGES,
    extras_require=EXTRA_PACKAGES,
    # Add in any packaged data.
    include_package_data=True,
    zip_safe=False,
    # PyPI package information.
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries',
    ],
    license='Apache 2.0',
    keywords='trfl truffle tensorflow tensor machine reinforcement learning',
    test_suite='nose.collector',
    tests_require=['nose'],
)
