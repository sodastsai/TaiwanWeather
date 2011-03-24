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
from Constants import errorMsg

## Return a service not found page
def main():
    print("Status: 404")
    print("Content-Type: text/html")
    print("<html><body>")
    print(errorMsg(200))
    print("</body></html>")

if __name__ == "__main__":
    main()
