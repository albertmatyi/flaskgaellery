"""
This controller is responsible for handling Categories
"""


from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import render_template, flash, url_for, redirect

#from models import CategoryModel
from  application.decorators import login_required, admin_required
from application.forms import CategoryForm
from application.models import CategoryModel, ImageModel
from application import app
from flask.globals import request
from flask.helpers import jsonify
from repr import repr

@admin_required
def admin_categories():
    """List all categories"""
    categories = CategoryModel.all()
    form = CategoryForm()
    kvps = [(c.key().id(), c.title) for c in CategoryModel.all()]
    kvps += [(-1, None)]
    form.parent_id.choices = kvps;
    if form.validate_on_submit():
        category = CategoryModel(
            title = form.title.data,
            description = form.description.data,
            parent_id = form.parent_id.data
        )
        try:
            category.put()
            category_id = category.key().id()
            flash(u'Category %s successfully saved.' % category_id, 'success')
            return redirect(url_for('admin_categories'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('admin_categories'))
        pass
    return render_template('category/admin_list.html', categories=categories, form=form)


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


def category(category_id):
    ''' This will render the main page with the selected category defined by category_id, and with the
    content that it contains  '''
    contents = [c.jsond() for c in ImageModel.all().filter('category_id', category_id)]
    if request.is_xhr:
        categories = [c.jsond() for c in CategoryModel.all().filter('parent_id', category_id)]
        return jsonify(categories=categories, contents=contents)
    else:
        category = CategoryModel.get_by_id(category_id)
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


