#!/usr/bin/python

CATEGORY = ''
SKIPTO = ''


import os.path
import time
from mechanize import Browser
import MySQLdb

divurl = 'http://ichart.yahoo.com/table.csv?s=%s&c=1990&a=1&b=1&f=%s&d=%s&e=%s&g=v&ignore=.csv'
priurl = 'http://ichart.yahoo.com/table.csv?s=%s&c=1990&a=1&b=1&f=%s&d=%s&e=%s&g=d&ignore=.csv'

year = time.strftime('%Y')
month = time.strftime('%m')
day = time.strftime('%d')

print year, month, day

mech = Browser()

conn=MySQLdb.connect(host="localhost",user="root",passwd="!23QweAsdZxc",charset="utf8", db='finance')
cursor = conn.cursor()

if CATEGORY != '':
	sql = 'SELECT * FROM SYMBOL WHERE CATEGORY=\'' + CATEGORY + '\''
else:
	sql = 'SELECT * FROM SYMBOL LIMIT 25'

num = cursor.execute( sql )

if SKIPTO != '':
	start = False
else:
	start = True

for row in cursor.fetchall():
	print '\033[1;33m', row[0], " ",  row[1] + '\033[0m'

	dividend_file = 'history/' + row[1] + '.dividend'

	if os.path.isfile( dividend_file ) == True:
		continue

	if row[1] == SKIPTO: 
		start = True

	if start == False:
		continue

	try:
		url = divurl % (row[1], year, month, day)
		print url
		page = mech.open( url ) 
	except Exception as e:
		pass
	else:
		try:
			html = page.read()
		except Exception as e:
			print html
			with open('history/errorlist.txt', 'a') as f:
				f.write( row[1] + '\n' )
		else:
			f = open('history/' + row[1] + '.dividend', 'w')
			f.write( '#' + html )
			f.close()

	try:
		url = priurl % (row[1], year, month, day)
		print url
		page = mech.open( url ) 
	except Exception as e:
		pass
	else:
		try:
			html = page.read()
		except Exception as e:
			print html
			with open('history/errorlist.txt', 'a') as f:
				f.write( row[1] + '\n' )
		else:
			f = open('history/' + row[1] + '.price', 'w')
			f.write( '#' + html )
			f.close()

