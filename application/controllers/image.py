"""
This controller is responsible for handling Categories
"""


from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import render_template, flash, url_for, redirect

#from models import ImageModel
from  application.decorators import admin_required
from application.forms import ImageForm
from application.models import ImageModel, CategoryModel
from google.appengine.api import blobstore, images, files
from werkzeug.datastructures import FileStorage

@admin_required
def create_thumbnail(blob_key):
    ''' Creates a thumbnail for the image stored at blob_key 
    @param blob_key: the key for the blobstore where the image is stored
    @return: A touple containing: 
            the blob_key of the thumbnail
            the width of the thumbnail
            the height of the thumbnail
    '''
    img = images.Image(blob_key=blob_key, )
    img.resize(width=80, height=100)
    thumbnail = img.execute_transforms(output_encoding=images.PNG)
    # Create the file
    file_name = files.blobstore.create(mime_type='image/png')
    # Open the file and write to it
    with files.open(file_name, 'a') as f:
        f.write(thumbnail)
    # Finalize the file. Do this before attempting to read it.
    files.finalize(file_name)
    return (str(files.blobstore.get_blob_key(file_name)), img.width(), img.height())
    pass

@admin_required
def admin_images():
    """List all images"""
    images = ImageModel.all()
    form = ImageForm()
    kvps = ((c.key().id(), c.title) for c in CategoryModel.all())
    form.category_id.choices = kvps;
    if form.validate_on_submit():
        blob_key = ''
        thumb_blob_key = ''
        if type(form.image.data) == FileStorage:
            blob_key = form.image.data.mimetype_params['blob-key']
            thumb_blob_key = create_thumbnail(blob_key)
        image = ImageModel(
            title = form.title.data,
            description = form.description.data,
            category_id = form.category_id.data,
            image_blob_key = blob_key,
            image_thumb_blob_key = thumb_blob_key
        )
        try:
            image.put()
            image_id = image.key().id()
            flash(u'Image %s successfully saved.' % image_id, 'success')
            return redirect(url_for('admin_images'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('admin_images'))
        pass
    return render_template('image/admin_list.html', images=images, form=form, upload_url=blobstore.create_upload_url(url_for('admin_images')))


@admin_required
def delete_image(image_id):
    """Delete an image object"""
    image = ImageModel.get_by_id(image_id)
    try:
        # delete image from blobstore
        blobstore.delete([image.image_blob_key, image.image_thumb_blob_key ])
        # delete tha data entry
        image.delete()
        flash(u'Image %s successfully deleted.' % image_id, 'success')
        return redirect(url_for('admin_images'))
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info')
        return redirect(url_for('admin_images'))
