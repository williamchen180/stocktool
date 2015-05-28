#!/usr/bin/python

#cond = 'price > 0 and RRI14 > price'
cond = 'price > 0 and RRI14 > price and exchange = "NAS"'

import MySQLdb
import plot
import os

conn=MySQLdb.connect(host="localhost",user="root",passwd="111111",charset="utf8", db='finance')
cursor = conn.cursor()

sql = 'SELECT * FROM SYMBOL WHERE ' + cond

if os.path.isdir( cond ) is False:
	os.mkdir( cond )

num = cursor.execute( sql )

for row in cursor.fetchall():

	plot.plot( row[1], path=cond)

with open( cond + '/index.html', 'w') as fp:
	fp.write( '<html><head><title>NMS</title></head><body><p align="center">\n')
	for root, dirs, files in os.walk(cond): 
		for f in files:
			if f.endswith('png') == True:
				fp.write( '\t<img src="./%s"/>\n' % f )
	fp.write( '</body></html>\n' )

				




