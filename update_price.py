#!/usr/bin/python

CATEGORY = ''
SKIPTO = 'OR7.F'


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

for row in cursor.fetchall():
	print '\033[1;33m' + row[1] + '\033[0m'

	if row[1] == SKIPTO: 
		start = True

	if start == False:
		continue

	try:
		stock = Share( row[1] )
	except Exception as e:
		pass
	else:
		price = stock.get_price()
		print price
		if price == None:
			price = -1.0

		sql = 'UPDATE `finance`.`SYMBOL` SET `PRICE` = %s WHERE `symbol`.`INDEX` = %d' % (price, row[0] )
		cursor.execute( sql )
		conn.commit()

