#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Basile Marchand"
__version__ = "0.1"
contact = "basile.marchand@mines-paristech.fr"
name = "wnm"

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
from codecs import open
from os import path

here = os.path.abspath( path.dirname( __file__ ) )

with open( os.path.join( here, 'README.rst'), encoding="utf-8") as f:
    long_description = f.read()


### List additionnal file to embedd in the package
datadir = os.path.join('share','data')
datafiles = [(d, [os.path.join(d,f) for f in files])
    for d, folders, files in os.walk(datadir)]

setup( 
    name = name,
    version = __version__,
    author_email = contact,
    description='',
    long_description=long_description,
    license='LGPL',
    url="",
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 1 - Beta',
        'Natural Language :: English',
        'Framework :: Sphinx, Qt'
    ],
    install_requires=["pyqt>=5.*",
                      "sphinx>=1.8.1",
                      "traitlets",
                      "pyyaml"],
    scripts=['bin/wnm',],
    packages=[name],
    include_package_data=True,
    data_files = datafiles,
)

