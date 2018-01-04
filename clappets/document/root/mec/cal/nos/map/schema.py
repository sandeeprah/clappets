from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from clappets.core import sDocPrj, sXfld
from clappets.core import validator as vd
import CoolProp.CoolProp as CP
from clappets.units import getUnits

class coldim_emissionPoint(Schema):
    dimensions_allowed = ['length']
    x = fields.String(validate=validate.OneOf(choices=dimensions_allowed))
    y = fields.String(validate=validate.OneOf(choices=dimensions_allowed))

class emissionPoint(Schema):
    tag = fields.String(required=True)
    pwl = fields.Float(required=True)
    Q = fields.Float(required=True)
    x = fields.Float(required=True)
    y = fields.Float(required=True)

    class Meta:
        ordered = True

class emissionPoints(Schema):
    _coldim = fields.Nested(coldim_emissionPoint)
    _list = fields.Nested(emissionPoint, many=True)


class areaGrid(Schema):
    x1 = fields.Nested(sXfld, validate=[vd.xNumber(blank=False), vd.xDim('length')])
    y1 = fields.Nested(sXfld, validate=[vd.xNumber(blank=False), vd.xDim('length')])
    x2 = fields.Nested(sXfld, validate=[vd.xNumber(blank=False), vd.xDim('length')])
    y2 = fields.Nested(sXfld, validate=[vd.xNumber(blank=False), vd.xDim('length')])
    x_step = fields.Nested(sXfld, validate=[vd.xNumber(blank=False), vd.xDim('length')])
    y_step = fields.Nested(sXfld, validate=[vd.xNumber(blank=False), vd.xDim('length')])

    class Meta:
        ordered = True


class coldim_noiseFieldPoint(Schema):
    dimensions_allowed = ['length']
    x = fields.String(validate=validate.OneOf(choices=dimensions_allowed))
    y = fields.String(validate=validate.OneOf(choices=dimensions_allowed))

class noiseFieldPoint(Schema):
    x = fields.Float(required=True)
    y = fields.Float(required=True)
    noise = fields.Float(required=True)

    class Meta:
        ordered = True

class noiseField(Schema):
    _coldim = fields.Nested(coldim_noiseFieldPoint)
    _list = fields.Nested(noiseFieldPoint, many=True)




class docInput(Schema):
    emissionPoints = fields.Nested(emissionPoints, required=True)
    mapArea = fields.Nested(areaGrid, required=True)

    class Meta:
        ordered = True


class docResult(Schema):
    noiseField = fields.Nested(noiseField)

    class Meta:
        ordered = True


class docSchema(sDocPrj):
    input = fields.Nested(docInput)
    result = fields.Nested(docResult)
