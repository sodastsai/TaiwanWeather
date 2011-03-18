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
from django.utils import simplejson as json

## Error code dictionary
# This dictionary records all error code in this web service api
errorDict = {
             100: "Google App Engine Error.",
             101: "Google App Engine Timeout.",
             
             200: "Service Not Found.",
             201: "REST path is error.",
             202: "GET argument is error.",
             
             300: "Fetch result is empty.",
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

# Base URL
baseURL = "http://www.cwb.gov.tw/V6/forecast/taiwan/"
## City List provided by cwb.gov.tw
# Current version is from http://www.cwb.gov.tw/V6/js/ForecastMenu.js
cityList = [
    (u"台北市", "Taipei", baseURL+"36_01_data.htm"),
    (u"新北市", "NewTaipei", baseURL+"36_04_data.htm"),
    (u"台中市", "Taichung", baseURL+"36_08_data.htm"),
    (u"台南市", "Tainan", baseURL+"36_13_data.htm"),
    (u"高雄市", "Kaohsiung", baseURL+"36_02_data.htm"),
    (u"基隆北海岸", "Keelung", baseURL+"36_03_data.htm"),
    (u"桃園", "Taoyuan", baseURL+"36_05_data.htm"),
    (u"新竹", "Hsinchu", baseURL+"36_06_data.htm"),
    (u"苗栗", "Miaoli", baseURL+"36_07_data.htm"),
    (u"彰化", "Changhua", baseURL+"36_09_data.htm"),
    (u"南投", "Nantou", baseURL+"36_10_data.htm"),
    (u"雲林", "Yunlin", baseURL+"36_11_data.htm"),
    (u"嘉義", "Chiayi", baseURL+"36_12_data.htm"),
    (u"屏東", "Pingtung", baseURL+"36_15_data.htm"),
    (u"恆春半島", "Hengchun", baseURL+"36_16_data.htm"),
    (u"宜蘭", "Yilan", baseURL+"36_17_data.htm"),
    (u"花蓮", "Hualien", baseURL+"36_18_data.htm"),
    (u"台東", "Taitung", baseURL+"36_19_data.htm"),
    (u"澎湖", "Penghu", baseURL+"36_20_data.htm"),
    (u"金門", "Kinmen", baseURL+"36_21_data.htm"),
    (u"馬祖", "Matsu", baseURL+"36_22_data.htm")
]

## Query for url by city name
def urlByCityName(cityName):
    cityLink = None
    for cityPair in cityList:
        if cityName == cityPair[1]:
            cityLink = cityPair[2]
            break
    return cityLink

##
# This class will return city forecast available from cwb.gov.tw
# Return:
#    - json array with city name and url
class CityHandler(webapp.RequestHandler):
    def get(self):
        # Header
        self.response.headers["Content-Type"] = "text/javascript"
        callback = None
        if self.request.get("callback")!="":
            callback = self.request.get("callback")
        
        resultList = []
        for item in cityList:
            resultList += [{"name": item[0], "enName": item[1]}]
            
        jsonObject = json.dumps(resultList, sort_keys=True)
        if callback is not None:
            result = callback + "(" + jsonObject + ");"
        else:
            result = jsonObject
        self.response.out.write(result)

## WebApp object
application = webapp.WSGIApplication([('/json/city/', CityHandler)], debug=True)

## Main function for speedup with memcache
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()