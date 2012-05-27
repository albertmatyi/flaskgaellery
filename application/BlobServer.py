'''
Created on May 27, 2012

@author: matyas
'''
from google.appengine.ext.webapp import blobstore_handlers
import urllib
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore_handlers.blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)
        pass
    
    
application = webapp.WSGIApplication(
[
 ('/blob/([^/]+)?', ServeHandler),
], debug=True)
run_wsgi_app(application)