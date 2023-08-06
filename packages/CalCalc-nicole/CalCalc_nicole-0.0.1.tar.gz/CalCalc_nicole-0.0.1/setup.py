#!/usr/bin/env python
import sys
from setuptools import setup

VERSION = '0.0.1'
DESCRIPTION = "Calculator, locally or using Wolfram API"

CLASSIFIERS = list(filter(None, map(str.strip,
"""
Development Status :: 2 - Pre-Alpha
Intended Audience :: Education
License :: OSI Approved :: BSD License
Programming Language :: Python
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: Implementation :: CPython
Topic :: Software Development :: Libraries :: Python Modules
""".splitlines())))

setup(
        name="CalCalc_nicole",
        version=VERSION,
        description=DESCRIPTION,
        long_description=DESCRIPTION,
        long_description_content_type="text/x-rst",
        classifiers=CLASSIFIERS,
        author="Nicole Greene",
        author_email="nsgreene@berkeley.edu",
        url="http://github.com/NicoleGreene/python-ay250-homeworks/NicoleGreene_hw3",
        python_requires='>=3',
        license="BSD",
        keywords='sample setuptools eduction data-science',
        packages=['CalCalc'],
        platforms=['any'],
        setup_requires=['pytest-runner'],
        tests_require=['pytest']
)