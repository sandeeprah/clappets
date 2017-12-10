import json
import os
import pymongo
from werkzeug.security import generate_password_hash
from collections import OrderedDict
from flask import request, render_template, jsonify, abort, make_response
from clappets import app, mongodb
#from clappets.documentor.core import sReq
from clappets.utils import json_response, sendMail
from clappets.user.userSchema import sUser, sUserReg

@app.route('/api/user/', methods=['GET'])
def api_get_users():
    users = mongodb['users']
    user_list = list(users.find())
    return json_response(user_list), 200


@app.route('/api/user/<user_id>/', methods=['GET'])
def api_get_user(user_id):
    errors = OrderedDict()
    users = mongodb['users']
    docMongo = users.find_one({"_id": user_id})
    if (docMongo== None):
        errors['message'] = "user with user ID as requested could not be found"
        return json_response(errors), 404
    else:
        return json_response(docMongo)

@app.route('/api/user/', methods=['POST'])
def api_post_user():
    errors = OrderedDict()
    req = request.get_json()

    if ('resource' not in req):
        errors['message'] = "'user' missing in REST API request"
        return json_response(errors), 400
    else:
        docRaw = req['resource']
        docSchema = sUserReg()
        docParsed = docSchema.load(docRaw)
        if (len(docParsed.errors) > 0):
            errors['message'] = "there are errors in your input"
            errors['schema'] = docParsed.errors
            return json_response(errors), 400
        else:
            user = docParsed.data
            user['password_hash'] = generate_password_hash(user['password'])
            user['confirmed'] = 'No'
            users = mongodb['users']
            try:
                users.insert_one(user)
            except pymongo.errors.DuplicateKeyError:
                errors['message'] = 'Insert Faileds as user ID already exists'
                return json_response(errors), 400
            except Exception as e:
                errors['message'] = str(e)
                return json_response(errors), 400

            sendMail([user["email"]],'appadmin@clappets.com','Registration','We have received your registration request.')
            response = {}
            response["message"] = "User Registered Successfully"
            response["redirect_url"] = "/htm/user/regstatus/"+user['_id']+"/"

            return json_response(response), 201


@app.route('/api/user/<user_id>/', methods=['PUT'])
def api_put_user(user_id):
    errors = OrderedDict()
    req = request.get_json()
    if ('resource' not in req):
        errors['message'] = "'user' missing in REST API request"
        return json_response(errors), 400
    else:
        docRaw = req['resource']
        docSchema = sUser()
        docParsed = docSchema.load(docRaw)
        if (len(docParsed.errors) > 0):
            errors['message'] = "user is not as per Schema"
            errors['schema'] = docParsed.errors
            return json_response(errors), 400
        else:
            user = docParsed.data
            users = mongodb['users']
            try:
                users.update({"_id" : user_id}, user)
            except Exception as e:
                errors['message'] = str(e)
                return json_response(errors), 400
            return json_response({'message' : 'user Updated Sucessfully'}), 200


@app.route('/api/user/<user_id>/', methods=['DELETE'])
def api_delete_user(user_id):
    errors = OrderedDict()
    users = mongodb["users"]
    try:
        users.delete_one({"_id" : user_id})
    except Exception as e:
        errors['message'] = str(e)
        return json_response(errors)

    response = {}
    response["message"] = "Deletion Successful"
    response["redirect_url"] = "/htm/user/"
    return json_response(response)



@app.route('/api/user/regstatus/<user_id>/', methods=['GET'])
def api_get_userregstatus(user_id):
    errors = OrderedDict()
    users = mongodb['users']
    user = users.find_one({"_id": user_id})
    if (user == None):
        errors['message'] = ['user with user ID as requested could not be found']
        return json_response(errors), 404
    else:
        confirmed = user['confirmed']
        response = {}
        if confirmed=="Yes":
            response['status'] = "User is Confirmed"
            return json_response(response)
        else:
            response['status'] = "User Email ID is not confirmed. User is required to confirm \
 mail id by clicking on the link sent to his registered mail id."
            return json_response(response)


@app.route('/htm/user/', methods=['GET'])
@app.route('/htm/user/list/', methods=['GET'])
def htm_get_users():
    users = mongodb['users']
    user_list = list(users.find())
    user_list = json.dumps(user_list)
    return render_template("user/user_list.html", user_list= user_list)


@app.route('/htm/user/add/', methods=['GET'])
def htm_register_user():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    print("THIS FOLDER {fld}".format(fld=THIS_FOLDER))
    input_filename = os.path.join(THIS_FOLDER, 'user_default.json')
    docRaw = json.load(open(input_filename))
    user = json.dumps(docRaw)
    return render_template("user/register.html", user = user, action="add")


@app.route('/htm/user/edit/<prj_id>/', methods=['GET'])
def htm_edit_user(prj_id):
    users = mongodb['users']
    docMongo = users.find_one({"_id": prj_id})
    if (docMongo== None):
        return "Document Not Found"
    else:
        user = json.dumps(docMongo)
        return render_template("user/user.html", user = user, action="edit")

@app.route('/htm/user/view/<prj_id>/', methods=['GET'])
def htm_view_user(prj_id):
    users = mongodb['users']
    docMongo = users.find_one({"_id": prj_id})
    if (docMongo== None):
        return "Document Not Found"
    else:
        doc = json.dumps(docMongo)
        return render_template("user/user.html", doc = doc, action="view")


@app.route('/htm/user/regstatus/<user_id>/', methods=['GET'])
def htm_get_userregstatus(user_id):
    users = mongodb['users']
    user = users.find_one({"_id": user_id})
    title = "User Mail ID Confirmation Status"
    if (user == None):
        message = "Username does not exist in database"
    else:
        confirmed = user['confirmed']
        if confirmed=="Yes":
            message = "User Mail ID is Confirmed"
        else:
            message = "User Email ID is not confirmed. User is required to confirm \
 mail id by clicking on the link sent to his registered mail id."

    return render_template("message.html", title=title, message=message)
