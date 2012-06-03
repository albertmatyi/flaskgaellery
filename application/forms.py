"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators


class ExampleForm(wtf.Form):
    example_name = wtf.TextField('Name', validators=[validators.Required()])
    example_description = wtf.TextAreaField('Description', validators=[validators.Required()])

class CategoryForm(wtf.Form):
    title = wtf.TextField('Title', validators=[validators.Required()])
    order = wtf.IntegerField('Order')
    visible = wtf.BooleanField('Visible')
    autoscroll = wtf.BooleanField('Auto scroll')
    menu_entry = wtf.BooleanField('Menu entry')
    non_menu_category = wtf.BooleanField('Non-menu category')
    key_id = wtf.HiddenField()
    parent_id = wtf.HiddenField()

class ImageForm(wtf.Form):
    title = wtf.TextField('Title', validators=[validators.Required()])
    description = wtf.TextAreaField('Description')
    category_id = wtf.SelectField('Parent category', coerce=int)
    image = wtf.FileField('Image')
