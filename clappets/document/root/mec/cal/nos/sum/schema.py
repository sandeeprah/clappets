from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from clappets.core import sDocPrj, sXfld
from clappets.core import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    noiseLevelList = fields.List(fields.Float, required=True)

class docResult(Schema):
    noiseTotal = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
