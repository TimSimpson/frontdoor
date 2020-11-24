#!/usr/bin/env python
import os

import setuptools


ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)))
with open(os.path.join(ROOT, 'README.md')) as file:
    description = file.read()


setuptools.setup(
    name='frontdoor',
    version='0.1.5',
    description='Aids the creation of "front door" scripts.',
    long_description="""
This simple module aids in the creation of "front door" scripts, which
can help organize automated scripts and reduce the need for overly
verbose docs.

See `the git repo
<https://github.com/TimSimpson/frontdoor>`_ for more info.
    """,
    author='Tim Simpson',
    license='MIT',
    packages=['frontdoor'],
    package_data={
        "": ["py.typed", "*.pyi"],
    }
)
