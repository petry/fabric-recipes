#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="fabric-recipes",
    version="0.2",
    author="Marcos Daniel Petry",
    author_email="marcospetry@gmail.com",
    description=("quick solution to perform deploy a Django app using nginx and gunicorn"),
    license="BSD",
    keywords="fabric django gunicorn deploy",
    url="https://github.com/petry/fabric-recipes/",
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=[
        'Fabric==1.6.0'
    ],
)
