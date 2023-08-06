#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: xingming
# Mail: huoxingming@gmail.com
# Created Time:  2015-12-11 01:25:34 AM
#############################################


from setuptools import setup, find_packages

setup(
    name = "cw_sumtool",
    version = "0.1.1",
    keywords = ("add"),
    description = "add tool",
    long_description = "add tool",
    license = "MIT Licence",

    author = "jack_chen",
    author_email = "1390212397@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)