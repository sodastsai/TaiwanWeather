# coding=utf8
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

##
# This class will return all forecast data from cwb.gov.tw
# Return:
#    - #TODO:
class AllForecastHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(self.request.path)

##
# This class will return particular city weather info
# Return:
#    - #TODO: 
class ForecastHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(self.request.path)

#        # Start to fetch cwb for city list
#        fetchResult = None
#        try:
#            fetchResult = urlfetch.fetch("http://www.cwb.gov.tw/V6/js/ForecastMenu.js")
#        except DownloadError:
#            self.response.out.write(MainHandler.errorMsg(101, "Fetching city list is timeout!"))
#        
#        # Check for result
#        if fetchResult is None or fetchResult.status_code!=200:
#            self.response.out.write(MainHandler.errorMsg(300, "Fetching city list is failed!"))
#            return
#            
#        # Make a soup and fetch necessary information
#        #soup = BeautifulSoup(fetchResult.content)
#        #self.response.out.write(soup.prettify())
#        self.response.out.write(fetchResult.content)

## WebApp object
application = webapp.WSGIApplication([('/json/forecast/', AllForecastHandler), ('/json/forecast/.*/', ForecastHandler)], debug=True)

## Main function for speedup with memcache
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()