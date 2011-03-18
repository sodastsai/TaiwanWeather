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

from Constants import errorMsg, cityList

## Memcache namespace
memcacheNamespace = "current"

##
# This class will return all current forecast info
class AllCurrentHandler(webapp.RequestHandler):
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
                result[item[1]] = currentDataOfCity(item[1], useJSON=False, useMemcache=useMemcache)
            memcache.set(memcacheKey, result, 4200, namespace=memcacheNamespace) #@UndefinedVariable
            
        if callback is not None:
            resultString = callback+"("+json.dumps(result)+");"
        else:
            resultString = json.dumps(result)
        self.response.out.write(resultString)

##
# This class will return city current forecast info
class CurrentHandler(webapp.RequestHandler):
    def get(self):
        # Header
        self.response.headers["Content-Type"] = "text/javascript"
        callback = None
        if self.request.get("callback")!="":
            callback = self.request.get("callback")
        # Data
        cityName = self.request.path[1:-1].split('/')[2]
        # Output
        jsonObject = currentDataOfCity(cityName)
        if callback is not None:
            result = callback+"("+jsonObject+");"
        else:
            result = jsonObject
        self.response.out.write(result)
            
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
    resultDict = {
               "city": chtCityName,
               "description": unicode(currentInfos[tablePosition].findAll("tr")[2].td.img["alt"].strip()),
               "image": unicode("http://www.cwb.gov.tw"+currentInfos[tablePosition].findAll("tr")[2].td.img["src"].strip()),
               "temperature": unicode(currentInfos[tablePosition].findAll("tr")[3].td.contents[0][:-6].strip()),
               }
    
    # Return
    memcache.set(memcacheKey, resultDict, 4200, namespace=memcacheNamespace) #@UndefinedVariable
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