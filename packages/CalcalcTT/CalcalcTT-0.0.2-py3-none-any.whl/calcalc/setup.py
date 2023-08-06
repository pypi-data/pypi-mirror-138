#!/usr/bin/env python
import sys
from setuptools import setup

VERSION = '0.0.2'
DESCRIPTION = "AY250 HW3: evaluate string expressions with numexpr and Wolfram Alpha."

CLASSIFIERS = list(filter(None, map(str.strip,
"""
Development Status :: 2 - Pre-Alpha
Intended Audience :: Education
License :: OSI Approved :: BSD License
Programming Language :: Python
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Topic :: Scientific/Engineering
""".splitlines())))

setup(
        name="CalcalcTT",
        version=VERSION,
        description=DESCRIPTION,
        long_description=DESCRIPTION,
        long_description_content_type="text/x-rst",
        classifiers=CLASSIFIERS,
        author="Toby Turney",
        author_email="tobyturney151@gmail.com",
        url="https://github.com/tobyturney151/python-ay250-homework/tobyturney_hw_3",
        python_requires='>=2.7',
        license="Livense to Kill Some Strings",
        packages=['calcalc', 'calcalc.tests'],
        platforms=['any'],
        setup_requires=['pytest-runner'],
        tests_require=['pytest'],
        install_requires=['numexpr', 'urllib.request', 'argparse','math']
)