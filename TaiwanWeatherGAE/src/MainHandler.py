# coding=utf8
#
#   Copyright 2011 NTU CSIE Mobile & HCI Research Lab
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# Django 1.2
from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import os

from MemcacheHandler import MemcacheHandler
from Constants import errorDict, cityList, errorMsg

## This webapp handler will process document for this webservice api
class DocumentHandler(webapp.RequestHandler):
    def get(self):
        # Convert Error Dict for Django display
        errorList = []
        for item in errorDict:
            errorList += [{"code":item , "msg":errorDict[item]}]
        # Make Django render html and output
        templateDict = { "errorDict": errorList, "cityList": cityList }
        indexPath = os.path.join(os.path.dirname(__file__), "html/index.html")
        self.response.out.write(template.render(indexPath, templateDict))

## This webapp handler will show example
class ExampleHandler(webapp.RequestHandler):
    def get(self):
        if self.request.get("category")=="":
            self.response.out.write(errorMsg(202, "category is required."))
            return
        templateDict = {"category": self.request.get("category")}
        htmlPath = os.path.join(os.path.dirname(__file__), "html/example.html")
        self.response.out.write(template.render(htmlPath, templateDict))

## WebApp object
application = webapp.WSGIApplication([('/', DocumentHandler),
                                      ('/example/', ExampleHandler),
                                      
                                      ('/tool/memcache/', MemcacheHandler)
                                      ],
                                     debug=True)

##
# Main function for speedup with memcache
#
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
