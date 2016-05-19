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

Weighting factors are based on primary energy use.
"""

import pandas as pd

# These are all provisional values subject to change

K_EXP = 1.0

K_RDEL = 1.0

# FpA - weighting factors accounting for the resources used to produce this energy
# FpB - weighting factors accounting for the resources avoided by the external grid due to the export
FACTORESDEPASOOFICIALES = pd.DataFrame([
#  Energy carrier         origin          use         step Fpren  Fpnren
    ['ELECTRICIDAD',        'grid',         'input',    'A', 0.341, 2.082], # Delivered energy
    ['ELECTRICIDAD',        'INSITU',       'input',    'A', 1.000, 0.000], # Produced energy
    ['ELECTRICIDAD',        'INSITU',       'to_grid',  'A', 1.000, 0.000], # Produced and exported to the grid
    ['ELECTRICIDAD',        'INSITU',       'to_nEPB',  'A', 1.000, 0.000], # Produced and exported to nEPB uses
    ['ELECTRICIDAD',        'INSITU',       'to_grid',  'B', 0.341, 2.082], # Savings to the grid due to produced and exported to the grid energy
    ['ELECTRICIDAD',        'INSITU',       'to_nEPB',  'B', 0.341, 2.082], # Savings to the grid due to produced and exported to nEPB uses
    ['ELECTRICIDAD',        'COGENERACION', 'input',    'A', 0.000, 0.000], # There is no delivery from grid for this carrier
    ['ELECTRICIDAD',        'COGENERACION', 'to_grid',  'A', 0.000, 1.000], # User defined!
    ['ELECTRICIDAD',        'COGENERACION', 'to_nEPB',  'A', 0.000, 1.000], # User defined!
    ['ELECTRICIDAD',        'COGENERACION', 'to_grid',  'B', 0.341, 2.082], # Savings to the grid when exporting to the grid
    ['ELECTRICIDAD',        'COGENERACION', 'to_nEPB',  'B', 0.341, 2.082], # Savings to the grid when exporting to nEPB uses

    ['ELECTRICIDADBALEARES','grid',         'input',    'A', 0.094, 3.060], # Delivered energy
    ['ELECTRICIDADBALEARES','INSITU',       'input',    'A', 1.000, 0.000], # Produced energy
    ['ELECTRICIDADBALEARES','INSITU',       'to_grid',  'A', 1.000, 0.000], # Produced and exported to the grid
    ['ELECTRICIDADBALEARES','INSITU',       'to_nEPB',  'A', 1.000, 0.000], # Produced and exported to nEPB uses
    ['ELECTRICIDADBALEARES','INSITU',       'to_grid',  'B', 0.094, 3.060], # Savings to the grid due to produced and exported to the grid energy
    ['ELECTRICIDADBALEARES','INSITU',       'to_nEPB',  'B', 0.094, 3.060], # Savings to the grid due to produced and exported to nEPB uses
    ['ELECTRICIDADBALEARES','COGENERACION', 'input',    'A', 0.000, 0.000], # There is no delivery from grid for this carrier
    ['ELECTRICIDADBALEARES','COGENERACION', 'to_grid',  'A', 0.000, 1.000], # User defined!
    ['ELECTRICIDADBALEARES','COGENERACION', 'to_nEPB',  'A', 0.000, 1.000], # User defined!
    ['ELECTRICIDADBALEARES','COGENERACION', 'to_grid',  'B', 0.094, 3.060], # Savings to the grid when exporting to the grid
    ['ELECTRICIDADBALEARES','COGENERACION', 'to_nEPB',  'B', 0.094, 3.060], # Savings to the grid when exporting to nEPB uses

    ['ELECTRICIDADCANARIAS','grid',         'input',    'A', 0.059, 3.058], # Delivered energy
    ['ELECTRICIDADCANARIAS','INSITU',       'input',    'A', 1.000, 0.000], # Produced energy
    ['ELECTRICIDADCANARIAS','INSITU',       'to_grid',  'A', 1.000, 0.000], # Produced and exported to the grid
    ['ELECTRICIDADCANARIAS','INSITU',       'to_nEPB',  'A', 1.000, 0.000], # Produced and exported to nEPB uses
    ['ELECTRICIDADCANARIAS','INSITU',       'to_grid',  'B', 0.059, 3.058], # Savings to the grid due to produced and exported to the grid energy
    ['ELECTRICIDADCANARIAS','INSITU',       'to_nEPB',  'B', 0.059, 3.058], # Savings to the grid due to produced and exported to nEPB uses
    ['ELECTRICIDADCANARIAS','COGENERACION', 'input',    'A', 0.000, 0.000], # There is no delivery from grid for this carrier
    ['ELECTRICIDADCANARIAS','COGENERACION', 'to_grid',  'A', 0.000, 1.000], # User defined!
    ['ELECTRICIDADCANARIAS','COGENERACION', 'to_nEPB',  'A', 0.000, 1.000], # User defined!
    ['ELECTRICIDADCANARIAS','COGENERACION', 'to_grid',  'B', 0.059, 3.058], # Savings to the grid when exporting to the grid
    ['ELECTRICIDADCANARIAS','COGENERACION', 'to_nEPB',  'B', 0.059, 3.058], # Savings to the grid when exporting to nEPB uses

    ['ELECTRICIDADCEUTAMELILLA','grid',     'input',    'A', 0.066, 2.759], # Delivered energy
    ['ELECTRICIDADCEUTAMELILLA','INSITU',   'input',    'A', 1.000, 0.000], # Produced energy
    ['ELECTRICIDADCEUTAMELILLA','INSITU',   'to_grid',  'A', 1.000, 0.000], # Produced and exported to the grid
    ['ELECTRICIDADCEUTAMELILLA','INSITU',   'to_nEPB',  'A', 1.000, 0.000], # Produced and exported to nEPB uses
    ['ELECTRICIDADCEUTAMELILLA','INSITU',   'to_grid',  'B', 0.066, 2.759], # Savings to the grid due to produced and exported to the grid energy
    ['ELECTRICIDADCEUTAMELILLA','INSITU',   'to_nEPB',  'B', 0.066, 2.759], # Savings to the grid due to produced and exported to nEPB uses
    ['ELECTRICIDADCEUTAMELILLA','COGENERACION','input', 'A', 0.000, 0.000], # There is no delivery from grid for this carrier
    ['ELECTRICIDADCEUTAMELILLA','COGENERACION','to_grid','A', 0.000, 1.000], # User defined!
    ['ELECTRICIDADCEUTAMELILLA','COGENERACION','to_nEPB','A', 0.000, 1.000], # User defined!
    ['ELECTRICIDADCEUTAMELILLA','COGENERACION','to_grid','B', 0.066, 2.759], # Savings to the grid when exporting to the grid
    ['ELECTRICIDADCEUTAMELILLA','COGENERACION','to_nEPB','B', 0.066, 2.759], # Savings to the grid when exporting to nEPB uses

    ['MEDIOAMBIENTE',       'grid',         'input',    'A', 1.000, 0.000], # Grid is able to deliver this carrier
    ['MEDIOAMBIENTE',       'INSITU',       'input',    'A', 1.000, 0.000], # in-situ production of this carrier
    ['MEDIOAMBIENTE',       'INSITU',       'to_grid',  'A', 0.000, 0.000], # export to grid is not accounted for
    ['MEDIOAMBIENTE',       'INSITU',       'to_nEPB',  'A', 1.000, 0.000], # export to nEPB uses in step A
    ['MEDIOAMBIENTE',       'INSITU',       'to_grid',  'B', 0.000, 0.000], # Savings to the grid when exporting to grid
    ['MEDIOAMBIENTE',       'INSITU',       'to_nEPB',  'B', 1.000, 0.000], # Savings to the grid when exporting to nEPB uses

    # BIOCARBURANTE == BIOMASA DENSIFICADA (PELLETS)
    ['BIOCARBURANTE',       'grid',         'input',    'A', 1.028, 0.085], # Delivered energy
    ['BIOMASA',             'grid',         'input',    'A', 1.003, 0.034], # Delivered energy
    ['BIOMASADENSIFICADA',  'grid',         'input',    'A', 1.028, 0.085], # Delivered energy
    ['CARBON',              'grid',         'input',    'A', 0.002, 1.082], # Delivered energy
    # FUELOIL == GASOLEO
    ['FUELOIL',             'grid',         'input',    'A', 0.003, 1.179], # Delivered energy
    ['GASNATURAL',          'grid',         'input',    'A', 0.005, 1.190], # Delivered energy
    ['GASOLEO',             'grid',         'input',    'A', 0.003, 1.179], # Delivered energy
    ['GLP',                 'grid',         'input',    'A', 0.030, 1.201], # Delivered energy
    ['RED1',                'grid',         'input',    'A', 0.000, 1.300], # User defined!, district heating/cooling carrier
    ['RED2',                'grid',         'input',    'A', 0.000, 1.300], # User defined!, district heating/cooling carrier
], columns=['vector',          'fuente',       'uso',  'factor', 'ren', 'nren'])
