/*
 *   Copyright 2011 NTU CSIE Mobile & HCI Research Lab
 *
 *   Licensed under the Apache License, Version 2.0 (the "License");
 *   you may not use this file except in compliance with the License.
 *   You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 *   Unless required by applicable law or agreed to in writing, software
 *   distributed under the License is distributed on an "AS IS" BASIS,
 *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *   See the License for the specific language governing permissions and
 *   limitations under the License.
 */
$(document).ready(function(){
	// Home
	$("button").click(function(){
		window.location = "/"
	});
	
	// Get original input
	lines = $("pre.json").html().split("\n");
	// Add span
	formatted = ""
	for (i=0; i<lines.length; i++) {
		// Comment
		targetString = lines[i].match(/\/\/.*$/);
		resultString = lines[i].replace(/\/\/.*$/, "<span class=\"comment\">"+targetString+"</span>");
		formatted+=resultString+"\n"
	}
	// Write back
	$("pre.json").html(formatted);
});