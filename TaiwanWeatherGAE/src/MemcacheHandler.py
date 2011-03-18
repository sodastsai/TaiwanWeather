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
from google.appengine.ext import webapp
from google.appengine.api import memcache
from Constants import errorMsg

## web app for memcache 
class MemcacheHandler(webapp.RequestHandler):
    def get(self):
        # Flush all memcache keys
        if self.request.get("flush")=="true":
            if memcache.flush_all(): #@UndefinedVariable
                self.response.out.write("{\"result\": 0, \"message\": \"All memcache has been flushed.\"}")
            else:
                self.response.out.write(errorMsg(100, "Memcache opration failed"))