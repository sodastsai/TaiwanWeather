# coding=utf8
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch, memcache
from google.appengine.api.urlfetch_errors import DownloadError
from django.utils import simplejson as json

from BeautifulSoup import BeautifulSoup

from Constants import urlByCityName, errorMsg, cityList

##
# This class will return all forecast data from cwb.gov.tw
# Return:
#    - #TODO:
class AllForecastHandler(webapp.RequestHandler):
    def get(self):
        resultDict = {}
        for item in cityList:
            tmpResult = forecastDataByCity(item[1], useJSON=False)
            resultDict[item[1]] = tmpResult
        self.response.out.write(json.dumps(resultDict))

##
# This class will return particular city weather info
# Return:
#  - JSON Array of JSON Objects which contains forecast in city.
#    The data contains next 3 periods of forecast
class ForecastHandler(webapp.RequestHandler):
    def get(self):
        # Get city name from REST path
        cityName = self.request.path[1:-1].split('/')[2]
        self.response.out.write(forecastDataByCity(cityName))

## Get city forecast data
def forecastDataByCity(cityName, useMemcache=True, useJSON=True):
    
    memcacheKey = cityName
    memcacheNamespace = "Forecast"
    # Get From memcache
    if useMemcache:
        result = memcache.get(memcacheKey, namespace=memcacheNamespace) #@UndefinedVariable
        if result is not None:
            if useJSON:
                return json.dumps(result)
            else:
                return result
    
    # Find city URL
    cityURL = urlByCityName(cityName)
    if cityURL is None:
        return errorMsg(201, "City is not found.")
    # Start to fetch cwb for city list
    fetchResult = None
    try:
        fetchResult = urlfetch.fetch(cityURL)
    except DownloadError:
        return errorMsg(101, "Fetching city list is timeout!")
    
    # Check for result
    if fetchResult is None or fetchResult.status_code!=200:
        return errorMsg(300, "Fetching city list is failed!")
        
    resultList = []
    # Make a soup and fetch necessary information
    soup = BeautifulSoup(fetchResult.content)
    soup.head.extract()
    contentTableRows = soup.body.table.table.contents[1].find("div", attrs={'class':'box'}).table.findAll("tr")[1:]
    soup.html.extract()
    # Save to dict/list
    for item in contentTableRows:
        tmpDict = {}
        rowCells = item.findAll("td")
        tmpDict["temperature"] = unicode(rowCells[0].contents[0])
        tmpDict["description"] = unicode(rowCells[2].contents[0])
        tmpDict["rainProbability"] = unicode(rowCells[3].contents[0])
        resultList += [tmpDict]
    # Memcache
    memcache.set(memcacheKey, resultList, 21600, namespace=memcacheNamespace) #@UndefinedVariable
    
    if useJSON:
        return json.dumps(resultList)
    else:
        return resultList

## WebApp object
application = webapp.WSGIApplication([('/json/forecast/', AllForecastHandler), ('/json/forecast/.*/', ForecastHandler)], debug=True)

## Main function for speedup with memcache
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()