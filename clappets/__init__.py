import os
import jinja2
from collections import OrderedDict
from flask import Flask, render_template
import pymongo

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

client = pymongo.MongoClient(document_class = OrderedDict)
mongodb = client["clappetsdb"]

'''
In addition to the standard package loader, there is also a choice of loading from the root directory located in documentor
'''
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
ROOT_FOLDER = os.path.join(THIS_FOLDER, 'document')
extended_loader = jinja2.ChoiceLoader([app.jinja_loader, jinja2.FileSystemLoader(ROOT_FOLDER)])
app.jinja_loader = extended_loader


'''
Since there are circular import the module views imports app and this module as to import views this imports
must always be after the above line where app instance has been created.
'''
from clappets import views

app.jinja_env.auto_reload = True
