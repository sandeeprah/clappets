from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from clappets.core import sDocPrj, sXfld
from clappets.core import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    calculation_options = [
                        "calcSPL",
                        "calcPWL",
                        "calcDistance"
                        ]

    calculation_option = fields.Nested(sXfld, validate=[vd.xString(), vd.xChoice(calculation_options)], required=True)
    PWL = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])
    SPL = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])
    distance = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('length')])
    Q_options = ["1","2","4","8"]
    Q = fields.Nested(sXfld, validate=[vd.xString(), vd.xChoice(Q_options)], required=True)

    @validates_schema()
    def check_missingvalid(self,data):
        err_fields = []
        if 'calculation_option' in data:
            if (data['calculation_option']['_val']=='calcSPL'):
                if vd.isMissing(data, 'PWL'):
                    err_fields.append('PWL')
                if vd.isMissing(data, 'distance'):
                    err_fields.append('distance')

            if (data['calculation_option']['_val']=='calcPWL'):
                if vd.isMissing(data, 'SPL'):
                    err_fields.append('SPL')
                if vd.isMissing(data, 'distance'):
                    err_fields.append('distance')

            if (data['calculation_option']['_val']=='calcDistance'):
                if vd.isMissing(data, 'PWL'):
                    err_fields.append('PWL')
                if vd.isMissing(data, 'SPL'):
                    err_fields.append('SPL')


        if (len(err_fields)>0):
            raise ValidationError("Field is required", err_fields)


class docResult(Schema):
    PWL = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])
    SPL = fields.Nested(sXfld, validate=[vd.xNumber(blank=True)])
    distance = fields.Nested(sXfld, validate=[vd.xNumber(blank=True), vd.xDim('length')])


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
