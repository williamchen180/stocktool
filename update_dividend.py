#!/usr/bin/python

CATEGORY = 'mutual'
SKIPTO = 'JHBIX'


from mechanize import Browser
import MySQLdb

mech = Browser()

conn=MySQLdb.connect(host="localhost",user="root",passwd="111111",charset="utf8", db='finance')

cursor = conn.cursor()


sql = 'SELECT * FROM SYMBOL WHERE CATEGORY=\'' + CATEGORY + '\''

num = cursor.execute( sql )

url = 'http://ichart.yahoo.com/table.csv?s=%s&c=1990&a=1&b=1&f=2015&d=5&e=1&g=v&ignore=.csv'


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
		page = mech.open( url % row[1] )
	except Exception as e:
		pass
	else:
		html = page.read()
		print html


		sql = 'UPDATE `finance`.`SYMBOL` SET `DIVIDEND` = 1 WHERE `symbol`.`INDEX` = %d' % row[0]
		cursor.execute( sql )
		conn.commit()

		data = html.split('\n')

		for x in data[1:]:
			if len(x) == 0:
				break;
			xx = x.split(',')
			sql = 'INSERT INTO `finance`.`DIVIDEND` (`INDEX`, `DATE`, `PRICING`) VALUES (\'%s\', \'%s\', \'%s\')' % ( row[0], xx[0], xx[1] )
			cursor.execute( sql )

		conn.commit()






