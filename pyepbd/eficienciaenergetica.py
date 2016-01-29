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
from . import settings
from balanceenergiafinal import energycomponents, readenergyfile, pondera_energia_primaria, calcula_eficiencia

def calcula_eficiencia_energetica(datafile, k_rdel=None, k_exp=None, fp=None):
    """Balance total de la energía ponderada usada por el edificio y ahorrada a la red.

    Es el balance de energía en la frontera de evaluación AB, descontada la
    parte que ahorra la red debido a la exportación, para todos los
    vectores energéticos y todas las fuentes.

    Este total descuenta al obtenido en el paso A lo que la red ahorra
    debido a la exportación de energía por la frontera (AB).

    Devuelve un diccionario con las claves 'ren' y 'nren' que corresponden
    a la parte renovable y no renovable.
    """
    data = readenergyfile(datafile)
    EP = calcula_eficiencia(data, k_rdel, k_exp, fp)

    return EP
