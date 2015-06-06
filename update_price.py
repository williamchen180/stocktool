#!/usr/bin/python
import signal
import sys
import time
import MySQLdb
import os
from yahoo_finance import Share


CATEGORY = ''
SKIPTO = 'ZSTJ1408.NYM'





def signal_handler( signal, frame ):
	with open( 'price_skip.txt', 'w') as f:
		f.write( current )
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


if os.path.isfile( 'price_skip.txt' ) is True:
	with open( 'price_skip.txt', 'r') as f:
		SKIPTO = f.readline()
	



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

	current = row[1]

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

