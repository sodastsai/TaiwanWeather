# coding=utf8
from django.utils import simplejson as json

## Error code dictionary
# This dictionary records all error code in this web service api
errorDict = {
             100: "Google App Engine Error.",
             101: "Google App Engine Timeout.",
             
             200: "Service Not Found.",
             201: "REST path is error.",
             
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