from base import *

try:
	import randre
except ImportError:
	from toolib.text.yapps import yapps2
	import os
	dir = os.path.split(os.path.abspath(__file__))[0]
	yapps2.generate(os.path.join(dir, 'randre.g'), os.path.join(dir, 'randre.py'))

	import randre

if __name__ == '__main__':
	print choice('oleg')

	s = '\d{10}'#'A{5} \- [A-K]{2}\-\d{4}\-[L-Z]{2}'
	p = randre.compile(s)
	print p

	from toolib.dbg.Timer import Timer

	t = Timer()

	for i in xrange(1):
		print p.rand()

	print t
