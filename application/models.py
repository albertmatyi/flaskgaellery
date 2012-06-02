"""
models.py

App Engine datastore models

"""


from google.appengine.ext import db
import datetime

def v2m(form, mdl_obj):
    ''' 
        Copies all data from a form object to the model object
    '''
    for prop, val in vars(form).iteritems():
        if not prop.startswith('__'):
            if prop in dir(mdl_obj):
                setattr(mdl_obj,prop,val.data)
    pass

class AbstractModel(db.Model):
    def jsond(self):
        ''' will return a json representation of the object'''
        vals = {'id': self.key().id()}
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

'''
    The virtual id of the root category
'''
ROOT_CAT_ID = -1
'''
    A dummy category object containing the ROOT_CAT_ID (@key().id()) and a title <Root>
'''
ROOT_CAT_DUMMY = {'key': lambda : {'id': lambda : ROOT_CAT_ID}, 'title': 'Root'}

class CategoryModel(AbstractModel):
    """Category Model"""
    title = db.StringProperty(required=True, default='Some title')
    parent_id = db.IntegerProperty(required=False)
    order = db.IntegerProperty(required=True, default=0)
    visible = db.BooleanProperty(required=True, default=False)
    non_menu_category = db.BooleanProperty(required=True, default=False)
    autoscroll = db.BooleanProperty(required=True, default=True)
    created = db.DateTimeProperty(auto_now_add=True)
    
    subcategories = None
    
    @staticmethod
    def get_root_categories(visibleOnly = True):
        ''' @return: The query for the root 
        '''
        qry = CategoryModel.all().filter('parent_id', ROOT_CAT_ID)
        if visibleOnly:
            qry.filter('visible', True)
        return qry 
        pass
    
    def get_subcategories(self, visible_only=True):
        '''
            @return: All subcategories of the current CategoryModel 
        '''
        cats = [cat for cat in CategoryModel.all().filter('parent_id', self.key().id())]
        return cats
        pass
    
    def get_path_ids_to_root(self):
        '''
            @see: get_path_to_root
        '''
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
    title = db.StringProperty(required=True, default='Title')
    description = db.TextProperty(required=False)
    category_id = db.IntegerProperty(required=False)
    height = db.IntegerProperty(required=False)
    width = db.IntegerProperty(required=False)
    image_blob_key = db.StringProperty()
    image_thumb_blob_key = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    order = db.IntegerProperty(required=True, default=0)
    
def initDB():
    CategoryModel(title='Home', parent_id=-1).put()
    key = CategoryModel(title='Portraits', parent_id=-1).put()
    CategoryModel(title='Men', parent_id=key.id()).put()
    CategoryModel(title='Women', parent_id=key.id()).put()
    key = CategoryModel(title='Cities', parent_id=-1).put()
    CategoryModel(title='London', parent_id=key.id()).put()
    CategoryModel(title='Antwerp', parent_id=key.id()).put()
    key = CategoryModel(title='Cities', parent_id=-1).put()
    CategoryModel(title='London', parent_id=key.id()).put()
    CategoryModel(title='Antwerp', parent_id=key.id()).put()
    CategoryModel(title='About', parent_id=-1).put()
    CategoryModel(title='Contact', parent_id=-1).put()
    pass
    