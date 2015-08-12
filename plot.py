#!/usr/bin/python

import os.path
import get_history
import Gnuplot
import time
from mechanize import Browser
import MySQLdb
import sys
from yahoo_finance import Share



class	plot:

	def __init__( self, symbol, path = '' ):

		self.path = path

		symbol = symbol.upper()

<<<<<<< HEAD
=======
		conn=MySQLdb.connect(host="localhost",user="root",passwd="!23QweAsdZxc",charset="utf8", db='finance')
		cursor = conn.cursor()

		sql = 'SELECT * FROM `SYMBOL` WHERE `TICKER` LIKE \'%s\'' % symbol 

		num = cursor.execute( sql )

		if num == 0:
                        #print '[%s] not found' % symbol
			return

		rows = cursor.fetchall()

>>>>>>> fe8472e8bd5492f2c0275ed6cc7ceef0a40967c3
		dividend_file = 'history/%s.dividend' % symbol 
		price_file = 'history/%s.price' % symbol 

		if os.path.isfile( dividend_file ) == False or os.path.isfile( price_file) == False:
			get_history.get_history().get(symbol)

		if os.path.isfile( dividend_file ) == False or os.path.isfile( price_file) == False:
<<<<<<< HEAD
			print "Dividend or history of %s can't be found from yahoo" % symbol
			return False
=======
			#print "can't get dividend or history price from yahoo"
                        return
>>>>>>> fe8472e8bd5492f2c0275ed6cc7ceef0a40967c3


		with open( dividend_file, 'r') as f:
			div_total = 0.0
			div_last = 0.0
<<<<<<< HEAD
			for line in f.readlines():
				if line[0] == '#':
					continue
				year = int(line.split('-')[0])
				dividend = float( line.split(',')[1] )
=======
			for d in dividends:
				#print d
				if d[1].year >= 2010 and d[1].year <= 2014:
					div_total += d[2]
>>>>>>> fe8472e8bd5492f2c0275ed6cc7ceef0a40967c3

				if year >= 2010 and year <= 2014:
					div_total += dividend
				if year == 2014:
					div_last += dividend

			#print "Average dividend: ", div_total / 5.0


		RRI9 = div_total / 5.0 / 0.09
		RRI11 = div_total / 5.0 / 0.11
		RRI14= div_total / 5.0 / 0.14

		RRI9Last = div_last / 0.09
		RRI11Last = div_last / 0.11
		RRI14Last = div_last / 0.14

		current_price = 0
		try:
			stock = Share( symbol )
		except Exception as e:
			print e
			pass
		else:
			price = stock.get_price()
			if price == None:
				current_price = 0
			else:
				print type(price), price
				current_price = float(price) 


		p = Gnuplot.Gnuplot()

		p('reset')
		p('RRI9(x)=%f' % RRI9 ) 
		p('RRI11(x)=%f' % RRI11 ) 
		p('RRI14(x)=%f' % RRI14 ) 

		p('RRI9Last(x)=%f' % RRI9Last )
		p('RRI11Last(x)=%f' % RRI11Last )
		p('RRI14Last(x)=%f' % RRI14Last )

		p('set title "%s, Price: %.2f ' \
		' (9,11,14)%% = (%.2f, %.2f, %.2f) '
		' (9,11,14)%% = (%.2f, %.2f, %.2f)%%"' \
			% (symbol, current_price, \
			RRI9, RRI11, RRI14, RRI9Last, RRI11Last, RRI14Last ) )

		p('set terminal png size 1200,600')
		cmd = 'set output \'%s\'' %  ('./' + path + '/' + symbol + '.PNG')
		#print cmd
		p(cmd)
		p('set datafile sep ","')
		p('set xdata time')
		p('set timefmt "%Y-%m-%d"')
		p('set format x ""')
		p('unset grid')
		p('set tmargin')
		p('set lmargin 10')
		p('set bmargin 0')
		p('set multiplot')
		p('set size 1, 0.4')
		p('set origin 0, 0.6')
		p('plot RRI9(x) title "9%", RRI11(x) title "11%", RRI14(x) title "14%", "' + price_file + '" using 1:5 notitle with lines')
		p('set grid')
		p('set title ""')
		p('set tmargin 0')
		p('set bmargin 0')
		p('set xdata time')
		p('set timefmt "%Y-%m-%d"')
		p('set format x ""')
		p('set size 1.0, 0.3')
		p('set origin 0.0, 0.3')
		p('plot "' + price_file + '" using 1:($6/1000) title "volume x1000" with impulses')
		p('set xdata time')
		p('set timefmt "%Y-%m-%d"')
		p('set format x "%y/%m/%d"')
		#p('set xtics ("2010/01/01","2011/01/01")')
		p('set size 1.0, 0.3')
		p('set origin 0.0, 0.0')

		p('set bmargin')
		p('plot "' + dividend_file + '" using 1:2 title "dividend" with linespoints')
		p('unset multiplot')

		#time.sleep(1)
		#os.system( 'open %s' % (symbol + '.png') ) 


if __name__ == '__main__':
	if len(sys.argv) == 1:
		print "Usage: ", sys.argv[0], " SYMBOL"
		sys.exit(0)

	for x in sys.argv[1:]:
		plot( x, path='PNG' )




