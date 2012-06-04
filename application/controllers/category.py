"""
This controller is responsible for handling Categories
"""


from application import app, models
from application.decorators import  admin_required
from application.forms import CategoryForm
from application.models import CategoryModel, ImageModel, v2m, ROOT_CAT_ID, \
 CircularCategoryException
from flask import render_template, flash, url_for, redirect
from flask.globals import request
from flask.helpers import jsonify
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError
from application.controllers import image
from application.controllers.image import get_images_for_category

#from models import CategoryModel

@admin_required
def admin():
    return redirect(url_for('admin_categories'), 302)
    pass

@admin_required
def admin_categories(parent_id=ROOT_CAT_ID):
    """List all categories"""
    form = CategoryForm(prefix='category')
    if form.validate_on_submit():
        if len(form.key_id.data) > 0 and long(form.key_id.data) > 0:
            category = CategoryModel.get_by_id(long(form.key_id.data)); 
        else:
            category = CategoryModel()
        v2m(form, category)
        try:
            category.put()
            category_id = category.key().id()
            flash(u'Category %s successfully saved.' % category_id, 'success')
            return redirect(url_for('admin_category', parent_id=category.parent_id))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('admin_category', parent_id=category.parent_id))
        except CircularCategoryException as cce:
            flash(cce.message, 'error')
            return redirect(url_for('admin_category', parent_id=category.parent_id))
        pass
    elif form.is_submitted():
        parent_id = long(form.parent_id.data)
    (categories, category_path, all_categories) = CategoryModel.get_categories_info(parent_id)
    form.parent_id.data = category_path[-1].key().id()
    reset_category = CategoryModel()
    reset_category.parent_id = parent_id
    return render_template('category/admin_categories.html',
                           categories=categories, form=form,
                           category_path=category_path,
                           current_category=category_path[-1],
                           all_categories=all_categories,
                           reset_category=reset_category)

@admin_required
def delete_category(category_id):
    """Delete an category object"""
    category = CategoryModel.get_by_id(category_id)
    parent_id = category.parent_id
    try:
        category.delete()
        flash(u'Category %s successfully deleted.' % category_id, 'success')
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info')
    return redirect(url_for('admin_category', parent_id=parent_id))
    
@admin_required
@app.route('/admin/initdb')
def init_db():
    models.init_db()
    return redirect(url_for('home'))
    pass

def init_sub_tree_along_path(category, path, visible_only=True):
    '''
        Initializes the subcategories for the category recursively, if the category is in the path
    '''
    category.subcategories = []
    query_set = CategoryModel.all().filter('parent_id', category.key().id())
    if visible_only:
        query_set.filter('visible', True)
    for cat in query_set:
        if cat.key().id() in path:
            init_sub_tree_along_path(cat, path)
            pass
        category.subcategories += [cat] 
    pass


def category(parent_id=ROOT_CAT_ID):
    ''' This will render the main page with the selected category defined by parent_id, and with the
    content that it contains  '''
    contents = get_images_for_category(parent_id)
    if request.is_xhr:
        categories = [c.jsond() for c in CategoryModel.all().filter('parent_id', parent_id).filter('visible', True)]
        categories = sorted(categories, key=lambda c: c.order)
        return jsonify(categories=categories, contents=contents)
    else:
        category = CategoryModel.get_by_id(parent_id)
        path = None
        if category:
            path = category.get_path_ids_to_root() + [category.key().id()]
        categories = []
        for cat in CategoryModel.all().filter('parent_id', ROOT_CAT_ID).filter('visible', True):
            if path is not None and cat.key().id() in path:
                init_sub_tree_along_path(cat, path)
            categories += [cat]
            pass
        pass
        categories = sorted(categories, key=lambda c: c.order)
        contents = sorted(contents, key=lambda c: c['order'])
        return render_template('category/index.html', categories=categories, contents=contents)
    pass

def home():
    ''' This will render the root category'''
    return category(ROOT_CAT_ID)
    pass

@admin_required
def move_category(category_id, parent_id=ROOT_CAT_ID):
    cat = CategoryModel.get_by_id(category_id)
    cat.parent_id = parent_id
    try:
        cat.put()
    except CircularCategoryException as cce:
        flash(cce.message, 'error')
        return redirect(url_for('admin_category', parent_id=parent_id))
    return redirect(url_for('admin_category', parent_id=parent_id), 302);
    pass


