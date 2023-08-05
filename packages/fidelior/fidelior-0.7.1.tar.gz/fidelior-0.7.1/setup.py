#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIDELIOR (c) by Nikolai G. Lehtinen

FIDELIOR is licensed under a
Creative Commons Attribution-NoDerivatives 4.0 International License.

You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by-nd/4.0/>.
"""

from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='fidelior',
    version='0.7.1',
    license='CC BY-ND 4.0',
    author="Nikolai G. Lehtinen",
    author_email='nlehtinen@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://gitlab.com/nleht/fidelior',
    description='FIDELIOR: FInite-Difference-Equation LInear OperatoR package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='fInite-difference equations, partial differential equations',
    install_requires=[
          'numpy>=1.14.0', 'scipy>=1.0.0'
      ],
)