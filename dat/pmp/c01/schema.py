from marshmallow import Schema, fields
from clappets.core import sDocPrj

class docInput(Schema):
    A = fields.Float()
    B = fields.Float()

class docSchema(sDocPrj):
    input = fields.Nested(docInput)
