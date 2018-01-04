from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from clappets.core import sDocPrj, sXfld
from clappets.core import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    calculation_options = ["NPS","Di","Do"]
    calculation_option = fields.Nested(sXfld, validate=[vd.xString(), vd.xChoice(calculation_options)], required=True)
    Schedule = fields.Nested(sXfld, validate=[vd.xString()], required=True)
    allowed_NPS = [0.125, 0.25, 0.375, 0.5, 0.75, 1, 1.25, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36]
    allowed_NPS = [str(item) for item in allowed_NPS]
    NPS = fields.Nested(sXfld, validate=[vd.xNumber(blank=True),vd.xChoice(allowed_NPS)])
    Di = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('length')])
    Do = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('length')])


class docResult(Schema):
    NPS = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)],)
    Di = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('length')])
    Do = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('length')])
    t = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('length')])


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
