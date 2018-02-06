from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from clappets.core import sDocPrj, sXfld, xisMissing, xisBlank
from clappets.core import validator as vd
import CoolProp.CoolProp as CP


class docInput(Schema):
    Q = fields.Nested(sXfld, required=True)
    H = fields.Nested(sXfld, required=True)
    rho = fields.Nested(sXfld, required=True)
    mu = fields.Nested(sXfld, required=True)
    NPSHA = fields.Nested(sXfld, required=True)
    Nss_limit = fields.Nested(sXfld, required=True)
    design_type = fields.Nested(sXfld, required=True)
    poles = fields.Nested(sXfld, required=True)

    @validates('design_type')
    def check_design_type(self, value):
        vd.xString(value)
        item_options = ["OH", "DS1", "DS2","SSMulti", "DSMulti"]
        vd.xChoice(value, item_options)

    @validates('Q')
    def check_Q(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value,'flow')

    @validates('H')
    def check_H(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value,'length')

    @validates('rho')
    def check_rho(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value,'density')

    @validates('mu')
    def check_mu(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value,'dynViscosity')

    @validates('NPSHA')
    def check_NPSHA(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)
        vd.xDim(value,'length')

    @validates('Nss_limit')
    def check_Nss_limit(self, value):
        vd.xNumber(value)
        vd.xGrtThan(value, 0)

    @validates('poles')
    def check_poles(self, value):
        vd.xInteger(value)
        value['_val'] = int(value['_val'])
        item_options = [2, 4, 6]
        vd.xChoice(value, item_options)

    '''
    @validates_schema()
    def check_I(self,data):
        if ('solve_using' not in data):
            return
        solve_using = data['solve_using']['_val']
        if (solve_using != "current"):
            return

        fName = "I"
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value,fName)
    '''
    

class docResult(Schema):
    eta = fields.Nested(sXfld)
    d2 = fields.Nested(sXfld)
    ns = fields.Nested(sXfld)
    nss = fields.Nested(sXfld)
    Ds = fields.Nested(sXfld)
    Dd = fields.Nested(sXfld)


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
