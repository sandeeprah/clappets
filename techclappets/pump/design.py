import json
import sys
import math
import os
import fluids
import pandas as pd
from fluids.friction import friction_factor
from fluids.core import Reynolds, K_from_f, K_from_L_equiv, dP_from_K
from fluids.fittings import Hooper2K, entrance_sharp, exit_normal
from fluids.piping import nearest_pipe
from marshmallow import Schema, fields, pprint, pre_load, validate, validates_schema, ValidationError
from techclappets.core import noemptySchema, CalcOutput, check_positive, check_nonnegative
#from techclappets.pressuredrop.reducer import reducer_sizes, reducer_dimensions
from collections import OrderedDict
from techclappets.core import schema_units_used, schema_dquant

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def pump_types():
    pass

def pump_sizes(pump_type):
    pass

def pump_dimensions(pump_size):
    pass

class schema_input_pump_estimate(Schema):
    rho = fields.Nested(schema_dquant)
    Q = fields.Nested(schema_dquant)
    H = fields.Nested(schema_dquant)


class schema_request_pump_estimate(Schema):
    input = fields.Nested(schema_input_pump_estimate)
    units_used = fields.Nested(schema_units_used)

def pump_estimate(request_json):
    calculation_output = CalcOutput()
    schema_request = schema_request_pump_estimate()
    parsed_request = schema_request.load(request_json)
    if (len(parsed_request.errors) > 0 ):
        calculation_output.errors = parsed_request.errors.copy()
    else:
        rho = parsed_request.data['input']['rho']['_val']
        Q = parsed_request.data['input']['Q']['_val']
        H = parsed_request.data['input']['H']['_val']
        g = 9.81
        Phydraulic = rho*Q*g*H

        calculation_output.result.update({'Phydraulic' : {"_val":Phydraulic, "_dim":"power"}})

    return calculation_output
