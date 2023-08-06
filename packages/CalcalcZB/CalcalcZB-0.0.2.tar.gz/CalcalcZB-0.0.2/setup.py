#!/usr/bin/env python
import sys
from setuptools import setup

VERSION = '0.0.2'
DESCRIPTION = "AY250 HW3: evaluate numeric string expressions."

CLASSIFIERS = list(filter(None, map(str.strip,
"""
Development Status :: 2 - Pre-Alpha
Intended Audience :: Education
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Topic :: Scientific/Engineering
""".splitlines())))

setup(
        name="CalcalcZB",
        version=VERSION,
        description=DESCRIPTION,
        long_description=DESCRIPTION,
        long_description_content_type="text/x-rst",
        classifiers=CLASSIFIERS,
        author="Zuzanna Balewski",
        author_email="balewski@berkeley.edu",
        url="https://github.com/zbalewski/python-ay250-homework/tree/main/hw_3",
        python_requires='>=3',
        license="MIT",
        packages=['calcalc', 'calcalc.tests'],
        platforms=['any'],
        setup_requires=['pytest-runner'],
        tests_require=['pytest'],
        install_requires=['numexpr', 'urllib3', 'requests']
)
