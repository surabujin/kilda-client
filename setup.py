#!/usr/bin/env python

import functools
import os
from setuptools import find_packages
import sys

from setuptools import setup

from kilda import client as app

root = os.path.dirname(__file__)
root = os.path.abspath(root)
root = os.path.normpath(root)

path = functools.partial(os.path.join, root)

run_deps = open(path('requirements.txt')).readlines()
test_deps = []
setup_deps = []

if {'pytest', 'test', 'ptr'}.intersection(sys.argv):
    setup_deps.append('pytest-runner')

setup(
    name='kilda-client',
    version=app.__version__,
    description='open-kilda python client',
    long_description=open(path('README.rst')).read(),
    packages=find_packages(),
    setup_requires=setup_deps,
    tests_require=test_deps,
    install_requires=run_deps)
