"""
Initialize Flask app

"""

from flask import Flask
from random import random, Random
from flask.helpers import jsonify

app = Flask('application')
app.config.from_object('application.settings')

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
            ret = ret + ', \'' + str(prop) + '\'' + ': ' + '\'' + str(val).replace('\'', '\\\'') +'\''
            pass
        ret = ret + '}'
    return 'var ' + name + ' = {' + ret+'}'
    pass


app.jinja_env.globals.update(jsonify=json_helper)

app.jinja_env.globals.update(random_int=random_int)