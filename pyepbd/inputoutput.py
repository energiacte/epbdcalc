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

"""Input and output utilities for energy efficiency data handling"""

# TODO: handle exceptions in CLI

import io
from .utils import *

def readenergydata(datalist):
    """Read input data from list and return data structure

    Returns dict of array of values indexed by carrier, ctype and originoruse

    data[carrier][ctype][originoruse] -> values as np.array with length=numsteps

    * carrier is an energy carrier
    * ctype is either 'PRODUCCION' or 'CONSUMO' por produced or used energy
    * originoruse defines:
      - the energy origin for produced energy (INSITU or COGENERACION)
      - the energy end use (EPB or NEPB) for delivered energy
    * values

    List of energy components has the following structure:

    [ {'carrier': carrier1, 'ctype': ctype1, 'originoruse': originoruse1, 'values': values1},
      {'carrier': carrier2, 'ctype': ctype2, 'originoruse': originoruse2, 'values': values2},
      ...
    ]
    """
    numsteps = max(len(data['values']) for data in datalist)

    energydata = {}
    for ii, data in enumerate(datalist):
        carrier = data['carrier']
        ctype = data['ctype']
        originoruse = data['originoruse']
        values = [float(value) for value in data['values']]

        if len(values) != numsteps:
            raise ValueError("All input must have the same number of timesteps. "
                             "Problem found in line %i:\n\t%s" % (ii+1, data))

        if carrier not in energydata:
            energydata[carrier] = {'CONSUMO': {'EPB': [0.0] * numsteps,
                                                  'NEPB': [0.0] * numsteps},
                                   'PRODUCCION': {'INSITU': [0.0] * numsteps,
                                                  'COGENERACION': [0.0] * numsteps}}

        energydata[carrier][ctype][originoruse] = vecvecsum(energydata[carrier][ctype][originoruse], values)
    return energydata

def readenergyfile(filename):
    """Read input data from filename and return data structure

    Returns dict of array of values indexed by carrier, ctype and originoruse

    data[carrier][ctype][originoruse] -> values as np.array with length=numsteps

    * carrier is an energy carrier
    * ctype is either 'PRODUCCION' or 'CONSUMO' por produced or used energy
    * originoruse defines:
      - the energy origin for produced energy (INSITU or COGENERACION)
      - the energy end use (EPB or NEPB) for delivered energy
    * values
    """
    with io.open(filename, 'r') as datafile:
        datalines = []
        for ii, line in enumerate(datafile):
            if line.startswith('vector') or line.startswith('#'):
                continue
            fields = line.strip().split(',')
            carrier, ctype, originoruse = fields[0:3]
            values = fields[3:]

            if ctype not in ('PRODUCCION', 'CONSUMO'):
                raise ValueError("Carrier type is not 'CONSUMO' or 'PRODUCCION' in line %i\n\t%s" % (ii+2, line))
            if originoruse not in ('EPB', 'NEPB', 'INSITU', 'COGENERACION'):
                raise ValueError(("Origin or end use is not 'EPB', 'NEPB', 'INSITU' or 'COGENERACION'"
                                  " in line %i\n\t%s" % (ii+2, line)))

            datalines.append({"carrier": carrier, "ctype": ctype, "originoruse": originoruse, "values": values})
    return readenergydata(datalines)

def readfactors(filename):
    """Read energy weighting factors data from file"""
    # TODO: check valid sources
    data = []
    with io.open(filename, 'r') as ff:
        for ii, line in enumerate(ff.readlines()):
            line = line.strip()
            if line == '' or line.startswith('#') or line.startswith('vector,'):
                continue
            line = line.rsplit('#')[0]
            fieldslist = [field.strip() for field in line.split(',')]
            try:
                vector, fuente, uso, step, fren, fnren = fieldslist
                fren, fnren = float(fren), float(fnren)
            except:
                raise ValueError(u"Número o tipo incorrecto de datos en campos de línea %i: %s" % (ii, line))
            data.append({'vector': vector, 'fuente': fuente, 'uso': uso, 'step': step, 'ren': fren, 'nren': fnren})
    return data

def readfactorsdata(data):
    """Read weighting factors from data object

    The data object is a list of entries which are themselves lists
    with the following structure: [carrier, source, use, step, ren, nren]
    where:
    - carrirer is the energy carrier name as string (e.g. GLP, MEDIOAMBIENTE...)
    - source is the source used as string (grid|INSITU|COGENERACION)
    - use is the energy use as string (input|to_grid|to_nEPB)
    - step is the calculation step as string (A|B)
    - ren is the factor value for its renewable share (e.g. 0.008)
    - nren is the factor value for its non-renewable share (e.g. 2.500)
    """
    #TODO: no validation done here
    return [{'vector': vector, 'fuente': fuente, 'uso': uso, 'step': step, 'ren': fren, 'nren': fnren}
            for (vector, fuente, uso, step, fren, fnren) in data]

def ep2string(EP, area=1.0):
    """Format energy efficiency indicators as string from primary energy data

    In the context of the CTE regulations, this refers to primary energy values.
    """
    areafactor = 1.0 / area
    eparen = areafactor * EP['EPpasoA']['ren']
    epanren = areafactor * EP['EPpasoA']['nren']
    epatotal = eparen + epanren
    eparer = eparen / epatotal if epatotal else 0.0

    epren = areafactor * EP['EP']['ren']
    epnren = areafactor * EP['EP']['nren']
    eptotal = epren + epnren
    eprer = epren / eptotal if eptotal else 0.0

    txt = ("EP(step A)  , ren ={:>8.1f}, nren={:>8.1f}, tot ={:>8.1f}, RER ={:>8.2f}\n"
           "EP(step A+B), ren ={:>8.1f}, nren={:>8.1f}, tot ={:>8.1f}, RER ={:>8.2f}\n"
           ).format(eparen, epanren, epatotal, eparer,
                    epren,  epnren, eptotal, eprer)

    return txt

def ep2dict(EP, area=1.0):
    """Format energy efficiency indicators as dict from primary energy data

    In the context of the CTE regulations, this refers to primary energy values.
    """
    areafactor = 1.0 / area
    eparen = areafactor * EP['EPpasoA']['ren']
    epanren = areafactor * EP['EPpasoA']['nren']
    epatotal = eparen + epanren
    eparer = eparen / epatotal if epatotal else 0.0

    epren = areafactor * EP['EP']['ren']
    epnren = areafactor * EP['EP']['nren']
    eptotal = epren + epnren
    eprer = epren / eptotal if eptotal else 0.0

    epdict = {"EPAren": eparen, "EPAnren": epanren, "EPAtotal": epatotal, "EPArer": eparer,
              "EPren": epren, "EPnren": epnren, "EPtotal": eptotal, "EPrer": eprer}

    return epdict

