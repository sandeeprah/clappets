from marshmallow import Schema, fields, pprint, pre_load, validate, validates,  validates_schema, ValidationError
from clappets.core import sDoc
from clappets import mongodb
from werkzeug.security import generate_password_hash, check_password_hash
import json
class sUser (Schema):
    _id = fields.String(required=True)
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String()
    password_hash = fields.String(required=True)

    class Meta:
        ordered=True


class sUserAccountUpdate (Schema):
    _id = fields.String(required=True)
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String()
    change_password = fields.Boolean(required=True)
    password = fields.String(validate=validate.Length(min=8))
    new_password = fields.String(validate=validate.Length(min=8))
    confirm_new_password = fields.String(validate=validate.Length(min=8))

    class Meta:
        ordered=True

    @pre_load
    def remove_empty(self, data):
        processed_data = data.copy()
        for key in data:
            if (data[key]==""):
                processed_data.pop(key)
        return processed_data

    @validates("_id")
    def validate_id(self, value):
        user_id = value
        Users = mongodb['users']
        user = Users.find_one({"_id": user_id})
        if (user== None):
            raise ValidationError('User ID does not exist')

    @validates_schema()
    def validate_password(self, data):
        if ('password' in data):
            user_id = data['_id']
            Users = mongodb['users']
            user = Users.find_one({"_id": user_id})
            password = data["password"]
            authenticated = check_password_hash(user['password_hash'], password)
            if (not authenticated):
                raise ValidationError('Incorrect Password',"password")


    @validates_schema()
    def validate_confirm_password(self, data):
        if ('change_password' in data):
            if (('new_password' in data) and ('confirm_new_password' in data)):
                if data['new_password'] != data['confirm_new_password']:
                    raise ValidationError('Passwords do not match','confirm_new_password')


    @validates_schema()
    def validate_password_change(self, data):
        missing_fields = []
        if (data['change_password']):
            if ('password' not in data):
                missing_fields.append("password")
            if ('new_password' not in data):
                missing_fields.append("new_password")
            if ('confirm_new_password' not in data):
                missing_fields.append("confirm_new_password")

        if (len(missing_fields) > 0):
            raise ValidationError('Field is definitely Required', missing_fields)

class sUserReg (Schema):
    _id = fields.String(required=True, validate=[validate.Length(min=6, max=20)])
    email = fields.Email(required=True)
    first_name = fields.String(required=True, validate=[validate.Length(min=1, error="First Name can not be blank")])
    last_name = fields.String()
    password = fields.String(required=True, validate=validate.Length(min=8))
    confirm_password = fields.String(required=True, validate=validate.Length(min=8))

    class Meta:
        ordered=True

    @validates_schema()
    def validate_confirm_password(self, data):
        if (('confirm_password' in data) and ('password' in data)):
            if data['confirm_password'] != data['password']:
                raise ValidationError('Passwords do not match','confirm_password')


    @validates("_id")
    def validate_id(self, value):
        user_id = value
        Users = mongodb['users']
        user = Users.find_one({"_id": user_id})
        if (user!= None):
            raise ValidationError('User ID already exists. Choose another ID')


class sUserForgot (Schema):
    _id = fields.String(required=True)

    class Meta:
        ordered=True

    @validates("_id")
    def validate_id(self, value):
        user_id = value
        Users = mongodb['users']
        user = Users.find_one({"_id": user_id})
        if (user== None):
            raise ValidationError('User ID does not exist')
