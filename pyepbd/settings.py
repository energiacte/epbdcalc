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

"""Default values for energy efficiency calculation

These are aimed towards energy efficiency evaluation in the spanish
building code regulations (Código Técnico de la Edificación CTE).
"""

import pandas as pd

# These are all provisional values subject to change

K_EXP = 1.0

K_RDEL = 1.0

FACTORESDEPASOOFICIALES = pd.DataFrame(
    [
        ['ELECTRICIDAD', 'grid', 'input', 'A', 0.341, 2.082],
        ['ELECTRICIDADBALEARES', 'grid', 'input', 'A', 0.094, 3.060],
        ['ELECTRICIDADCANARIAS', 'grid', 'input', 'A', 0.059, 3.058],
        ['ELECTRICIDADCEUTAMELILLA', 'grid', 'input', 'A', 0.066, 2.759],
        ['ELECTRICIDAD', 'INSITU', 'input', 'A', 1.0, 0.0],
        ['ELECTRICIDAD', 'INSITU', 'to_grid', 'A', 1.0, 0.0],
        ['ELECTRICIDAD', 'INSITU', 'to_nEPB', 'A', 1.0, 0.0],
        ['ELECTRICIDAD', 'INSITU', 'to_grid', 'B', 0.5, 2.0],
        ['ELECTRICIDAD', 'INSITU', 'to_nEPB', 'B', 0.5, 2.0],
        ['GASOLEO', 'grid', 'input', 'A', 0.003, 1.179],
        ['GLP', 'grid', 'input', 'A', 0.03, 1.201],
        ['GASNATURAL', 'grid', 'input', 'A', 0.005, 1.190],
        ['CARBON', 'grid', 'input', 'A', 0.002, 1.082],
        # BIOCARBURANTE == BIOMASA DENSIFICADA (PELLETS)
        ['BIOCARBURANTE', 'grid', 'input', 'A', 1.028, 0.085],
        ['MEDIOAMBIENTE', 'INSITU', 'input', 'A', 1.0, 0.0],
        ['ELECTRICIDAD', 'COGENERACION', 'input', 'A', 0.0, 0.0],
        ['ELECTRICIDAD', 'COGENERACION', 'to_grid', 'A', 1.0, 0.0],
        ['ELECTRICIDAD', 'COGENERACION', 'to_nEPB', 'A', 1.0, 0.0],
        ['ELECTRICIDAD', 'COGENERACION', 'to_grid', 'B', 0.5, 2.0],
        ['ELECTRICIDAD', 'COGENERACION', 'to_nEPB', 'B', 0.5, 2.0]
    ],
    columns=['vector', 'fuente', 'uso', 'factor', 'ren', 'nren'])
