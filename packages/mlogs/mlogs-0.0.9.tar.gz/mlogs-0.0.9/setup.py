#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/8 10:36 AM
# @Author  : chenDing
from setuptools import setup, find_packages

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


setup(
    name='mlogs',
    version='0.0.9',
    description='loguru packaging log tools',
    packages=find_packages(),
    author='Caturbhuja',
    author_email='caturbhuja@foxmail.com',
    url='',
    install_requires=[
       'loguru',
       'numpy',
    ],
    license='MIT'
)
