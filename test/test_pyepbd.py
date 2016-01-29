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

import os, sys
import pandas as pd

currpath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(currpath, '..'))

from pyepbd import (FACTORESDEPASOOFICIALES,
                    calcula_eficiencia_energetica,
                    formatIndicators, readfactors)

def check(EPB, res):
    res = EPB.EP - pd.Series({'ren': res[0], 'nren': res[1]})
    if abs(res.sum()) > 2.0:
        print 'Resultado no coincidente: ', res.sum()
        print formatIndicators(EPB)
        print '#####################################################'
        print '--------------------'
        return False
    else:
        return True

TESTFP = readfactors(os.path.join(currpath, '../data/factores_paso_test.csv'))
CTEFP = FACTORESDEPASOOFICIALES
TESTKRDEL = 1.0
TESTKEXP = 1.0

def test_ejemplo1base():
    EP = calcula_eficiencia_energetica(os.path.join(currpath, 'ejemplo1base.csv'),
                                       k_rdel=TESTKRDEL, k_exp=TESTKEXP, fp=TESTFP)
    assert check(EP, [50.0, 200.0]) == True

def test_ejemplo1base_fail():
    EP = calcula_eficiencia_energetica(os.path.join(currpath, 'ejemplo1base.csv'),
                                       k_rdel=TESTKRDEL, k_exp=TESTKEXP, fp=TESTFP)
    assert check(EP, [53.0, 200.0]) == False

def test_ejemplo1base_normativo():
    EP = calcula_eficiencia_energetica(os.path.join(currpath, 'ejemplo1base.csv'),
                                       k_rdel=TESTKRDEL, k_exp=TESTKEXP, fp=CTEFP)
    assert check(EP, [34.1, 208.20]) == True

def test_ejemplo1PV():
    EP = calcula_eficiencia_energetica( os.path.join(currpath, 'ejemplo1PV.csv'),
                                        k_rdel=TESTKRDEL, k_exp=TESTKEXP, fp=TESTFP)
    assert check(EP, [75.0, 100.0]) == True

def test_ejemplo1PV_normativo():
    EP = calcula_eficiencia_energetica(os.path.join(currpath, 'ejemplo1PV.csv'),
                                       k_rdel=TESTKRDEL, k_exp=TESTKEXP, fp=CTEFP)
    assert check(EP, [67.1, 104.1]) == True

def test_ejemplo1xPV():
    EP = calcula_eficiencia_energetica(os.path.join(currpath, 'ejemplo1xPV.csv'),
                                       k_rdel=TESTKRDEL, k_exp=TESTKEXP, fp=TESTFP)
    assert check(EP, [120.0, -80.0]) == True

def test_ejemplo1xPV_normativo():
    EP = calcula_eficiencia_energetica(os.path.join(currpath, 'ejemplo1xPV.csv'),
                                       k_rdel=TESTKRDEL, k_exp=TESTKEXP, fp=CTEFP)
    assert check(EP, [120.0, -80.0]) == True

def test_ejemplo1xPVk0():
    EP = calcula_eficiencia_energetica(os.path.join(currpath, 'ejemplo1xPV.csv'),
                                       k_rdel=TESTKRDEL, k_exp=0.0, fp=TESTFP)
    assert check(EP, [100.0, 0.0]) == True

def test_ejemplo1xPVk0_normativo():
    EP = calcula_eficiencia_energetica(os.path.join(currpath, 'ejemplo1xPV.csv'),
                                       k_rdel=TESTKRDEL, k_exp=0.0, fp=CTEFP)
    assert check(EP, [100.0, 0.0]) == True

def test_ejemplo2xPVgas():
    EP = calcula_eficiencia_energetica(os.path.join(currpath, 'ejemplo2xPVgas.csv'),
                                       k_rdel=TESTKRDEL, k_exp=TESTKEXP, fp=TESTFP)
    assert check(EP, [30.0, 169.0]) == True

def test_ejemplo2xPVgas_normativo():
    EP = calcula_eficiencia_energetica(os.path.join(currpath, 'ejemplo2xPVgas.csv'),
                                       k_rdel=TESTKRDEL, k_exp=TESTKEXP, fp=CTEFP)
    assert check(EP, [30.9, 186.1]) == True

def test_ejemplo3PVBdC():
    EP = calcula_eficiencia_energetica(os.path.join(currpath, 'ejemplo3PVBdC.csv'),
                                       k_rdel=TESTKRDEL, k_exp=TESTKEXP, fp=TESTFP)
    assert check(EP, [180.0, 38.0]) == True

def test_ejemplo3PVBdC_normativo():
    EP = calcula_eficiencia_energetica(os.path.join(currpath, 'ejemplo3PVBdC.csv'),
                                       k_rdel=TESTKRDEL, k_exp=TESTKEXP, fp=CTEFP)
    assert check(EP, [177.5, 39.6]) == True

def test_ejemplo4cgnfosil():
    EP = calcula_eficiencia_energetica(os.path.join(currpath, 'ejemplo4cgnfosil.csv'),
                                       k_rdel=TESTKRDEL, k_exp=TESTKEXP, fp=TESTFP)
    assert check(EP, [-14.0, 227.0]) == True

def test_ejemplo4cgnfosil_normativo():
    EP = calcula_eficiencia_energetica(os.path.join(currpath, 'ejemplo4cgnfosil.csv'),
                                       k_rdel=TESTKRDEL, k_exp=TESTKEXP, fp=CTEFP)
    assert check(EP, [-12.7, 251]) == True

def test_ejemplo5cgnbiogas():
    EP = calcula_eficiencia_energetica(os.path.join(currpath, 'ejemplo5cgnbiogas.csv'),
                                       k_rdel=TESTKRDEL, k_exp=TESTKEXP, fp=TESTFP)
    assert check(EP, [159.0, 69.0]) == True

def test_ejemplo5cgnbiogas_normativo():
    EP = calcula_eficiencia_energetica(os.path.join(currpath, 'ejemplo5cgnbiogas.csv'),
                                       k_rdel=TESTKRDEL, k_exp=TESTKEXP, fp=CTEFP)
    assert check(EP, [148.9, 76.4]) == True

def test_ejemplo6K3():
    EP = calcula_eficiencia_energetica(os.path.join(currpath, 'ejemplo6K3.csv'),
                                       k_rdel=TESTKRDEL, k_exp=TESTKEXP, fp=TESTFP)
    assert check(EP, [1385.5, -662]) == True

def test_ejemplo6K3_normativo():
    EP = calcula_eficiencia_energetica(os.path.join(currpath, 'ejemplo6K3.csv'),
                                       k_rdel=TESTKRDEL, k_exp=TESTKEXP, fp=CTEFP)
    assert check(EP, [1385.5, -662]) == True
