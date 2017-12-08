from marshmallow import Schema, fields, pprint, pre_load, validate, validates,  validates_schema, ValidationError
from clappets.core import sDoc

class sUser (Schema):
    _id = fields.String(required=True)
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String()
    password_hash = fields.String(required=True)

    class Meta:
        ordered=True


class sUserReg (Schema):
    _id = fields.String(required=True)
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String()
    password = fields.String(required=True)
    confirm_password = fields.String(required=True)

    class Meta:
        ordered=True

    @validates_schema
    def validate_confirm_password(self, data):
        if data['confirm_password'] != data['password']:
            raise ValidationError('Passwords do not match','confirm_password')
