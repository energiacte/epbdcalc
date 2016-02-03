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

"""Auxiliary module to create output files"""

import os
import numpy as np

currpath = os.path.abspath(os.path.dirname(__file__))
upperpath = os.path.abspath(os.path.join(currpath, '..'))

VALIDCARRIERS = ['ELECTRICIDAD', 'ELECTRICIDADCANARIAS', 'ELECTRICIDADBALEARES',
                 'ELECTRICIDADCEUTAMELILLA', 'GASOLEO', 'FUELOIL', 'GLP',
                 'GASNATURAL', 'CARBON', 'BIOMASA', 'BIOMASADENSIFICADA',
                 'BIOCARBURANTE', 'MEDIOAMBIENTE', 'COGENERACION']
VALIDCTYPES = ['CONSUMO', 'PRODUCCION']
VALID_ORIGINORUSE = ['EPB', 'NEPB', 'INSITU', 'COGENERACION']

def perfilC(valortotal):
    perfil = np.array([0.1639344262, 0.1311475410, 0.0819672131, 0.0737704918, 0.0409836066, 0.0491803279, 0.0655737705, 0.0573770492, 0.0409836066, 0.0655737705, 0.0983606557, 0.1311475410])
    return float(valortotal) * perfil

def perfilP1(valortotal):
    perfil = np.array([0.0283687943, 0.0354609929, 0.0496453901, 0.0709219858, 0.12056737590, 0.134751773, 0.1418439716, 0.1276595745, 0.1134751773, 0.0851063830, 0.0567375887, 0.0354609929])
    return float(valortotal) * perfil

def perfilP2(valortotal):
    perfil = np.array([0.0851063830, 0.0567375887, 0.0354609929, 0.0283687943, 0.0354609929, 0.0496453901, 0.0709219858, 0.1205673759, 0.1347517730, 0.1418439716, 0.1276595745, 0.1134751773])
    return float(valortotal) * perfil

def createfile(nombre_fichero, data):
    with open(nombre_fichero, 'w') as f:
        f.writelines('vector,tipo,src_dst\n')
        if data is not None:
            datalines = []
            for carrier, ctype, originoruse, values in data:
                if carrier not in VALIDCARRIERS:
                    print u'__error__ no reconozco a %s como vector, no está en la lista' % carrier, VALIDCARRIERS
                if ctype not in VALIDCTYPES:
                    print u'__error__ no reconozco a %s como tipo, no está en la lista' % ctype, VALIDCTYPES
                if originoruse not in VALID_ORIGINORUSE:
                    print u'__error__ no reconozco a %s como fuente/destino, no está en la lista' % originoruse, VALID_ORIGINORUSE
                if isinstance(values, int):
                    values = [values]
                datalines.append('%s,%s,%s,' % (carrier, ctype, originoruse) + ','.join(['%.2f' % e for e in values]) + '\n')
            f.writelines(datalines)

if __name__ == "__main__":
    createfile(os.path.join(currpath, 'ejemplo1base.csv'),
               data=[('ELECTRICIDAD','CONSUMO', 'EPB', perfilC(100))])

    createfile(os.path.join(currpath, 'ejemplo1PV.csv'),
               [('ELECTRICIDAD','CONSUMO', 'EPB', perfilC(100)),
                ('ELECTRICIDAD','PRODUCCION', 'INSITU', perfilC(50))])

    createfile(os.path.join(currpath, 'ejemplo1xPV.csv'),
               [('ELECTRICIDAD','CONSUMO', 'EPB', perfilC(100)),
                ('ELECTRICIDAD','PRODUCCION', 'INSITU', perfilC(140))])

    createfile(os.path.join(currpath, 'ejemplo1xPV.csv'),
               [('ELECTRICIDAD','CONSUMO', 'EPB', perfilC(100)),
                ('ELECTRICIDAD','PRODUCCION', 'INSITU', perfilC(140))])

    createfile(os.path.join(currpath, 'ejemplo2xPVgas.csv'),
               [('ELECTRICIDAD','CONSUMO', 'EPB', perfilC(20)),
                ('ELECTRICIDAD','PRODUCCION','INSITU', perfilP1(40)),
                ('GASNATURAL','CONSUMO',  'EPB', perfilC(190))])

    createfile(os.path.join(currpath, 'ejemplo3PVBdC.csv'),
               [('ELECTRICIDAD','CONSUMO', 'EPB', perfilC(59)),
                ('ELECTRICIDAD','PRODUCCION','INSITU', perfilP1(40)),
                ('MEDIOAMBIENTE','CONSUMO',   'EPB', perfilC(131)),
                ('MEDIOAMBIENTE','PRODUCCION','INSITU', perfilC(131))])

    createfile(os.path.join(currpath, 'ejemplo4cgnfosil.csv'),
               [('GASNATURAL','CONSUMO',  'EPB', perfilC(100)),
                ('GASNATURAL','CONSUMO',  'EPB', perfilC(158)),
                ('ELECTRICIDAD','PRODUCCION','COGENERACION', perfilP1(28))])

    createfile(os.path.join(currpath, 'ejemplo5cgnbiogas.csv'),
               [('GASNATURAL','CONSUMO', 'EPB', perfilC(100)),
                ('BIOCARBURANTE','CONSUMO', 'EPB', perfilC(158)),
                ('ELECTRICIDAD','PRODUCCION','COGENERACION', perfilP1(28))])

    createfile(os.path.join(currpath, 'ejemplo6K3.csv'),
               [('ELECTRICIDAD','CONSUMO', 'EPB', [200,160,100,90,50,60,80,70,50,80,120,160]),
                ('ELECTRICIDAD','CONSUMO', 'NEPB', np.ones(12) * 30),
                ('ELECTRICIDAD','PRODUCCION', 'INSITU', [44,55,77,110,187,209,220,198,176,132,88,55])])
