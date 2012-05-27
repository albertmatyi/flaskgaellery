"""
models.py

App Engine datastore models

"""


from google.appengine.ext import db
import datetime
from random import random

class AbstractModel(db.Model):
    def jsond(self):
        ''' will return a json representation of the objec'''
        vals = {}
        for prop in self.properties():
            val = self.__getattribute__(prop)
            if type(val) is datetime.datetime:
                val = val.strftime('%b %d, %Y %I:%M %p')
                pass
            vals[prop] = val
        return vals

class ExampleModel(AbstractModel):
    """Example Model"""
    example_name = db.StringProperty(required=True)
    example_description = db.TextProperty(required=True)
    added_by = db.UserProperty()
    timestamp = db.DateTimeProperty(auto_now_add=True)

class CategoryModel(AbstractModel):
    """Category Model"""
    title = db.StringProperty(required=True)
    description = db.TextProperty(required=False)
    parent_id = db.IntegerProperty(required=False)
    index = db.IntegerProperty(required=False)
    created = db.DateTimeProperty(auto_now_add=True)
    
    subcategories = None
    
    def get_subcategories(self):
        '''
            @return: All subcategories of the current CategoryModel 
        '''
        cats = [cat for cat in CategoryModel.all().filter('parent_id', self.key().id())]
        return cats
        pass
    
    def get_path_ids_to_root(self):
        ids = [el.key().id() for el in self.get_path_to_root()]
        return ids
        pass
    
    def get_path_to_root(self):
        '''
            @return: All of the CategoryModel objects starting with its parent until the root. (it does not contain self)  
        '''
        if self.parent_id == -1:
            return []
        else:
            parent = CategoryModel.get_by_id(self.parent_id)
            return [parent] + parent.get_path_to_root() 
        pass

class ImageModel(AbstractModel):
    """Image Model"""
    title = db.StringProperty(required=True)
    description = db.TextProperty(required=False)
    category_id = db.IntegerProperty(required=False)
    height = db.IntegerProperty(required=False)
    width = db.IntegerProperty(required=False)
    image_blob_key = db.StringProperty()
    image_thumb_blob_key = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    index = db.IntegerProperty(required=False)