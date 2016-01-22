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
import pandas as pd

def calcular_balance_vector(E_EPB, E_nEPB, E_prod, k_rdel):

    if isinstance(E_prod, dict):
        E_prod_tot = sum(E_prod.values()) #element wise
    else:
        E_prod_tot = E_prod

    if isinstance(E_nEPB, dict):
        E_nEPB = sum(E_nEPB.values())

    E_EPB_t = np.minimum(E_EPB, E_prod_tot) #element wise

    #____exportable___
    exportable = E_prod_tot - E_EPB_t
    factor_exportable_producido = [1-E_EPB_t[n]/e if e != 0 else 0 for n, e in enumerate(E_prod_tot)]
    if isinstance(E_prod, dict):
        E_exportable_source = {} #es directamente lo producido en cada source por el factor exportable
        for source, values in E_prod.items():
            E_exportable_source[source] = values * factor_exportable_producido

    #___nEPB_____
    E_nEPB_used_t = np.minimum(exportable, E_nEPB) # linea 26
    factor_nEPB_exportable = [E_nEPB_used_t[n]/e if e != 0 else 0 for n, e in enumerate(exportable)]
    # podemos asociarlo a cada uno de los productores
    if isinstance(E_prod, dict):
        E_nEPB_source = {}
        for source, values in E_exportable_source.items():
            E_nEPB_source[source] = values * factor_nEPB_exportable

    # ____exceso ___
    exceso_t = E_prod_tot - E_EPB_t - E_nEPB_used_t #linea 32
    exceso = np.sum(exceso_t)
    # porcentaje de la exportable que es exceso (no va a nEPB)
    # el exceso se minora con k_rdel para ser resuministrado
    # y luego con k_exp para ser exportado
    factor_exceso_exportable = [exceso_t[n]/e if e != 0 else 0 for n, e in enumerate(exportable)] #linea 33
    if isinstance(E_prod, dict):
        E_exceso_source = {}
        for source, values in E_exportable_source.items():
            E_exceso_source[source] = values * factor_exceso_exportable

    #_______ EPB no cubierto _____
    E_EPB_unfilled_t = E_EPB - E_EPB_t
    E_EPB_unfilled = np.sum(E_EPB_unfilled_t)

    #_______ resuministrada _____
    #maxima_rdel_paso = k_rdel * E_EPB_unfilled #en caso de que haya producción
    maxima_rdel = min(E_EPB_unfilled, exceso) #línea 40
    E_rdel_total = k_rdel * maxima_rdel # resuministrable permitida
    # la resuministrada se puede ver desde el punto de vista de la producción,
    # cuando se recoge esa energía, o desde el punto de vista del consumo,
    # cunado se sirve esa energía recogida. El total es el mismo, pero los valores
    # temporales varían.
    factor_resuministrada_producida = E_rdel_total / exceso
    if isinstance(E_prod, dict):
        E_rdel_source = {}
        for source, values in E_exceso_source.items():
            E_rdel_source[source] = values * factor_resuministrada_producida

    E_rdel_t = factor_resuministrada_producida * exceso_t
    factor_unfilled_rdel = E_rdel_total / E_EPB_unfilled

    E_rdel_servida_t = factor_unfilled_rdel * E_EPB_unfilled_t

    # ___ energía suministrada por la red ____
    E_del_grid = sum(E_EPB) - sum(E_EPB_t) - sum(E_rdel_t)
    E_del_grid_t = E_EPB - E_EPB_t - E_rdel_servida_t
    E_exp_grid = exceso - E_rdel_total
    # hay que repercutirlo por combustible
    prop_exceso_red = E_exp_grid / exceso if exceso != 0 else 0
    if isinstance(E_prod, dict):
        E_exp_grid_source = {}
        for clave, valor in E_exceso_source.items(): #exceso por fuente
            E_exp_grid_source[clave]= prop_exceso_red * valor
        E_exp_grid_t = sum(E_exp_grid_source.values())
    else:
        E_exp_grid_t = np.zeros(len(E_EPB))

    balance_temporal = {'grid': {'input': sum(E_del_grid_t)}}
    if isinstance(E_prod, dict):
        for source in E_prod:
            srcenergy = {'input': E_prod[source],
                         'to_nEPB': E_nEPB_source[source],
                         'to_grid': E_exp_grid_source[source]}
            balance_temporal[source] = srcenergy

    balance_anual = {}
    for source, uses in balance_temporal.items():
        balance_anual[source] = {}
        for use, value in uses.items():
            if abs(value.sum()) > 0.1:
                balance_anual[source][use] = value.sum()

    return balance_anual, balance_temporal


def readdata(filename):
    """Read input data from filename

    vector, atype, srcdst, (values ...)
    """
    with open(filename, 'r') as datafile:
        lines = datafile.readlines()

    data = {}
    nvalues = False
    for line in lines[1:]:
        fields = line.split(',')
        vector, atype, srcdst = fields[0:3]
        values = np.array([float(e.strip('\n')) for e in fields[3:]])
        
        if not nvalues:
            nvalues = len(values)
        else:
            if nvalues != len(values):
                print '___error___', 'hay un vector con un número de datos erróneo'
                print vector, atype, srcdst, values
                #TODO: raise exception and handle in CLI

        if vector not in data:
            data[vector] = {}

        if atype not in data[vector]:
            data[vector][atype] = {}

        atypedata = data[vector][atype]
        if srcdst not in atypedata:
            atypedata[srcdst] = np.zeros(nvalues)
        atypedata[srcdst] = atypedata[srcdst] + values
    return nvalues, data

def calcular_balance(filename, k_rdel):
    nsteps, data = readdata(filename)
    balance = {}
    for vector in data:
        atypes = data[vector]
        consumo_EPB = pd.Series(atypes['CONSUMO']['EPB']) if 'CONSUMO' in atypes and 'EPB' in atypes['CONSUMO'] else np.zeros(nsteps)
        consumo_nEPB = pd.Series(atypes['CONSUMO']['NEPB']) if 'CONSUMO' in atypes and 'NEPB' in atypes['CONSUMO'] else np.zeros(nsteps)
        produccion = atypes['PRODUCCION'] if 'PRODUCCION' in atypes else np.zeros(nsteps)
        # produccion es un diccionario con las fuentes
        bal_an, bal_t = calcular_balance_vector(consumo_EPB, consumo_nEPB, produccion, k_rdel)
        balance[vector] = {'anual': bal_an, 'temporal': bal_t}
    return balance

