import numbers
from marshmallow import Schema, fields, pprint, pre_load, ValidationError, validate
from marshmallow.validate import Validator
from collections import OrderedDict
from clappets import units

class validator :
    class xChoice(Validator):
        def __init__(self, choices):
            self.choices = choices

        def __call__(self, value):
            try:
                if value['_val'] not in self.choices:
                    raise ValidationError("Invalid Choice")
            except:
                raise ValidationError("Invalid Choice")

            return value


    class xNumber(Validator):
        def __init__(self, blank=False):
            self.blank = blank
        def __call__(self, value):
            try:
                if (isinstance(value['_val'], str)):
                    if (self.blank==True):
                        if (value['_val']!=''):
                            myfloat = float(value['_val'])
                    else:
                        myfloat = float(value['_val'])

                elif (not isinstance(value['_val'], numbers.Real)):
                    raise ValidationError("Invalid Number")
            except:
                raise ValidationError("Invalid Number")

            return value


    class fMin(Validator):
        def __init__(self, minimum):
            self.minimum = minimum
        def __call__(self, value):
            try:
                val = float(value)
                if val < self.minimum :
                    raise ValidationError("Value below Min")
            except ValueError:
                    raise ValidationError("Invalid Value")
            return value


    class xMin(Validator):
        def __init__(self, minimum):
            self.minimum = minimum
        def __call__(self, value):
            try:
                val = float(value['_val'])
                if val < self.minimum :
                    raise ValidationError("Value below {}".format(self.minimum))
            except ValueError:
                    raise ValidationError("Invalid Value")

            return value

    class fMinExcl(Validator):
        def __init__(self, minimum):
            self.minimum = minimum
        def __call__(self, value):
            try:
                val = float(value)
                if val <= self.minimum :
                    raise ValidationError("Value below Min")
            except ValueError:
                    raise ValidationError("Invalid Value")
            return value

    class xMinExcl(Validator):
        def __init__(self, minimum):
            self.minimum = minimum
        def __call__(self, value):
            try:
                val = float(value['_val'])
                if val <= self.minimum :
                    raise ValidationError("Value below Min")
            except ValueError:
                    raise ValidationError("Invalid Value")
            return value

    class fMax(Validator):
        def __init__(self, maximum):
            self.maximum = maximum

        def __call__(self, value):
            try:
                val = float(value)
                if val > self.maximum :
                    raise ValidationError("Value above Max")
            except ValueError:
                    raise ValidationError("Invalid Value")
            return value

    class xMax(Validator):
        def __init__(self, maximum):
            self.maximum = maximum

        def __call__(self, value):
            try:
                val = float(value['_val'])
                if val > self.maximum :
                    raise ValidationError("Value above {}".format(self.maximum))
            except ValueError:
                    raise ValidationError("Invalid Value")
            return value


    class fMaxExcl(Validator):
        def __init__(self, maximum):
            self.maximum = maximum

        def __call__(self, value):
            try:
                val = float(value)
                if val >= self.maximum :
                    raise ValidationError("Value above Max")
            except ValueError:
                    raise ValidationError("Invalid Value")
            return value


    class xMaxExcl(Validator):
        def __init__(self, maximum):
            self.maximum = maximum

        def __call__(self, value):
            try:
                val = float(value['_val'])
                if val >= self.maximum :
                    raise ValidationError("Value above ".format(self.maximum))
            except ValueError:
                    raise ValidationError("Invalid Value")

            return value

    class xString(Validator):
        def __call__(self, value):
            try:
                if (not isinstance(value['_val'], str)):
                    raise ValidationError("Invalid String")
            except ValueError:
                    raise ValidationError("Invalid String")

            return value

    class xDim(Validator):
        def __init__(self, dim):
            self.dim = dim

        def __call__(self,value):
            try:
                if '_dim' in value:
                    if (value['_dim'] not in self.dim):
                        raise ValidationError("Invalid Dimension")
                else:
                    raise ValidationError("Missing '_dim' Key")

            except ValueError:
                    raise ValidationError("Invalid dimension")

            return value

    class xPrm(Validator):
        def __init__(self, prm):
            self.prm = prm

        def __call__(self,value):
            try:
                if '_prm' in value:
                    if (value['_prm'] not in self.prm):
                        raise ValidationError("Invalid Permissions")
                else:
                    raise ValidationError("Missing '_prm' Key")

            except ValueError:
                    raise ValidationError("Invalid dimension")

            return value


    def isMissing(data, key):
        if (key not in data):
            return True
        elif ('_val' not in data[key]):
            return True
        elif (data[key]['_val']==''):
            return True
        else:
            return False


class sXfld(Schema):
    _val = fields.Raw(required=True)
    _dim = fields.String()
    _lbl = fields.String()
    _prm = fields.String()
    class Meta:
        ordered = True

class sUnitConfig(Schema):
    custom = fields.String(required=True)
    default = fields.String(required=True)
    class Meta:
        ordered = True


class sUnits(Schema):
    length_units = units.getUnits('length')
    length = fields.String(validate=validate.OneOf(length_units))
    length_micro_units = units.getUnits('length_micro')
    length_micro = fields.String(validate=validate.OneOf(length_units))
    length_mili_units = units.getUnits('length_mili')
    length_mili = fields.String(validate=validate.OneOf(length_units))
    length_kilo_units = units.getUnits('length_kilo')
    length_kilo = fields.String(validate=validate.OneOf(length_units))
    mass_units = units.getUnits('mass')
    mass = fields.String(validate=validate.OneOf(mass_units))
    time_units = units.getUnits('time')
    time = fields.String(validate=validate.OneOf(time_units))
    speed_units = units.getUnits('speed')
    speed = fields.String(validate=validate.OneOf(speed_units))
    acceleration_units = units.getUnits('acceleration')
    acceleration = fields.String(validate=validate.OneOf(acceleration_units))
    force_units = units.getUnits('force')
    force = fields.String(validate=validate.OneOf(force_units))
    energy_units = units.getUnits('energy')
    energy = fields.String(validate=validate.OneOf(energy_units))
    power_units = units.getUnits('power')
    power = fields.String(validate=validate.OneOf(power_units))
    pressure_units = units.getUnits('pressure')
    pressure = fields.String(validate=validate.OneOf(pressure_units))
    temperature_units = units.getUnits('temperature')
    temperature = fields.String(validate=validate.OneOf(temperature_units))
    flow_units = units.getUnits('flow')
    flow = fields.String(validate=validate.OneOf(flow_units))
    density_units = units.getUnits('density')
    density = fields.String(validate=validate.OneOf(density_units))
    molecularMass_units = units.getUnits('molecularMass')
    molecularMass = fields.String(validate=validate.OneOf(molecularMass_units))
    specificVolume_units = units.getUnits('specificVolume')
    specificVolume = fields.String(validate=validate.OneOf(specificVolume_units))
    specificEnergy_units = units.getUnits('specificEnergy')
    specificEnergy = fields.String(validate=validate.OneOf(specificEnergy_units))
    specificEnergyMolar_units = units.getUnits('specificEnergyMolar')
    specificEnergyMolar = fields.String(validate=validate.OneOf(specificEnergyMolar_units))
    specificHeat_units = units.getUnits('specificHeat')
    specificHeat = fields.String(validate=validate.OneOf(specificHeat_units))
    specificHeatMolar_units = units.getUnits('specificHeatMolar')
    specificHeatMolar = fields.String(validate=validate.OneOf(specificHeatMolar_units))
    thermalConductivity_units = units.getUnits('thermalConductivity')
    thermalConductivity = fields.String(validate=validate.OneOf(thermalConductivity_units))
    dynViscosity_units = units.getUnits('dynViscosity')
    dynViscosity = fields.String(validate=validate.OneOf(dynViscosity_units))

    class Meta:
        ordered = True



class sMeta(Schema):
    projectID = fields.String(required=True)
    project_title = fields.String(required=True)
    discipline = fields.String(required=True)
    docCategory = fields.String(required=True)
    docSubCategory = fields.String(required=True)
    docClass = fields.String(required=True)
    docClass_title = fields.String(required=True)
    docInstance = fields.String(required=True)
    docInstance_title = fields.String(required=True)
    doc_no = fields.String()
    rev = fields.String()
    date = fields.String()
    status = fields.String()
    performer = fields.String()
    reviewer = fields.String()
    approver = fields.String()

    class Meta:
        ordered=True


class sDoc(Schema):
    _id = fields.String(required=True)
    class Meta:
        ordered = True

class sDocPrj(Schema):
    _id = fields.String(required=True)
    meta = fields.Nested(sMeta, required=True)
    units = fields.Nested(sUnits)
    input = fields.Dict(required = True)
    result = fields.Dict()
    report = fields.Url()
    errors = fields.Dict()

    class Meta:
        ordered = True
