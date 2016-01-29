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

import os, sys
currpath = os.path.abspath(os.path.dirname(__file__))
upperpath = os.path.abspath(os.path.join(currpath, '..'))
sys.path.append(upperpath)
import pyepbd as ep

vectores_posibles = ['ELECTRICIDAD', 'ELECTRICIDADCANARIAS', 'ELECTRICIDADBALEARES', 'ELECTRICIDADCEUTAMELILLA',\
    'GASOLEO', 'FUELOIL', 'GLP', 'GASNATURAL', 'CARBON', 'BIOMASA', 'BIOMASADENSIFICADA', 'BIOCARBURANTE',\
    'MEDIOAMBIENTE', 'COGENERACION']
tipos_posibles = ['CONSUMO', 'PRODUCCION']
fuentes_destinos_posibles = ['EPB', 'NEPB', 'INSITU', 'COGENERACION']

def perfilC(valortotal):
    perfil = np.array([0.1639344262, 0.1311475410, 0.0819672131, 0.0737704918, 0.0409836066, 0.0491803279, 0.0655737705, 0.0573770492, 0.0409836066, 0.0655737705, 0.0983606557, 0.1311475410])
    return calc_perfil(valortotal, perfil)

def perfilP1(valortotal):
    perfil = np.array([0.0283687943, 0.0354609929, 0.0496453901, 0.0709219858, 0.12056737590, 0.134751773, 0.1418439716, 0.1276595745, 0.1134751773, 0.0851063830, 0.0567375887, 0.0354609929])
    return calc_perfil(valortotal, perfil)

def perfilP2(valortotal):
    perfil = np.array([0.0851063830, 0.0567375887, 0.0354609929, 0.0283687943, 0.0354609929, 0.0496453901, 0.0709219858, 0.1205673759, 0.1347517730, 0.1418439716, 0.1276595745, 0.1134751773])
    return calc_perfil(valortotal, perfil)

def calc_perfil(valortotal, perfil):
    if isinstance(valortotal, int):
        valortotal = float(valortotal)
    if isinstance(valortotal, float):
        return valortotal * perfil
    else:
        raise ValueError

def crear_fichero(nombre_fichero=None):
    if not nombre_fichero:
        nombre_fichero = 'valores_vectores.csv'
    with open(nombre_fichero, 'w') as f:
        f.writelines('vector,tipo,src_dst\n')

def concepto(vector, tipo, origendestino, valor, nombre_fichero = None):
    if vector not in vectores_posibles:
        print u'__error__ no reconozco a %s como vector, no está en la lista' % vector, vectores_posibles
    if tipo not in tipos_posibles:
        print u'__error__ no reconozco a %s como tipo, no está en la lista' % tipo, tipos_posibles
    if origendestino not in fuentes_destinos_posibles:
        print u'__error__ no reconozco a %s como fuente/destino, no está en la lista' % origendestino, fuentes_destinos_posibles

    with open(nombre_fichero, 'a') as f:
        if isinstance(valor, int):
            valor = [valor]
        f.writelines('%s,%s,%s,' % (vector, tipo, origendestino) + ','.join([str(e) for e in valor]) + '\n')


def verificar(EPB, res):
    import pandas as pd
    res = pd.Series({'ren': res[0], 'nren': res[1]})
    res = EPB.EP - pd.Series(res)
    if abs(res.sum()) > 2:
        print 'Resultado no coincidente: ', res.sum()
        print ep.formatIndicators(EPB)
        print '#####################################################'
        print '--------------------'
        return False
    else:
        return True


def test_ejemplo1base():
    datafile = os.path.join(currpath, 'ejemplo1base.csv')
    crear_fichero(datafile)
    concepto('ELECTRICIDAD','CONSUMO', 'EPB', perfilC(100), datafile)
    fp = os.path.join(currpath, '../data/factores_paso_test.csv')
    EP = ep.calcula_eficiencia_energetica(datafile, fp=fp)
    res = [50.0, 200.0]
    assert verificar(EP,res) == True

def test_ejemplo1base_fail():
    datafile = os.path.join(currpath, 'ejemplo1base.csv')    
    fp = os.path.join(currpath, '../data/factores_paso_test.csv')
    EP = ep.calcula_eficiencia_energetica(datafile, fp=fp)
    res = [53.0, 200.0]    
    assert verificar(EP,res) == False

def test_ejemplo1base_normativo():
    datafile = os.path.join(currpath, 'ejemplo1base.csv')
    EP = ep.calcula_eficiencia_energetica(datafile)
    res = [34.1, 208.20]
    assert verificar(EP,res) == True

def test_ejemplo1PV():
    datafile = os.path.join(currpath, 'ejemplo1PV.csv')
    crear_fichero(datafile)
    concepto('ELECTRICIDAD','CONSUMO', 'EPB', perfilC(100), datafile)
    concepto('ELECTRICIDAD','PRODUCCION', 'INSITU', perfilC(50), datafile)
    fp = os.path.join(currpath, '../data/factores_paso_test.csv')
    EP = ep.calcula_eficiencia_energetica(datafile, fp=fp)
    res = [75.0, 100.0]
    assert verificar(EP,res) == True
    
def test_ejemplo1PV_normativo():
    datafile = os.path.join(currpath, 'ejemplo1PV.csv')
    EP = ep.calcula_eficiencia_energetica(datafile)
    res = [67.1, 104.1]
    assert verificar(EP,res) == True

def test_ejemplo1xPV():
    datafile = os.path.join(currpath, 'ejemplo1xPV.csv')
    crear_fichero(datafile)
    concepto('ELECTRICIDAD','CONSUMO', 'EPB', perfilC(100), datafile)
    concepto('ELECTRICIDAD','PRODUCCION', 'INSITU', perfilC(140), datafile)
    fp = os.path.join(currpath, '../data/factores_paso_test.csv')
    EP = ep.calcula_eficiencia_energetica(datafile, fp=fp)
    res = [120.0, -80.0]
    assert verificar(EP,res) == True
    
def test_ejemplo1xPV_normativo():
    datafile = os.path.join(currpath, 'ejemplo1xPV.csv')
    EP = ep.calcula_eficiencia_energetica(datafile)
    res = [120.0, -80.0]
    assert verificar(EP,res) == True
    
def test_ejemplo1xPVk0():
    datafile = os.path.join(currpath, 'ejemplo1xPV.csv')
    crear_fichero(datafile)
    concepto('ELECTRICIDAD','CONSUMO', 'EPB', perfilC(100), datafile)
    concepto('ELECTRICIDAD','PRODUCCION', 'INSITU', perfilC(140), datafile)
    fp = os.path.join(currpath, '../data/factores_paso_test.csv')
    EP = ep.calcula_eficiencia_energetica(datafile, fp=fp, k_exp=0.0)
    res = [100.0, 0.0]
    assert verificar(EP,res) == True

def test_ejemplo1xPVk0_normativo():
    datafile = os.path.join(currpath, 'ejemplo1xPV.csv')
    EP = ep.calcula_eficiencia_energetica(datafile, k_exp=0.0)
    res = [100.0, 0.0]
    assert verificar(EP,res) == True

def test_ejemplo2xPVgas():
    datafile = os.path.join(currpath, 'ejemplo2xPVgas.csv')
    crear_fichero(datafile)
    concepto('ELECTRICIDAD','CONSUMO', 'EPB', perfilC(20), datafile)
    concepto('ELECTRICIDAD','PRODUCCION','INSITU', perfilP1(40),datafile)
    concepto('GASNATURAL','CONSUMO',  'EPB', perfilC(190),datafile)
    fp = os.path.join(currpath, '../data/factores_paso_test.csv')
    EP = ep.calcula_eficiencia_energetica(datafile, fp=fp)
    res = [30.0, 169.0]
    assert verificar(EP,res) == True

def test_ejemplo2xPVgas_normativo():
    datafile = os.path.join(currpath, 'ejemplo2xPVgas.csv')
    EP = ep.calcula_eficiencia_energetica(datafile)
    res = [30.9, 186.1]
    assert verificar(EP,res) == True

    
def test_ejemplo3PVBdC():
    datafile = os.path.join(currpath, 'ejemplo3PVBdC.csv')
    crear_fichero(datafile)
    concepto('ELECTRICIDAD','CONSUMO', 'EPB', perfilC(59), datafile)
    concepto('ELECTRICIDAD','PRODUCCION','INSITU', perfilP1(40),datafile)
    concepto('MEDIOAMBIENTE','CONSUMO',   'EPB', perfilC(131), datafile)
    concepto('MEDIOAMBIENTE','PRODUCCION','INSITU', perfilC(131), datafile)        
    fp = os.path.join(currpath, '../data/factores_paso_test.csv')
    EP = ep.calcula_eficiencia_energetica(datafile, fp=fp)
    res = [180.0, 38.0]
    assert verificar(EP,res) == True

def test_ejemplo3PVBdC_normativo():
    datafile = os.path.join(currpath, 'ejemplo3PVBdC.csv')
    EP = ep.calcula_eficiencia_energetica(datafile)
    res = [177.5, 39.6]
    assert verificar(EP,res) == True
    
def test_ejemplo4cgnfosil():
    datafile = os.path.join(currpath, 'ejemplo4cgnfosil.csv')
    crear_fichero(datafile)
    concepto('GASNATURAL','CONSUMO',  'EPB', perfilC(100),datafile)
    concepto('GASNATURAL','CONSUMO',  'EPB', perfilC(158),datafile)
    concepto('ELECTRICIDAD','PRODUCCION','COGENERACION', perfilP1(28),datafile)
    fp = os.path.join(currpath, '../data/factores_paso_test.csv')
    EP = ep.calcula_eficiencia_energetica(datafile, fp=fp)
    res = [-14.0, 227.0]
    assert verificar(EP,res) == True

def test_ejemplo4cgnfosil_normativo():
    datafile = os.path.join(currpath, 'ejemplo4cgnfosil.csv')
    EP = ep.calcula_eficiencia_energetica(datafile)
    res = [-12.7, 251]
    assert verificar(EP,res) == True
    
def test_ejemplo5cgnbiogas():
    datafile = os.path.join(currpath, 'ejemplo5cgnbiogas.csv')
    crear_fichero(datafile)
    concepto('GASNATURAL','CONSUMO',  'EPB', perfilC(100),datafile)
    concepto('BIOCARBURANTE','CONSUMO',  'EPB', perfilC(158),datafile)
    concepto('ELECTRICIDAD','PRODUCCION','COGENERACION', perfilP1(28),datafile)
    fp = os.path.join(currpath, '../data/factores_paso_test.csv')
    EP = ep.calcula_eficiencia_energetica(datafile, fp=fp)
    res = [159.0, 69.0]
    assert verificar(EP,res) == True

def test_ejemplo5cgnbiogas_normativo():
    datafile = os.path.join(currpath, 'ejemplo5cgnbiogas.csv')
    EP = ep.calcula_eficiencia_energetica(datafile)
    res = [148.9, 76.4]
    assert verificar(EP,res) == True

def test_ejemplo6K3():
    datafile = os.path.join(currpath, 'ejemplo6K3.csv')
    crear_fichero(datafile)
    concepto('ELECTRICIDAD','CONSUMO',    'EPB',   [200,160,100,90,50,60,80,70,50,80,120,160], datafile)
    concepto('ELECTRICIDAD','CONSUMO',    'NEPB',  np.ones(12)*30, datafile)
    concepto('ELECTRICIDAD','PRODUCCION', 'INSITU',[44,55,77,110,187,209,220,198,176,132,88,55], datafile)   
    fp = os.path.join(currpath, '../data/factores_paso_test.csv')
    EP = ep.calcula_eficiencia_energetica(datafile, fp=fp)
    res = [1385.5, -662]
    assert verificar(EP,res) == True

def test_ejemplo6K3_normativo():
    datafile = os.path.join(currpath, 'ejemplo6K3.csv')
    EP = ep.calcula_eficiencia_energetica(datafile)
    res = [1385.5, -662]
    assert verificar(EP,res) == True
