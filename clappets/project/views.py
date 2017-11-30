import json
import os
import pymongo

from collections import OrderedDict
from flask import request, render_template, jsonify, abort, make_response
from clappets import app, mongodb
#from clappets.documentor.core import sReq
from clappets.utils import json_response
from clappets.project.projectSchema import sProject

@app.route('/api/documentor/project/', methods=['GET'])
def api_get_projects():
    projects = mongodb['projects']
    project_list = list(projects.find())
    return json_response(project_list), 200

@app.route('/api/documentor/project/<project_id>/', methods=['GET'])
def api_get_project(project_id):
    errors = OrderedDict()
    projects = mongodb['projects']
    prj_id = project_id
    docMongo = projects.find_one({"_id": prj_id})
    if (docMongo== None):
        errors['operation'] = ['Project with Project ID as requested could not be found']
        return json_response(errors), 404
    else:
        return json_response(docMongo)

@app.route('/api/documentor/project/', methods=['POST'])
def api_post_project():
    errors = OrderedDict()
    req = request.get_json()

    if ('resource' not in req):
        errors['request'] = "'project' missing in REST API request"
        return json_response(errors), 400
    else:
        docRaw = req['resource']
        docSchema = sProject()
        docParsed = docSchema.load(docRaw)
        if (len(docParsed.errors) > 0):
            errors['project'] = docParsed.errors
            return json_response(errors), 400
        else:
            project = docParsed.data
            projects = mongodb['projects']
            try:
                projects.insert_one(project)
            except pymongo.errors.DuplicateKeyError:
                errors['operation'] = ['Insert Faileds as Project ID already exists']
                return json_response(errors), 400
            except Exception as e:
                errors['operation'] = str(e)
                return json_response(errors), 400


            return json_response({'_message' : 'Document Added Sucessfully'}), 201


@app.route('/api/documentor/project/<project_id>/', methods=['PUT'])
def api_put_project(project_id):
    errors = OrderedDict()
    req = request.get_json()
    if ('resource' not in req):
        errors['request'] = "'project' missing in REST API request"
        return json_response(errors), 400
    else:
        docRaw = req['resource']
        docSchema = sProject()
        docParsed = docSchema.load(docRaw)
        if (len(docParsed.errors) > 0):
            errors['project'] = docParsed.errors
            return json_response(errors), 400
        else:
            project = docParsed.data
            projects = mongodb['projects']
            try:
                projects.update({"_id" : project_id}, project)
            except Exception as e:
                errors['operation'] = str(e)
                return json_response(errors), 400
            return json_response({'_message' : 'Resource Updated Sucessfully'}), 201


@app.route('/api/documentor/project/<project_id>/', methods=['DELETE'])
def api_delete_project(project_id):
    errors = OrderedDict()
    projects = mongodb["projects"]
    try:
        projects.delete_one({"_id" : project_id})
    except Exception as e:
        errors['operation'] = str(e)
        return json_response(errors)

    return json_response({'_message': "Deletion Successful"})


@app.route('/htm/documentor/project/', methods=['GET'])
@app.route('/htm/documentor/project/list/', methods=['GET'])
def htm_get_projects():
    projects = mongodb['projects']
    project_list = list(projects.find())
    project_list = json.dumps(project_list)
    return render_template("documentor/project/project_list.html", project_list= project_list)



@app.route('/htm/documentor/project/add/', methods=['GET'])
def htm_add_project():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    print("THIS FOLDER {fld}".format(fld=THIS_FOLDER))
    input_filename = os.path.join(THIS_FOLDER, 'project_default.json')
    docRaw = json.load(open(input_filename))
    docSchema = sProject()
    docParsed = docSchema.load(docRaw)
    if (len(docParsed.errors) > 0):
        return "Invalid Default Project Data"
    else:
        project = json.dumps(docParsed.data)
        return render_template("documentor/project/project.html", project = project, action="add")

@app.route('/htm/documentor/project/edit/<prj_id>/', methods=['GET'])
def htm_edit_project(prj_id):
    projects = mongodb['projects']
    docMongo = projects.find_one({"_id": prj_id})
    if (docMongo== None):
        return "Document Not Found"
    else:
        project = json.dumps(docMongo)
        return render_template("documentor/project/project.html", project = project, action="edit")

@app.route('/htm/documentor/project/view/<prj_id>/', methods=['GET'])
def htm_view_project(prj_id):
    projects = mongodb['projects']
    docMongo = projects.find_one({"_id": prj_id})
    if (docMongo== None):
        return "Document Not Found"
    else:
        doc = json.dumps(docMongo)
        return render_template("documentor/project/project.html", doc = doc, action="view")
