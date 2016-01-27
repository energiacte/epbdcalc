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

def get_temp_balance_forvector(vdata, k_rdel):

    E_EPB = vdata['CONSUMO']['EPB']
    E_nEPB = vdata['CONSUMO']['NEPB']
    E_prod = vdata['PRODUCCION']
    
    E_prod_tot = np.sum(E_prod.values(), axis=0) # total for each step from all origins
    E_EPB_t = np.minimum(E_EPB, E_prod_tot) # minimum for each step

    #____exportable___
    exportable = E_prod_tot - E_EPB_t
    factor_exportable_producido = np.array([1 - E_EPB_t[n] / e if e != 0 else 0 for n, e in enumerate(E_prod_tot)])
    E_exportable_bysource = {source: E_prod[source] * factor_exportable_producido for source in E_prod}

    #___nEPB_____
    E_nEPB_used_t = np.minimum(exportable, E_nEPB)
    factor_nEPB_exportable = [E_nEPB_used_t[n] / e if e != 0 else 0 for n, e in enumerate(exportable)]
    E_nEPB_bysource = {source: E_exportable_bysource[source] * factor_nEPB_exportable for source in E_exportable_bysource}

    # ____exceso ___
    # parte de la exportable que no va a nEPB
    # esa energía se minora con k_rdel para su resuministro y con k_exp para su exportación
    exceso_t = E_prod_tot - E_EPB_t - E_nEPB_used_t
    exceso = np.sum(exceso_t)
    factor_exceso_exportable = np.array([exceso_t[n] / e if e != 0 else 0 for n, e in enumerate(exportable)])
    E_exceso_bysource = {source: E_exportable_bysource[source] * factor_exceso_exportable for source in E_exportable_bysource}

    #_______ EPB no cubierto _____
    E_EPB_unfilled_t = E_EPB - E_EPB_t
    E_EPB_unfilled = np.sum(E_EPB_unfilled_t)

    #_______ resuministrada _____
    # la resuministrada se puede ver desde el punto de vista de la producción,
    # cuando se recoge esa energía, o desde el punto de vista del consumo,
    # cunado se sirve esa energía recogida. El total es el mismo, pero los valores
    # temporales varían.
    maxima_rdel = min(E_EPB_unfilled, exceso)
    E_rdel_total = k_rdel * maxima_rdel # resuministrable permitida
    factor_resuministrada_producida = E_rdel_total / exceso
    # Valor no usado
    # E_rdel_bysource = {source: E_exceso_bysource[source] * factor_resuministrada_producida for source in E_exceso_bysource}

    E_rdel_t = factor_resuministrada_producida * exceso_t
    factor_unfilled_rdel = E_rdel_total / E_EPB_unfilled

    E_rdel_servida_t = factor_unfilled_rdel * E_EPB_unfilled_t

    # ___ energía suministrada por la red ____
    # Valor no usado
    # E_del_grid = sum(E_EPB) - sum(E_EPB_t) - sum(E_rdel_t)
    E_del_grid_t = E_EPB - E_EPB_t - E_rdel_servida_t
    E_exp_grid = exceso - E_rdel_total
    prop_exceso_red = E_exp_grid / exceso if exceso != 0 else 0
    E_exp_grid_bysource = {source: E_exceso_bysource[source] * prop_exceso_red for source in E_exceso_bysource}
    # Valor no usado
    # E_exp_grid_t = sum(E_exp_grid_bysource.values())

    temp_balance = {'grid': {'input': sum(E_del_grid_t)}}

    temp_balance.update({source: {'input': E_prod[source],
                                  'to_nEPB': E_nEPB_bysource[source],
                                  'to_grid': E_exp_grid_bysource[source]} for source in E_prod})
    return temp_balance

def get_annual_balance_forvector(temp_balance):
    """Compute annual balance for vector from stepwise (temp) balance"""
    annual_balance = {}
    for source in temp_balance:
        annual_balance[source] = {}
        temp_balance_for_source = temp_balance[source]
        for use in temp_balance_for_source:
            sumforuse = temp_balance_for_source[use].sum()
            if abs(sumforuse) > 0.1:
                annual_balance[source][use] = sumforuse
    return annual_balance

def readdata(filename):
    """Read input data from filename and return data structure

    Returns dict of array of values indexed by vector, vtype and originoruse

    data[vector][vtype][originoruse] -> values as np.array with length=numsteps

    * vector is and energy vector (carrier)
    * vtype is either 'PRODUCCION' or 'CONSUMO' por produced or used energy
    * originoruse defines:
      - the energy origin for produced energy (INSITU or COGENERACION)
      - the energy end use (EPB or NEPB) for used energy
    * values
    """
    with open(filename, 'r') as datafile:
        lines = datafile.readlines()

        # Find number of calculation steps used
        numsteps = len(lines[1].split(',')[3:])

        data = {}
        for ii, line in enumerate(lines[1:]):
            fields = line.strip().split(',')
            vector, vtype, originoruse = fields[0:3]
            values = np.array(fields[3:]).astype(np.float)

            # Checks
            #TODO: handle Exceptions in CLI
            if len(values) != numsteps:
                raise ValueError, ("All input must use the same number of steps. "
                                   "Problem found in line %i of %s\n\t%s" % (ii + 2, filename, line))
            if vtype not in ('PRODUCCION', 'CONSUMO'):
                raise ValueError, "Vector type is not 'CONSUMO' or 'PRODUCCION' in line %i\n\t%s" % (ii+2, line)
            if originoruse not in ('EPB', 'NEPB', 'INSITU', 'COGENERACION'):
                raise ValueError, ("Origin or end use is not 'EPB', 'NEPB', 'INSITU' or 'COGENERACION'"
                                   " in line %i\n\t%s" % (ii+2, line))

            if vector not in data:
                data[vector] = {'CONSUMO': {'EPB': np.zeros(numsteps),
                                            'NEPB': np.zeros(numsteps)},
                                'PRODUCCION': {'INSITU': np.zeros(numsteps),
                                               'COGENERACION': np.zeros(numsteps)}}

            data[vector][vtype][originoruse] = data[vector][vtype][originoruse] + values
    return data

def calcular_balance(filename, k_rdel):
    data = readdata(filename)
    balance = {}
    for vector in data:
        vdata = data[vector]
        # produccion es un diccionario con las fuentes
        bal_t = get_temp_balance_forvector(vdata, k_rdel)
        bal_an = get_annual_balance_forvector(bal_t)
        balance[vector] = {'anual': bal_an, 'temporal': bal_t}
    return balance

