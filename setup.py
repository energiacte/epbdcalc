#!/usr/bin/env python
#encoding: utf-8
#
#   Programa epbdcalc: Cálculo de la eficiencia energética ISO/DIS 52000-1:2015
#
#   Copyright (C) 2015  Rafael Villar Burke <pachi@ietcc.csic.es>
#                       Daniel Jiménez González <danielj@ietcc.csic.es>
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 2
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
#   02110-1301, USA.
"""epbdcalc - Cálculo de la eficiencia energética según ISO/DIS 52000-1:2015

Based on the pypa setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
import codecs
import os.path
import re

from setuptools import setup, find_packages

def find_version(*file_paths, **kwargs):
    with codecs.open(os.path.join(os.path.dirname(__file__), *file_paths),
                     encoding=kwargs.get("encoding", "utf8")) as fp:
        version_file = fp.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

here = os.path.abspath(os.path.dirname(__file__))

README = codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8').read()
NEWS = codecs.open(os.path.join(here, 'NEWS.txt'), encoding='utf-8').read()

setup(
    name="pyepbd",
    author="Rafael Villar Burke, Daniel Jiménez González",
    author_email="pachi@ietcc.csic.es",
    version=find_version("pyepbd", "__init__.py"),
    description="Cálculo de la eficiencia energética según ISO/DIS 52000-1:2015",
    long_description=README + "\n\n" + NEWS,
    url="https://github.com/pachi/epbdcalc",
    license="MIT",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: Implementation :: CPython',

        # Environment
        'Environment :: Console',
        'Operating System :: OS Independent'
    ],
    keywords=[u"energía", u"edificación", u"CTE", u"energy", u"buildings"],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().

    packages=find_packages(),
    include_package_data = True,

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['pandas >= 0.15', 'numpy >= 1.7'],

    # dependencies for the setup script to run
    setup_requires=['pytest-runner'],

    # dependencies for the test command to run
    tests_require=['pytest', 'pytest-cov'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'test': ['pytest', 'pytest-cov'],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'epbdcalc=pyepbd.cli:main',
        ],},
)
