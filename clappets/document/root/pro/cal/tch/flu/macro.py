import CoolProp.CoolProp as CP
from clappets.units import treeUnitConvert, SI_UNITS
from copy import deepcopy

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    fluid = doc['input']['fluid']['_val']
    P = float(doc['input']['P']['_val'])
    T = float(doc['input']['T']['_val'])
    result = {}

    phase = CP.PhaseSI('T',T, 'P',P, fluid)
    doc['result']['phase']['_val'] = phase


    try:
        phase = CP.PhaseSI('T',T, 'P',P, fluid)
    except:
        phase = ""
    finally:
        doc['result']['phase']['_val'] = phase

    try:
        MW = round(CP.PropsSI('M', fluid),5)
    except:
        MW =""
    finally:
        doc['result']['MW']['_val'] = MW

    try:
        Pcritical = round(CP.PropsSI('Pcrit', 'T',T, 'P',P, fluid),1)
    except:
        Pcritical = ""
    finally:
        doc['result']['Pcritical']['_val'] = Pcritical

    try:
        Tcritical = round(CP.PropsSI('Tcrit', 'T',T, 'P',P, fluid),1)
    except:
        Tcritical = ""
    finally:
        doc['result']['Tcritical']['_val'] = Tcritical

    try:
        Ptriple = round(CP.PropsSI('P_TRIPLE', 'T',T, 'P',P, fluid),1)
    except:
        Ptriple = ""
    finally:
        doc['result']['Ptriple']['_val'] = Ptriple


    try:
        Ttriple = round(CP.PropsSI('T_TRIPLE', 'T',T, 'P',P, fluid),1)
    except:
        Ttriple = ""
    finally:
        doc['result']['Ttriple']['_val'] = Ttriple


    try:
        acentric = round(CP.PropsSI('acentric', 'T',T, 'P',P, fluid),4)
    except:
        acentric = ""
    finally:
        doc['result']['acentric']['_val'] = acentric

    try:
        Z = round(CP.PropsSI('Z', 'T',T, 'P',P, fluid),4)
    except:
        Z = ""
    finally:
        doc['result']['Z']['_val'] = Z

    try:
        rho = round(CP.PropsSI('D', 'T',T, 'P',P, fluid),4)
        v = round(1/rho,4)
    except:
        rho = ""
        v = ""
    finally:
        doc['result']['rho']['_val'] = rho
        doc['result']['v']['_val'] = v


    try:
        h =  round(CP.PropsSI('H', 'T',T, 'P',P, fluid),1)
    except:
        h = ""
    finally:
        doc['result']['h']['_val'] = h


    try:
        u = round(CP.PropsSI('U', 'T',T, 'P',P, fluid),1)
    except:
        u = ""
    finally:
        doc['result']['u']['_val'] = u

    try:
        s = round(CP.PropsSI('S', 'T',T, 'P',P, fluid),1)
    except:
        s = ""
    finally:
        doc['result']['s']['_val'] = s


    try:
        gibbs = round(CP.PropsSI('G', 'T',T, 'P',P, fluid),1)
    except:
        gibbs = ""
    finally:
        doc['result']['gibbs']['_val'] = gibbs

    try:
        helmholtz = round(CP.PropsSI('Helmholtzmass', 'T',T, 'P',P, fluid),1)
    except:
        helmholtz = ""
    finally:
        doc['result']['helmholtz']['_val'] = helmholtz


    try:
        Cp = round(CP.PropsSI('Cpmass', 'T',T, 'P',P, fluid),1)
    except:
        Cp = ""
    finally:
        doc['result']['Cp']['_val'] = Cp


    try:
        Cv = round(CP.PropsSI('Cvmass', 'T',T, 'P',P, fluid),1)
    except:
        Cv = ""
    finally:
        doc['result']['Cv']['_val'] = Cv

    try:
        Cp_molar = round(CP.PropsSI('Cpmolar', 'T',T, 'P',P, fluid),1)
    except:
        Cp_molar = ""
    finally:
        doc['result']['Cp_molar']['_val'] = Cp_molar

    try:
        Cv_molar = round(CP.PropsSI('Cvmolar', 'T',T, 'P',P, fluid),1)
    except:
        Cv_molar = ""
    finally:
        doc['result']['Cv_molar']['_val'] = Cv_molar

    try:
        Cp0 = round(CP.PropsSI('Cp0mass', 'T',T, 'P',P, fluid),1)
    except:
        Cp0 = ""
    finally:
        doc['result']['Cp0']['_val'] = Cp0

    try:
        Prandtl = round(CP.PropsSI('Prandtl', 'T',T, 'P',P, fluid),4)
    except:
        Prandtl = ""
    finally:
        doc['result']['Prandtl']['_val'] = Prandtl

    try:
        dynViscosity = round(CP.PropsSI('viscosity', 'T',T, 'P',P, fluid),8)
    except:
        dynViscosity = ""
    finally:
        doc['result']['dynViscosity']['_val'] = dynViscosity


    try:
        conductivity  = round(CP.PropsSI('conductivity', 'T',T, 'P',P, fluid),8)
    except:
        conductivity = ""
    finally:
        doc['result']['conductivity']['_val'] = conductivity

    try:
        HH = CP.PropsSI('HH', 'T',T, 'P',P, fluid)
    except:
        HH=""
    finally:
        doc['result']['HH']['_val'] = HH


    try:
        PH = CP.PropsSI('PH', 'T',T, 'P',P, fluid)
    except:
        PH = ""
    finally:
        doc['result']['PH']['_val'] = PH

    try:
        GWP = CP.PropsSI('GWP100', 'T',T, 'P',P, fluid)
    except:
        GWP = ""
    finally:
        doc['result']['GWP']['_val'] = GWP

    try:
        ODP = CP.PropsSI('ODP', 'T',T, 'P',P, fluid)
    except:
        ODP = ""
    finally:
        doc['result']['ODP']['_val'] = ODP


    treeUnitConvert(doc, SI_UNITS, doc['units'])
    doc_original['result'].update(doc['result'])
    return True
