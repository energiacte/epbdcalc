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

"""Utilidades auxiliares.

Cálculos vectorizados
"""

# Vector utilities --------------------------------------------
def vecvecmin(vec1, vec2):
    """Elementwise minimum min res[i] = min(vec1[i], vec2[i])"""
    return [min(v1, v2) for v1, v2 in zip(vec1, vec2)]

def vecvecsum(args):
    """Elementwise sum res[i] = vec1[i] + vec2[i]"""
    return [sum(valsi) for valsi in zip(*args)]

def vecvecdif(vec1, vec2):
    """Elementwise difference res[i] = vec1[i] - vec2[i]"""
    return [v1 - v2 for v1, v2 in zip(vec1, vec2)]

def vecvecmul(vec1, vec2):
    """Elementwise multiplication res[i] = vec1[i] * vec2[i]"""
    return [v1 * v2 for v1, v2 in zip(vec1, vec2)]

def veckmul(vec1, k):
    """Multiply vector by scalar"""
    return [v1 * k for v1 in vec1]
# --------------------------------------------------------------
