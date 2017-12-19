from marshmallow import Schema, fields, validate
from clappets.core import sDocPrj, sXfld
from clappets.core import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    fluid_options = CP.FluidsList()
#    fluid_list = fields.List(fields.String(validate=validate.OneOf(fluid_options)))
    fluid = fields.Nested(sXfld, validate=[vd.xString()])
    P = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('pressure')])
    T = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('temperature')])

class docResult(Schema):
    phase = fields.Nested(sXfld)
    MW = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('molecularMass')])
    Pcritical = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('pressure')])
    Tcritical = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('temperature')])
    Ptriple = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('pressure')])
    Ttriple = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('temperature')])
    acentric = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])
    Z = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])
    rho = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('density')])
    v = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificVolume')])
    h = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificEnergy')])
    u = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificEnergy')])
    s = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificHeat')])
    gibbs = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificEnergy')])
    helmholtz = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificEnergy')])
    Cp = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificEnergy')])
    Cv = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificEnergy')])
    Cp_molar = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificHeatMolar')])
    Cv_molar = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificHeatMolar')])
    Cp0 = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificEnergy')])
    Prandtl = fields.Nested(sXfld)
    dynViscosity = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('dynViscosity')])
    conductivity = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('thermalConductivity')])
    HH = fields.Nested(sXfld)
    PH = fields.Nested(sXfld)
    GWP = fields.Nested(sXfld)
    ODP = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
