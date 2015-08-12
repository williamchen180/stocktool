#!/usr/bin/python


import os
import os.path
import time
from mechanize import Browser
import MySQLdb

class getStock: 

	def __init__( self ):
		self.divurl = 'http://ichart.yahoo.com/table.csv?s=%s&c=1990&a=1&b=1&f=%s&d=%s&e=%s&g=v&ignore=.csv'
		self.priurl = 'http://ichart.yahoo.com/table.csv?s=%s&c=1990&a=1&b=1&f=%s&d=%s&e=%s&g=d&ignore=.csv'

		self.year = time.strftime('%Y')
		self.month = time.strftime('%m')
		self.day = time.strftime('%d')

		print self.year, self.month, self.day

		self.mech = Browser()

		if os.path.isdir( 'history/' ) is False:
			os.mkdir( 'history/' )

	def get( self, symbol ):

		symbol = symbol.upper()

		self.dividends_got = False
		try:
			url = self.divurl % (symbol, self.year, self.month, self.day)
			print url
			page = self.mech.open( url ) 
		except Exception as e:
			print e
			pass
		else:
			try:
				html = page.read()
			except Exception as e:
				print e
				pass
			else:
				f = open('history/' + symbol + '.dividend', 'w')
				f.write( '#' + html )
				f.close()
				self.dividends_got = True

		self.prices_got = False
		try:
			url = self.priurl % (symbol, self.year, self.month, self.day)
			print url
			page = self.mech.open( url ) 
		except Exception as e:
			print e
			pass
		else:
			try:
				html = page.read()
			except Exception as e:
				print e
				pass
			else:
				f = open('history/' + symbol + '.price', 'w')
				f.write( '#' + html )
				f.close()
				self.prices_got = True
		if self.dividends_got == True and self.prices_got == True:
			return True
		else:
			return False

