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

import pandas as pd

def ponderar_vector(data, factor):
    salida = pd.DataFrame()
    salida['ren'] = data * factor['ren']
    salida['nren'] = data * factor['nren']
    return salida

def ponderar_escalar(E, fp):
    return pd.Series({'ren': E*fp['ren'], 'nren': E*fp['nren']})


def pasoA(cruces, constantes):
    # se tratad de sumar las entradas y restar las salidas ponderadas
    
    entrada = pd.Series({'ren':0, 'nren':0})
    salida = pd.Series({'ren':0, 'nren':0})
    #salida = pd.DataFrame
    
    combustible = False
    for cruce in cruces:        
        if not combustible:
            combustible = cruce.combustible
        else:
            if combustible != cruce.combustible:
                raise()
        if cruce.tipo == 'input': 
            weightedEnergy = ponderar_escalar(cruce.valor, cruce.fp_A_o)
            entrada = entrada + weightedEnergy
            
        elif cruce.tipo == 'output':
            combustible = cruce.combustible
            fp_A_d = constantes[combustible][cruce.subtipo]
            weightedEnergy = ponderar_escalar(cruce.valor, fp_A_d)
            salida = salida + weightedEnergy
        
    EP_A = entrada - salida
    
    return EP_A
        
def pasoB(cruces, constantes):
    
    EP_A = pasoA(cruces, constantes)
    #hay que encontrar los subtipos 'nEPB' y 'exp_grid' en los cruces de output
    
    combustible = cruces[0].combustible
    #~ Ewe_nEPB_used_sB = pd.Series({'ren':0, 'nren':0})
    #~ Ewe_exp_grid_sB  = pd.Series({'ren':0, 'nren':0})
    sB_maxima = pd.Series({'ren':0, 'nren':0})
    
    salidas = [i for i in cruces if i.tipo == 'output']
    cruce_nEPB = [i for i in salidas if i.subtipo == 'nEPB']
    cruce_grid = [i for i in salidas if i.subtipo == 'exp_grid']
    
    if cruce_nEPB != []:
        sB_maxima = sB_maxima + ponderar_escalar(cruce_nEPB[0].valor, constantes[combustible]['fpB_nEPB'])
    if cruce_grid != []:
        sB_maxima = sB_maxima + ponderar_escalar(cruce_grid[0].valor, constantes[combustible]['fpB_exp'])
    
    k_exp = constantes[combustible]['k_exp']
    EP_AB = EP_A - k_exp * sB_maxima
    
    return {'EP_AB': EP_AB, 'EP_A' : EP_A}
    
    #~ EP_AB = sA_origen - EP_B
    #~ EP_B = sA_destino + k_exp * sB_maxima
    #~ EP_AB = sA_origen - (sA_destino + k_exp * sB_maxima)
    #~ EP_AB = sA_origen - sA_destino - k_exp * sB_maxima)
    #~ EP_AB = EPA - k_exp * sB_maxima)
