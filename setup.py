# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Intel Corp.
#
"""
Setup Module
"""
from setuptools import setup, find_packages

description = "A datastore for exascale clusters"
author = "Intel Corporation"
license = "Apache"
tests_require = ['python-dateutil>=2.6.0',
                 'pytz',
                 'coverage',
                 'pytest',
                 'pylint',
                 'mock']

setup(name='ctrlsys-datastore',
      version='0.2.0',
      description=description,
      author=author,
      license=license,
      packages=find_packages(),
      entry_points={
          'console_scripts': ['datastore = datastore.__main__:main']
      },
      install_requires=['psycopg2', 'python-dateutil>=2.6.0', 'pytz'],
      test_suite='tests',
      tests_require=tests_require,
      extras_require={
          'testing': tests_require
      })
