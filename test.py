#!/usr/bin/python

cond = 'price > 0 and RRI14 > price and exchange = "NMS"'

import os

with open( cond + '/index.html', 'w') as fp:
	fp.write( '<html><head><title>NMS</title></head><body><p align="center">')
	for root, dirs, files in os.walk(cond): 
		for f in files:
			if f.endswith('png') == True:
				fp.write( '<img src="%s"/>' % f )
	fp.write( '</body></html>' )

				

