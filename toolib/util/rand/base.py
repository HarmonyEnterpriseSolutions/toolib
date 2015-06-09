"""
Lite Random implementation
"""

from _random import Random

__all__ = [
	'random',
	'randrange',
	'randint',
	'randbelow',
	'choice',
]
             
random = Random().random

def randrange(start, stop):
	return start + int(random() * (stop - start))

def randint(a, b):
	return randrange(a, b+1)

def randbelow(width):
	return int(random() * width)

def choice(l):
	return l[int(random() * len(l))]

if __name__ == '__main__':
	m = 0
	N = 1000000
	
	import sys
	a = sys.maxint
	b = -sys.maxint

	for i in xrange(N):
		x = randrange(1, 10)
		m += x
		a = min(a, x)
		b = max(b, x)
	print a, b
	print float(m) / N
