#!/usr/bin/python

import os.path
import get_history
import Gnuplot
import time
from mechanize import Browser
import MySQLdb
import sys

class	plot:

	def __init__( self, symbol, path = '' ):

		self.path = path

		symbol = symbol.upper()

		conn=MySQLdb.connect(host="localhost",user="root",passwd="111111",charset="utf8", db='finance')
		cursor = conn.cursor()

		sql = 'SELECT * FROM `SYMBOL` WHERE `TICKER` LIKE \'%s\'' % symbol 

		num = cursor.execute( sql )

		if num == 0:
			print "%s not found" % symbol 
			sys.exit(0)

		rows = cursor.fetchall()

		for r in rows:
			print r

		dividend_file = 'history/%s.dividend' % symbol 
		price_file = 'history/%s.price' % symbol 

		if os.path.isfile( dividend_file ) == False or os.path.isfile( price_file) == False:
			get_history.get_history().get(symbol)

		if os.path.isfile( dividend_file ) == False or os.path.isfile( price_file) == False:
			print "can't get dividend or history price from yahoo"
			sys.exit(0)

		if True:
			num = cursor.execute( 'SELECT * FROM `DIVIDEND` WHERE `INDEX` = %d' % rows[0][0] )
			dividends = cursor.fetchall()

			div_total = 0.0
			for d in dividends:
				print d
				if d[1].year >= 2010 and d[1].year <= 2014:
					div_total += d[2]
			print "Average dividend: ", div_total / 5.0

		if True:
			RRI9 = div_total / 5.0 / 0.09
			RRI11 = div_total / 5.0 / 0.11
			RRI14= div_total / 5.0 / 0.14
		else:
			RRI9 = rows[0][11] 
			RRI11 = rows[0][12] 
			RRI14= rows[0][13] 


		p = Gnuplot.Gnuplot()

		p('reset')
		p('RRI9(x)=%f' % RRI9 ) 
		p('RRI11(x)=%f' % RRI11 ) 
		p('RRI14(x)=%f' % RRI14 ) 

		p('set title "%s, %s\\n %s @ %s\\nPrice: %f, (9,11,14)%% = (%f, %f, %f) "' \
			% (symbol, rows[0][3], rows[0][4], rows[0][2], rows[0][10], RRI9, RRI11, RRI14 ) )

		p('set terminal png size 1200,600')
		cmd = 'set output \'%s\'' %  ('./' + path + '/' + symbol + '.png')
		print cmd
		p(cmd)
		p('set datafile sep ","')
		p('set xdata time')
		p('set timefmt "%Y-%m-%d"')
		p('set format x ""')
		p('set tmargin')
		p('set lmargin 10')
		p('set bmargin 0')
		p('set multiplot')
		p('set size 1, 0.4')
		p('set origin 0, 0.6')
		p('plot RRI9(x) title "9%", RRI11(x) title "11%", RRI14(x) title "14%", "' + price_file + '" using 1:5 notitle with lines')
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

	plot( sys.argv[1] )



