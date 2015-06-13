#!/usr/bin/python

CATEGORY = ''
SKIPTO = ''

import datetime
import MySQLdb
from yahoo_finance import Share


conn=MySQLdb.connect(host="localhost",user="root",passwd="!23QweAsdZxc",charset="utf8", db='finance')

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

	years = (dividends[0][1] - dividends[-1][1]).days / 365.0

	#print 'years: ', years
	if years < 2.0:
		continue

	dividends_a_year = 0

	for d in dividends:
		if d[1].year == 2014:
			dividends_a_year += 1

	sql = 'UPDATE `finance`.`SYMBOL` SET `YEARS` = %d, `DIVIDENDS_A_YEAR` = %d WHERE `SYMBOL`.`INDEX` = %d' % (years, dividends_a_year, row[0] )
	#print sql
	cursor.execute( sql )
conn.commit()

b = datetime.datetime.now()

c = b - a

print "It takes " , c.microseconds , " micro seconds"
