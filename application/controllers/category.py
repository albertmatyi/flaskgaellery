"""
This controller is responsible for handling Categories
"""


from application import app, models
from application.decorators import login_required, admin_required
from application.forms import CategoryForm
from application.models import CategoryModel, ImageModel, v2m, ROOT_CAT_ID,\
    ROOT_CAT_DUMMY, CircularCategoryException
from flask import render_template, flash, url_for, redirect
from flask.globals import request
from flask.helpers import jsonify
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError


#from models import CategoryModel

@admin_required
def admin():
    return redirect(url_for('admin_categories'), 302)
    pass

@admin_required
def admin_categories(parent_id=ROOT_CAT_ID):
    """List all categories"""
    form = CategoryForm()
    if form.validate_on_submit():
        if len(form.key_id.data) > 0 and long(form.key_id.data)  > 0:
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
    category_path = [ROOT_CAT_DUMMY]
    category = None
    
    if parent_id != ROOT_CAT_ID:
        category = CategoryModel.get_by_id(parent_id)
        category_path += category.get_path_to_root() + [category]
        categories = [c for c in category.get_subcategories(False)]
        form.parent_id.data = category.key().id()
    else:
        category = ROOT_CAT_DUMMY
        categories = [c for c in CategoryModel.get_root_categories(False)]
        form.parent_id.data = ROOT_CAT_ID
    categories = sorted(categories, key=lambda c: c.order)
    return render_template('category/admin_list.html', categories=categories, form=form, category_path=category_path, current_category=category, all_categories=[c for c in CategoryModel.all()])


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
    contents = [c.jsond() for c in ImageModel.all().filter('category_id', parent_id).filter('visible', True)]
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


