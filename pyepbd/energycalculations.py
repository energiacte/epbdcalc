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


# origin for produced energy must be either 'INSITU' or 'COGENERACION'
VALIDORIGINS = ['INSITU', 'COGENERACION']

def components_t_forcarrier(vdata, k_rdel):
    """Calculate energy components for each time step from energy carrier data

    This follows the EN15603 procedure for calculation of delivered and
    exported energy components.
    """

    # Energy used by technical systems for EPB services, for each time step
    E_EPus_t = vdata['CONSUMO']['EPB']
    # Energy used by technical systems for non-EPB services, for each time step
    E_nEPus_t = vdata['CONSUMO']['NEPB']
    numsteps = E_EPus_t.size # TODO: numpy method

    # (Electricity) produced on-site and inside the assessment boundary, by origin
    E_pr_t_byorigin = vdata['PRODUCCION']
    # (Electric) energy produced on-site and inside the assessment boundary, for each time step (formula 23)
    E_pr_t = vecvecsum([E_pr_t_byorigin[origin] for origin in VALIDORIGINS])

    # Produced energy from all origins for EPB services for each time step (formula 24)
    E_pr_used_EPus_t = vecvecmin(E_EPus_t, E_pr_t)

    ## Exported energy for each time step (produced energy not consumed in EPB uses) (formula 25)
    E_exp_t = vecvecdif(E_pr_t, E_pr_used_EPus_t)

    # Exported energy by production origin for each time step, weigthing done by produced energy
    F_exp_t = [E_exp_t[i] / E_pr_ti if E_pr_ti != 0 else 0 for (i, E_pr_ti) in enumerate(E_pr_t)]
    E_exp_t_byorigin = {origin: vecvecmul(E_pr_t_byorigin[origin], F_exp_t) for origin in VALIDORIGINS}

    # Exported (electric) energy used for non-EPB uses for each time step (formula 26)
    E_exp_used_nEPus_t = vecvecmin(E_exp_t, E_nEPus_t)
    # Exported energy used for non-EPB services for each time step, by origin, weighting done by exported energy
    F_exp_used_nEPus_t = [E_exp_used_nEPus_t[i] / E_exp_ti if E_exp_ti !=0 else 0 for (i, E_exp_ti) in enumerate(E_exp_t)]
    E_exp_used_nEPus_t_byorigin = {origin: vecvecmul(E_exp_t_byorigin[origin], F_exp_used_nEPus_t) for origin in VALIDORIGINS}

    # Exported energy not used for any service for each time step (formula 27)
    # Note: this is later affected by k_rdel for redelivery and k_exp for exporting
    E_exp_nused_t = vecvecdif(E_exp_t, E_exp_used_nEPus_t)
    # Exported energy not used for any service for each time step, by origin, weighting done by exported energy
    F_exp_nused_t = [E_exp_nused_t[i] / E_exp_ti if E_exp_ti !=0 else 0 for (i, E_exp_ti) in enumerate(E_exp_t)]
    E_exp_nused_t_byorigin = {origin: vecvecmul(E_exp_t_byorigin[origin], F_exp_nused_t) for origin in VALIDORIGINS}

    # Annual exported energy not used for any service (formula 28)
    E_exp_nused_an = sum(E_exp_nused_t)

    # Delivered (electric) energy for each time step (formula 29)
    E_del_t = vecvecdif(E_EPus_t, E_pr_used_EPus_t)
    # Annual delivered (electric) energy for EPB uses (formula 30)
    E_del_an = sum(E_del_t)

    # Annual temporary exported (electric) energy (formula 31)
    E_exp_tmp_an = min(E_exp_nused_an, E_del_an)

    # Temporary exported energy for each time step (formula 32)
    # E_exp_tmp_t = np.zeros(numsteps) if (E_exp_nused_an == 0) else E_exp_tmp_an * E_exp_nused_t / E_exp_nused_an # not used

    # Redelivered energy for each time step (formula 33)
    if E_del_an == 0:
        E_del_rdel_t = [0] * numsteps
    else:
        E_del_rdel_t = [E_exp_tmp_an * E_del_ti / E_del_an for E_del_ti in E_del_t]
    # Annual redelivered energy
    # E_del_rdel_an = sum(E_del_rdel_t) # not used

    # Exported (electric) energy to the grid for each time step (formula 34)
    # E_exp_grid_t = vecdif(E_exp_nused_t, E_exp_tmp_t) # not used

    # Annual exported (electric) energy to the grid (formula 35)
    E_exp_grid_an = E_exp_nused_an - E_exp_tmp_an
    # Energy exported to grid, by origin, weighting done by exported and not used energy
    F_exp_grid_an = E_exp_grid_an / E_exp_nused_an if E_exp_nused_an != 0 else 0
    E_exp_grid_t_byorigin = {origin: veckmul(E_exp_nused_t_byorigin[origin], F_exp_grid_an) for origin in VALIDORIGINS}

    # (Electric) energy delivered by the grid for each time step (formula 36)
    # E_del_grid_t = vecdif(E_del_t, E_del_rdel_t)  # not used

    # Annual (electric) energy delivered by the grid (formula 37)
    # E_del_grid_an = E_del_an - E_del_rdel_an # not used

    # Corrected delivered energy for each time step (formula 38)
    E_del_t_corr = [E_del_ti - k_rdel * E_del_rdel_t[i] for (i, E_del_ti) in enumerate(E_del_t)]

    # Corrected temporary exported energy (formula 39)
    # E_exp_tmp_t_corr = [E_exp_tmp_ti * (1 - k_rdel) for E_exp_tmp_ti in E_exp_tmp_t] # not used

    components_t = {'grid': {'input': sum(E_del_t_corr)}} # Scalar

    components_t.update({origin: {'input': E_pr_t_byorigin[origin],
                                  'to_nEPB': E_exp_used_nEPus_t_byorigin[origin],
                                  'to_grid': E_exp_grid_t_byorigin[origin]} for origin in VALIDORIGINS})
    return components_t

def components_an_forcarrier(components_t):
    """Calculate annual energy composition by carrier from time step components"""
    components_an = {}
    for origin in components_t: # This is grid + VALIDORIGINS
        components_an[origin] = {}
        components_t_byorigin = components_t[origin]
        for use in components_t_byorigin:
            try: # we get a list
                sumforuse = sum(components_t_byorigin[use])
            except TypeError: # if origin == 'grid' and use == 'input' we get an scalar
                sumforuse = components_t_byorigin[use]
            # TODO we need to know numsteps to make this shortcut work
            # TODO some input data doesn't have timestep data and this fails
            # try:
            #     components_an[origin][use] = sumforuse if abs(sumforuse) > 0.1 else np.zeros(numsteps)
            # except:
            #     print origin, use, sumforuse, components_an
            if abs(sumforuse) > 0.1:
                components_an[origin][use] = sumforuse
    return components_an

def energycomponents(energydata, k_rdel):
    "Calculate timestep and annual energy composition by carrier from input data"

    components = {}
    for carrier in energydata:
        bal_t = components_t_forcarrier(energydata[carrier], k_rdel)
        bal_an = components_an_forcarrier(bal_t)
        components[carrier] = {'temporal': bal_t,
                               'anual': bal_an}
    return components

####################################################

def delivered_weighted_energy_stepA(components, fp):
    """Total delivered (or produced) weighted energy entering the assessment boundary in step A

    Energy is weighted depending on its origin (by source or grid).

    This function returns a data structure with keys 'ren' and 'nren' corresponding
    to the renewable and not renewable share of this weighted energy (step A).
    """

    delivered_wenergy_stepA = {'ren': 0.0, 'nren': 0.0}
    fpA = fp[(fp.uso=='input') & (fp.step=='A')] # TODO: dataframe
    #fpA = [fpi for fpi in fp if fpi.uso=='input' and fpi.step=='A']
    for source in components:
        origins = components[source]
        if 'input' in origins:
            factor_paso_A = fpA[(fpA.fuente==source)][['ren', 'nren']].iloc[0] # TODO: dataframe
            delivered_wenergy_stepA = {'ren': delivered_wenergy_stepA['ren'] + factor_paso_A['ren'] * origins['input'],
                                       'nren': delivered_wenergy_stepA['nren'] + factor_paso_A['nren'] * origins['input'] }
    return delivered_wenergy_stepA

def exported_weighted_energy_stepA(components, fpA):
    """Total exported weighted energy going outside the assessment boundary in step A

    Energy is weighted depending on its destination (non-EPB uses or grid).

    This function returns a data structure with keys 'ren' and 'nren' corresponding
    to the renewable and not renewable share of this weighted energy (step A).
    """

    to_nEPB = {'ren': 0.0, 'nren': 0.0}
    to_grid = {'ren': 0.0, 'nren': 0.0}
    fpAnEPB = fpA[(fpA.uso=='to_nEPB')] # TODO: dataframe
    fpAgrid = fpA[(fpA.uso=='to_nEPB')] # TODO: dataframe
    for source in components:
        destinations = components[source]
        if 'to_nEPB' in destinations:
            fp_tmp = fpAnEPB[fpAnEPB.fuente==source][['ren', 'nren']].iloc[0] # TODO: dataframe
            to_nEPB = { 'ren': to_nEPB['ren'] + fp_tmp['ren'] * destinations['to_nEPB'],
                        'nren': to_nEPB['nren'] + fp_tmp['nren'] * destinations['to_nEPB'] } # TODO: numpy

        if 'to_grid' in destinations:
            fp_tmp = fpAgrid[fpAgrid.fuente== source][['ren', 'nren']].iloc[0] # TODO: dataframe
            to_grid = { 'ren': to_grid['ren'] + fp_tmp['ren'] * destinations['to_grid'],
                        'nren': to_grid['nren'] + fp_tmp['nren'] * destinations['to_grid'] } # TODO: numpy

    exported_energy_stepA = { 'ren': to_nEPB['ren'] + to_grid['ren'],
                              'nren': to_nEPB['nren'] + to_grid['nren'] } # TODO: numpy?
    return exported_energy_stepA

def gridsavings_stepB(components, fp, k_exp):
    """Avoided weighted energy resources in the grid due to exported electricity

    The computation is done for a single energy carrier, considering the
    exported energy used for non-EPB uses (to_nEPB) and the energy exported
    to the grid (to_grid), each with its own weigting factors and k_exp.

    This function returns a data structure with keys 'ren' and 'nren' corresponding
    to the renewable and not renewable share of this weighted energy (step B).
    """

    to_nEPB = {'ren': 0.0, 'nren': 0.0}
    to_grid = {'ren': 0.0, 'nren': 0.0}
    fpA = fp[fp.step=='A'] # TODO: dataframe
    fpB = fp[fp.step=='B'] # TODO: dataframe
    fpAnEPB,fpAgrid = fpA[fpA.uso=='to_nEPB'], fpA[fpA.uso=='to_grid'] # TODO: dataframe
    fpBnEPB,fpBgrid = fpB[fpB.uso=='to_nEPB'], fpB[fpB.uso=='to_grid'] # TODO: dataframe

    for source in components:
        destinations = components[source]
        if 'to_nEPB' in destinations:
            fpA_tmp= fpAnEPB[fpAnEPB.fuente==source][['ren','nren']].iloc[0] # TODO: dataframe
            fpB_tmp= fpBnEPB[fpBnEPB.fuente==source][['ren','nren']].iloc[0] # TODO: dataframe
            to_nEPB = { 'ren': to_nEPB['ren'] + (fpB_tmp['ren'] - fpA_tmp['ren']) * destinations['to_nEPB'],
                        'nren': to_nEPB['nren'] + (fpB_tmp['nren'] - fpA_tmp['nren']) * destinations['to_nEPB'] } # TODO: dataframe
        if 'to_grid' in destinations:
            fpA_tmp= fpAgrid[fpAgrid.fuente==source][['ren','nren']].iloc[0] # TODO: dataframe
            fpB_tmp= fpBgrid[fpBgrid.fuente==source][['ren','nren']].iloc[0] # TODO: dataframe
            to_grid = { 'ren': to_grid['ren'] + (fpB_tmp['ren'] - fpA_tmp['ren']) * destinations['to_grid'],
                        'nren': to_grid['nren'] + (fpB_tmp['nren'] - fpA_tmp['nren']) * destinations['to_grid'] } # TODO: dataframe

    gridsavings = {'ren': k_exp * (to_nEPB['ren'] + to_grid['ren']), 'nren': k_exp * (to_nEPB['nren'] + to_grid['nren'])} # TODO: numpy?
    return gridsavings

def weighted_energy(data, k_rdel, fp, k_exp):
    """Total weighted energy (step A + B) = used energy (step A) - saved energy (step B)

    The energy saved to the grid due to exportation (step B) is substracted
    from the the energy balance in the asessment boundary AB (step A).
    This is  computed for all energy carrier and all energy sources.

    This function returns a data structure with keys 'ren' and 'nren'
    corresponding to the renewable and not renewable parts of the balance.

    In the context of the CTE regulation weighted energy corresponds to
    primary energy.
    """
    components = energycomponents(data, k_rdel)
    EPA = {'ren': 0.0, 'nren': 0.0}
    EPB = {'ren': 0.0, 'nren': 0.0}

    for carrier in components:
        fp_cr = fp[fp.vector==carrier] # TODO: dataframe
        components_cr_an = components[carrier]['anual']

        delivered_wenergy_stepA = delivered_weighted_energy_stepA(components_cr_an, fp_cr)
        exported_wenergy_stepA = exported_weighted_energy_stepA(components_cr_an, fp_cr)
        weighted_energy_stepA = { 'ren': delivered_wenergy_stepA['ren'] - exported_wenergy_stepA['ren'],
                                  'nren': delivered_wenergy_stepA['nren'] - exported_wenergy_stepA['nren'] } # TODO: dataframe

        gsavings_stepB = gridsavings_stepB(components_cr_an, fp_cr, k_exp)
        weighted_energy_stepAB = { 'ren': weighted_energy_stepA['ren'] - gsavings_stepB['ren'],
                                   'nren': weighted_energy_stepA['nren'] - gsavings_stepB['nren'] } # TODO: dataframe

        EPA = {'ren': EPA['ren'] + weighted_energy_stepA['ren'], 'nren': EPA['nren'] + weighted_energy_stepA['nren']} # TODO: dataframe
        EPB = {'ren': EPB['ren'] + weighted_energy_stepAB['ren'], 'nren': EPB['nren'] + weighted_energy_stepAB['nren']} # TODO: dataframe

    return {'EP': EPB, 'EPpasoA': EPA}
