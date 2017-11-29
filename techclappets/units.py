from collections import OrderedDict
import json
import os
from marshmallow import Schema, fields, pprint, pre_load, validate, validates, ValidationError
from collections import OrderedDict


unitLib = OrderedDict({

    "length": {
        "dimtitle": "Length",
        "units": {
            "um": {
                "label": "μm",
                "cf": 1e-6,
                "off": 0
            },
            "mm": {
                "label": "mm",
                "cf": 1e-3,
                "off": 0
            },
            "m": {
                "label": "m",
                "cf": 1,
                "off": 0
            },
            "ft": {
                "label": "ft",
                "cf": 0.3048,
                "off": 0
            },
            "yd": {
                "label": "yd",
                "cf": 0.9144,
                "off": 0
            }
        }
    },

    "mass": {
        "dimtitle": "Mass",
        "units": {
            "ug": {
                "label": "μg",
                "cf": 1e-9,
                "off": 0
            },
            "mg": {
                "label": "mg",
                "cf": 1e-6,
                "off": 0
            },
            "g": {
                "label": "g",
                "cf": 1e-3,
                "off": 0
            },
            "kg": {
                "label": "kg",
                "cf": 1,
                "off": 0
            },
            "ton": {
                "label": "ton",
                "cf": 1e3,
                "off": 0
            },
            "lb": {
                "label": "lb",
                "cf": 0.453592,
                "off": 0
            }
        }
    },
    "time": {
        "dimtitle": "Time",
        "units": {
            "us": {
                "label": "μs",
                "cf": 1e-6,
                "off": 0
            },
            "ms": {
                "label": "ms",
                "cf": 1e-3,
                "off": 0
            },
            "s": {
                "label": "μs",
                "cf": 1,
                "off": 0
            },
            "min": {
                "label": "min",
                "cf": 60,
                "off": 0
            },
            "hr": {
                "label": "hr",
                "cf": 3600,
                "off": 0
            },
            "day": {
                "label": "day",
                "cf": 86400,
                "off": 0
            }
        }
    },
    "speed": {
        "dimtitle": "Speed",
        "units": {
            "m/s": {
                "label": "m/s",
                "cf": 1,
                "off": 0
            },
            "km/hr": {
                "label": "km/hr",
                "cf": 0.277778,
                "off": 0
            },
            "ft/s": {
                "label": "ft/s",
                "cf": 0.3048,
                "off": 0
            }
        }
    },
    "acceleration": {
        "dimtitle": "Acceleration",
        "units": {
            "m/s2": {
                "label": "m/s²",
                "cf": 1,
                "off": 0
            },
            "ft/s2": {
                "label": "ft/s²",
                "cf": 0.3048,
                "off": 0
            }
        }
    },

    "force": {
        "dimtitle": "Force",
        "units": {
            "N": {
                "label": "N",
                "cf": 1,
                "off": 0
            },
            "kN": {
                "label": "kN",
                "cf": 1e3,
                "off": 0
            },
            "lbf": {
                "label": "lbf",
                "cf": 4.44822,
                "off": 0
            }
        }
    },

    "energy": {
        "dimtitle": "Energy",
        "units": {
            "J": {
                "label": "J",
                "cf": 1,
                "off": 0
            },
            "kJ": {
                "label": "kJ",
                "cf": 1e3,
                "off": 0
            },
            "Btu": {
                "label": "Btu",
                "cf": 1055.06,
                "off": 0
            }
        }
    },

    "power": {
        "dimtitle": "Power",
        "units": {
            "W": {
                "label": "W",
                "cf": 1,
                "off": 0
            },
            "kW": {
                "label": "kW",
                "cf": 1e3,
                "off": 0
            },
            "hp": {
                "label": "hp",
                "cf": 746,
                "off": 0
            }
        }
    },

    "pressure": {
        "dimtitle": "Pressure",
        "units": {
            "Pa": {
                "label": "Pa",
                "cf": 1,
                "off": 0
            },
            "kPa": {
                "label": "kPa",
                "cf": 1e3,
                "off": 0
            },
            "MPa": {
                "label": "MPa",
                "cf": 1e6,
                "off": 0
            },
            "bar": {
                "label": "bar",
                "cf": 1e5,
                "off": 0
            },
            "atm": {
                "label": "atm",
                "cf": 101325,
                "off": 0
            },
            "kg/cm2": {
                "label": "kg/cm²",
                "cf": 98066.5,
                "off": 0
            }
        }
    },

    "temperature": {
        "dimtitle": "Temperature",
        "units": {
            "K": {
                "label": "K",
                "cf": 1,
                "off": 0
            },
            "C": {
                "label": "°C",
                "cf": 1,
                "off": 273.15
            },
            "F": {
                "label": "°F",
                "cf": 5 / 9,
                "off": -32 * 5 / 9 + 273.15,
            },
            "R": {
                "label": "°R",
                "cf": 5 / 9,
                "off": 0
            }
        }
    },

    "flow": {
        "dimtitle": "Flow",
        "units": {
            "m3/s": {
                "label": "m³/s",
                "cf": 1,
                "off": 0
            },
            "m3/min": {
                "label": "m³/min",
                "cf": 1 / 60,
                "off": 0
            },
            "m3/hr": {
                "label": "m³/hr",
                "cf": 1 / 3600,
                "off": 0
            },
            "lpm": {
                "label": "lpm",
                "cf": 1.6667e-5,
                "off": 0
            },
            "usgpm": {
                "label": "usgpm",
                "cf": 6.309e-5,
                "off": 0
            },
            "bbl/day": {
                "label": "bbl/day",
                "cf": 1.840e-6,
                "off": 0
            },
        }
    },

    "density": {
        "dimtitle": "Density",
        "units": {
            "kg/m3": {
                "label": "kg/m³",
                "cf": 1,
                "off": 0
            },
            "g/cm3": {
                "label": "g/cm³",
                "cf": 1e3,
                "off": 0
            },
            "lb/ft3": {
                "label": "lb/ft³",
                "cf": 16.018,
                "off": 0
            }
        }
    },

    "dynViscosity": {
        "dimtitle": "Dynamic Viscosity",
        "units": {
            "Pa.s": {
                "label": "Pa.s",
                "cf": 1,
                "off": 0
            },
            "mPa.s": {
                "label": "mPa.s",
                "cf": 1e-3,
                "off": 0
            },
            "cP": {
                "label": "cP",
                "cf": 1e-3,
                "off": 0
            },
        }
    }
})

def get_dimensions():
    dim_list = []
    for key in unitLib:
        dim_list.append(key)

    return dim_list

def get_units(dimension):
    units_list = []
    if dimension in unitLib:
        units = unitLib[dimension]['units']
        for key in units:
            units_list.append(key)

    return units_list
