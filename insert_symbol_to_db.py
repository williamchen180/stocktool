#!/usr/bin/python

import re
import string
import MySQLdb

data = { 'stock':'symbols_stock.csv', 'mutual' : 'symbols_mutual_fund.csv', 'ETF' : 'symbols_ETF.csv' } 

conn=MySQLdb.connect(host="localhost",user="root",passwd="!23QweAsdZxc",charset="utf8", db='finance')

cursor = conn.cursor()

for CATEGORY in data:
	FILE = data[CATEGORY]
	
	with open(FILE, mode='r') as f:
		line = f.readline()
		line = line.replace('\r"','"')
		stocks = line.split('\r')
		for x in stocks:
			s = x.split(',')
			print s[0], s[1], s[2]

			sql = 'INSERT INTO SYMBOL (TICKER, NAME, EXCHANGE, CATEGORY ) VALUES ("%s", "%s", "%s" , "%s")' % (s[0], re.sub('[\W_]', ' ', s[1].replace('"','')) , s[2], CATEGORY)

			print sql
			cursor.execute( sql )

		conn.commit()


