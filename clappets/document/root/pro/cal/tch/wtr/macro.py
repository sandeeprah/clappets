import CoolProp.CoolProp as CP
from clappets.units import treeUnitConvert, SI_UNITS
from copy import deepcopy

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)

    state = doc['input']['state']['_val']

    if (state=='Saturated_P'):
        P = float(doc['input']['P']['_val'])
        Q = float(doc['input']['Q']['_val'])
        phase = CP.PhaseSI('P', P, 'Q', Q, 'Water')
        Tsat = round(CP.PropsSI('T','P', P, 'Q', Q, 'Water'),1)
        rho = round(CP.PropsSI('D','P', P, 'Q', Q, 'Water'),4)
        v = round(1/rho,4)
        h = round(CP.PropsSI('H','P', P, 'Q', Q, 'Water'),1)
        u = round(CP.PropsSI('U','P', P, 'Q', Q, 'Water'),1)
        s = round(CP.PropsSI('S','P', P, 'Q', Q, 'Water'),1)
        doc['result']['Tsat']['_val'] = str(Tsat)
        doc['result']['Psat']['_val'] = ""

    if (state=='Saturated_T'):
        T = float(doc['input']['T']['_val'])
        Q = float(doc['input']['Q']['_val'])
        phase = CP.PhaseSI('T', T, 'Q', Q, 'Water')
        Psat = round(CP.PropsSI('P','T', T, 'Q', Q, 'Water'),1)
        rho = round(CP.PropsSI('D','T', T, 'Q', Q, 'Water'),4)
        v = round(1/rho,4)
        h = round(CP.PropsSI('H','T', T, 'Q', Q, 'Water'),1)
        u = round(CP.PropsSI('U','T', T, 'Q', Q, 'Water'),1)
        s = round(CP.PropsSI('S','T', T, 'Q', Q, 'Water'),1)
        doc['result']['Psat']['_val'] = str(Psat)
        doc['result']['Tsat']['_val'] = ""

    if (state=='Superheated_or_Compressed'):
        T = float(doc['input']['T']['_val'])
        P = float(doc['input']['P']['_val'])
        phase = CP.PhaseSI('T', T, 'P', P, 'Water')
        rho = round(CP.PropsSI('D','T', T, 'P', P, 'Water'),4)
        v = round(1/rho,1)
        h = round(CP.PropsSI('H','T', T, 'P', P, 'Water'),1)
        u = round(CP.PropsSI('U','T', T, 'P', P, 'Water'),1)
        s = round(CP.PropsSI('S','T', T, 'P', P, 'Water'),1)
        doc['result']['Psat']['_val'] = ""
        doc['result']['Tsat']['_val'] = ""


    doc['result']['phase']['_val'] = phase
    doc['result']['rho']['_val'] = str(rho)
    doc['result']['v']['_val'] = str(v)
    doc['result']['h']['_val'] = str(h)
    doc['result']['u']['_val'] = str(u)
    doc['result']['s']['_val'] = str(s)

    treeUnitConvert(doc, SI_UNITS, doc['units'])
    doc_original['result'].update(doc['result'])
    return True
