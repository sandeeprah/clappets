from clappets import app
from io import StringIO
import os
import json
from collections import OrderedDict
from flask import render_template, request, abort, g
import pymongo
from clappets import app, mongodb
from clappets.authentication import auth, auth_relaxed
from clappets.core import sDocPrj
from clappets.utils import json_response
from clappets.document.utils import load_schema, get_repository, get_folder_title, get_project_title, get_subfolder_names, get_subfolder_list
from clappets.utils import load_function
# first all apis
@app.route('/api/document/tpl/', methods=['GET'])
@app.route('/api/document/tpl/<repository>/', methods=['GET'])
@app.route('/api/document/tpl/<repository>/<discipline>/', methods=['GET'])
@app.route('/api/document/tpl/<repository>/<discipline>/<docCategory>/', methods=['GET'])
@app.route('/api/document/tpl/<repository>/<discipline>/<docCategory>/<docSubCategory>/', methods=['GET'])
@app.route('/api/document/tpl/<repository>/<discipline>/<docCategory>/<docSubCategory>/<docClass>/', methods=['GET'])
def api_template(repository="", discipline="", docCategory="", docSubCategory="", docClass=""):
    #this_folderpath = os.path.dirname(os.path.abspath(__file__))
    context = OrderedDict()
    context["title"] = "New Document"

    #folderpath = os.path.join(this_folderpath)
    folderpath = os.path.join("")
    if (repository==""):
        context["subtitle"] = "Repository"
        subfolder_list = get_subfolder_list(folderpath)
        context['subfolder_list'] = subfolder_list
        return json_response(context)
    else:
        allowed_repositories = get_subfolder_names(folderpath)
        if repository not in allowed_repositories:
            return "Invalid Repository"

    folderpath = os.path.join(repository)
    if (discipline==""):
        context["subtitle"] = "Discipline"
        subfolder_list = get_subfolder_list(folderpath)
        context['subfolder_list'] = subfolder_list
        return json_response(context)
    else:
        allowed_disciplines = get_subfolder_names(folderpath)
        if discipline not in allowed_disciplines:
            return "Invalid Discipline"

    folderpath = os.path.join(repository, discipline)
    if (docCategory==""):
        context["subtitle"] = "Doc Category"
        subfolder_list = get_subfolder_list(folderpath)
        context['subfolder_list'] = subfolder_list
        return json_response(context)
    else:
        allowed_docCategories = get_subfolder_names(folderpath)
        if docCategory not in allowed_docCategories:
            return "Invalid docCategory"

    folderpath = os.path.join(repository, discipline, docCategory)
    if (docSubCategory==""):
        context["subtitle"] = "Doc SubCategory"
        subfolder_list = get_subfolder_list(folderpath)
        context['subfolder_list'] = subfolder_list
        return json_response(context)
    else:
        allowed_docSubCategories = get_subfolder_names(folderpath)
        if docSubCategory not in allowed_docSubCategories:
            return "Invalid docSubCategory"

    folderpath = os.path.join(repository, discipline, docCategory, docSubCategory)
    if (docClass==""):
        context["subtitle"] = "Doc Class"
        subfolder_list = get_subfolder_list(folderpath)
        context['subfolder_list'] = subfolder_list
        return json_response(context)
    else:
        allowed_docClasses = get_subfolder_names(folderpath)
        if docClass not in allowed_docClasses:
            return "Invalid docClass"

    this_folderpath = os.path.dirname(os.path.abspath(__file__))
    folderpath = os.path.join(repository, discipline, docCategory, docSubCategory, docClass)
    doc_json_path = os.path.join(this_folderpath, folderpath, "doc.json")
    try:
        doc_json = json.load(open(doc_json_path), object_pairs_hook=OrderedDict)
    except Exception as e:
        return "Error Occured" + str(e)

    return json_response(doc_json)


@app.route('/api/document/query/', methods=['GET'])
@app.route('/api/document/query/<project>/', methods=['GET'])
@app.route('/api/document/query/<project>/<discipline>/', methods=['GET'])
@app.route('/api/document/query/<project>/<discipline>/<docCategory>/', methods=['GET'])
@app.route('/api/document/query/<project>/<discipline>/<docCategory>/<docSubCategory>/', methods=['GET'])
@app.route('/api/document/query/<project>/<discipline>/<docCategory>/<docSubCategory>/<docClass>/', methods=['GET'])
@app.route('/api/document/query/<project>/<discipline>/<docCategory>/<docSubCategory>/<docClass>/<docInstance>', methods=['GET'])
def api_document(project="", discipline="", docCategory="", docSubCategory="", docClass="", docInstance=""):
    #this_folderpath = os.path.dirname(os.path.abspath(__file__))
    context = OrderedDict()
    context["title"] = "Open Document"

    documents = mongodb["documents"]

    pipeline = [
    { "$match" : {"$and" :[{}]}}, # match all documents, the and operator has a list with only one element {} which means match all
    { "$group" : {"_id" : "$meta.projectID"}} # group results by projectID
    ]
    subfolder_names = list(documents.aggregate(pipeline))

    if (project == "" ):
        context["subtitle"] = "Project"
        subfolder_list = []
        for folder in subfolder_names:
            entry = OrderedDict()
            entry["name"] = folder["_id"]
            entry["title"] = get_project_title(folder["_id"])
            entry["url"] = "/" + "/".join(["api", "document", "query", folder['_id']]) + "/"
            subfolder_list.append(entry)
        context['subfolder_list'] = subfolder_list
        return json_response(context)
    else:
        allowable_projects = [x['_id'] for x in subfolder_names]
        if project not in allowable_projects:
            return "Invalid Project"

    repository = get_repository(project)

    pipeline = [
    { "$match" : {"$and" :[{"meta.projectID" : project}]}},
    { "$group" : {"_id" : "$meta.discipline"}} # group results by discipline
    ]
    subfolder_names = list(documents.aggregate(pipeline))
    if (discipline == "" ):
        context["subtitle"] = "Discipline"
        subfolder_list = []
        for folder in subfolder_names:
            entry = OrderedDict()
            entry["name"] = folder["_id"]
            entry["title"] = get_folder_title(repository, folder["_id"])
            entry["url"] = "/" + "/".join(["api", "document", "query", project, folder['_id']]) + "/"
            subfolder_list.append(entry)
        context['subfolder_list'] = subfolder_list
        return json_response(context)
    else:
        allowable_disciplines = [x['_id'] for x in subfolder_names]
        if discipline not in allowable_disciplines:
            return "Invalid Discipline Entered"



    pipeline = [{ "$match" : {"$and" :[
                            {"meta.projectID" : project},
                            {"meta.discipline" : discipline}]}},
                { "$group" : {"_id" : "$meta.docCategory"}}]
    subfolder_names = list(documents.aggregate(pipeline))
    if (docCategory == "" ):
        subfolder_list = []
        for folder in subfolder_names:
            entry = OrderedDict()
            entry["name"] = folder["_id"]
            entry["title"] = get_folder_title(repository, discipline, folder["_id"])
            entry["url"] = "/" + "/".join(["api", "document", "query", project, discipline, folder['_id']]) + "/"
            subfolder_list.append(entry)
        context['subfolder_list'] = subfolder_list
        return json_response(context)
    else:
        allowable_docCategories = [x['_id'] for x in subfolder_names]
        if docCategory not in allowable_docCategories:
            return "Invalid docCategory Entered"


    pipeline = [{ "$match" : {"$and" :[ {"meta.projectID" : project},
                            {"meta.discipline" : discipline},
                            {"meta.docCategory" : docCategory}]}},
                { "$group" : {"_id" : "$meta.docSubCategory"}}]
    subfolder_names = list(documents.aggregate(pipeline))
    if (docSubCategory == "" ):
        subfolder_list = []
        for folder in subfolder_names:
            entry = OrderedDict()
            entry["name"] = folder["_id"]
            entry["title"] = get_folder_title(repository, discipline, docCategory, folder["_id"])
            entry["url"] = "/" + "/".join(["api", "document", "query", project, discipline, docCategory, folder['_id']]) + "/"
            subfolder_list.append(entry)
        context['subfolder_list'] = subfolder_list
        return json_response(context)
    else:
        allowable_docSubCategories = [x['_id'] for x in subfolder_names]
        if docSubCategory not in allowable_docSubCategories:
            return "Invalid docSubCategory Entered"

    pipeline = [{ "$match" : {"$and" :[ {"meta.projectID" : project},
                            {"meta.discipline" : discipline},
                            {"meta.docCategory" : docCategory},
                            {"meta.docSubCategory" : docSubCategory}]}},
                {"$group" : {"_id" : "$meta.docClass"}} ]
    subfolder_names = list(documents.aggregate(pipeline))
    if (docClass == "" ):
        subfolder_list = []
        for folder in subfolder_names:
            entry = OrderedDict()
            entry["name"] = folder["_id"]
            entry["title"] = get_folder_title(repository, discipline, docCategory, docSubCategory, folder["_id"])
            entry["url"] = "/" + "/".join(["api", "document", "query", project, discipline, docCategory, docSubCategory, folder['_id']]) + "/"
            subfolder_list.append(entry)
        context['subfolder_list'] = subfolder_list
        return json_response(context)
    else:
        allowable_docClasses = [x['_id'] for x in subfolder_names]
        if docClass not in allowable_docClasses:
            return "Invalid docClass Entered"



    query = { "$and" :[ {"meta.projectID" : project},
                            {"meta.discipline" : discipline},
                            {"meta.docCategory" : docCategory},
                            {"meta.docSubCategory" : docSubCategory},
                            {"meta.docClass" : docClass},
                            ]}
    docInstance_list = list(documents.find(query, {"meta.docInstance":1, "meta.docInstance_title":1}))
    if (docInstance == "" ):
        subfolder_list = []
        for doc in docInstance_list:
            entry = OrderedDict()
            entry["name"] = doc["meta"]["docInstance"]
            entry["title"] = doc["meta"]["docInstance_title"]
            entry["url"] = "/" + "/".join(["htm", "document", "db", doc['_id']]) + "/"
            subfolder_list.append(entry)
        context['subfolder_list'] = subfolder_list
        return json_response(context)
    else:
        allowable_docInstances = [x['meta']['docInstance'] for x in docInstance_list]
        if docInstance not in allowable_docInstances:
            return "Invalid docInstance Entered"


    query = { "$and" :[ {"meta.projectID" : project},
                            {"meta.discipline" : discipline},
                            {"meta.docCategory" : docCategory},
                            {"meta.docSubCategory" : docSubCategory},
                            {"meta.docClass" : docClass},
                            {"meta.docInstance" : docInstance},
                            ]}
    doc = documents.find_one(query)
    return json_response(doc)

@app.route('/api/document/db/', methods=['GET'])
def api_get_documents():
    documents = mongodb['documents']
    document_list = list(documents.find())
    return json_response(document_list), 200

@app.route('/api/document/db/<doc_id>/', methods=['GET'])
def api_get_document(doc_id):
    errors = OrderedDict()
    documents = mongodb['documents']
    docMongo = documents.find_one({"_id": doc_id})
    if (docMongo== None):
        errors['operation'] = ['Document with Document ID as requested could not be found']
        return json_response(errors), 404
    else:
        return json_response(docMongo)

@app.route('/api/document/db/', methods=['POST'])
def api_post_document():
    errors = OrderedDict()
    req = request.get_json()

    #perform a series of checks an return error responses
    #check if the request body contains 'doc'
    if ('resource' not in req):
        errors['message'] = "'resource' missing in request"
        return json_response(errors), 400

    #check if the raw document conforms to the generic document schema for the project (basically meta check)
    docRaw = req['resource']
    basicSchema = sDocPrj()
    docParsed = basicSchema.load(docRaw)
    if (len(docParsed.errors) > 0):
        errors["message"] = "The Document Meta Information has errors"
        errors["schema"] = docParsed.errors
        return json_response(errors), 400

    #check if the raw document conforms to the specific document schema for the class
    try:
        projectID = docRaw['meta']['projectID']
        repository = get_repository(projectID)
        discipline = docRaw['meta']['discipline']
        docCategory = docRaw['meta']['docCategory']
        docSubCategory = docRaw['meta']['docSubCategory']
        docClass = docRaw['meta']['docClass']

        # get the absolute folder path in folderpath
        this_folderpath = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(repository, discipline, docCategory, docSubCategory, docClass)
        docClassFolder = os.path.join(this_folderpath, path)
        schemaModuleFile = os.path.join(docClassFolder, "schema.py")
        docSchema = load_schema(schemaModuleFile)
    except FileNotFoundError as e:
        errors["message"] = "Schema File could not be found"
        errors["operation"] = str(e)
        return json_response(errors), 400

    docParsed = docSchema.load(docRaw)
    if (len(docParsed.errors) > 0):
        errors['message'] = "Document Contains Errors"
        errors["schema"] = docParsed.errors
        return json_response(errors), 400


    doc = docParsed.data
    docInstance = doc["meta"]["docInstance"]
    doc["_id"] = "-".join([projectID, discipline, docCategory, docSubCategory, docClass, docInstance])
    try:
        documents = mongodb['documents']
        documents.insert_one(doc)
    except pymongo.errors.DuplicateKeyError as e:
        errors['message'] = ['Insert Failed as Document ID already exists. Change docInstance to make it unique']
        errors['operation'] = str(e)
        return json_response(errors), 400
    except Exception as e:
        errors['message'] = ['Database Connection Error.']
        errors['operation'] = str(e)
        return json_response(errors), 400

    response = {}
    response["message"] = "Document Added Successfully"
    response["_id"] = doc["_id"]
    response["redirect_url"] = "/htm/document/db/"+doc["_id"]+"/"
    return json_response(response), 201

@app.route('/api/document/db/<doc_id>/', methods=['PUT'])
def api_put_document(doc_id):
    errors = OrderedDict()
    req = request.get_json()

    #perform a series of checks an return error responses
    #check if the request body contains 'doc'
    if ('resource' not in req):
        errors['message'] = "'resource' missing in request"
        return json_response(errors), 400

    #check if the raw document conforms to the generic document schema for the project (basically meta check)
    docRaw = req['resource']
    basicSchema = sDocPrj()
    docParsed = basicSchema.load(docRaw)
    if (len(docParsed.errors) > 0):
        errors["message"] = "The Document Meta Information has errors"
        errors["schema"] = docParsed.errors
        return json_response(errors), 400

    #check if the raw document conforms to the specific document schema for the class
    try:
        projectID = docRaw['meta']['projectID']
        repository = get_repository(projectID)
        discipline = docRaw['meta']['discipline']
        docCategory = docRaw['meta']['docCategory']
        docSubCategory = docRaw['meta']['docSubCategory']
        docClass = docRaw['meta']['docClass']

        # get the absolute folder path in folderpath
        this_folderpath = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(repository, discipline, docCategory, docSubCategory, docClass)
        docClassFolder = os.path.join(this_folderpath, path)
        schemaModuleFile = os.path.join(docClassFolder, "schema.py")
        docSchema = load_schema(schemaModuleFile)
    except FileNotFoundError as e:
        errors["message"] = "Schema File could not be found"
        errors["operation"] = str(e)
        return json_response(errors), 400

    docParsed = docSchema.load(docRaw)
    if (len(docParsed.errors) > 0):
        errors['message'] = "Document Contains Errors"
        errors["schema"] = docParsed.errors
        return json_response(errors), 400

    doc = docParsed.data
    try:
        documents = mongodb['documents']
        documents.update({"_id" : doc["_id"]}, doc)
    except Exception as e:
        errors['message'] = ['Database Connection Error.']
        errors['operation'] = str(e)
        return json_response(errors), 400

    return json_response({'message' : 'Document Updated Sucessfully', '_id' : doc['_id']}), 201


@app.route('/api/document/db/<doc_id>/', methods=['DELETE'])
def api_delete_document(doc_id):
    errors = OrderedDict()
    documents = mongodb["documents"]
    try:
        documents.delete_one({"_id" : doc_id})
    except Exception as e:
        errors['operation'] = str(e)
        return json_response(errors)

    response ={}
    response["message"] = "Deletion Successful"
    response["redirect_url"] = "/htm/document/"
    return json_response(response)


@app.route('/api/document/calculate/', methods=['POST'])
def api_calculate():
    errors={}
    req = request.get_json()
    if ('doc' not in req):
        errors['message'] = "'doc' missing in request"
        return json_response(errors), 400

    #check if the raw document conforms to the generic document schema for the project (basically meta check)
    docRaw = req['doc']
    basicSchema = sDocPrj()
    docParsed = basicSchema.load(docRaw)
    if (len(docParsed.errors) > 0):
        errors["message"] = "The Document Meta Information has errors"
        errors["schema"] = docParsed.errors
        return json_response(errors), 400

    #check if the raw document conforms to the specific document schema for the class
    projectID = docRaw['meta']['projectID']
    repository = get_repository(projectID)
    discipline = docRaw['meta']['discipline']
    docCategory = docRaw['meta']['docCategory']
    docSubCategory = docRaw['meta']['docSubCategory']
    docClass = docRaw['meta']['docClass']

    # get the absolute folder path in folderpath
    this_folderpath = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(repository, discipline, docCategory, docSubCategory, docClass)
    docClassFolder = os.path.join(this_folderpath, path)
    schemaModuleFile = os.path.join(docClassFolder, "schema.py")
    macroModuleFile = os.path.join(docClassFolder, "macro.py")

    try:
        docSchema = load_schema(schemaModuleFile)
    except FileNotFoundError as e:
        errors["message"] = "Schema File could not be found"
        errors["operation"] = str(e)
        return json_response(errors), 400

    try:
        calculate = load_function(macroModuleFile, 'calculate')
    except FileNotFoundError as e:
        errors["message"] = "Calculation Function could not be loaded"
        errors["operation"] = str(e)
        return json_response(errors), 400

    docParsed = docSchema.load(docRaw)
    if (len(docParsed.errors) > 0):
        errors['message'] = "Document Contains Errors"
        errors["schema"] = docParsed.errors
        return json_response(errors), 400

    doc = docParsed.data
    calculate(doc)
    return json_response(doc)


@app.route('/api/document/macro/', methods=['POST'])
def api_macro():
    response = {}
    response["message"] = "You successfully ran the macros"
    return json_response(response)

#then all htm views

@app.route('/htm/document/', methods=['GET', 'POST'])
def htm_Doc():
    if (request.method=='GET'):
        this_folderpath = os.path.dirname(os.path.abspath(__file__))
        folderpath = this_folderpath
        doc_json_path = os.path.join(folderpath, "base.json")
        try:
            doc_json = json.load(open(doc_json_path), object_pairs_hook=OrderedDict)
            doc = json.dumps(doc_json, indent=4)
        except Exception as e:
            return "Error Occured" + str(e)
        template = "/document/document.html"

        return render_template(template, doc=doc,authenticated=False)
    else:
        doc_file = request.files['doc']
        docRaw = json.loads(doc_file.read().decode('utf-8'))
        basicSchema = sDocPrj()
        docParsed = basicSchema.load(docRaw)
        if (len(docParsed.errors) > 0):
            errors["message"] = "The Document Meta Information has errors"
            errors["schema"] = docParsed.errors
            return json_response(errors), 400

        #check if the raw document conforms to the specific document schema for the class
        try:
            projectID = docRaw['meta']['projectID']
            repository = get_repository(projectID)
            discipline = docRaw['meta']['discipline']
            docCategory = docRaw['meta']['docCategory']
            docSubCategory = docRaw['meta']['docSubCategory']
            docClass = docRaw['meta']['docClass']
            path = os.path.join(repository, discipline, docCategory, docSubCategory, docClass, "doc.html")
            template = "/".join(path.split(os.sep))
        except:
            pass

        doc = json.dumps(docRaw, indent=4)
        return render_template(template, doc=doc, authenticated=False)




@app.route('/htm/documentauth/', methods=['GET', 'POST'])
@auth.login_required
def htm_DocAuth():
    if (request.method=='GET'):
        this_folderpath = os.path.dirname(os.path.abspath(__file__))
        folderpath = this_folderpath
        doc_json_path = os.path.join(folderpath, "base.json")
        try:
            doc_json = json.load(open(doc_json_path), object_pairs_hook=OrderedDict)
            doc = json.dumps(doc_json, indent=4)
        except Exception as e:
            return "Error Occured" + str(e)
        template = "/document/document.html"
        return render_template(template, doc=doc,authenticated=True)
    else:
        doc_file = request.files['doc']
        docRaw = json.loads(doc_file.read().decode('utf-8'))
        basicSchema = sDocPrj()
        docParsed = basicSchema.load(docRaw)
        if (len(docParsed.errors) > 0):
            errors["message"] = "The Document Meta Information has errors"
            errors["schema"] = docParsed.errors
            return json_response(errors), 400

        #check if the raw document conforms to the specific document schema for the class
        try:
            projectID = docRaw['meta']['projectID']
            repository = get_repository(projectID)
            discipline = docRaw['meta']['discipline']
            docCategory = docRaw['meta']['docCategory']
            docSubCategory = docRaw['meta']['docSubCategory']
            docClass = docRaw['meta']['docClass']
            path = os.path.join(repository, discipline, docCategory, docSubCategory, docClass, "doc.html")
            template = "/".join(path.split(os.sep))
        except:
            pass

        doc = json.dumps(docRaw, indent=4)
        return render_template(template, doc=doc, authenticated=True)


@app.route('/htm/document/tpl/<repository>/<discipline>/<docCategory>/<docSubCategory>/<docClass>/', methods=['GET'])
def htm_template(repository, discipline, docCategory, docSubCategory, docClass):
    this_folderpath = os.path.dirname(os.path.abspath(__file__))
    folderpath = os.path.join(this_folderpath, repository, discipline, docCategory, docSubCategory, docClass)
    doc_html_path = os.path.join(folderpath, "doc.html")
    doc_json_path = os.path.join(folderpath, "doc.json")
    try:
        doc_html = open(doc_html_path)
        doc_json = json.load(open(doc_json_path), object_pairs_hook=OrderedDict)
        doc = json.dumps(doc_json, indent=4)
    except Exception as e:
        return "Error Occured" + str(e)
    ostemplatepath = os.path.join(repository, discipline, docCategory, docSubCategory, docClass, "doc.html")
    template = "/".join(ostemplatepath.split(os.sep))

    return render_template(template, doc=doc, authenticated=False)


@app.route('/htm/document/db/<doc_id>/', methods=['GET'])
@auth.login_required
def htm_dbDoc(doc_id):
    context = {}
    documents = mongodb["documents"]
    doc = documents.find_one({"_id": doc_id})
    if (doc==None):
        return "Document not found"
    else :
        projectID = doc["meta"]["discipline"]
        repository = get_repository(projectID)
        discipline = doc["meta"]["discipline"]
        docCategory = doc["meta"]["docCategory"]
        docSubCategory = doc["meta"]["docSubCategory"]
        docClass = doc["meta"]["docClass"]
        path = os.path.join(repository, discipline, docCategory, docSubCategory, docClass, "doc.html")
        template = "/".join(path.split(os.sep))
        doc = json.dumps(doc, indent=4)
        if g.user:
            authenticated=True
        else:
            authenticated = False

        return render_template(template, doc=doc, authenticated=authenticated)
