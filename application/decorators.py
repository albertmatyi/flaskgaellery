"""
decorators.py

Decorators for URL handlers

"""

from functools import wraps
from google.appengine.api import users
from flask import redirect, request
from flask.helpers import url_for


def login_required(func):
    """Requires standard login credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not users.get_current_user():
            return redirect(users.create_login_url(request.url))
        return func(*args, **kwargs)
    return decorated_view

administrators = ['albertmatyi@gmail.com', 'anabella.veress@googlemail.com', 'bakosstamas@gmail.com']
def admin_required(func):
    """Requires App Engine admin credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        usr = users.get_current_user()
        if not usr:
            return redirect(users.create_login_url(request.url))
        elif usr.email().lower() not in administrators:
            return redirect(url_for('home'), 302)
        return func(*args, **kwargs)
    return decorated_view

