"""
This controller is responsible for handling Categories
"""


from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import render_template, flash, url_for, redirect

#from models import ImageModel
from  application.decorators import admin_required
from application.forms import ImageForm
from application.models import ImageModel, CategoryModel, ROOT_CAT_ID, v2m
from google.appengine.api import blobstore, images, files
from werkzeug.datastructures import FileStorage
from jinja2 import environment
from flask.templating import Environment

@admin_required
def create_thumbnail(blob_key):
    ''' Creates a thumbnail for the image stored at blob_key 
    @param blob_key: the key for the blobstore where the image is stored
    @return: A touple containing: 
            the blob_key of the thumbnail
            the width of the thumbnail
            the height of the thumbnail
    '''
    img = images.Image(blob_key=blob_key,)
    img.resize(width=80, height=100)
    thumbnail = img.execute_transforms(output_encoding=images.PNG)
    # Create the file
    file_name = files.blobstore.create(mime_type='image/png')
    # Open the file and write to it
    with files.open(file_name, 'a') as f:
        f.write(thumbnail)
    # Finalize the file. Do this before attempting to read it.
    files.finalize(file_name)
    return (str(files.blobstore.get_blob_key(file_name)), img.width, img.height)
    pass

@admin_required
def admin_images(parent_id= -1):
    """
        List all images from within a category
    """
    category_id = parent_id
    form = ImageForm(prefix='image')
    if form.validate_on_submit():
        is_new = False
        if len(form.key_id.data) > 0 and long(form.key_id.data) > 0:
            image = ImageModel.get_by_id(long(form.key_id.data))
        else:
            image = ImageModel()
            is_new = True
        v2m(form, image)
        category_id = long(form.category_id.data)
        blob_key = ''
        thumb_blob_key = ''
        w = 0
        h = 0
        if type(form.image.data) == FileStorage and (is_new or form.update_image.data):
            blob_key = form.image.data.mimetype_params['blob-key']
            (thumb_blob_key, w, h) = create_thumbnail(blob_key)
        elif not is_new and form.update_image: # we set to update with an empty image so we delete the one in the db
            blobstore.delete([image.image_blob_key, image.image_thumb_blob_key ])
        image.image_blob_key = blob_key
        image.image_thumb_blob_key = thumb_blob_key
        image.width = w   
        image.height = h            
        try:
            image.put()
            image_id = image.key().id()
            flash(u'Image %s successfully saved.' % image_id, 'success')
            return redirect(url_for('admin_images_in_category', parent_id=category_id))
        except CapabilityDisabledError:
            blobstore.delete([image.image_blob_key, image.image_thumb_blob_key ])
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('admin_images_in_category', parent_id=category_id))
        pass
    elif form.is_submitted():
        category_id = long(form.category_id.data)  
    images = ImageModel.all().filter('category_id', category_id)
    (categories, category_path, all_categories) = CategoryModel.get_categories_info(category_id)
    form.category_id.data = category_path[-1].key().id()
    return render_template('image/admin_images.html', images=images,
                           form=form,
                           categories=categories,
                           category_path=category_path,
                           current_category=category_path[-1],
                           all_categories=all_categories,
                           reset_image=ImageModel(category_id=category_id),
                           upload_url=blobstore.create_upload_url(url_for('admin_images')))


@admin_required
def delete_image(image_id):
    """Delete an image object"""
    image = ImageModel.get_by_id(image_id)
    parent_id = image.category_id
    try:
        # delete image from blobstore
        blobstore.delete([image.image_blob_key, image.image_thumb_blob_key ])
        # delete tha data entry
        image.delete()
        flash(u'Image %s successfully deleted.' % image_id, 'success')
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info')
    return redirect(url_for('admin_images_in_category', parent_id=parent_id))


def move_image(image_id, parent_id=ROOT_CAT_ID):
    cat = ImageModel.get_by_id(image_id)
    cat.category_id = parent_id
    cat.put()
    return redirect(url_for('admin_images_in_category', parent_id=parent_id), 302)
    pass


