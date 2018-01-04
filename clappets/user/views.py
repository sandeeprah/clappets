import json
import os
import pymongo
import string
import random
from werkzeug.security import generate_password_hash
from collections import OrderedDict
from flask import request, render_template, jsonify, abort, make_response, g
from clappets import app, mongodb
from clappets.authentication import auth
#from clappets.documentor.core import sReq
from clappets.utils import json_response, sendMail
from clappets.user.userSchema import sUser, sUserReg, sUserForgot, sUserAccountUpdate
from itsdangerous import URLSafeTimedSerializer

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
            user['confirmed'] = False
            users = mongodb['users']
            try:
                users.insert_one(user)
            except pymongo.errors.DuplicateKeyError:
                errors['message'] = 'Insert Faileds as user ID already exists'
                return json_response(errors), 400
            except Exception as e:
                errors['message'] = str(e)
                return json_response(errors), 400

            token = generate_confirmation_token(user["email"])
            confirm_link = "https://www.clappets.com/htm/user/confirm/"+user['_id']+"/"+token+"/"


            html_template = """\
            <html>
              <head></head>
              <body>
                <p>Hi!<br>
                   We have received your user registration request. <br>
                   Please click on the link to confirm your email id. <a href="{}">{}</a>
                </p>
                <p>
                This mail is auto generated. Please do not reply to this mail.
                </p>
              </body>
            </html>
            """

            mailbody = html_template.format(confirm_link, confirm_link)
#            sendMail([user["email"]],'appadmin@clappets.com','User Registration',mailbody)
            response = {}
            response["message"] = "User Registered Successfully."

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
        docSchema = sUserAccountUpdate()
        docParsed = docSchema.load(docRaw)
        if (len(docParsed.errors) > 0):
            errors['message'] = "user is not as per Schema"
            errors['schema'] = docParsed.errors
            return json_response(errors), 400
        else:
            user = docParsed.data
            user_id = user['_id']
            update_doc = {
            "$set" :
                    {"first_name" : user['first_name'],
                     "last_name" : user['last_name'],
                     "email" : user['email'],
                     }
            }

            if (user['change_password']):
                user['password_hash'] = generate_password_hash(user['new_password'])
                update_doc['$set']['password_hash'] = user['password_hash']

            users = mongodb['users']
            try:
                users.update({"_id" : user_id}, update_doc)
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



@app.route('/api/user/forgot/', methods=['POST'])
def api_forgotpasswd():
    errors = OrderedDict()
    req = request.get_json()
    errors = {}
    if ('resource' not in req):
        errors['message'] = "'resource' missing in REST API request"
        return json_response(errors), 400
    else:
        docRaw = req['resource']
        docSchema = sUserForgot()
        docParsed = docSchema.load(docRaw)
        if (len(docParsed.errors) > 0):
            errors['message'] = "There are errors in input"
            errors['schema'] = docParsed.errors
            return json_response(errors), 400
        else:
            user = docParsed.data
            user_id = user["_id"]
            users = mongodb['users']
            user = users.find_one({"_id": user_id})
            email = user["email"]
            new_password = pw_gen()
            user['password_hash'] = generate_password_hash(new_password)
            try:
                users.update({"_id" : user_id}, user)
            except Exception as e:
                errors['message'] = str(e)
                return json_response(errors), 400

            html_template = """\
            <html>
              <head></head>
              <body>
                <p>Hi!<br>
                   We have received your new passoword request. <br>
                   Your new passoword is {}
                   <br>
                   Please remember to reset your password after login.
                </p>
                <p>
                This mail is auto generated. Please do not reply to this mail.
                </p>
              </body>
            </html>
            """
            mailbody = html_template.format(new_password)
            sendMail([user["email"]],'appadmin@clappets.com','Password Reset',mailbody)
            response = {}
            response["message"] = "You will receive your new password on email. If you do not find the mail in your mail box\
            please ensure to check your spam folder"
            return json_response(response), 201


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
        docMongo["change_password"] = False
        docMongo["password"] = ""
        docMongo["new_password"] = ""
        docMongo["confirm_new_password"] = ""

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




@app.route('/htm/user/confirm/<user_id>/<token>/', methods=['GET'])
def confirm_email(user_id, token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')

    users = mongodb['users']
    user = users.find_one({"_id": user_id})
    title = "User Mail ID Confirmation Status"

    if user["confirmed"]:
        message = 'Email ID already confirmed. Please login.'
    else:
        if (email == user["email"]):
            user["confirmed"] = True
            message = 'Email ID is confirmed. Please login.'
            users.update({"_id" : user_id}, user)
        else:
            message = 'Email could  not be confirmed. Please register again.'

    return render_template("message.html", title=title, message=message)


@app.route('/htm/user/account/', methods=['GET'])
@auth.login_required
def user_account():
    user_id = g.user
    users = mongodb['users']
    docMongo = users.find({"_id": user_id}, {"password_hash":0, "confirmed":0, "confirm_password":0})[0]
    if (docMongo== None):
        return "Document Not Found"
    else:
        docMongo["change_password"] = False
        docMongo["password"] = ""
        docMongo["new_password"] = ""
        docMongo["confirm_new_password"] = ""

        user = json.dumps(docMongo)
        return render_template("user/account.html", user = user)

    print(user)
    return render_template("user/account.html")


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


def pw_gen(size = 8, chars=string.ascii_letters + string.digits + string.punctuation):
	return ''.join(random.choice(chars) for _ in range(size))
