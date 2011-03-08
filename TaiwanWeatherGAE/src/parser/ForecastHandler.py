from google.appengine.ext import webapp

##
# This class will return forecast data from cwb.gov.tw
#
# Arguments:
#    
#
# Return:
#    - json array with object as city
class ForecastHandler(webapp.RequestHandler):
    pass
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