from math import *
from clappets.units import treeUnitConvert, SI_UNITS
from copy import deepcopy
from clappets.utils import roundit
from techclappets.electrical.phase import phase_parameters
from techclappets.Pump

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] =[]


    Q = float(doc['input']['Q']['_val'])
    H = float(doc['input']['H']['_val'])
    rho = float(doc['input']['rho']['_val'])
    mu = float(doc['input']['mu']['_val'])
    NPSHA = float(doc['input']['NPSHA']['_val'])
    Nss_limit = float(doc['input']['Nss_limit']['_val'])
    poles = int(doc['input']['poles']['_val'])
    design_type = doc['input']['design_type']['_val']


    try:
        eta = 0.8
        d2 = 90
        P = 200
        ns = 2.5
        nss = 23
        Ds = 2
        Dd = 4

    except Exception as e:
        doc['errors'].append(str(e))
        doc['errors'].append("Failed to calculate phase parameters. Check Inputs")


    eta = roundit(eta)
    d2 = roundit(d2)
    P = roundit(P)
    ns = roundit(ns)
    nss = roundit(nss)

    doc['result'].update({'eta':{'_val' : str(eta)}})
    doc['result'].update({'d2':{'_val' : str(d2)}})
    doc['result'].update({'P':{'_val' : str(P)}})
    doc['result'].update({'ns':{'_val' : str(ns)}})
    doc['result'].update({'nss':{'_val' : str(nss)}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']

    return True
