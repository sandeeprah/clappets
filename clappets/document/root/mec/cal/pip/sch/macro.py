import math
from copy import deepcopy
from clappets.units import treeUnitConvert, SI_UNITS
from clappets.utils import parseFloat, roundit
from fluids.piping import nearest_pipe

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)

    doc['errors'] = []

    calculation_option = doc['input']['calculation_option']['_val']


    try:
        if (calculation_option=='NPS'):
            NPS = parseFloat(doc['input']['NPS']['_val'])
            Schedule = doc['input']['Schedule']['_val']
            nps, di, do, t = nearest_pipe(NPS = NPS, schedule = Schedule)
        if (calculation_option=='Di'):
            Di = parseFloat(doc['input']['Di']['_val'])
            Schedule = doc['input']['Schedule']['_val']
            nps, di, do, t = nearest_pipe(Di = Di, schedule = Schedule)
        if (calculation_option=='Do'):
            Do = parseFloat(doc['input']['Do']['_val'])
            Schedule = doc['input']['Schedule']['_val']
            nps, di, do, t = nearest_pipe(Do = Do, schedule = Schedule)
    except Exception as e:
        doc['errors'].append(str(e))
        nps = math.nan
        di = math.nan
        do = math.nan
        t = math.nan


    doc['result']['NPS']['_val'] = str(roundit(nps))
    doc['result']['Di']['_val'] = str(roundit(di))
    doc['result']['Do']['_val'] = str(roundit(do))
    doc['result']['t']['_val'] = str(roundit(t))

    treeUnitConvert(doc, SI_UNITS, doc['units'])
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']
    return True
