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

import numpy as np
import pandas as pd

def readenergyfile(filename):
    """Read input data from filename and return data structure

    Returns dict of array of values indexed by carrier, ctype and originoruse

    data[carrier][ctype][originoruse] -> values as np.array with length=numsteps

    * carrier is an energy carrier
    * ctype is either 'PRODUCCION' or 'SUMINISTRO' por produced or used energy
    * originoruse defines:
      - the energy origin for produced energy (INSITU or COGENERACION)
      - the energy end use (EPB or NEPB) for used energy
    * values
    """
    with open(filename, 'r') as datafile:
        lines = datafile.readlines()

        # Find number of calculation steps used
        numsteps = len(lines[1].split(',')[3:])

        data = {}
        for ii, line in enumerate(lines[1:]):
            fields = line.strip().split(',')
            carrier, ctype, originoruse = fields[0:3]
            values = np.array(fields[3:]).astype(np.float)

            # Checks
            #TODO: handle Exceptions in CLI
            if len(values) != numsteps:
                raise ValueError, ("All input must have the same number of timesteps. "
                                   "Problem found in line %i of %s\n\t%s" % (ii+2, filename, line))
            if ctype not in ('PRODUCCION', 'SUMINISTRO'):
                raise ValueError, "Carrier type is not 'SUMINISTRO' or 'PRODUCCION' in line %i\n\t%s" % (ii+2, line)
            if originoruse not in ('EPB', 'NEPB', 'INSITU', 'COGENERACION'):
                raise ValueError, ("Origin or end use is not 'EPB', 'NEPB', 'INSITU' or 'COGENERACION'"
                                   " in line %i\n\t%s" % (ii+2, line))

            if carrier not in data:
                data[carrier] = {'SUMINISTRO': {'EPB': np.zeros(numsteps),
                                             'NEPB': np.zeros(numsteps)},
                                 'PRODUCCION': {'INSITU': np.zeros(numsteps),
                                                'COGENERACION': np.zeros(numsteps)}}

            data[carrier][ctype][originoruse] = data[carrier][ctype][originoruse] + values
    return data

def readfactors(filename):
    """Read energy weighting factors data from file"""

    # TODO: check valid sources
    return pd.read_csv(filename,
                       skipinitialspace=True,
                       comment='#',
                       skip_blank_lines=True)

def formatIndicators(EP):
    """Format energy efficiency indicators as string from primary energy data

    In the context of the CTE regulations, this refers to primary energy values.
    """

    epren, epnren = EP.EP['ren'], EP.EP['nren']
    eparen, epanren = EP.EPpasoA['ren'], EP.EPpasoA['nren']
    total = epren + epnren
    totala = eparen + epanren
    txt = ("EP(step A)  , ren ={:>8.1f}, nren={:>8.1f}, tot ={:>8.1f}, RER ={:>8.2f}\n"
           "EP(step A+B), ren ={:>8.1f}, nren={:>8.1f}, tot ={:>8.1f}, RER ={:>8.2f}\n"
           ).format(eparen, epanren, totala, eparen / totala,
                    epren,  epnren, total, epren / total)
    return txt
