# coding=utf8
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp
from django.utils import simplejson as json

from Constants import urlByCityName, errorMsg, cityList

##
# This class will return city forecast available from cwb.gov.tw
# Return:
#    - json array with city name and url
class CityListHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(json.dumps(cityList, sort_keys=True))
        
##
# This class will return city forecast available from cwb.gov.tw
# Return:
#    - json object of url
class PageURLHandler(webapp.RequestHandler):
    def get(self):
        cityName = self.request.path[27:-1]
        # Empty City Name
        if cityName=="":
            self.response.out.write(errorMsg(201, "City abbr is required."))
            return
        
        # Find city link
        cityLink = urlByCityName(cityName)
        # Could not find city ...
        if cityLink is None:
            self.response.out.write(errorMsg(201, "City abbr is not found."))
            return
        
        # Return a city
        result = { "url": cityLink }
        self.response.out.write(json.dumps(result))

## WebApp object
application = webapp.WSGIApplication([('/json/forecastCity/', CityListHandler),
                                      ('/json/forecastCity/pageURL/.*/', PageURLHandler)],
                                     debug=True)

##
# Main function for speedup with memcache
#
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()