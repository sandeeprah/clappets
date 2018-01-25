import math
from copy import deepcopy
from clappets.units import treeUnitConvert, SI_UNITS
from clappets.utils import parseFloat, roundit
from techclappets.noise import noise_utils

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)

    unfilteredSpectrum = doc['input']['unfilteredSpectrum']
    filteredSpectrum = noise_utils.aWeightedSpectrum(spectrum = unfilteredSpectrum)
    totalAudibleNoise = noise_utils.spectrumTotal(filteredSpectrum)

    doc['result']['filteredSpectrum'] = filteredSpectrum
    doc['result'].update({'totalAudibleNoise':{'_val' : str(totalAudibleNoise)}})

    treeUnitConvert(doc, SI_UNITS, doc['units'])
    doc_original['result'].update(doc['result'])
    return True
