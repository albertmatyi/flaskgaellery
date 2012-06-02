"""
This controller is responsible for handling Categories
"""


from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import render_template, flash, url_for, redirect

#from models import CategoryModel
from  application.decorators import login_required, admin_required
from application.forms import CategoryForm
from application.models import CategoryModel, ImageModel
from flask.globals import request
from flask.helpers import jsonify
from application import app, models

def v2m(form, mdl_obj):
    for prop, val in vars(form).iteritems():
        if not prop.startswith('__'):
            if prop in dir(mdl_obj):
                setattr(mdl_obj,prop,val.data)
    pass

@admin_required
def admin():
    return redirect(url_for('admin_categories'), 302)
    pass

@admin_required
def admin_categories(parent_id=-1):
    """List all categories"""
    categories = [c for c in CategoryModel.all().filter('parent_id', parent_id)]
    form = CategoryForm()
    kvps = [(-1, None)]
    kvps += [(c.key().id(), c.title) for c in CategoryModel.all()]
    form.parent_id.choices = kvps;
    if form.validate_on_submit():
        if len(form.key_id.data) > 0 and long(form.key_id.data)  > 0:
            category = CategoryModel.get_by_id(long(form.key_id.data)); 
        else:
            category = CategoryModel.
        v2m(form, category)
        try:
            category.put()
            category_id = category.key().id()
            flash(u'Category %s successfully saved.' % category_id, 'success')
            return redirect(url_for('admin_categories'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('admin_categories'))
        pass
    return render_template('category/admin_list.html', categories=categories, form=form, categoriesJS = [c.jsond() for c in categories])


@admin_required
def delete_category(category_id):
    """Delete an category object"""
    category = CategoryModel.get_by_id(category_id)
    try:
        category.delete()
        flash(u'Category %s successfully deleted.' % category_id, 'success')
        return redirect(url_for('admin_categories'))
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info')
        return redirect(url_for('admin_categories'))
@admin_required
@app.route('/admin/initdb')
def initDB():
    models.initDB()
    return redirect(url_for('home'))
    pass

def init_sub_tree_along_path(category, path):
    '''
        Initializes the subcategories for the category recursively, if the category is in the path
    '''
    category.subcategories = []
    for cat in CategoryModel.all().filter('parent_id', category.key().id()):
        if cat.key().id() in path:
            init_sub_tree_along_path(cat, path)
            pass
        category.subcategories += [cat] 
    pass


def category(parent_id=-1):
    ''' This will render the main page with the selected category defined by parent_id, and with the
    content that it contains  '''
    contents = [c.jsond() for c in ImageModel.all().filter('category_id', parent_id)]
    if request.is_xhr:
        categories = [c.jsond() for c in CategoryModel.all().filter('parent_id', parent_id)]
        return jsonify(categories=categories, contents=contents)
    else:
        category = CategoryModel.get_by_id(parent_id)
        path = None
        if category:
            path = category.get_path_ids_to_root() + [category.key().id()]
        categories = []
        for cat in CategoryModel.all().filter('parent_id', -1):
            if path is not None and cat.key().id() in path:
                init_sub_tree_along_path(cat, path)
            categories += [cat]
            pass
        pass
        return render_template('category/index.html', categories=categories, contents=contents)
    pass

def home():
    ''' This will render the root category'''
    return category(-1)
    pass


