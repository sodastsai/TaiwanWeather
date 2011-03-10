# coding=utf8
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
from google.appengine.api.urlfetch_errors import DownloadError
from django.utils import simplejson as json

from BeautifulSoup import BeautifulSoup

from Constants import urlByCityName, errorMsg

##
# This class will return all forecast data from cwb.gov.tw
# Return:
#    - #TODO:
class AllForecastHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(self.request.path.split('/'))

##
# This class will return particular city weather info
# Return:
#  - JSON Array of JSON Objects which contains forecast in city.
#    The data contains next 3 periods of forecast
class ForecastHandler(webapp.RequestHandler):
    def get(self):
        # Get city name from REST path
        cityName = self.request.path[1:-1].split('/')[2]
        # Find city URL
        cityURL = urlByCityName(cityName)
        if cityURL is None:
            self.response.out.write(errorMsg(201, "City is not found."))
        # Start to fetch cwb for city list
        fetchResult = None
        try:
            fetchResult = urlfetch.fetch(cityURL)
        except DownloadError:
            self.response.out.write(errorMsg(101, "Fetching city list is timeout!"))
        
        # Check for result
        if fetchResult is None or fetchResult.status_code!=200:
            self.response.out.write(errorMsg(300, "Fetching city list is failed!"))
            return
            
        resultList = []
        # Make a soup and fetch necessary information
        soup = BeautifulSoup(fetchResult.content)
        soup.head.extract()
        contentTableRows = soup.body.table.table.contents[1].find("div", attrs={'class':'box'}).table.findAll("tr")[1:]
        soup.html.extract()
        for item in contentTableRows:
            tmpDict = {}
            rowCells = item.findAll("td")
            tmpDict["temperature"] = unicode(rowCells[0].contents[0])
            tmpDict["description"] = unicode(rowCells[2].contents[0])
            tmpDict["rainProbability"] = unicode(rowCells[3].contents[0])
            resultList += [tmpDict]
        self.response.out.write(json.dumps(resultList))

## WebApp object
application = webapp.WSGIApplication([('/json/forecast/', AllForecastHandler), ('/json/forecast/.*/', ForecastHandler)], debug=True)

## Main function for speedup with memcache
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()