from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError
from clappets.core import sDocPrj, sXfld, xisBlank, xisMissing
from clappets.core import validator as vd


class schema_fluidfraction(Schema):
    fluid_list = ["Carbon",
                "Hydrogen",
                "Oxygen",
                "Nitrogen",
                "CarbonMonoxide",
                "CarbonDioxide",
                "Methane",
                "Ethane",
                "Ethylene",
                "Acetylene",
                "Propane",
                "Propylene",
                "Butane",
                "Butylene",
                "Pentane",
                "Hexane",
                "Benzene",
                "Methanol",
                "Ammonia",
                "Sulphur",
                "HydrogenSulphide",
                "Water"]
    fluid = fields.String(required=True, validate=validate.OneOf(choices=fluid_list))
    fraction = fields.Float(required=True)
    class Meta:
        ordered = True

    @validates('fraction')
    def check_fraction(self, value):
        vd.fGrtThanEq(value,0)
        vd.fLessThanEq(value,1)



class docInput(Schema):
    Ta = fields.Nested(sXfld)
    RH = fields.Nested(sXfld)
    excess_O2 = fields.Nested(sXfld)
    m_st = fields.Nested(sXfld)
    Pm = fields.Nested(sXfld)
    Tm = fields.Nested(sXfld)
    radiation_loss_pc = fields.Nested(sXfld)
    Texit = fields.Nested(sXfld)

    fraction_type = fields.Nested(sXfld)

    gasfuel = fields.Nested(schema_fluidfraction, many=True, required=True)
    Tf = fields.Nested(sXfld)

    class Meta:
        ordered = True

    @validates_schema()
    def check_Ta(self, data):
        fName = 'Ta'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value, ['temperature'], fName)

    @validates_schema()
    def check_RH(self, data):
        fName = 'RH'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xLessThanEq(value, 100, fName)

    @validates_schema()
    def check_excess_O2(self, data):
        fName = 'excess_O2'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)


    @validates_schema()
    def check_radiation_loss_pc(self, data):
        fName = 'radiation_loss_pc'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xGrtThanEq(value, 0, fName)
        vd.xLessThanEq(value, 100, fName)

    @validates_schema()
    def check_Texit(self, data):
        fName = 'Texit'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value, ['temperature'], fName)

    @validates_schema()
    def check_fraction_type(self, data):
        fName = 'fraction_type'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xString(value, fName)
        fraction_type_options = ["mole_fraction","mass_fraction"]
        vd.xChoice(value, fraction_type_options, fName)


    @validates_schema()
    def check_gasfuel(self, data):
        if ('gasfuel' in data):
            gasfuel = data['gasfuel']
            sigma_y = 0
            for component in gasfuel:
                if ('fraction' in component):
                    sigma_y = sigma_y + component['fraction']

            if (sigma_y <=0):
                raise ValidationError('No gas composition entered. Total > 0 reqd','schema_gasfuel')

    @validates_schema()
    def check_Tf(self, data):
        fName = 'Tf'
        vd.xRequired(data,fName,fName)
        value = data[fName]
        vd.xNumber(value, fName)
        vd.xDim(value, ['temperature'], fName)



class docResult(Schema):
    MW = fields.Nested(sXfld)
    LHV = fields.Nested(sXfld)

    class Meta:
        ordered = True


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
