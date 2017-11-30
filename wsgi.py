
# Below are templates for Django and Flask.  You should update the file
# appropriately for the web framework you're using, and then
# click the 'Reload /yourdomain.com/' button on the 'Web' tab to make your site
# live.

# +++++++++++ VIRTUALENV +++++++++++
# If you want to use a virtualenv, set its path on the web app setup tab.
# Then come back here and import your application object as per the
# instructions below


# +++++++++++ CUSTOM WSGI +++++++++++
# If you have a WSGI file that you want to serve using PythonAnywhere, perhaps
# in your home directory under version control, then use something like this:
#
#import sys
#
#path = '/home/sraheja/path/to/my/app
#if path not in sys.path:
#    sys.path.append(path)
#
#from my_wsgi_file import application


# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
#import os
#import sys
#
## assuming your django settings file is at '/home/sraheja/mysite/mysite/settings.py'
## and your manage.py is is at '/home/sraheja/mysite/manage.py'
#path = '/home/sraheja/mysite'
#if path not in sys.path:
#    sys.path.append(path)
#
#os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
#
## then, for django >=1.5:
#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()
## or, for older django <=1.4
#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()



# +++++++++++ FLASK +++++++++++
# Flask works like any other WSGI-compatible framework, we just need
# to import the application.  Often Flask apps are called "app" so we
# may need to rename it during the import:
#
#
#import sys
#
## The "/home/sraheja" below specifies your home
## directory -- the rest should be the directory you uploaded your Flask
## code to underneath the home directory.  So if you just ran
## "git clone git@github.com/myusername/myproject.git"
## ...or uploaded files to the directory "myproject", then you should
## specify "/home/sraheja/myproject"
#path = '/home/sraheja/path/to/flask_app_directory'
#if path not in sys.path:
#    sys.path.append(path)
#
## After you uncomment the line below, the yellow triangle on the left
## side in our in-browser editor shows a warning saying:
##     'application' imported but unused.
## You can ignore this error. The line is necessary, and the variable
## is used externally.
#from main_flask_app_file import app as application
#
# NB -- many Flask guides suggest you use a file called run.py; that's
# not necessary on PythonAnywhere.  And you should make sure your code
# does *not* invoke the flask development server with app.run(), as it
# will prevent your wsgi file from working.


import sys
path = '/home/sraheja/flaskclappets/'
if path not in sys.path:
   sys.path.append(path)

from clappets import app as application
