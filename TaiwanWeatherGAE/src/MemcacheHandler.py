# coding=utf8
from google.appengine.ext import webapp
from google.appengine.api import memcache
from Constants import errorMsg

## web app for memcache 
class MemcacheHandler(webapp.RequestHandler):
    def get(self):
        # Flush all memcache keys
        if self.request.get("flush")=="true":
            if memcache.flush_all(): #@UndefinedVariable
                self.response.out.write("{\"result\": 0, \"message\": \"All memcache has been flushed.\"}")
            else:
                self.response.out.write(errorMsg(100, "Memcache opration failed"))