from marshmallow import Schema, fields, pprint, pre_load, validate, validates,  validates_schema, ValidationError
from clappets.core import sDoc

class sProject (Schema):
    _id = fields.String(required=True, validate=validate.Regexp('^\d{4}$'))
    title = fields.String(required=True)
    admin_id = fields.String(required=True)

    class Meta:
        ordered=True
