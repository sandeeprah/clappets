from flask import request, render_template, jsonify, abort
from flask_httpauth import HTTPBasicAuth
from clappets import app
from clappets.project import views
from clappets.user import views
from clappets.document import views
from clappets.pdf import views
from clappets.calc import views
from clappets import authentication

@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")

@app.route('/admin/')
def admin():
    return render_template("admin.html")

@app.route('/login/')
def login():
    return render_template("login.html")

@app.route('/google5ca5209499debead.html')
def google_verify():
    return render_template("google5ca5209499debead.html")


@app.route('/forgot/', methods=['GET'])
def forgot_password():
    return render_template("forgot_password.html")

@app.route('/register/', methods=['GET'])
def register_user():
    return render_template("register.html")

@app.route('/profile/', methods=['GET'])
def profile_user():
    return render_template("profile.html")

@app.route('/indexlogin/', methods=['GET'])
def index_user():
    return render_template("indexlogin.html")
