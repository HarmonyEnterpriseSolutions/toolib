#################################################################
# Program:   toolib
"""
Generates random ids
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2007/01/19 16:51:21 $"
__version__ = "$Revision: 1.5 $"
# $Source: D:/HOME/cvs/toolib/utility/uid.py,v $
#																#
#################################################################
import sys
from _random import Random
from toolib.util.lang import ulong

__all__ = ["randInt", "getInt", "getId", "getId64", "getId128", "getId256"]

INT_MAX = long(sys.maxint)
INT_MIN = -INT_MAX - 1
K = 2 * (INT_MAX + 1)

random = Random()

def randInt(): 
	return int(long(random.random() * K) + INT_MIN)

def getInt(dict=None):
	while True:
		n = randInt()
		if dict is None or n not in dict:
			return n

def getId(bits=32, prefix="", afix="", delim="-", dict=None):
	assert bits/32*32 == bits, "Bits must me 32*N"
	while True:
		ids = ["%08X" % ulong(randInt()) for i in range(bits/32)]
		s = "".join((prefix,  delim.join(ids), afix))
		if dict is None or not dict.has_key(s):
			return s

def getId64(*p): return getId(64, *p)
def getId128(*p): return getId(128, *p)
def getId256(*p): return getId(256, *p)

if __name__ =='__main__':
	import types
	i=0
	try:
		while 1:
			x = randInt()
			if type(x) != types.IntType:
				print "! Type missmatch: ", type(x), x, "0x%X" % int(x)
			if x > 0x7FFF0000:
				print "+ 0x%X" % ulong(int(x))
			else:
				if x < -0x7FFF0000:
					print "- 0x%X" % ulong(int(x))
			i+=1
	except:
		print i

	print "randInt: ", randInt()
	print getId64("Id64:")
	print getId128("Id128:")
	print getId256("Id256:")
	print "id(1024): ", getId(1024)
