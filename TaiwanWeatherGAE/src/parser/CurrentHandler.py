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

from Constants import errorMsg, cityList

## Memcache namespace
memcacheNamespace = "current"

##
# This class will return all current forecast info
class AllCurrentHandler(webapp.RequestHandler):
    def get(self):
        useMemcache = True
        if self.request.get("memcache")=="false":
            useMemcache = False
        
        memcacheKey = "AllCity"
        if useMemcache:
            result = memcache.get(memcacheKey, namespace=memcacheNamespace) #@UndefinedVariable
            if result is not None:
                self.response.out.write(json.dumps(result))
            
        resultDict = {}
        for item in cityList:
            resultDict[item[0]] = currentDataOfCity(item[1], useJSON=False, useMemcache=useMemcache)
        memcache.set(memcacheKey, resultDict, 3600, namespace=memcacheNamespace) #@UndefinedVariable
        self.response.out.write(json.dumps(resultDict))

##
# This class will return city current forecast info
class CurrentHandler(webapp.RequestHandler):
    def get(self):
        cityName = self.request.path[1:-1].split('/')[2]
        self.response.out.write(currentDataOfCity(cityName))
            
## Get current data of city
def currentDataOfCity(cityName, useJSON=True, useMemcache=True):
    
    memcacheKey = cityName
    if useMemcache:
        result = memcache.get(memcacheKey, namespace=memcacheNamespace) #@UndefinedVariable
        if result is not None:
            if useJSON:
                return json.dumps(result)
            else:
                return result
    
    # Check valid cityName
    cityNameCheckFlag = False
    chtCityName = ""
    for item in cityList:
        if cityName==item[1]:
            chtCityName = item[0]
            cityNameCheckFlag = True
    if not cityNameCheckFlag:
        return errorMsg(201, "City is not found.")
    
    pageURL = dataDict[cityName][0]
    tablePosition = dataDict[cityName][1]
    
    # Start to fetch cwb for city list
    fetchResult = None
    try:
        fetchResult = urlfetch.fetch(pageURL)
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
    #cityName = unicode(currentInfos[tablePosition].findAll("tr")[0].th.contents[0].strip())
    resultDict = {
               "city": chtCityName,
               "description": unicode(currentInfos[tablePosition].findAll("tr")[2].td.img["alt"].strip()),
               "image": unicode("http://www.cwb.gov.tw"+currentInfos[tablePosition].findAll("tr")[2].td.img["src"].strip()),
               "temperature": unicode(currentInfos[tablePosition].findAll("tr")[3].td.contents[0].strip()),
               }
    
    # Return
    memcache.set(memcacheKey, resultDict, 3600, namespace=memcacheNamespace) #@UndefinedVariable
    if useJSON:
        return json.dumps(resultDict)
    else:
        return resultDict
    
        
## Data list for current
dataDict = {
    cityList[0][1]: ("http://www.cwb.gov.tw/V6/observe/real/current_n.htm", 0), # 台北市
    cityList[5][1]: ("http://www.cwb.gov.tw/V6/observe/real/current_n.htm", 2), # 基隆北海岸
    cityList[7][1]: ("http://www.cwb.gov.tw/V6/observe/real/current_n.htm", 4), # 新竹
    cityList[6][1]: ("http://www.cwb.gov.tw/V6/observe/real/current_n.htm", 5), # 桃園
    cityList[8][1]: ("http://www.cwb.gov.tw/V6/observe/real/current_n.htm", 8), # 苗栗
    cityList[1][1]: ("http://www.cwb.gov.tw/V6/observe/real/current_n.htm", 10),# 新北市
    cityList[2][1]: ("http://www.cwb.gov.tw/V6/observe/real/current_c.htm", 0), # 台中市
    cityList[10][1]:("http://www.cwb.gov.tw/V6/observe/real/current_c.htm", 2), # 南投
    cityList[12][1]:("http://www.cwb.gov.tw/V6/observe/real/current_c.htm", 3), # 嘉義
    cityList[9][1]: ("http://www.cwb.gov.tw/V6/observe/real/current_c.htm", 6), # 彰化
    cityList[11][1]:("http://www.cwb.gov.tw/V6/observe/real/current_c.htm", 8), # 雲林
    cityList[3][1]: ("http://www.cwb.gov.tw/V6/observe/real/current_s.htm", 0), # 台南市
    cityList[4][1]: ("http://www.cwb.gov.tw/V6/observe/real/current_s.htm", 1), # 高雄市
    cityList[14][1]:("http://www.cwb.gov.tw/V6/observe/real/current_s.htm", 2), # 恆春半島
    cityList[13][1]:("http://www.cwb.gov.tw/V6/observe/real/current_s.htm", 5), # 屏東
    cityList[15][1]:("http://www.cwb.gov.tw/V6/observe/real/current_e.htm", 1), # 宜蘭
    cityList[16][1]:("http://www.cwb.gov.tw/V6/observe/real/current_e.htm", 2), # 花蓮
    cityList[17][1]:("http://www.cwb.gov.tw/V6/observe/real/current_e.htm", 4), # 台東
    cityList[18][1]:("http://www.cwb.gov.tw/V6/observe/real/current_i.htm", 0), # 澎湖
    cityList[19][1]:("http://www.cwb.gov.tw/V6/observe/real/current_i.htm", 2), # 金門
    cityList[20][1]:("http://www.cwb.gov.tw/V6/observe/real/current_i.htm", 3), # 馬祖
}

## WebApp object
application = webapp.WSGIApplication([('/json/current/', AllCurrentHandler), ("/json/current/.*/", CurrentHandler)], debug=True)

## Main function for speedup with memcache
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()