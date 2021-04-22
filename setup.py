#!/usr/bin/python

from setuptools import setup
import sys

if sys.version_info < (3,):
    raise RuntimeError("diterator requires Python 3 or higher")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='diterator',
    version="0.3.1",
    description='Iterator and wrapper for processing IATI activities.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='David Megginson',
    author_email='megginson@un.org',
    install_requires=[
        'requests>=2.11',
        'py-dom-xpath-six',
    ],
    packages=['diterator',],
    test_suite='tests',
)
