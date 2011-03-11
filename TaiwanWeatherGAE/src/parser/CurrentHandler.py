# coding=utf8
# Django 1.2
from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch, memcache
from google.appengine.api.urlfetch_errors import DownloadError
from django.utils import simplejson as json

from BeautifulSoup import BeautifulSoup

from Constants import errorMsg

## Memcache namespace
memcacheNamespace = "current"

##
# This class will return current forecast info
class CurrentHandler(webapp.RequestHandler):
    def get(self):
        useMemcache = True
        if self.request.get("memcache")=="false":
            useMemcache = False
        memcacheKey = "AllCurrent"
        
        if useMemcache:
            result = memcache.get(memcacheKey, namespace=memcacheNamespace) #@UndefinedVariable
            if result is not None:
                self.response.out.write(json.dumps(result))
                return
        
        # Page List
        pageList = ["http://www.cwb.gov.tw/V6/observe/real/current_c.htm",
                    "http://www.cwb.gov.tw/V6/observe/real/current_n.htm",
                    "http://www.cwb.gov.tw/V6/observe/real/current_s.htm",
                    "http://www.cwb.gov.tw/V6/observe/real/current_e.htm",
                    "http://www.cwb.gov.tw/V6/observe/real/current_i.htm"]
        
        # Go
        resultDict = {}
        for url in pageList:
            # Start to fetch cwb for city list
            fetchResult = None
            try:
                fetchResult = urlfetch.fetch(url)
            except DownloadError:
                return errorMsg(101, "Fetching city list is timeout!")
            
            # Check for result
            if fetchResult is None or fetchResult.status_code!=200:
                return errorMsg(300, "Fetching current data is failed!")
            
            # Make a soup and fetch necessary information
            soup = BeautifulSoup(fetchResult.content)
            soup.head.extract()
            currentInfos = soup.html.find("div", attrs={'class':'Current_info'}).findAll("table", attrs={"class":"datatable"})
            soup.extract()
            
            # Process information
            for item in currentInfos:
                cityName = unicode(item.findAll("tr")[0].th.contents[0].strip())
                tmpDict = {
                           "city": cityName,
                           "description": unicode(item.findAll("tr")[2].td.img["alt"].strip()),
                           "temperature": unicode(item.findAll("tr")[3].td.contents[0].strip()),
                           }
                resultDict[cityName] = tmpDict
        # Memcache
        memcache.set(memcacheKey, resultDict, 21600, namespace=memcacheNamespace) #@UndefinedVariable
        self.response.out.write(json.dumps(resultDict))
            

## WebApp object
application = webapp.WSGIApplication([('/json/current/', CurrentHandler)], debug=True)

## Main function for speedup with memcache
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()