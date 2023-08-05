#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="maue-parser",
    version="0.1.1",
    author="Calvin Neumann",
    description="parser for maue files version 1.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/code-and-fire/maue-parser",
    license="GNU Affero General Public License, Version 3",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
    ]
)