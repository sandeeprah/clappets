from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from clappets.core import sDocPrj, sXfld
from clappets.core import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    T = fields.Nested(sXfld, validate=[vd.xNumber(), vd.xDim('temperature')])
    MW = fields.Nested(sXfld, validate=[vd.xNumber(), vd.xDim('molecularMass')])
    mu = fields.Nested(sXfld, validate=[vd.xNumber(), vd.xDim('dynViscosity')])
    gamma = fields.Nested(sXfld, validate=[vd.xNumber()])
    Z = fields.Nested(sXfld, validate=[vd.xNumber()])
    P1 = fields.Nested(sXfld, validate=[vd.xNumber(), vd.xDim('pressure')])
    P2 = fields.Nested(sXfld, validate=[vd.xNumber(), vd.xDim('pressure')])
    Q = fields.Nested(sXfld, validate=[vd.xNumber(), vd.xDim('flow')])
    D1 = fields.Nested(sXfld, validate=[vd.xNumber(), vd.xDim('length_mili')])
    D2 = fields.Nested(sXfld, validate=[vd.xNumber(), vd.xDim('length_mili')])
    d = fields.Nested(sXfld, validate=[vd.xNumber(), vd.xDim('length_mili')])
    FL = fields.Nested(sXfld, validate=[vd.xNumber()])
    Fd = fields.Nested(sXfld, validate=[vd.xNumber()])
    xT = fields.Nested(sXfld, validate=[vd.xNumber()])

    class Meta:
        ordered = True


class docResult(Schema):
    Cmetric = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
