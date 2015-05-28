#!/usr/bin/python

with open('exchange.txt','r') as f:

	lines = f.readlines()
	d={}
	for x in lines:
		s = x.split('\n')[0]
		if d.has_key(s) is False:
			d[s] = 1
		else:
			d[s] += 1


with open('count.txt', 'w') as f:
	for x in d:
		f.write( "%5.5d\t%s\n" % (d[x], x) )


