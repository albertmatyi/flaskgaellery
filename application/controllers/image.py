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
from random import Random


'''
    Maximum dimensions of the image
'''
MAX_WIDTH = 720
MAX_HEIGHT = 515

@admin_required
def create_thumbnail(blob_key, width=MAX_WIDTH, height=MAX_HEIGHT):
    ''' Creates a thumbnail for the image stored at blob_key 
    @param blob_key: the key for the blobstore where the image is stored
    @return: A touple containing: 
            the blob_key of the thumbnail
            the width of the thumbnail
            the height of the thumbnail
    '''
    img = images.Image(blob_key=blob_key,)
    img.resize(width=width, height=height)
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
        if type(form.image.data) == FileStorage and (is_new or form.update_image.data):
            blob_key = form.image.data.mimetype_params['blob-key']
            #create a small
            (image.image_thumb_blob_key, image.width, image.height) = create_thumbnail(blob_key, 50, 50)
            #and a slightly larger version 
            (image.image_blob_key, image.width, image.height) = create_thumbnail(blob_key)
            #delete the uploaded (possibly 'uge file)
            blobstore.delete(blob_key)
        elif not is_new and form.update_image.data: # we set to update with an empty image so we delete the one in the db
            image.delete_images()
            image.image_blob_key = ''
            image.image_thumb_blob_key = ''
            image.width = 0
            image.height = 0
        try:
            image.put()
            image_id = image.key().id()
            flash(u'Image %s successfully saved.' % image_id, 'success')
            return redirect(url_for('admin_images_in_category', parent_id=category_id))
        except CapabilityDisabledError:
            image.delete_images()
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('admin_images_in_category', parent_id=category_id))
        pass
    elif form.is_submitted():
        category_id = long(form.category_id.data)  
    images = sorted(ImageModel.all().filter('category_id', category_id), key=lambda i: i.order)
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
        image.delete_images()
        # delete tha data entry
        image.delete()
        flash(u'Image %s successfully deleted.' % image_id, 'success')
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info')
    return redirect(url_for('admin_images_in_category', parent_id=parent_id))

@admin_required
def move_image(image_id, parent_id=ROOT_CAT_ID):
    cat = ImageModel.get_by_id(image_id)
    cat.category_id = parent_id
    cat.put()
    return redirect(url_for('admin_images_in_category', parent_id=parent_id), 302)
    pass

def get_images_for_category(category_id):
    ''' 
        Retrieves images for a given category
    '''
    # FIXME lorempixum
    n = Random().randint(8, 20);
    contents = []
    for i in range(0, n):
        c = ImageModel()
        c.title = get_random_text(Random().randint(5, 25)).replace('\n', '').replace('\r', '')
        c.description = get_random_text(Random().randint(45, 325))
        c.height = MAX_HEIGHT
        c.width = Random().randint(300, MAX_WIDTH)
        c.image_blob_key = 'pixum'
        c = c.jsond()
        c['id'] = i
        contents += [c]
        pass
#    contents = [c.jsond() for c in ImageModel.all().filter('category_id', category_id).filter('visible', True)]
    return contents 
    pass

def get_random_text(length):
    if length > len(fixieText):
        return fixieText
    start = Random().randint(0, len(fixieText) - length)
    return fixieText[start : start + length].capitalize()
    pass

fixieText = '''Rado 1982 is classy gluten-free ethical esse authentic nulla. Bennie dumpster art reprehenderit DSLR whatever esse. Kale fresh trust-fund vegan beer wes reprehenderit delectus. Kale mollit magna polaroid.

    Instagram anime party ethical
    Bushwick salvia fresh 1982 moon
    Beer yr etsy vegan
    Voluptate wayfarers 8-bit
    Sriracha delectus magna party
    Frado gastropub fin daisy is
    DSLR non beer

Latte wayfarers kale beer viral selvage. Twee 8-bit pony is liberal original capitalism. Anim liberal reprehenderit classy sunt. Sint viral bennie Anderson bushwick frado.
Is Instagram anime

Brony street-art esse seitan etsy. Delectus salvia delectus bronson placeat liberal narwhal. Mollit vinyl incididunt dreamcatcher DSLR authentic 8-bit. Frado daisy pour-over vinyl clothesline ethical.

Hog vegan gluten-free authentic DSLR. Pinterest 8-bit placeat seitan latte fin kale kale. Frado chillwave gastropub authentic non dumpster authentic bushwick. Art narwhal whatever iphone placeat esse letterpress ut liberal. Art mollit sint non fixie authentic classy salvia.

Bronson I delectus tassel. Of voluptate vegan mollit. Of fin letterpress art ut Anderson of tassel non-ethical. Party viral fixie chowder fresh.

Non-ethical shot anime sriracha trust-fund iphone brooklyn original fresh. 8-bit magna art etsy gluten-free incididunt party. Helvetica salvia party art vintage fin. Brony gluten-free authentic hog street-art twee viral. Narwhal gluten-free shot art bennie yr hog placeat.
'''
