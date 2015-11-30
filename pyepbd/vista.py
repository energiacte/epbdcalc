#!/usr/bin/python
# -*- coding: utf-8 -*-
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

import numpy as np

def verInd(EP, ver=True, texto=None):

    total = EP.EP['ren'] + EP.EP['nren']
    salida = []
    if texto:
        salida.append(texto + '\n')
    salida.append('EP           | EPpasoA\n')
    salida.append('ren ='+ str(round(EP.EP['ren'],1)).rjust(8)      +\
                '| ren ='+ str(round(EP.EPpasoA['ren'],1)).rjust(8) + '\n')
    salida.append('nren='+ str(round(EP.EP['nren'],1)).rjust(8)     +\
                '| nren='+ str(round(EP.EPpasoA['nren'],1)).rjust(8) +'\n')
    salida.append('tot ='+ str(round(total,1)).rjust(8)             +\
                '|\n')
    salida.append('RER ='+ str(round((EP.EP['ren']/total),2)).rjust(8) +\
                '|\n')
    #salida.append('----------------------------------------')
    if ver:
        print ''.join(salida)

    return salida

def ver_balance(balance):
    #import balance
    print '___balance___'
    for vector, datos_periodo in balance.items():
        print 'vector: ',vector
        for periodo, datos_fuentes in datos_periodo.items():
            print '  periodo:', periodo
            for fuente, usos in datos_fuentes.items():
                print '    fuente', fuente
                for uso, valor in usos.items():
                    print '      uso', uso, redondeo(valor)
    print '--------------'

def ver_datos_entrada(vector_data):
    print '___ vector data ____'
    for vector, balance_vector in vector_data.items():
        print 'vector: ',vector#, '\tclaves', balance_vector.keys()
        for fuente, usos in balance_vector['anual'].items():
            print '  fuente: ', fuente
            for uso, valor in usos.items():
                print '    uso', uso, redondeo(valor)
    print '--------------'


def redondeo(objeto, n=0):
    if (isinstance(objeto, list) or isinstance(objeto, np.ndarray)):
        if n == 0:
            return int(round(sum(objeto),n)),[int(round(e,n)) for e in objeto]
        else:
            return round(sum(objeto),n),[round(e,n) for e in objeto]
    elif isinstance(objeto, dict):
        salida = ['\n']
        for clave, valor in objeto.items():
            if isinstance(valor, float):
                salida.append('%s %.2f\n' % (clave, valor))
        return ''.join(salida)
            #print type(valor)
    elif isinstance(objeto, float):
        return round(objeto,n)
    else:
        print objeto
        return type(objeto),'no reconozco este tipo en la función redondeo'

