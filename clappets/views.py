from flask import request, render_template, jsonify, abort
from clappets import app
from clappets.project import views
from clappets.document import views
from clappets.pdf import views

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/test/demo/')
@app.route('/test/demo/index')
def demo():
    return render_template("test/demo.html")


@app.route('/htm/documentor/')
@app.route('/htm/documentor/index')
def documentor_index():
    return render_template("documentor/index.html")
