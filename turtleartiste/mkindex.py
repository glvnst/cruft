#!/usr/bin/python
"""
Write out an html file that lists all the items in the png directory
"""

import os

print ("<!doctype html>\n"
       "<html>\n"
       "<head>\n"
       '<meta charset="UTF-8">\n'
       "<title>I Like Turtles</title>\n"
       '<style type="text/css">\n'
       'body { color: silver; background-color: black; '
       'font-family: "NewsGotTDem"; font-size: 16pt; '
       'margin: 0; padding: 1px;}\n'
       'img { float: left; margin: 1px 1px 0 0; width: 175px; border: 0;}\n'
       '</style>\n'
       "</head>\n"
       "<body>\n")

for root, dirs, files in os.walk('png'):
    for f in files:
        print '<a href="png/{}"><img src="png/{}" /></a>'.format(f, f)

print ("</body>\n"
       "</html>\n")
