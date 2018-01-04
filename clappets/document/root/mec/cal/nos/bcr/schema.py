from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from clappets.core import sDocPrj, sXfld
from clappets.core import validator as vd
import CoolProp.CoolProp as CP

class schema_Spectrum(Schema):
    f63 = fields.Float(required=True)
    f125 = fields.Float(required=True)
    f250 = fields.Float(required=True)
    f500 = fields.Float(required=True)
    f1000 = fields.Float(required=True)
    f2000 = fields.Float(required=True)
    f4000 = fields.Float(required=True)
    f8000 = fields.Float(required=True)

class docInput(Schema):
    correction_options = ["overall","spectrum"]
    correction_option = fields.Nested(sXfld, validate=[vd.xString(), vd.xChoice(correction_options)], required=True)
    totalSpectrum = fields.Nested(schema_Spectrum)
    backgroundSpectrum = fields.Nested(schema_Spectrum)
    totalNoise = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])
    backgroundNoise = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])


class docResult(Schema):
    sourceSpectrum = fields.Nested(schema_Spectrum)
    sourceNoise = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
