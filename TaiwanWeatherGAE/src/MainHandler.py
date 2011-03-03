from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import os

## This webapp handler will process document for this webservice api
class DocumentHandler(webapp.RequestHandler):
    def get(self):
        # Convert Error Dict for Django display
        errorList = []
        for item in errorDict:
            errorList += [{"code":item , "msg":errorDict[item]}]
        # Make Django render html and output
        templateDict = { "errorDict": errorList }
        indexPath = os.path.join(os.path.dirname(__file__), "html/index.html")
        self.response.out.write(template.render(indexPath, templateDict))

## WebApp object
application = webapp.WSGIApplication([('/', DocumentHandler)
                                      ],
                                     debug=True)

## Error code dictionary
# This dictionary records all error code in this web service api
errorDict = {100: "XD"
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
    pass

##
# Main function for speedup with memcache
#
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
