import math
from copy import deepcopy
from clappets.units import treeUnitConvert, SI_UNITS
from clappets.utils import parseFloat, roundit
from techclappets.noise import noise_utils

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)

    calculation_option = doc['input']['calculation_option']['_val']

    doc['result']['PWL']['_val'] = ""
    doc['result']['SPL']['_val'] = ""
    doc['result']['distance']['_val'] = ""


    if (calculation_option=='calcSPL'):
        PWL = parseFloat(doc['input']['PWL']['_val'])
        distance = parseFloat(doc['input']['distance']['_val'])
        Q = parseFloat(doc['input']['Q']['_val'])

        SPL = noise_utils.getSPL(PWL,distance,Q)
        doc['result']['SPL']['_val'] = str(SPL)

    if (calculation_option=='calcPWL'):
        SPL = parseFloat(doc['input']['SPL']['_val'])
        distance = parseFloat(doc['input']['distance']['_val'])
        Q = parseFloat(doc['input']['Q']['_val'])

        PWL = noise_utils.getPWL(SPL,distance,Q)
        doc['result']['PWL']['_val'] = str(PWL)

    if (calculation_option=='calcDistance'):
        PWL = parseFloat(doc['input']['PWL']['_val'])
        SPL = parseFloat(doc['input']['SPL']['_val'])
        Q = parseFloat(doc['input']['Q']['_val'])

        distance = noise_utils.getDistance(PWL,SPL,Q)
        doc['result']['distance']['_val'] = str(distance)


    treeUnitConvert(doc, SI_UNITS, doc['units'])
    doc_original['result'].update(doc['result'])
    return True
