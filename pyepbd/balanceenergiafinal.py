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
import collections

def calcular_balance_vector(E_EPB, E_nEPB, E_prod, k_rdel, ver=False):
    if ver:
        import vista as v
    ndata = len(E_EPB)

    if isinstance(E_prod, dict):
        E_prod_tot = sum(E_prod.values())#element wise
    else:
        E_prod_tot = E_prod

    if isinstance(E_nEPB, dict):
        E_nEPB = sum(E_nEPB.values())
    #~ if not E_nEPB != None:
        #~ E_nEPB = np.zeros(ndata)

    if ver: print '\nproducción total', v.redondeo(E_prod_tot)
    E_EPB_t = np.minimum(E_EPB,E_prod_tot) #element wise
    if ver: print 'consm EPB instan', v.redondeo(E_EPB_t)

    #____exportable___
    exportable = E_prod_tot - E_EPB_t # linea 20
    if ver: print 'exportable       ', v.redondeo(exportable)
    factor_exportable_producido = [1-E_EPB_t[n]/e  if e != 0 else 0 for n,e in enumerate(E_prod_tot)]
    if ver: print 'factor_exportable' , v.redondeo(factor_exportable_producido,1) #linea 21
    #porcenExport = [1-E_EPB_t[n]/e  if e != 0 else 0 for n,e in enumerate(E_prod_tot)]
    #if ver: print '%_exportab', redondeo(porcenExport,1)[1]
    if isinstance(E_prod, dict):
        E_exportable_source = {} #es directamente lo producido en cada source por el factor exportable
        for source, values in E_prod.items():
            E_exportable_source[source] = values * factor_exportable_producido
            if ver: print '   exportable %s ' % source, v.redondeo(E_exportable_source[source])

    #___nEPB_____
    E_nEPB_used_t = np.minimum(exportable, E_nEPB) # linea 26
    if ver: print 'nEPB_used_t', v.redondeo(E_nEPB_used_t)
    factor_nEPB_exportable = [E_nEPB_used_t[n]/e  if e != 0 else 0 for n,e in enumerate(exportable)]
    if ver: print 'factor_nEPB_exportable  ', v.redondeo(factor_nEPB_exportable,1)
    # podemos asociarlo a cada uno de los productores
    if isinstance(E_prod, dict):
        E_nEPB_source = {}
        for source, values in E_exportable_source.items():
            E_nEPB_source[source] = values * factor_nEPB_exportable
            if ver: print '   nEPB_used_t %s' % source, v.redondeo(E_nEPB_source[source])

    # ____exceso ___
    exceso_t = E_prod_tot - E_EPB_t - E_nEPB_used_t #linea 32
    if ver: print 'exceso           ', v.redondeo(exceso_t)
    exceso = np.sum(exceso_t)
    # porcentaje de la exportable que es exceso (no va a nEPB)
    # el exceso se minora con k_rdel para ser resuministrado
    # y luego con k_exp para ser exportado
    factor_exceso_exportable = [exceso_t[n]/e  if e != 0 else 0 for n,e in enumerate(exportable)] #linea 33
    if ver: print '%_exceso', v.redondeo(factor_exceso_exportable,1)
    if isinstance(E_prod, dict):
        E_exceso_source = {}
        for source, values in E_exportable_source.items():
            E_exceso_source[source] = values * factor_exceso_exportable
            if ver: print '   exceso %s' % source, v.redondeo(E_exceso_source[source])

    #_______ EPB no cubierto _____
    E_EPB_unfilled_t = E_EPB - E_EPB_t
    E_EPB_unfilled = np.sum(E_EPB_unfilled_t)
    if ver: print 'E_EPB_unfilled', v.redondeo(E_EPB_unfilled_t,1) #linea 39

    #_______ resuministrada _____
    #maxima_rdel_paso = k_rdel * E_EPB_unfilled #en caso de que haya producción
    maxima_rdel = min(E_EPB_unfilled, exceso) #línea 40
    if ver: print 'máxima rdel', maxima_rdel
    E_rdel_total = k_rdel * maxima_rdel
    if ver: print 'resuministrable premitida', E_rdel_total
    # la resuministrada se puede ver desde el punto de vista de la producción,
    # cuando se recoge esa energía, o desde el punto de vista del consumo,
    # cunado se sirve esa energía recogida. El total es el mismo, pero los valores
    # temporales varían.
    factor_resuministrada_producida = E_rdel_total/exceso #
    if isinstance(E_prod, dict):
        E_rdel_source = {}
        for source, values in E_exceso_source.items():
            E_rdel_source[source] = values * factor_resuministrada_producida
            if ver: print '   rdel %s ' %source, v.redondeo(E_rdel_source[source],1)

    E_rdel_t = factor_resuministrada_producida * exceso_t
    if ver: print 'E_rdel_t ', v.redondeo(E_rdel_t)
    factor_unfilled_rdel = E_rdel_total/E_EPB_unfilled

    E_rdel_servida_t = factor_unfilled_rdel * E_EPB_unfilled_t
    if ver: print 'E_rdel_servida_t ', v.redondeo(E_rdel_servida_t)

    # ___ energía suministrada por la red ____
    E_del_grid = sum(E_EPB) - sum(E_EPB_t) - sum(E_rdel_t)
    E_del_grid_t = E_EPB - E_EPB_t - E_rdel_servida_t
    if ver: print 'suminist grid_t', v.redondeo(E_del_grid_t)
    if ver: print 'suminist grid', v.redondeo(E_del_grid)
    E_exp_grid = exceso - E_rdel_total
    if ver: print 'exportada', int(round(E_exp_grid)) #me tienes que decir quién exporta
    # hay que repercutirlo por combustible
    prop_exceso_red = E_exp_grid/exceso if exceso != 0 else 0
    if ver: print 'prop_exceso_red', prop_exceso_red
    if isinstance(E_prod, dict):
        E_exp_grid_source = {}
        for clave, valor in E_exceso_source.items(): #exceso por fuente
            E_exp_grid_source[clave]= prop_exceso_red * valor
            if ver: print 'exp_grid_src', clave, v.redondeo(prop_exceso_red * valor)
        E_exp_grid_t = sum(E_exp_grid_source.values())
    else:
        E_exp_grid_t = np.zeros(ndata)

    def verificar_balance():
        valor1 = E_EPB - (E_EPB_t + E_rdel_t + E_del_grid_t)
        valor2 = E_prod_tot - (E_EPB_t + E_nEPB_used_t + E_rdel_t + E_exp_grid_t)
        if abs(valor1.sum()) > 1:
            print '___###____ error de verificación 1 ___###____ '
            print v.redondeo(valor1)
        if abs(valor2.sum()) > 2:
            print '___###____ error de verificación 2 ___###____ '
            print v.redondeo(valor2)
            print 'E_prod_tot', E_prod_tot
            print 'E_EPB_t', E_EPB_t
            print 'E_nEPB_used_t', E_nEPB_used_t
            print 'E_rdel_t', E_rdel_t
            print 'E_exp_grid_t', E_exp_grid_t

    verificar_balance()

    balance_temporal = {'grid': {'input': sum(E_del_grid_t)}}
    if isinstance(E_prod,dict):
        for clave, valor in E_prod.items():
            fuente = {}
            fuente['input'] = E_prod[clave]
            if ver: print '\tto_nEPB', v.redondeo(E_nEPB_source[clave])
            fuente['to_nEPB'] = E_nEPB_source[clave]
            if ver: print '\tto_grid', v.redondeo(E_exp_grid_source[clave])
            fuente['to_grid'] = E_exp_grid_source[clave]
            balance_temporal[clave] = fuente

    balance_anual = {}
    for fuente,usos in balance_temporal.items():
        balance_anual[fuente] = {}
        for uso, valor in usos.items():
            if abs(valor.sum()) > 0.1:
                balance_anual[fuente][uso] = valor.sum()

    return balance_anual, balance_temporal


def calcular_balance(fichero, k_rdel, ver = False):

    if hasattr(fichero, 'readlines'):
        lineas = fichero.readlines()
    else:
        with open(fichero, 'r') as f:
            lineas = f.readlines()

    datos_balance = {}
    nvalores = False
    for linea in lineas[1:]:
        campos = linea.split(',')
        vector = campos[0]
        tipo = campos[1]
        src_dst = campos[2]
        valores = np.array([float(e.strip('\n')) for e in campos[3:]])
        if not nvalores:
            nvalores = len(valores)
        else:
            if nvalores != len(valores):
                print '___error___', 'hay un vector con un número de datos erróneo'
                print vector, tipo, src_dst, valores

        if vector not in datos_balance.keys():
            datos_balance[vector] = {}

        if tipo not in datos_balance[vector].keys():
            datos_balance[vector][tipo] = {}

        if src_dst not in datos_balance[vector][tipo].keys():
            datos_balance[vector][tipo][src_dst] = np.zeros(nvalores)

        datos_balance[vector][tipo][src_dst] = datos_balance[vector][tipo][src_dst] + valores

    for vector, conceptos in datos_balance.items():
        if ver: print vector
        consumo_EPB, consumo_nEPB, produccion = np.zeros(nvalores),np.zeros(nvalores),np.zeros(nvalores)
        if 'CONSUMO' in conceptos.keys():
            if 'EPB' in conceptos['CONSUMO'].keys():
                consumo_EPB = pd.Series(conceptos['CONSUMO']['EPB'])
                if ver: print '\tconsumo', 'EPB', conceptos['CONSUMO']['EPB']
            if 'NEPB' in conceptos['CONSUMO'].keys():
                consumo_nEPB = pd.Series(conceptos['CONSUMO']['NEPB'])
                if ver: print '\tconsumo', 'nEPB', conceptos['CONSUMO']['NEPB']
        if 'PRODUCCION' in conceptos.keys(): ### produccion es un diccionario con las fuentes!!!!
            produccion = conceptos['PRODUCCION']
            if ver: print '\tproduccion', 'varios', conceptos['PRODUCCION']

        bal_an, bal_t =  calcular_balance_vector(consumo_EPB, consumo_nEPB, produccion, k_rdel, ver)
        datos_balance[vector] = {'anual': bal_an, 'temporal': bal_t}
    if ver: print 'datos_balance\n', datos_balance
    return datos_balance

    # para cada vector calcular el balance de vector.
    # con eso formar el vector_data y devolverlo a control para calcular
    # la eficiencia enrgética.

def calc_balance(E_EPB, E_nEPB, E_prod, k_rdel, ver = False):
    E_EPB_t = np.minimum(E_EPB,E_prod) #element wise
    exportable = E_prod - E_EPB_t
    E_nEPB_used_t = np.minimum(exportable, E_nEPB)
    exceso = np.sum(E_prod - E_EPB_t - E_nEPB_used_t)
    E_EPB_noCubierto = np.sum(E_EPB - E_EPB_t)
    maxima_rdel = min(E_EPB_noCubierto, exceso)

    E_nEPB_used = np.sum(E_nEPB_used_t)
    E_rdel = k_rdel * maxima_rdel
    E_del_grid = np.sum(E_EPB) - np.sum(E_EPB_t) - E_rdel
    E_exp_grid = exceso - E_rdel

    salida = {'nEPB_used': E_nEPB_used,
              'rdel': E_rdel,
              'del_grid': E_del_grid,
              'exp_grid': E_exp_grid}

