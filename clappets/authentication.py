from flask import g, request, render_template, jsonify, abort
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as JWT
from clappets import app, mongodb
from clappets.utils import json_response


jwt = JWT(app.config['SECRET_KEY'], expires_in=360000)
auth = HTTPBasicAuth()
auth_relaxed = HTTPBasicAuth()
auth_admin = HTTPBasicAuth()

users = {
    "admin" : generate_password_hash("admin"),
    "sraheja" : generate_password_hash("sraheja"),
}

@app.route('/auth/', methods=['POST'])
def getAuthToken():
    req = request.get_json()
    username = req["username"]
    password = req["password"]
    auth_response = {}
    users = mongodb['users']
    user = users.find_one({"_id": username})
    if (user == None):
        auth_response["message"] = "Invalid User Credentials"
        return json_response(auth_response), 401
    else:
        authenticated = check_password_hash(user['password_hash'], password)
        if authenticated:
            access_token = jwt.dumps({'username': user['_id'] })
            auth_response = {}
            auth_response["access_token"] = access_token.decode('utf-8')
            return json_response(auth_response)
        else:
            auth_response["message"] = "Invalid User Credentials"
            return json_response(auth_response), 401



@auth.verify_password
def verify_token(username, password):
    '''
    In the method chosen for authentication, basic authentication is used. Username is the JWT token and Password is not used.
    '''
    g.user = None
    token = username
    try:
        data = jwt.loads(token)
    except:
        return False
    if 'username' in data:
        g.user = data['username']
        return True
    return False



@auth_relaxed.verify_password
def verify_token_relaxed(username, password):
    '''
    In the method chosen for authentication, basic authentication is used. Username is the JWT token and Password is not used.
    '''
    g.user = None

    if (username =="anonymous"):
        return True
    else:
        token = username

    try:
        data = jwt.loads(token)
    except:
        return False

    if 'username' in data:
        g.user = data['username']
        return True

    return False



@app.route('/auth2/', methods=['POST'])
def getAuthToken2():
    req = request.get_json()
    username = req["username"]
    password = req["password"]
    auth_response = {}
    if username in users:
        authenticated = check_password_hash(users.get(username), password)
        if authenticated:
            access_token = jwt.dumps({'username': username})
            auth_response = {}
            auth_response["access_token"] = access_token.decode('utf-8')
        else:
            auth_response["message"] = "Invalid User Credentials"
            return json_response(auth_response), 401
    else:
        auth_response["message"] = "Invalid User Credentials"
        return json_response(auth_response), 401

    return json_response(auth_response)


@app.route('/login-test/')
@auth.login_required
def login_test():
    return "You are Logged In"
