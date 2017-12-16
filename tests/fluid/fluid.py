import requests
import json
import os
from techclappets.pressuredrop.line import schema_input_pressuredrop_line, pressuredrop_line


def run_tests():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    input_filename = os.path.join(THIS_FOLDER, 'line.json')

    # load the input json to a python dictionary named input_json
    input_json = json.load(open(input_filename))
    print(json.dumps(input_json, indent=4))

    #validate the input using the schema
    print("Testing the data with the schema")
    input_schema = schema_input_pressuredrop_line()
    parsed_data = input_schema.load(input_json)
    print("Parsed Data: ")
    print("==============")
    print(json.dumps(parsed_data.data, indent=4))
    print("Errors :")
    print("========")
    print(json.dumps(parsed_data.errors, indent=4))

    #test the function with the input_json
    print("Testing the techclappets function with the data")
    calc_output =  pressuredrop_line(input_json)
    print(json.dumps(calc_output.result, indent=4))
    print(json.dumps(calc_output.errors, indent=4))

    #test the Rest API
    print("Testing the calcapi REST API function")
    headers = {'Content-type': 'application/json'}

    url = "http://127.0.0.1:5000/calcapi/pressuredrop/liquidline2K/"
    json_string = json.dumps(input_json, indent=4)
    response = requests.post(url, data=json_string, headers=headers)
    print(response.status_code)
    print(response.text)
