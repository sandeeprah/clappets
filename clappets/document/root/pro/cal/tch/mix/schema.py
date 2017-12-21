from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from clappets.core import sDocPrj, sXfld
from clappets.core import validator as vd
import CoolProp.CoolProp as CP


class schema_fluidfraction(Schema):
    fluid_list = CP.FluidsList()
    fluid = fields.String(required=True, validate=validate.OneOf(choices=fluid_list))
    molefraction = fields.Float(required=True)
    class Meta:
        ordered = True

class docInput(Schema):
    mixture = fields.Nested(schema_fluidfraction, many=True)
    P = fields.Nested(sXfld, validate=[vd.xNumber(blank=False), vd.xDim('pressure')])
    T = fields.Nested(sXfld, validate=[vd.xNumber(blank=False), vd.xDim('temperature')])

class docResult(Schema):
    MW = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('molecularMass')])
    Pcritical = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('pressure')])
    Tcritical = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('temperature')])
    Pr = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])
    Tr = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])
    acentric = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])
    Z_PR = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])
    Z_LKP = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])
    Z_NO = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])
    Cp0mass = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificHeat')])
    Cv0mass = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificHeat')])
    Cp0molar = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificHeatMolar')])
    Cv0molar = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificHeatMolar')])


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
