import CoolProp.CoolProp as CP
from clappets.units import treeUnitConvert, SI_UNITS
from techclappets.thermochem.thermochem_utils import mixture_props
from copy import deepcopy

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)

    mixture = doc['input']['mixture']
    P = float(doc['input']['P']['_val'])
    T = float(doc['input']['T']['_val'])
    mixprops = mixture_props(mixture,P=P,T=T)

    doc['result']['MW']['_val'] = str(mixprops['MW'])
    doc['result']['Pcritical']['_val'] = str(mixprops['Pcritical'])
    doc['result']['Tcritical']['_val'] = str(mixprops['Tcritical'])
    doc['result']['Pr']['_val'] = str(mixprops['Pr'])
    doc['result']['Tr']['_val'] = str(mixprops['Tr'])
    doc['result']['acentric']['_val'] = str(mixprops['acentric'])
    doc['result']['Z_PR']['_val'] = str(mixprops['Z_PR'])
    doc['result']['Z_LKP']['_val'] = str(mixprops['Z_LKP'])
    doc['result']['Z_NO']['_val'] = str(mixprops['Z_NO'])
    doc['result']['Cp0mass']['_val'] = str(mixprops['Cp0mass'])
    doc['result']['Cv0mass']['_val'] = str(mixprops['Cv0mass'])
    doc['result']['Cp0molar']['_val'] = str(mixprops['Cp0molar'])
    doc['result']['Cv0molar']['_val'] = str(mixprops['Cv0molar'])

    treeUnitConvert(doc, SI_UNITS, doc['units'])
    doc_original['result'].update(doc['result'])
    return True
