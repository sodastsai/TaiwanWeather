# coding=utf8
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp
from django.utils import simplejson as json
import MainHandler

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
            self.response.out.write(MainHandler.errorMsg(201, "City abbr is required."))
            return
        
        # Find city link
        cityLink = None
        for item in cityList:
            if cityName==item[1]:
                cityLink = item[2]
                break
        # Could not find city ...
        if cityLink is None:
            self.response.out.write(MainHandler.errorMsg(201, "City abbr is not found."))
            return
        
        # Return a city
        result = { "url": cityLink }
        self.response.out.write(json.dumps(result))
        
# Some constants
baseURL = "http://www.cwb.gov.tw/V6/forecast/taiwan/"
cityStr01 = u"台北市"
cityStr02 = u"新北市"
cityStr03 = u"台中市"
cityStr04 = u"台南市"
cityStr05 = u"高雄市"
cityStr06 = u"基隆北海岸"
cityStr07 = u"桃園"
cityStr08 = u"新竹"
cityStr09 = u"苗栗"
cityStr10 = u"彰化"
cityStr11 = u"南投"
cityStr12 = u"雲林"
cityStr13 = u"嘉義"
cityStr14 = u"屏東"
cityStr15 = u"恆春半島"
cityStr16 = u"宜蘭"
cityStr17 = u"花蓮"
cityStr18 = u"台東"
cityStr19 = u"澎湖"
cityStr20 = u"金門"
cityStr21 = u"馬祖"
## City List provided by cwb.gov.tw
# Current version is from http://www.cwb.gov.tw/V6/js/ForecastMenu.js
cityList = [
    (cityStr01, "Taipei", baseURL+"36_01_data.htm"),
    (cityStr02, "NewTaipei", baseURL+"36_04_data.htm"),
    (cityStr03, "Taichung", baseURL+"36_08_data.htm"),
    (cityStr04, "Tainan", baseURL+"36_13_data.htm"),
    (cityStr05, "Kaohsiung", baseURL+"36_02_data.htm"),
    (cityStr06, "Keelung", baseURL+"36_03_data.htm"),
    (cityStr07, "Taoyuan", baseURL+"36_05_data.htm"),
    (cityStr08, "Hsinchu", baseURL+"36_06_data.htm"),
    (cityStr09, "Miaoli", baseURL+"36_07_data.htm"),
    (cityStr10, "Changhua", baseURL+"36_09_data.htm"),
    (cityStr11, "Nantou", baseURL+"36_10_data.htm"),
    (cityStr12, "Yunlin", baseURL+"36_11_data.htm"),
    (cityStr13, "Chiayi", baseURL+"36_12_data.htm"),
    (cityStr14, "Pingtung", baseURL+"36_15_data.htm"),
    (cityStr15, "Hengchun", baseURL+"36_16_data.htm"),
    (cityStr16, "Yilan", baseURL+"36_17_data.htm"),
    (cityStr17, "Hualien", baseURL+"36_18_data.htm"),
    (cityStr18, "Taitung", baseURL+"36_19_data.htm"),
    (cityStr19, "Penghu", baseURL+"36_20_data.htm"),
    (cityStr20, "Kinmen", baseURL+"36_21_data.htm"),
    (cityStr21, "Matsu", baseURL+"36_22_data.htm")
]

## WebApp object
application = webapp.WSGIApplication([
                                      ('/json/forecastCity/', CityListHandler),
                                      ('/json/forecastCity/pageURL/.*/', PageURLHandler)
                                      ],
                                     debug=True)

##
# Main function for speedup with memcache
#
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()