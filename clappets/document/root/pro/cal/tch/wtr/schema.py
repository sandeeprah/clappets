from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from clappets.core import sDocPrj, sXfld
from clappets.core import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    state_options = ["Saturated_T", "Saturated_P", "Superheated_or_Compressed"]
    state = fields.Nested(sXfld, validate=[vd.xString(), vd.xChoice(state_options)], required=True)
    P = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('pressure')])
    T = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('temperature')])
    Q = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])

    @validates_schema()
    def check_missingvalid(self,data):
        err_fields = []
        if 'state' in data:
            if (data['state']['_val']=='Saturated_T'):
                if vd.isMissing(data, 'T'):
                    err_fields.append('T')
                if vd.isMissing(data, 'Q'):
                    err_fields.append('Q')

            if (data['state']['_val']=='Saturated_P'):
                if vd.isMissing(data, 'P'):
                    err_fields.append('P')
                if vd.isMissing(data, 'Q'):
                    err_fields.append('Q')

            if (data['state']['_val']=='Superheated_or_Compressed'):
                if vd.isMissing(data, 'P'):
                    err_fields.append('P')
                if vd.isMissing(data, 'T'):
                    err_fields.append('T')

        if (len(err_fields)>0):
            raise ValidationError("Field is required", err_fields)


class docResult(Schema):
    phase = fields.Nested(sXfld)
    rho = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('density')])
    Psat = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('pressure')])
    Tsat = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('temperature')])
    v = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificVolume')])
    h = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificEnergy')])
    u = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificEnergy')])
    s = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificHeat')])


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
