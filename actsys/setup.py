# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Intel Corp.
#
"""
Setup Module
"""
from setuptools import setup, find_packages

description = "A control component for exascale clusters"
author = "Intel Corporation"
license = "Apache"

setup(name='actsys',
      version='0.1.0',
      description=description,
      author=author,
      license=license,
      packages=find_packages(),
      scripts=['ctrl', 'actsys'],
      install_requires=['python-dateutil',
                        'ctrlsys-datastore',
                        'timeout-decorator',
                        'parallel-ssh',
                        'ipython'],
      test_suite='tests',
      tests_require=['pytest',
                     'pytest-cov',
                     'pylint',
                     'mock'])
