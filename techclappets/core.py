from marshmallow import Schema, fields, pprint, pre_load, ValidationError, validate
from marshmallow.validate import Validator
from collections import OrderedDict
from techclappets import units
import numbers


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
                    raise ValidationError("Value below Min")
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
                    raise ValidationError("Value above Max")
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
                    raise ValidationError("Value above Max")
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

class chkDefUnit(Validator):
    def __init__(self, dimension):
        self.dimension = dimension

    def __call__(self,value):
        try:
            allowable_units = units.get_units(self.dimension)

            if 'default' in value:
                if (value['default'] not in allowable_units):
                    raise ValidationError("Invalid Choice for Default Unit")
            else:
                raise ValidationError("Missing 'default' Key")

        except ValueError:
                raise ValidationError("Invalid dimension")

        return value

class chkCusUnit(Validator):
    def __init__(self, dimension):
        self.dimension = dimension

    def __call__(self,value):
        try:
            allowable_units = units.get_units(self.dimension)

            if 'custom' in value:
                if (value['custom'] not in allowable_units):
                    raise ValidationError("Invalid Choice for Custom Unit")
            else:
                raise ValidationError("Missing 'custom' Key")

        except ValueError:
                raise ValidationError("Invalid dimension")

        return value

class sUnits(Schema):
    length_units = units.get_units('length')
    length = fields.Nested(sUnitConfig, validate=[chkDefUnit('length'), chkCusUnit('length')])

    time_units = units.get_units('time')
    time = fields.Nested(sUnitConfig)

    speed_units = units.get_units('speed')
    speed = fields.Nested(sUnitConfig)

    acceleration_units = units.get_units('acceleration')
    acceleration = fields.Nested(sUnitConfig)

    force_units = units.get_units('force')
    force = fields.Nested(sUnitConfig)

    energy_units = units.get_units('energy')
    energy = fields.Nested(sUnitConfig)

    power_units = units.get_units('power')
    power = fields.Nested(sUnitConfig)

    pressure_units = units.get_units('pressure')
    pressure = fields.Nested(sUnitConfig)

    temperature_units = units.get_units('temperature')
    temperature = fields.Nested(sUnitConfig)

    flow_units = units.get_units('flow')
    flow = fields.Nested(sUnitConfig)

    density_units = units.get_units('density')
    density = fields.Nested(sUnitConfig)

    dynViscosity_units = units.get_units('dynViscosity')
    dynViscosity = fields.Nested(sUnitConfig)

    class Meta:
        ordered = True

class sMeta(Schema):
    projectID = fields.String(required=True)
    discipline = fields.String(required=True)
    docCategory = fields.String(required=True)
    docClass = fields.String(required=True)
    docID = fields.String(required=True)
    docTitle = fields.String(required=True)
    rev = fields.String()
    revNote = fields.String(many=True)
    purpose = fields.String()
    performer = fields.String()
    reviewer = fields.String()
    approver = fields.String()
    clientDocNo = fields.String()
    clientDocRev = fields.String()
    clientDocTitle = fields.String()
    apiUrl = fields.Url()
    class Meta:
        ordered=True

class sDocBase(Schema):
    _id = fields.String()
    meta = fields.Nested(sMeta, required=True)
    unitSystem = fields.String()
    units = fields.Nested(sUnits)
    input = fields.Dict(required = True)
    result = fields.Dict()
    report = fields.Url()
    errors = fields.Dict()

    class Meta:
        ordered = True
