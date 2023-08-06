#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/4/28 4:39 下午
# @File    : setup.py.py
# @author  : Bai
from setuptools import setup, find_packages
reqs = [
]

setup(
    name='chain-processors-framework',
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    package_dir={'': '.'},
    url='https://github.com/byscut/chain-processors-framework.git',
    license='MIT',
    author='byscut',
    author_email='byscut@foxmail.com',
    zip_safe=True,
    description='coding with a chain framework',
    install_requires=reqs
)

