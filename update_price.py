#!/usr/bin/python
import signal
import sys
import time
import MySQLdb
import os
import threading
from yahoo_finance import Share

stocks_per_thread = 100

CATEGORY = ''
SKIPTO = ''

def signal_handler( signal, frame ):
	with open( 'price_skip.txt', 'w') as f:
		f.write( current )
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)



def worker( i, targets, ret ):
	for row in targets:
		try:
			stock = Share( row[1] )
		except Exception as e:
			pass
		else:
			price = stock.get_price()
			#print i, ' ', price
			if price == None:
				price = -1.0
			ret[ row ] = price
			



if __name__ == '__main__':
	if False and os.path.isfile( 'price_skip.txt' ) is True:
		with open( 'price_skip.txt', 'r') as f:
			SKIPTO = f.readline()

	conn=MySQLdb.connect(host="localhost",user="root",passwd="!23QweAsdZxc",charset="utf8", db='finance')

	cursor = conn.cursor()


	if CATEGORY != '':
		sql = 'SELECT * FROM SYMBOL WHERE CATEGORY=\'' + CATEGORY + '\''
	else:
		sql = 'SELECT * FROM SYMBOL'

	Total = cursor.execute( sql )
	print 'Total:', Total

	if SKIPTO != '':
		start = False
	else:
		start = True

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

	for x in ret:
		sql = 'UPDATE `finance`.`SYMBOL` SET `PRICE` = %s WHERE `symbol`.`INDEX` = %d' % (ret[x], x[0] )
		print sql
		cursor.execute( sql )
		conn.commit()
