#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='TextColorized',
    packages=find_packages(),
    version='0.0.1',
    description='To make screen prints more colorful very easily, similar to the javascript console',
    long_description="To make screen prints more colorful very easily, similar to the javascript console."
                     "Easy to use, just importing 'console' and using any function of the class, examples: "
                     "header, assertion, fail and so on. and passing the text as parameter 'm='.",
    author='Horlando Leão',
    author_email='horlandojcleao.developer@gmail.com',
    url='https://github.com/Horlando-Leao/TextColorized',
    install_requires=[],
    license='MIT',
    keywords=['dev', 'script', 'text', 'print', 'color'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)