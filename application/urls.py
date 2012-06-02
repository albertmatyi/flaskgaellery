"""
urls.py

URL dispatch route mappings and error handlers

"""

from flask import render_template

from application import app
from application.controllers import example, category, image


## URL dispatch rules

# Home page
app.add_url_rule('/', 'home', view_func=category.home)
# Say hello
app.add_url_rule('/hello/<username>', 'say_hello', view_func=example.say_hello)

# Examples
app.add_url_rule('/examples', 'admin_examples', view_func=example.admin_examples, methods=['GET', 'POST'])
app.add_url_rule('/examples/delete/<int:example_id>', view_func=example.delete_example, methods=['POST'])
# Contrived admin-only view example
app.add_url_rule('/admin', 'admin', view_func=category.admin)
app.add_url_rule('/admin/categories/', 'admin_categories', view_func=category.admin_categories, methods=['GET', 'POST'])
app.add_url_rule('/admin/categories/-1', 'admin_categories', view_func=category.admin_categories, methods=['GET', 'POST'])
app.add_url_rule('/admin/categories/<int:parent_id>', 'admin_category', view_func=category.admin_categories, methods=['GET', 'POST'])
app.add_url_rule('/admin/category_delete/<int:category_id>', 'delete_category', view_func=category.delete_category, methods=['GET', 'POST'])
app.add_url_rule('/category/<int:parent_id>', 'category', view_func=category.category, methods=['GET'])

app.add_url_rule('/admin/images/', 'admin_images', view_func=image.admin_images, methods=['GET', 'POST'])
app.add_url_rule('/admin/images/<int:category_id>', 'admin_images_in_category', view_func=image.admin_images, methods=['GET', 'POST'])
app.add_url_rule('/images', 'images', view_func=image.admin_images, methods=['GET'])
app.add_url_rule('/admin/image_delete/<int:image_id>', 'delete_image', view_func=image.delete_image, methods=['GET', 'POST'])



## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

