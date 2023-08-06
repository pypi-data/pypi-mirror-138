#!/usr/bin/env python

from io import open
from setuptools import setup

'''
:authors: Deuqz
'''

version = '1.0'

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
    long_description_content_type='text/markdown',

    url='https://github.com/Deuqz/hw_python_show_graph_lib',
    download_url='https://github.com/Deuqz/hw_python_show_graph_lib/archive/v{}.zip'.format(version),

    packeges=['hw_python_show_graph_lib'],
    # install_requires['networkx', 'matplotlib'],

    classifiers=[
        'Programming Language :: Python'
    ]
)
