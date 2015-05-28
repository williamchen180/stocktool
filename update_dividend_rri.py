#!/usr/bin/python

CATEGORY = ''
SKIPTO = ''

import datetime
import MySQLdb
from yahoo_finance import Share


conn=MySQLdb.connect(host="localhost",user="root",passwd="111111",charset="utf8", db='finance')

cursor = conn.cursor()


if CATEGORY != '':
	sql = 'SELECT * FROM SYMBOL WHERE CATEGORY=\'' + CATEGORY + '\''
else:
	sql = 'SELECT * FROM SYMBOL'

num = cursor.execute( sql )

if SKIPTO != '':
	start = False
else:
	start = True

symbols = cursor.fetchall()


sql = 'SELECT * FROM DIVIDEND'

num = cursor.execute( sql )

dividend = cursor.fetchall()

divhash = dict()

print symbols[0]
print dividend[0]

for d in dividend:
	if divhash.has_key( d[0] ) == False:
		divhash[ d[0] ] = list()
	divhash[ d[0] ].append( d )

a = datetime.datetime.now()

for row in symbols:
	#print '\033[1;33m' + row[1] + '\033[0m'

	if row[1] == SKIPTO: 
		start = True
	if start == False:
		continue

	if divhash.has_key( row[0] ) == False:
		continue

	dividends = divhash[ row[0] ]

	# row[8] is 'YEARS'
	if row[8] < 6:		
		continue


	div_total = float(0.0)


	for d in dividends:
		if d[1].year >= 2010 and d[1].year <= 2014:
			div_total += d[2]

	div_avg = div_total / 5.0

	RRI9 = div_avg / 0.09 
	RRI11 = div_avg / 0.11
	RRI14 = div_avg / 0.14
	
	sql = 'UPDATE `finance`.`SYMBOL` SET `RRI9` = %f, `RRI11` = %f, `RRI14` = %f WHERE `SYMBOL`.`INDEX` = %d' % (RRI9, RRI11, RRI14, row[0] )
	#print sql
	cursor.execute( sql )
	conn.commit()




b = datetime.datetime.now()
c = b - a
print "It takes " , c.microseconds , " micro seconds"
