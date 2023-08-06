#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Jake Cui
# Mail: hbucqp1991@sina.cn
# Created Time:  2022-02-10 19:17:34
#############################################


from setuptools import setup, find_packages

requirements = [
    'numpy', 'pandas', 'setuptools'
]


setup(
    name="restidy",
    version="0.1.0",
    keywords=("pip", "wgs", "resfinder"),
    description="resfinder result tidy",
    long_description="Organize resfinder result to tabluar format",
    license="MIT Licence",

    url="https://github.com/hbucqp/restidy",
    author="Jake Cui",
    author_email="hbucqp1991@sina.cn",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=requirements,
)
