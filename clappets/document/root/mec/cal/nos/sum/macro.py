import math
from copy import deepcopy
from clappets.units import treeUnitConvert, SI_UNITS
from clappets.utils import parseFloat, roundit
from techclappets.noise import noise_utils

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)

    noiseLevelList = doc['input']['noiseLevelList']
    noiseTotal = noise_utils.addNoise(noiseLevelList=noiseLevelList)

    doc['result']['noiseTotal']['_val'] = str(noiseTotal)

    treeUnitConvert(doc, SI_UNITS, doc['units'])
    doc_original['result'].update(doc['result'])
    return True
