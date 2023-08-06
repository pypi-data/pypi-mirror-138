#!/usr/bin/env python

from setuptools import find_packages,setup

version = '3.0'

long_description = '''Python module for hw1 that shows graph of fib function'''

setup(
    name='hw_python_show_graph_lib',
    version=version,

    author='Deuqz',
    author_email='ddemon2002@mail.ru',

    description=(
        u'Python module for showing graph'
    ),
    long_description=long_description,

    url='https://github.com/Deuqz/hw_python_show_graph_lib',
    
    packages = find_packages()
)
