import math
import CoolProp.CoolProp as CP
from clappets.units import treeUnitConvert, SI_UNITS
from clappets.utils import parseFloat, roundit
from copy import deepcopy

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)

    calculation_option = doc['input']['calculation_option']['_val']
    Tdb = parseFloat(doc['input']['Tdb']['_val'])
    P = parseFloat(doc['input']['P']['_val'])

    try:
        if (calculation_option=='Tdb_RH_P'):
            RH = parseFloat(doc['input']['RH']['_val'])
        if (calculation_option=='Tdb_Twb_P'):
            Twb = parseFloat(doc['input']['Twb']['_val'])
            RH = CP.HAPropsSI('R', 'Tdb', Tdb, 'P', P, 'Twb', Twb)
        if (calculation_option=='Tdb_Tdp_P'):
            Tdp = parseFloat(doc['input']['Tdp']['_val'])
            RH = CP.HAPropsSI('R', 'Tdb', Tdb, 'P', P, 'Tdp', Tdp)
        if (calculation_option=='Tdb_Tdp_P'):
            Tdp = parseFloat(doc['input']['Tdp']['_val'])
            RH = CP.HAPropsSI('R', 'Tdb', Tdb, 'P', P, 'Tdp', Tdp)
        if (calculation_option == 'Tdb_W_P'):
            W = parseFloat(doc['input']['W']['_val'])
            RH = CP.HAPropsSI('R', 'Tdb', Tdb, 'P', P, 'W', W)
        if (calculation_option == 'Tdb_h_P'):
            h = parseFloat(doc['input']['h']['_val'])
            RH = CP.HAPropsSI('R', 'Tdb', Tdb, 'P', P, 'H', h)
    except Exception:
        RH = math.nan


    try:
        Twb = CP.HAPropsSI('Twb','Tdb', Tdb, 'P', P, 'R', RH)
        Tdp = CP.HAPropsSI('Tdp','Tdb', Tdb, 'P', P, 'R', RH)
    except Exception:
        Twb = math.nan
        Tdp = math.nan 

    try:
        v = CP.HAPropsSI('Vha','Tdb', Tdb, 'P', P, 'R', RH)
        rho = 1/v
    except Exception:
        v = math.nan
        rho = math.nan

    try:
        W = CP.HAPropsSI('W','Tdb', Tdb, 'P', P, 'R', RH)
    except Exception:
        W = math.nan

    try:
        h = CP.HAPropsSI('H','Tdb', Tdb, 'P', P, 'R', RH)
        u = CP.HAPropsSI('U','Tdb', Tdb, 'P', P, 'R', RH)
        s = CP.HAPropsSI('S','Tdb', Tdb, 'P', P, 'R', RH)
    except Exception:
        h = math.nan
        u = math.nan
        s = math.nan

    try:
        Cp = CP.HAPropsSI('cp','Tdb', Tdb, 'P', P, 'R', RH)
        Cp_ha = CP.HAPropsSI('cp_ha','Tdb', Tdb, 'P', P, 'R', RH)
    except Exception:
        Cp = math.nan
        Cp_ha = math.nan


    RH = roundit(RH, 4)
    Twb = roundit(Twb, 1)
    Tdp = roundit(Tdp, 1)
    W = roundit(W,4)
    rho = roundit(rho,4)
    v = roundit(v,4)
    h = roundit(h,4)
    u = roundit(u,4)
    s = roundit(s,4)
    Cp = roundit(Cp,4)
    Cp_ha = roundit(Cp_ha,4)

    doc['result']['RH']['_val'] = str(RH)
    doc['result']['Twb']['_val'] = str(Twb)
    doc['result']['Tdp']['_val'] = str(Tdp)
    doc['result']['W']['_val'] = str(W)
    doc['result']['rho']['_val'] = str(rho)
    doc['result']['v']['_val'] = str(v)
    doc['result']['h']['_val'] = str(h)
    doc['result']['u']['_val'] = str(u)
    doc['result']['s']['_val'] = str(s)
    doc['result']['Cp']['_val'] = str(Cp)
    doc['result']['Cp_ha']['_val'] = str(Cp_ha)

    treeUnitConvert(doc, SI_UNITS, doc['units'])
    doc_original['result'].update(doc['result'])
    return True
