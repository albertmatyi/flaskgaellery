"""
Initialize Flask app

"""

from flask import Flask
from random import random, Random
from flask.helpers import jsonify, json
import re
from google.appengine.api import datastore_types
import sys
import os

app = Flask('application')
app.config.from_object('application.settings')

'''
    Add markdown support
'''
#sys.path.append(os.path.join(os.path.dirname(file), 'lib'))
from flaskext.fmarkdown import Markdown
Markdown(app)

import urls

def random_int(a, b): return Random().randint(a,b)

def json_helper(array, name):
    firstEl = True
    ret = ''
    for elQry in array:
        el = elQry.jsond()
        if not firstEl:
            ret = ret + ', '
        else:
            firstEl = False
        ret = ret + str(el['id']) + ' : { \'key_id\':'+ str(el['id'])
        for prop, val in el.items():
            if type(val) is str or type(val) is datastore_types.Text:
                val = reduce(lambda s1, s2: s1+s2, re.split('\r+', str(val))) 
            val = json.dumps(val)
            ret = ret + ', \'' + str(prop) + '\'' + ': ' + val
            pass
        ret = ret + '}'
    return 'var ' + name + ' = {' + ret+'};'
    pass


app.jinja_env.globals.update(jsonify=json_helper)

app.jinja_env.globals.update(len=len)

app.jinja_env.globals.update(random_int=random_int)