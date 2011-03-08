from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from django.utils import simplejson as json

import os

from MemcacheHandler import MemcacheHandler
from parser import ForecastCityListHandler

## This webapp handler will process document for this webservice api
class DocumentHandler(webapp.RequestHandler):
    def get(self):
        # Convert Error Dict for Django display
        errorList = []
        for item in errorDict:
            errorList += [{"code":item , "msg":errorDict[item]}]
        # Make Django render html and output
        templateDict = { "errorDict": errorList, "cityList": ForecastCityListHandler.cityList }
        indexPath = os.path.join(os.path.dirname(__file__), "html/index.html")
        self.response.out.write(template.render(indexPath, templateDict))

## WebApp object
application = webapp.WSGIApplication([('/', DocumentHandler),
                                      
                                      ('/tool/memcache', MemcacheHandler)
                                      ],
                                     debug=True)

## Error code dictionary
# This dictionary records all error code in this web service api
errorDict = {
             100: "Google App Engine Error.",
             101: "Google App Engine Timeout.",
             
             200: "Service Not Found.",
             201: "REST path is error.",
             
             300: "Fetch result is empty."
             }

##
# Error message generator
#
# Argument
# - errorCode: the error code
# - reason: (optional) the reason of this error
#
# Return
# - A json string which represent a dict with error code and reason.
#
def errorMsg(errorCode, reason=""):
    result = {"error":int(errorCode), "reason": (errorDict[errorCode]+" "+reason).strip()}
    return json.dumps(result, sort_keys=True)

##
# Main function for speedup with memcache
#
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
