#!/usr/bin/env python
#encoding: utf-8
#
#   Programa epbdcalc: Cálculo de la eficiencia energética EN 15603
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
"""Configuración de epbdcalc para generar ejecutable en win32 con cx_freeze

$ python setup.py build
"""

import os, sys
from glob import glob
from cx_Freeze import setup, Executable
from pyepbd import __version__

## Create the list of includes as cx_freeze likes
include_files = []

## Let's add data dirs from pyepbd
pats = ['data/*.csv']
staticfiles = ['Manual_epbdcalc.pdf',
               'README.rst',
               'NEWS.txt',
               'HACKING.txt',
               'LICENSE.txt',
               'LICENSE_ES.txt',
               'CONTRIBUTORS.txt'
]
include_files.extend(ff for ffpat in pats for ff in glob(ffpat))
for ff in staticfiles:
    include_files.append(ff)

base = None

## Lets not open the console while running the app
#if sys.platform == "win32":
#    base = "Win32GUI"

executables = [
    Executable("bin/epbdcalc.py",
               base=None
    )
]

buildOptions = dict(
    compressed=False,
    #includes=["gi"],
    excludes=["Tkinter", "tcl", "PyQt5", "_ssl", "doctest", "ssl", "PIL", "gi", "matplotlib", "glib", "gio", "gtk", "cairo", "gobject"],
    #packages=["gi"],
    include_files=include_files,
    #bin_excludes=['gtk._gdk.pyd', 'gdiplus.dll'],
    icon='res/epbdcalc.ico',
    silent=True
    )

README = open('README.rst').read()
NEWS = open('NEWS.txt').read()
setup(
    name="epbdcalc",
    author="Rafael Villar Burke, Daniel Jiménez González",
    author_email='pachi@ietcc.csic.es',
    version=__version__,
    description="Cálculo de la eficiencia energética según EN 15603",
    long_description=README + '\n\n' + NEWS,
    options=dict(build_exe=buildOptions),
    executables=executables,
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Natural Language :: Spanish',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering'],
    keywords=u"energía,edificación,CTE",
    url="http://www.ietcc.csic.es/",
    license="GPL-2.0+"
)
