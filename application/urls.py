"""
urls.py

URL dispatch route mappings and error handlers

"""

from flask import render_template

from application import app
from application.controllers import category, image
from application.models import ROOT_CAT_ID


## URL dispatch rules

# Home page
app.add_url_rule('/', 'home', view_func=category.home)

app.add_url_rule('/admin/', 'admin', view_func=category.admin)
app.add_url_rule('/admin/categories/', 'admin_categories', view_func=category.admin_categories, methods=['GET', 'POST'])
app.add_url_rule('/admin/categories/' + str(ROOT_CAT_ID) + '', 'admin_categories', view_func=category.admin_categories, methods=['GET', 'POST'])
app.add_url_rule('/admin/categories/<int:parent_id>', 'admin_category', view_func=category.admin_categories, methods=['GET', 'POST'])
app.add_url_rule('/admin/categories/move/<int:category_id>/<int:parent_id>', 'move_category', view_func=category.move_category, methods=['GET'])
app.add_url_rule('/admin/categories/move/<int:category_id>/' + str(ROOT_CAT_ID), 'move_category', view_func=category.move_category, methods=['GET'])
app.add_url_rule('/admin/category_delete/<int:category_id>', 'delete_category', view_func=category.delete_category, methods=['GET', 'POST'])
app.add_url_rule('/category/<int:parent_id>', 'category', view_func=category.category, methods=['GET'])

app.add_url_rule('/admin/images/', 'admin_images', view_func=image.admin_images, methods=['GET', 'POST'])
app.add_url_rule('/admin/images/' + str(ROOT_CAT_ID) + '', 'admin_images', view_func=image.admin_images, methods=['GET', 'POST'])
app.add_url_rule('/admin/images/<int:parent_id>', 'admin_images_in_category', view_func=image.admin_images, methods=['GET', 'POST'])
app.add_url_rule('/images', 'images', view_func=image.admin_images, methods=['GET'])
app.add_url_rule('/admin/image_delete/<int:image_id>', 'delete_image', view_func=image.delete_image, methods=['GET', 'POST'])
app.add_url_rule('/admin/images/move/<int:image_id>/' + str(ROOT_CAT_ID), 'move_image', view_func=image.move_image, methods=['GET'])
app.add_url_rule('/admin/images/move/<int:image_id>/<int:parent_id>', 'move_image', view_func=image.move_image, methods=['GET'])

## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

