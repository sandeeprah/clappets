from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from clappets.core import sDocPrj, sXfld
from clappets.core import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    source_options = ["point","line","wall"]
    source_option = fields.Nested(sXfld, validate=[vd.xString(), vd.xChoice(source_options)], required=True)
    SPL1 = fields.Nested(sXfld, validate=[vd.xNumber(blank=False)], required=True)
    R1 = fields.Nested(sXfld, validate=[vd.xNumber(blank=False), vd.xDim('length')],required=True)
    R2 = fields.Nested(sXfld, validate=[vd.xNumber(blank=False), vd.xDim('length')],required=True)
    width = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('length')])
    height = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('length')])



class docResult(Schema):
    SPL2 = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
