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
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch, memcache
from google.appengine.api.urlfetch_errors import DownloadError
from django.utils import simplejson as json

from BeautifulSoup import BeautifulSoup

from Constants import urlByCityName, errorMsg, cityList

## Memcache namespace
memcacheNamespace = "Forecast"

##
# This class will return all forecast data from cwb.gov.tw
# Return:
#    - JSON object with each cities forecast
class AllForecastHandler(webapp.RequestHandler):
    def get(self):
        # Header
        self.response.headers["Content-Type"] = "text/javascript"
        callback = None
        if self.request.get("callback")!="":
            callback = self.request.get("callback")
        
        useMemcache = True
        if self.request.get("memcache")=="false":
            useMemcache = False
        
        memcacheKey = "AllCity"
        result = None
        if useMemcache:
            result = memcache.get(memcacheKey, namespace=memcacheNamespace) #@UndefinedVariable
            
        if result is None:
            result = {}
            for item in cityList:
                tmpResult = forecastDataByCity(item[1], useJSON=False, useMemcache=useMemcache)
                result[item[1]] = tmpResult        
            # Memcache
            memcache.set(memcacheKey, result, 22200, namespace=memcacheNamespace) #@UndefinedVariable
            
        if callback is not None:
            resultString = callback+"("+json.dumps(result)+");"
        else:
            resultString = json.dumps(result)
        self.response.out.write(resultString)

##
# This class will return particular city weather info
# Return:
#  - JSON Array of JSON Objects which contains forecast in city.
#    The data contains next 3 periods of forecast
class ForecastHandler(webapp.RequestHandler):
    def get(self):
        # Header
        self.response.headers["Content-Type"] = "text/javascript"
        callback = None
        if self.request.get("callback")!="":
            callback = self.request.get("callback")
        # Get city name from REST path
        cityName = self.request.path[1:-1].split('/')[2]
        # Output
        jsonObject = forecastDataByCity(cityName, recentOnly=False)
        if callback is not None:
            result = callback + "(" + jsonObject + ");"
        else:
            result = jsonObject
        self.response.out.write(result)

## Get city forecast data
# Arguments:
#  - cityName: English name of city
#  - recentOnly: (optional) Return recent data only
#  - useMemcache: (optional) Return data with memcache
#  - useJSON: (optional) Return JSON data
def forecastDataByCity(cityName, recentOnly=True, useMemcache=True, useJSON=True):
    
    # Memcache key
    memcacheKey = cityName
    if recentOnly:
        memcacheKey += "_recent"
    
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
        
    resultDict = {}
    # Make a soup and fetch necessary information
    soup = BeautifulSoup(fetchResult.content)
    soup.head.extract()
    contentTables = soup.body.table.table.contents[1].findAll("div", attrs={'class':'box'})
    recentTableRows = contentTables[0].table.findAll("tr")[1:]
    if not recentOnly:
        weekTableRow = contentTables[1].table.findAll("tr")[1]
        touristTableRows = contentTables[2]
    soup.html.extract()
    # Recent part
    recentList = []
    for item in recentTableRows:
        rowCells = item.findAll("td")
        tmpDict = {"temperature": unicode(rowCells[0].contents[0]),
                   "description": unicode(rowCells[1].img["alt"]),
                   "image": unicode("http://www.cwb.gov.tw"+rowCells[1].img["src"]),
                   "feel": unicode(rowCells[2].contents[0]),
                   "rainProbability": unicode(rowCells[3].contents[0])}
        recentList += [tmpDict]
    resultDict["recent"] = recentList
    # Week part
    if not recentOnly:
        weekList = []
        for item in weekTableRow.findAll("td"):
            tmpDict = {"description": unicode(item.contents[1]["alt"]),
                       "image": unicode("http://www.cwb.gov.tw"+item.contents[1]["src"]),
                       "temperature": unicode(item.contents[3].strip())}
            weekList += [tmpDict]
        resultDict["week"] = weekList
    # Tourist part
    if not recentOnly:
        tourists = touristTableRows.table.findAll("tr")[1:]
        touristsList = []
        for item in tourists:
            tmpDict = {"name": unicode(item.find("th"))}
            tmpList = []
            for cell in item.findAll("td"):
                subDict = {"description": unicode(cell.contents[1]["alt"]),
                           "image": unicode("http://www.cwb.gov.tw"+cell.contents[1]["src"]),
                           "temperature": unicode(cell.contents[3].strip())}
                tmpList += [subDict]
            tmpDict["forecast"] = tmpList
            touristsList += [tmpDict]
        resultDict["tourist"] = touristsList
    # Memcache
    memcache.set(memcacheKey, resultDict, 22200, namespace=memcacheNamespace) #@UndefinedVariable
    
    if useJSON:
        return json.dumps(resultDict)
    else:
        return resultDict

## WebApp object
application = webapp.WSGIApplication([('/json/forecast/', AllForecastHandler), ('/json/forecast/.*/', ForecastHandler)], debug=True)

## Main function for speedup with memcache
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()