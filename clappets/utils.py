import json
from flask import current_app
from bson import json_util


def json_response(input):
    str_response = json.dumps(input, indent=4, default=json_util.default)
    return current_app.response_class(str_response, mimetype='application/json')
