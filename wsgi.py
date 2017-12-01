# the below wsgi works on digitalocean
from clappets import app

if __name__ == "__main__":
    app.run(debug=True, threaded=True)


'''
# the below works on pythonanywhere

import sys
path = '/home/sraheja/flaskclappets/'
if path not in sys.path:
   sys.path.append(path)

from clappets import app as application
'''
