import os
import imp
import json
import pymongo
from clappets import mongodb, app
from collections import OrderedDict
from flask import request, render_template, jsonify, abort, redirect


def generate_breadcrumbs(bcpath, rootname):
    # generate an array from path of levels in heirarchial sequence
    bcpath = bcpath.split('/')
    # remove all occurences of empty strings
    bcpath = [value for value in bcpath if value != ""]
    # prepend a root name when no path parameter is provided
    bcpath = [rootname] + bcpath
    levels = len(bcpath)
    if levels==0:
        url_list = []
    if levels==1:
        url_list = []
        url_list.append("#")
    if levels>=2:
        url_list = []
        url_list.append("#")
        url_list.append("..")
        for i in range(2, levels):
            url = url_list[i-1] + "/" + ".."
            url_list.append(url)

    # reverse the order of url_list
    bc_urls = url_list[::-1]

    # generate breadcrumbs
    breadcrumbs = []
    for i in range(0, len(bcpath)):
        entry = {"name" : bcpath[i], "href" : bc_urls[i]}
        breadcrumbs.append(entry)

    return breadcrumbs

def get_subfolder_names(folderpath):
    this_folderpath = os.path.dirname(os.path.abspath(__file__))
    abs_folderpath = os.path.join(this_folderpath, folderpath)
    subfolder_names = [f.name for f in os.scandir(abs_folderpath) if f.is_dir()]
    if ("__pycache__" in subfolder_names):
        subfolder_names.remove("__pycache__")
    return subfolder_names


def get_subfolder_list(folderpath):
    this_folderpath = os.path.dirname(os.path.abspath(__file__))
    abs_folderpath = os.path.join(this_folderpath, folderpath)
    subfolder_list = []
    subfolder_names = get_subfolder_names(abs_folderpath)

    print('folderpath is {}'.format(folderpath))
    if (folderpath != ''):
        entry = OrderedDict()
        entry["name"] = ".."
        entry["title"] = " ^^ Level Up ^^"
        entry["type"] = "folder"
        prefix_split = ["api", "document", "tpl"]
        folderpath_split = folderpath.split(os.sep)
        if ("" in folderpath_split):
            folderpath_split.remove("")
        url_split = prefix_split + folderpath_split + [".."]
        url = "/".join(url_split)
        url = "/" + url + "/"
        entry["url"] = url
        subfolder_list.append(entry)

    for subfolder in subfolder_names:
        subfolder_path = os.path.join(abs_folderpath, subfolder)
        subfolder_type = "N"
        meta_file = os.path.join(subfolder_path, "_meta.json")
        try:
            meta = json.load(open(meta_file))
            subfolder_title = meta["title"]
            subfolder_type = "folder"
        except :
            subfolder_title = ""

        docfile = os.path.join(subfolder_path, "doc.html")
        try:
            doc = open(docfile)
            subfolder_type = "file"
        except:
            pass

        entry = OrderedDict()

        entry["name"] = subfolder
        entry["title"] = subfolder_title
        entry["type"] = subfolder_type
        if (subfolder_type=='file'):
            prefix_split = ["htm", "document", "tpl"]
        else:
            prefix_split = ["api", "document", "tpl"]
        folderpath_split = folderpath.split(os.sep)
        if ("" in folderpath_split):
            folderpath_split.remove("")
        url_split = prefix_split + folderpath_split + [subfolder]
        url = "/".join(url_split)
        url = "/" + url + "/"
        entry["url"] = url
        subfolder_list.append(entry)
    return subfolder_list


def get_folder_title(repository, discipline=None, docCategory=None, docSubCategory=None, docClass=None):
    path_array = []
    path_array.append(repository)
    if(discipline is not None):
        path_array.append(discipline)
    if(docCategory is not None):
        path_array.append(docCategory)
    if(docSubCategory is not None):
        path_array.append(docSubCategory)
    if(docClass is not None):
        path_array.append(docClass)

    path = os.sep.join(path_array)
    # get the absolute folder path in folderpath
    this_folder_path = os.path.dirname(os.path.abspath(__file__))
    folderpath = os.path.join(this_folder_path, path)
    metafile = os.path.join(folderpath, "_meta.json")
    try:
        meta = json.load(open(metafile))
        folder_title = meta["title"]
    except:
        folder_title = ""

    return folder_title

def get_project_title(projectID):
    try:
        projects = mongodb["projects"]
        project = projects.find_one({"_id": projectID})
        name = project['title']
    except:
        name = ""
    return name


def load_schema(filepath):
    class_inst = None
    expected_class = 'docSchema'
    mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])
    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)

    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name, filepath)

    if hasattr(py_mod, expected_class):
        class_inst = getattr(py_mod, expected_class)()

    return class_inst

def get_repository(projectID):
    return "root"


def render_document(discipline,docCategory,docSubCategory,docClass):
    path= app.root_path
    project_path = os.path.sep.join(app.instance_path.split(os.path.sep)[:-1])
    folderpath = os.path.join(project_path, 'clappets','document','root', discipline, docCategory, docSubCategory, docClass)
    try:
        doc_html_path = os.path.join(folderpath, "doc.html")
        doc_json_path = os.path.join(folderpath, "doc.json")
        doc_html = open(doc_html_path)
        doc_json = json.load(open(doc_json_path), object_pairs_hook=OrderedDict)
        doc = json.dumps(doc_json, indent=4)
    except Exception as e:
        return "Error Occured" + str(e)

    ostemplatepath = os.path.join('root', discipline, docCategory, docSubCategory, docClass, "doc.html")
    template = "/".join(ostemplatepath.split(os.sep))

    return render_template(template, doc=doc, authenticated=False)
