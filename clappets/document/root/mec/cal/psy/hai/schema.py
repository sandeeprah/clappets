from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from clappets.core import sDocPrj, sXfld
from clappets.core import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    calculation_options = [
                        "Tdb_RH_P",
                        "Tdb_Twb_P",
                        "Tdb_Tdp_P",
                        "Tdb_W_P",
                        "Tdb_h_P"]

    calculation_option = fields.Nested(sXfld, validate=[vd.xString(), vd.xChoice(calculation_options)], required=True)
    Tdb = fields.Nested(sXfld, validate=[vd.xNumber(blank=False), vd.xDim('temperature')], required=True)
    P = fields.Nested(sXfld, validate=[vd.xNumber(blank=False), vd.xMin(0), vd.xDim('pressure')], required=True)
    Twb = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('temperature')])
    Tdp = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('temperature')])
    RH = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xMin(0), vd.xMax(1)])
    W = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])
    h = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificEnergy')])


    @validates_schema()
    def check_missingvalid(self,data):
        err_fields = []
        if 'calculation_option' in data:
            if (data['calculation_option']['_val']=='Tdb_RH_P'):
                if vd.isMissing(data, 'RH'):
                    err_fields.append('RH')

            if (data['calculation_option']['_val']=='Tdb_Twb_P'):
                if vd.isMissing(data, 'Twb'):
                    err_fields.append('Twb')

            if (data['calculation_option']['_val']=='Tdb_Tdp_P'):
                if vd.isMissing(data, 'Tdp'):
                    err_fields.append('Tdp')

            if (data['calculation_option']['_val']=='Tdb_W_P'):
                if vd.isMissing(data, 'W'):
                    err_fields.append('W')

            if (data['calculation_option']['_val']=='Tdb_h_P'):
                if vd.isMissing(data, 'h'):
                    err_fields.append('h')

        if (len(err_fields)>0):
            raise ValidationError("Field is required", err_fields)


class docResult(Schema):
    RH = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])
    Twb = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('temperature')])
    Tdp = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('temperature')])
    W = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])
    rho = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('density')])
    v = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificVolume')])
    h = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificEnergy')])
    u = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificEnergy')])
    s = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificHeat')])
    Cp = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificHeat')])
    Cp_ha = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('specificHeat')])


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
