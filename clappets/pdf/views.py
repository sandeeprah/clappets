import os
import json
import tempfile

import pdfkit
from flask import render_template, make_response, request
from clappets import app, mongodb
from clappets.document.utils import get_repository
from clappets.core import sDocPrj
from clappets.utils import json_response, change_date_format
from collections import OrderedDict


@app.route('/pdf/document/', methods=['POST'])
def pdf_report():
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

    doc = docParsed.data
    #check if the raw document conforms to the specific document schema for the class
    projectID = doc['meta']['projectID']
    repository = get_repository(projectID)
    discipline = doc['meta']['discipline']
    docCategory = doc['meta']['docCategory']
    docSubCategory = doc['meta']['docSubCategory']
    docClass = doc['meta']['docClass']
    title = doc["meta"]["docInstance_title"]
    rev = doc['meta']['rev']
    date = doc['meta']['date']
    doc_no = doc['meta']['doc_no']

    path = os.path.join(repository, discipline, docCategory, docSubCategory, docClass, "doc.html")
    template = "/".join(path.split(os.sep))
    doc = json.dumps(doc, indent=4)
    main_content = render_template(template, doc=doc)

    options = {
        'page-size' : 'A4',
        'margin-top':'25mm',
        'margin-bottom':'19mm',
        'margin-left':'19mm',
        'margin-right':'19mm',
        'encoding':'UTF-8',
        'print-media-type' : None,
#            'header-left' : 'My Static Header',
        'header-line' : None,
        'header-font-size' : '8',
        'header-font-name' : 'Calibri',
        'header-spacing' : '5',
        'footer-left' : "template_url : http://www.clappets.com/htm/document/tpl/mec/dat/pmp/c01/",
        'footer-line' : None,
        'footer-font-size' : '8',
        'footer-font-name' : 'Calibri',
        'footer-spacing' : '5',
        'disable-smart-shrinking' : None,
        'no-stop-slow-scripts' : None,
        'javascript-delay': 300,
        'enable-javascript': None,
        'debug-javascript': None,
        '--encoding': "utf-8"
    }

    this_folderpath = os.path.dirname(os.path.abspath(__file__))
#    wkhtmltopdf_path = r'/home/appadmin/wkhtmltox/bin/wkhtmltopdf'
    wkhtmltopdf_path = r'/home/sandeep/www/wkhtmltox/bin/wkhtmltopdf'
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    this_folderpath = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(this_folderpath, 'print.css')

    context_header = {}
    context_header['title'] = title
    context_header['rev'] = rev
    context_header['doc_no'] = doc_no

    context_header['date'] = change_date_format(date)
    add_pdf_header(options, context_header=context_header)

    try:
        pdf = pdfkit.from_string(main_content, False, configuration=config, options=options, css=css_path)
    except Exception as e:
        print(str(e))
        return (str(e))
    finally:
        os.remove(options['header-html'])

    response = build_response(pdf)
    return response




@app.route('/pdf/document/db/<doc_id>/', methods=['GET'])
def pdf_dbDoc(doc_id):
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
        title = doc["meta"]["docInstance_title"]
        rev = doc['meta']['rev']
        doc_id = doc['_id']

        path = os.path.join(repository, discipline, docCategory, docSubCategory, docClass, "doc.html")
        template = "/".join(path.split(os.sep))
        doc = json.dumps(doc, indent=4)
        main_content = render_template(template, doc=doc)

        options = {
            'page-size' : 'A4',
            'margin-top':'25mm',
            'margin-bottom':'19mm',
            'margin-left':'19mm',
            'margin-right':'19mm',
            'encoding':'UTF-8',
            'print-media-type' : None,
#            'header-left' : 'My Static Header',
            'header-line' : None,
            'header-font-size' : '8',
            'header-font-name' : 'Calibri',
            'header-spacing' : '5',
            'footer-left' : "template_url : http://www.clappets.com/htm/document/tpl/mec/dat/pmp/c01/",
            'footer-line' : None,
            'footer-font-size' : '8',
            'footer-font-name' : 'Calibri',
            'footer-spacing' : '5',
            'disable-smart-shrinking' : None,
            'no-stop-slow-scripts' : None,
            '--encoding': "utf-8"
        }

        this_folderpath = os.path.dirname(os.path.abspath(__file__))
        wkhtmltopdf_path = "/" + os.path.join("home", "wkhtmltox", "bin", "wkhtmltopdf")
        wkhtmltopdf_path = r'/home/appadmin/wkhtmltox/bin/wkhtmltopdf'
#        wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        this_folderpath = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(this_folderpath, 'print.css')

        context_header = {}
        context_header['title'] = title
        context_header['rev'] = rev
        context_header['doc_no'] = doc_no
        add_pdf_header(options, context_header=context_header)

        try:
            pdf = pdfkit.from_string(main_content, False, options=options, configuration=config, css=css_path)
        except Exception as e:
            print(str(e))
            return (str(e))
        finally:
            os.remove(options['header-html'])

        response = build_response(pdf)
        return response




def add_pdf_header(options, context_header):
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as header:
        options['header-html'] = header.name
        header.write(
            render_template('document/header.html', context_header=context_header).encode('utf-8')
        )
    return

def add_pdf_footer(options):
    # same behaviour as add_pdf_header but without passing any variable
    return

def build_response(pdf):
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    filename = 'pdf-from-html.pdf'
    response.headers['Content-Disposition'] = ('attachment; filename=' + filename)
    return response
