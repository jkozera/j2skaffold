# -*- coding: utf-8 -*-
"""setup.py"""

import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

class Tox(TestCommand):
    user_options = [('tox-args=', 'a', 'Arguments to pass to tox')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex
        if self.tox_args:
            errno = tox.cmdline(args=shlex.split(self.tox_args))
        else:
            errno = tox.cmdline(self.test_args)
        sys.exit(errno)


def read_content(filepath):
    with open(filepath) as fobj:
        return fobj.read()


classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]


long_description = (
    read_content("README.rst") +
    read_content(os.path.join("docs/source", "CHANGELOG.rst")))

requires = ['setuptools', 'jinja2>=2.10', 'pyyaml>=3.13']

extras_require = {
    'reST': ['Sphinx'],
    }
if os.environ.get('READTHEDOCS', None):
    extras_require['reST'].append('recommonmark')

setup(name='j2skaffold',
      version='0.1.0',
      description='Simple wrapper around skaffold for rendering skaffold.yaml',
      long_description=long_description,
      author='Jerzy Kozera',
      author_email='jerzy.kozera@gmail.com',
      url='https://github.com/jkozera/j2skaffold',
      classifiers=classifiers,
      packages=['j2skaffold'],
      data_files=[],
      install_requires=requires,
      include_package_data=True,
      extras_require=extras_require,
      tests_require=['tox'],
      cmdclass={'test': Tox},
      entry_points={
          'console_scripts': ['j2skaffold=j2skaffold.cli:main'],
      })
