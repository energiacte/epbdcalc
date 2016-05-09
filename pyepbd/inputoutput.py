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

from io import open
import numpy as np
import pandas as pd

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
        values = np.array(data['values']).astype(np.float)

        if len(values) != numsteps:
            raise ValueError("All input must have the same number of timesteps. "
                             "Problem found in line %i:\n\t%s" % (ii+1, line))

        if carrier not in energydata:
            energydata[carrier] = {'CONSUMO': {'EPB': np.zeros(numsteps),
                                                  'NEPB': np.zeros(numsteps)},
                                   'PRODUCCION': {'INSITU': np.zeros(numsteps),
                                                  'COGENERACION': np.zeros(numsteps)}}

        energydata[carrier][ctype][originoruse] = energydata[carrier][ctype][originoruse] + values
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
    with open(filename, 'r') as datafile:
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
    return pd.read_csv(filename,
                       skipinitialspace=True,
                       comment='#',
                       skip_blank_lines=True)

def ep2string(EP):
    """Format energy efficiency indicators as string from primary energy data

    In the context of the CTE regulations, this refers to primary energy values.
    """

    eparen, epanren = EP.EPpasoA['ren'], EP.EPpasoA['nren']
    epatotal = eparen + epanren
    eparer = eparen / epatotal if epatotal else 0.0

    epren, epnren = EP.EP['ren'], EP.EP['nren']
    eptotal = epren + epnren
    eprer = epren / eptotal if eptotal else 0.0

    txt = ("EP(step A)  , ren ={:>8.1f}, nren={:>8.1f}, tot ={:>8.1f}, RER ={:>8.2f}\n"
           "EP(step A+B), ren ={:>8.1f}, nren={:>8.1f}, tot ={:>8.1f}, RER ={:>8.2f}\n"
           ).format(eparen, epanren, epatotal, eparer,
                    epren,  epnren, eptotal, eprer)

    return txt

def ep2dict(EP):
    """Format energy efficiency indicators as dict from primary energy data

    In the context of the CTE regulations, this refers to primary energy values.
    """

    eparen, epanren = EP.EPpasoA['ren'], EP.EPpasoA['nren']
    epatotal = eparen + epanren
    eparer = eparen / epatotal if epatotal else 0.0

    epren, epnren = EP.EP['ren'], EP.EP['nren']
    eptotal = epren + epnren
    eprer = epren / eptotal if eptotal else 0.0

    epdict = {"EPAren": eparen, "EPAnren": epanren, "EPAtotal": epatotal, "EPArer": eparer,
              "EPren": epren, "EPnren": epnren, "EPtotal": eptotal, "EPrer": eprer}

    return epdict

