import json
import re
import imp
import math
from flask import current_app
from bson import json_util
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import os


def json_response(input):
    str_response = json.dumps(input, indent=4, default=json_util.default)
    return current_app.response_class(str_response, mimetype='application/json')


def sendMail(to, fro, subject, text, files=[],server="localhost"):
    assert type(to)==list
    assert type(files)==list
    msg = MIMEMultipart()
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text, 'html') )

    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file,"rb").read() )
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(file))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(fro, to, msg.as_string() )
    smtp.close()

# Example:
#sendMail(['maSnun <masnun@gmail.com>'],'phpGeek <masnun@leevio.com>','Hello Python!','Heya buddy! Say hello to Python! :)',['masnun.py','masnun.php'])

def load_function(filepath, function_name):
    fn = None
    mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])
    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)

    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name, filepath)

    if hasattr(py_mod, function_name):
        fn = getattr(py_mod, function_name)

    return fn


def change_date_format(dt):
        return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', dt)

def parseFloat(value):
    try:
        return float(value)
    except Exception:
        return math.nan

def roundit(value,  max_decim=6, allowed_error=0.001):
    try:
        value = float(value)
    except Exception:
        return value

    
    decims = 1
    rounded_value = round(value, max_decim)

    if (value == 0):
        rounded_value = 0
    else:
        for decims in range(1, max_decim+1):
            rounded_value = round(value, decims)
            abs_error = abs(value - rounded_value)
            rel_error = abs_error/abs(value)
            if rel_error < allowed_error:
                return rounded_value


    if (isinstance(value, str)):
        return str(rounded_value)
    else:
        return rounded_value
