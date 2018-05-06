from math import *
from copy import deepcopy
from clappets.units import treeUnitConvert, SI_UNITS
from clappets.utils import parseFloat, roundit
from fluids.piping import nearest_pipe
from techclappets.mechanical.heater.combustion  import gasfuelProperties,airMoistureContent,wetAirRequired, excessAir, excessAir_pc
from techclappets.mechanical.heater.combustion  import flueMassicHeatContent, H2OformedEAcorrected, getEnthalphy, radiationLoss
from techclappets.mechanical.heater.combustion  import enthalpySteam, netThermalEfficiency, fuelEfficiency, grossThermalEfficiency, getHHV

def calculate(doc_original):
    doc = deepcopy(doc_original)
    treeUnitConvert(doc, doc['units'], SI_UNITS)
    doc['errors'] = []

    ups_load_kW = parseFloat(doc['input']['ups_load_kW']['_val'])
    lagging_pf = parseFloat(doc['input']['lagging_pf']['_val'])
    ups_efficiency = parseFloat(doc['input']['ups_efficiency']['_val'])
    design_margin = parseFloat(doc['input']['design_margin']['_val'])

    ups_load_kVA = ups_load_kW/lagging_pf
    ups_rating_kVA = (ups_load_kVA*100)/ups_efficiency
    ups_rating_kVA = ups_rating_kVA*(1+design_margin/100)

    doc['result'].update({'ups_rating_kVA':{'_val' : str(roundit(ups_rating_kVA))}})

    treeUnitConvert(doc, SI_UNITS, doc['units'], autoRoundOff=True)
    doc_original['result'].update(doc['result'])
    doc_original['errors'] = doc['errors']
    return True
