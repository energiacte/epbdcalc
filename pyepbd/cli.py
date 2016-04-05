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

import argparse
import sys
from .settings import K_EXP, K_RDEL, FACTORESDEPASOOFICIALES
from .energycalculations import weighted_energy
from .inputoutput import readenergyfile, readfactors, ep2string

def main():
    from .__init__ import __version__
    COPY = u"""\tversión: %s
\t(c) 2015-2016 Ministerio de Fomento
\t    2015-2016 Instituto de Ciencias de la Construcción Eduardo Torroja (IETcc-CSIC)
\tAutores: Daniel Jiménez González <danielj@ietcc.csic.es>
\t         Rafael Villar Burke <pachi@ietcc.csic.es>
""" % __version__
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
        print(u'Usando factor de resuministro (k_rdel) predeterminado')
    k_rdel = K_RDEL if args.krdel is None else args.krdel

    if args.kexp is None:
        print(u'Usando factor de exportación (k_exp) predeterminado')
    k_exp  = K_EXP if args.kexp is None else args.kexp

    if args.fpfile:
        fpdatafile = args.fpfile
        print(u'Archivo de factores de paso: ', fpdatafile.name, '\n')
    else:
        fpdatafile = None
        print(u'Usando factores de paso predeterminados')
    fP = (FACTORESDEPASOOFICIALES if args.fpfile is None
          else readfactors(args.fpfile))

    data = readenergyfile(args.vecfile.name)
    EP = weighted_energy(data, k_rdel, fP, k_exp)

    cadenasalida = ['%s\n' % args.vecfile.name,
                    ep2string(EP)]
    print(''.join(cadenasalida))

    if args.outputfile:
        print('Guardando resultados en el archivo:', args.outputfile.name)
        args.outputfile.writelines(cadenasalida)

if __name__ == '__main__':
    main()
