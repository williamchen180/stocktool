#!/usr/bin/env python

import cgi, cgitb 
import plot
import time
import os

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
if form.getvalue('textcontent'):
    text_content = form.getvalue('textcontent')
else:
    text_content = "Not entered"

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>";
print "<title>Stock information</title>"
print "</head>"
print "<body>"
print "<p>"

stocks = []

for x in text_content.splitlines():
    for xx in x.split('\t'):
        for xxx in xx.split(' '):
            if xxx != '':
                stocks.append(xxx.upper())


for x in stocks:
    plot.plot(x, path='PNG')

time.sleep(1)

for x in stocks:
    pngfile =  'PNG/' + x + '.PNG';
    if os.path.isfile( pngfile ):
        print '<a href="http://finance.yahoo.com/q?s=%s" target="_blank"/>' % x
        print '<img border=10 src="/%s"/>' % pngfile 
        print '<a/>'



print "</p>"
print "</body>"

