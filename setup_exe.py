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
"""Configuración de epbdcalc para generar ejecutable en win32 con cx_freeze

$ python setup.py build
"""

import os, sys, codecs, re
from glob import glob
from cx_Freeze import setup, Executable

def find_version(*file_paths, **kwargs):
    with codecs.open(os.path.join(os.path.dirname(__file__), *file_paths),
                     encoding=kwargs.get("encoding", "utf8")) as fp:
        version_file = fp.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

## Create the list of includes as cx_freeze likes
include_files = []

## Let's add data dirs from pyepbd
pats = ['pyepbd/examples/*.csv']
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

executables = [Executable("bin/epbdcalc.py",
                          base=None,
                          targetName="epbdcalc.exe")]

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
    name="pyepbd",
    author="Rafael Villar Burke, Daniel Jiménez González",
    author_email='pachi@ietcc.csic.es',
    version=find_version("pyepbd", "__init__.py"),
    description="Cálculo de la eficiencia energética según ISO/DIS 52000-1:2015",
    long_description=README + '\n\n' + NEWS,
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
    options=dict(build_exe=buildOptions),
    executables=executables,
)
