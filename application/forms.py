"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators

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
    title = wtf.TextField('Title')
    description = wtf.TextAreaField('Description')
    order = wtf.IntegerField('Order', default=0)
    visible = wtf.BooleanField('Visible')
    update_image = wtf.BooleanField('Update image');
    image = wtf.FileField('Image')
    category_id = wtf.HiddenField()
    key_id = wtf.HiddenField()
