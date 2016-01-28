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

""" Calcula la eficiencia energética como balance entre la energía usada y la ahorrada a la red.

El proceso de calculo de la eficiencia energética se calcula en dos pasos:

- En un primer paso se consideran las producciones y consumos de cada combustible,
  que se equilibran mediante el suministro de la red correspondiente.

- Después se aplican los pasos A, de importación, y B, de exportación y ahorro,
  para obtener la eficiencia energética del caso considerado.

La red proporciona la cantidad suficiente de cada tipo de combustible para
equilibrar el balance entre producción y consumo. Además, es necesario obtener qué
parte de la demanda energética no ha podido ser satisfecha instantáneamente pero
podría serlo con la energía producida en otros pasos de cálculo. Esto se regula
mediante el parámetro normativo de resuministro ($k_{rdel}$).

Realizado el calculo del balance, los valores energéticos se agrupan en unos pocos
conceptos con valores anuales de los que se obtendrá el indicador de eficiencia
energética según indica la norma \textit{ISO/DIS 52000-1:2015} aplicando los pasos A y B.

Estos indicadores tienen una parte renovable y otra no renovable, lo que permite
calcular el valor de consumo energético total, además del porcentaje de uso de
energías renovables.


Las funciones devuelven un diccionario con la parte renovable y no renovable
de los indicadores, que aportan en base anual, aunque el cálculo se realice
en pasos temporales menores.

El cálculo está organizado por:
    - vectores energéticos
    - fuentes de energía
    - destino o uso de la energía.
"""

import pandas as pd

def calcula_energia_entrante_pasoA(sources, fp):
    """Energía total ponderada que entra en el paso A en la frontera de evaluación (AB)

    La energía que entra se pondera según su origen.

    Devuelve un diccionario con las claves 'ren' y 'nren' que corresponden
    a la parte renovable y no renovable.
    """

    energia_entrante_pasoA = pd.Series({'ren': 0.0, 'nren': 0.0})
    fpA = fp[(fp.uso=='input') & (fp.factor=='A')]
    for source in sources:
        value = sources[source]
        if 'input' in value:
            factor_paso_A = fpA[(fpA.fuente==source)][['ren', 'nren']].iloc[0]
            energia_entrante_pasoA = energia_entrante_pasoA + factor_paso_A * value['input']
    return energia_entrante_pasoA

def calcula_energia_saliente_pasoA(sources, fpA):
    """Energía total ponderada que sale en el paso A por la frontera de evaluación (AB)

    La energía que sale se pondera según su destino.

    Devuelve un diccionario con las claves 'ren' y 'nren' que corresponden
    a la parte renovable y no renovable.
    """

    to_nEPB = pd.Series({'ren': 0.0, 'nren': 0.0})
    to_grid = pd.Series({'ren': 0.0, 'nren': 0.0})
    fpA_to_nEPB = fpA[(fpA.uso=='to_nEPB')]
    fpA_to_grid = fpA[(fpA.uso=='to_nEPB')]
    for source in sources:
        value = sources[source]
        if 'to_nEPB' in value:
            fp_tmp = fpA_to_nEPB[fpA_to_nEPB.fuente==source][['ren', 'nren']].iloc[0]
            to_nEPB = to_nEPB + fp_tmp * value['to_nEPB']

        if 'to_grid' in value:
            fp_tmp = fpA_to_grid[fpA_to_grid.fuente== source][['ren', 'nren']].iloc[0]
            to_grid = to_grid + fp_tmp * value['to_grid']

    energia_saliente_pasoA = to_nEPB + to_grid
    return energia_saliente_pasoA

def calcula_balance_pasoA(pasoA_o, pasoA_d):
    """Balance de la energía total ponderada, en el paso A.

    El balance se realiza en la frontera de evaluación (AB).
    La característica de este balance es que los factores de entrada y
    los de salida son iguales. Se obtiene la diferencia entre la energía
    importada y exportada.

    Devuelve un diccionario con las claves 'ren' y 'nren' que corresponden
    a la parte renovable y no renovable del balance en el paso A.
    """

    balance_pasoA = pasoA_o - pasoA_d
    return balance_pasoA

def calcula_ahorro_pasoB(sources, fp, k_exp):
    """Energia total ponderada ahorrada por la red.

    Este valor representa la energía ponderada que ahorra la red
    debido a la exportación de energía por la frontera (AB).

    Devuelve un diccionario con las claves 'ren' y 'nren' que corresponden
    a la parte renovable y no renovable de la eficiencia energética,
    medida como energía primaria, en el paso B.
    """

    to_nEPB = pd.Series({'ren': 0.0, 'nren': 0.0})
    to_grid = pd.Series({'ren': 0.0, 'nren': 0.0})
    fpB = fp[fp.factor=='B']
    fpA = fp[fp.factor=='A']
    for source in sources:
        value = sources[source]
        if 'to_nEPB' in value:
            fpB_tmp= fpB[(fpB.uso=='to_nEPB') & (fpB.fuente==source)][['ren','nren']].iloc[0]
            fpA_tmp= fpA[(fpA.uso=='to_nEPB') & (fpA.fuente==source)][['ren','nren']].iloc[0]
            to_nEPB = to_nEPB + (fpB_tmp - fpA_tmp) * value['to_nEPB']
        if 'to_grid' in value:
            fpB_tmp= fpB[(fpB.uso=='to_grid') & (fpB.fuente==source)][['ren','nren']].iloc[0]
            fpA_tmp= fpA[(fpA.uso=='to_grid') & (fpA.fuente==source)][['ren','nren']].iloc[0]
            to_grid = to_grid + (fpB_tmp - fpA_tmp) * value['to_grid']

    ahorro_pasoB = k_exp * (to_nEPB + to_grid)
    return ahorro_pasoB

def calcula_eficiencia_energetica_vec(vector, sources, fp, k_exp):
    """Balance total de la energía ponderada de un vector energético

    Es el balance de energía para un vector energético en la frontera de
    evaluación descontada la parte que ahorra la red debido a la exportación.

    Este total descuenta al obtenido en el paso A lo que la red ahorra
    debido a la exportación de energía por la frontera (AB).

    Devuelve un diccionario con las claves 'ren' y 'nren' que corresponden
    a la parte renovable y no renovable de la eficiencia energética
    medida como energía primaria.
    """
    fp_vec = fp[fp.vector==vector]
    sources = sources['anual']

    energia_entrante_pasoA = calcula_energia_entrante_pasoA(sources, fp_vec)
    energia_saliente_pasoA = calcula_energia_saliente_pasoA(sources, fp_vec)
    balance_pasoA = calcula_balance_pasoA(energia_entrante_pasoA, energia_saliente_pasoA)
    ahorro_pasoB = calcula_ahorro_pasoB(sources, fp_vec, k_exp)
    eficiencia_energetica = balance_pasoA - ahorro_pasoB

    return pd.DataFrame({'EP': eficiencia_energetica, 'EPpasoA': balance_pasoA})

def pondera_energia_primaria(balance, fp, k_exp):
    """Balance total de la energía ponderada usada por el edificio y ahorrada a la red.

    Es el balance de energía en la frontera de evaluación descontada la
    parte que ahorra la red debido a la exportación para todos los
    vectores energéticos y todas las fuentes.

    Este total descuenta al obtenido en el paso A lo que la red ahorra
    debido a la exportación de energía por la frontera (AB).

    Devuelve un diccionario con las claves 'ren' y 'nren' que corresponden
    a la parte renovable y no renovable.
    """
    EP = pd.DataFrame({'EP': {'ren': 0.0,
                              'nren': 0.0},
                       'EPpasoA': {'ren': 0.0,
                                   'nren': 0.0}})
    for vector in balance:
        EP = EP + calcula_eficiencia_energetica_vec(vector, balance[vector], fp, k_exp)
    return EP
