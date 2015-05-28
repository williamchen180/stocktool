#!/usr/bin/python


base = 'stocks'

conds = [ \
	'price > 0 and RRI14 > price', 
	'price > 0 and RRI14 > price and exchange = "NMS"',
	'price > 0 and RRI14 > price and exchange = "NAS"',
	'price > 0 and RRI14 > price and exchange = "NYQ"',
	'price > 0 and RRI14 > price and exchange = "FRA"',
	'price > 0 and RRI14 > price and exchange = "PAR"',
	'price > 0 and RRI14 > price and exchange = "KHG"'
	]

conds = [ \
	'price > 0 and RRI14 > price and exchange = "NMS"',
	'price > 0 and RRI14 > price and exchange = "NAS"',
	]


import MySQLdb
import plot
import os

conn=MySQLdb.connect(host="localhost",user="root",passwd="111111",charset="utf8", db='finance')
cursor = conn.cursor()

if os.path.isdir( base ) is False:
	os.mkdir( base )

with open( base + '/index.html', 'w') as f:
	f.write( '<html><head><title>Stock list</title></head><body><p align="center">\n' )

i = 0
for cond in conds:

	sql = 'SELECT * FROM SYMBOL WHERE ' + cond
	num = cursor.execute( sql )

	path = base + '/' + str(i)

	if os.path.isdir( path ) is False:
		os.mkdir( path )

	for row in cursor.fetchall():

		plot.plot( row[1], path=path)

	with open( path + '/index.html', 'w') as fp:
		fp.write( '<html><head><title>NMS</title></head><body><p align="center">\n')
		for root, dirs, files in os.walk( path ): 
			for f in files:
				if f.endswith('png') == True:
					fp.write( '\t<img src="./%s"/>\n' % f )
		fp.write( '</body></html>\n' )

	with open( base + '/index.html', 'a') as f:
		f.write( '<a href=\'%d/index.html\'>%s</a></br>\n' % (i, cond ) )

	i += 1

with open( base + '/index.html', 'a') as f:
	f.write( '</body></html>' )

