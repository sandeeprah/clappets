from clappets.units import treeUnitConvert, SI_UNITS
from techclappets.mechanical.pump import motor_syncspeed, specific_speed, efficiency_overall, head_coefficient, nozzle_size, getNPSHR, model_select, pump_power

doc_original = {
  "units": {
    "flow":"m3/hr",
    "length":"m",
    "density":"kg/m3",
    "power": "kW",
    "dynViscosity":"cP"
  },

  "input": {
    "Q" : {"_val":"100", "_dim":"flow"},
    "H": {"_val":"40", "_dim":"length"},
    "rho": {"_val":"1000","_dim":"density"},
    "mu": {"_val":"1","_dim":"dynViscosity"},
    "NPSHA": {"_val":"9", "_dim":"length"},
    "Nss_limit": {"_val":"20"},
    "design_type": {"_val":"OH"},
    "poles": {"_val":"2"},
    "frequency": {"_val":"50"}
  },

  "result": {
    "eta": {"_val":""},
    "d2": {"_val":"", "_dim":"length"},
    "P": {"_val":"", "_dim":"power"},
    "Nq":{"_val":""},
    "NPSHR": {"_val":"", "_dim":"length"},
    "selected_model":{"_val":""}
  },

  "errors": []
}


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
frequency = float(doc['input']['frequency']['_val'])
design_type = doc['input']['design_type']['_val']
