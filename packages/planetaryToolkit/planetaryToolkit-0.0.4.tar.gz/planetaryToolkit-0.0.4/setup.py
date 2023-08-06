#!/usr/bin/env python

import sys
from setuptools import setup

VERSION = '0.0.4'
DESCRIPTION = "Python tools for processing observations of solar system bodies; modeling tools for rings, planets, and moons"

CLASSIFIERS = list(filter(None, map(str.strip,
"""
Development Status :: 1 - Planning
Intended Audience :: Science/Research
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
        name="planetaryToolkit",
        version=VERSION,
        description=DESCRIPTION,
        long_description=DESCRIPTION,
        long_description_content_type="text/x-rst",
        classifiers=CLASSIFIERS,
        author="Ned Molter",
        author_email="emolter@berkeley.edu",
        url="https://github.com/emolter/planetaryToolkit",
        python_requires='>=3',
        license="BSD",
        keywords='planets astronomy moons ephemeris',
        packages=['ephem', 'ephem.tests'],
        platforms=['any'],
        setup_requires=['pytest-runner'],
        tests_require=['pytest']
)