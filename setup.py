#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


from setuptools import setup, find_packages, findall
from os.path import abspath, join

def not_py(file_path):
    return not(file_path.endswith('.py') or file_path.endswith('.pyc'))

core_packages = find_packages()
core_package_data = {}
for package in core_packages:
    package_path = package.replace('.', '/')
    core_package_data[package] = filter(not_py, findall(package_path))



setup(
    name="fabric-recipes",
    version="0.3.1",
    author="Marcos Daniel Petry",
    author_email="marcospetry@gmail.com",
    description=("quick solution to perform deploy a Django app using nginx and gunicorn"),
    license="BSD",
    keywords="fabric django gunicorn deploy",
    url="https://github.com/petry/fabric-recipes/",
    packages=core_packages,
    package_data=core_package_data,
    include_package_data=True,
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
