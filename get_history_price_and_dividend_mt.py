#!/usr/bin/python

CATEGORY = ''
SKIPTO = 'DKE1.SG'

stocks_per_thread = 10000000

import threading
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

def worker( i, targets, ret ):
    mech = Browser()
    for row in targets:
	print '\033[1;33m', row[0], " ",  row[1] + '\033[0m'
	dividend_file = 'history/' + row[1] + '.dividend'
	if os.path.isfile( dividend_file ) == True:
		continue

	try:
		url = divurl % (row[1], year, month, day)
		#print url
		page = mech.open( url ) 
	except Exception as e:
                print 'something wrong here' , e
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
		#print url
		page = mech.open( url ) 
	except Exception as e:
                print 'something wrong here1' , e
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


conn=MySQLdb.connect(host="localhost",user="root",passwd="!23QweAsdZxc",charset="utf8", db='finance')
cursor = conn.cursor()

if CATEGORY != '':
	sql = 'SELECT * FROM SYMBOL WHERE CATEGORY=\'' + CATEGORY + '\''
else:
	sql = 'SELECT * FROM SYMBOL'

Total = cursor.execute( sql )

if SKIPTO != '':
	start = False
else:
	start = True

if os.path.isdir( 'history' ) == False:
	os.mkdir( 'history' )

rows = cursor.fetchall()
threads = []
ret = {}

for i in range(0, Total/stocks_per_thread + 1):
        if i*stocks_per_thread < Total:
                target = rows[ i*stocks_per_thread: i*stocks_per_thread + stocks_per_thread ]
        else:
                target = rows[ i*stocks_per_thread: ]
        t = threading.Thread( target=worker, args=(i, target,ret))
        threads.append(t)
        t.start() 

for t in threads:
        t.join()

