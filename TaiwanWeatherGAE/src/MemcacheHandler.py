from google.appengine.ext import webapp
from google.appengine.api import memcache
import MainHandler

## web app for memcache 
class MemcacheHandler(webapp.RequestHandler):
    def get(self):
        # Flush all memcache keys
        if self.request.get("flush")=="true":
            if memcache.flush_all(): #@UndefinedVariable
                self.response.out.write("{\"result\": 0, \"message\": \"All memcache has been flushed.\"}")
            else:
                self.response.out.write(MainHandler.errorMsg(100, "Memcache opration failed"))