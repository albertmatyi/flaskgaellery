"""
Initialize Flask app

"""

from flask import Flask
from random import random, Random

app = Flask('application')
app.config.from_object('application.settings')

import urls

def random_int(a, b): return Random().randint(a,b)

app.jinja_env.globals.update(random_int=random_int)