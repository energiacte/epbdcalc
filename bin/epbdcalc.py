#!/usr/bin/env python
# encoding: utf-8
# 
# Copyright (c) 2015 Ministerio de Fomento
#                    Instituto de Ciencias de la Construcción Eduardo Torroja (IETcc-CSIC)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Cálculo de la eficiencia energética de los edificios según ISO/DIS 52000-1:2005"""

import os, sys
import warnings

if not hasattr(sys, 'frozen'):
    currpath = os.path.abspath(os.path.dirname(__file__))
    upperpath = os.path.abspath(os.path.join(currpath, '..'))
    sys.path.append(upperpath)
else:
    currpath, upperpath = None, None
    warnings.simplefilter('ignore')

import pyepbd as ep
import pandas as pd

COPY = u"""\tversión: %s
\t(c) 2015 Ministerio de Fomento
\t    2015 Instituto de Ciencias de la Construcción Eduardo Torroja (IETcc-CSIC)
\tAutores: Daniel Jiménez González <danielj@ietcc.csic.es>
\t         Rafael Villar Burke <pachi@ietcc.csic.es>
""" % ep.__version__

if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(description=u'Cálculo de la eficiencia energética según ISO/DIS 52000-1:2015 y CTE DB-HE',
                                     usage=u"%(prog)s [-h] [-f [FPFILE]] [--krdel [KRDEL]] [--kexp [KEXP]] vecfile\n\n" + COPY,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(dest='vecfile', nargs='?',
                        type=argparse.FileType('r'),
                        help=u'archivo de datos de los vectores energéticos')
    parser.add_argument('-f', '--factores', dest='fpfile', nargs='?',
                        type=argparse.FileType('r'), default=None,
                        help=u'archivo de definición de los factores de paso')
    parser.add_argument('--krdel', nargs='?', default=None, type=float,
                        help=u'factor de resuministro (k_rdel)')
    parser.add_argument('--kexp', nargs='?', default=None, type=float,
                        help=u'factor de exportacion (k_exp)')
    parser.add_argument('-o', '--outfile', dest='outputfile', nargs='?',
                        type=argparse.FileType('w'), default=None,
                        help=u'archivo de salida de resultados')
    args = parser.parse_args()

    if not args.vecfile:
        parser.print_help()
        sys.exit(2)

    if args.krdel is None:
        print u'Usando factor de resuministro (k_rdel) predeterminado'
    k_rdel = ep.K_RDEL if args.krdel is None else args.krdel

    if args.kexp is None:
        print u'Usando factor de exportación (k_exp) predeterminado'
    k_exp  = ep.K_EXP if args.kexp is None else args.kexp

    if args.fpfile:
        fpdatafile = args.fpfile
        print u'Archivo de factores de paso: ', fpdatafile.name, '\n'
    else:
        fpdatafile = None
        print u'Usando factores de paso predeterminados'
    fP = (ep.FACTORESDEPASOOFICIALES if args.fpfile is None
          else ep.readfactors(args.fpfile))

    EP = ep.calcula_eficiencia_energetica(args.vecfile.name, k_rdel, fP, k_exp)

    cadenasalida = ['Archivo de entrada: %s\n' % args.vecfile.name,
                    ep.formatIndicators(EP)]
    print ''.join(cadenasalida)

    if args.outputfile:
        print 'Guardando resultados en el archivo:', args.outputfile.name
        args.outputfile.writelines(cadenasalida)
