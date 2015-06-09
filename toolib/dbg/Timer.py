#################################################################
# Program:   toolib
"""
"""
__author__  = "Lesha"
__date__	= "$Date: 2006/03/28 17:02:45 $"
__version__ = "$Revision: 1.2 $"
# $Source: D:/HOME/cvs/toolib/dbg/Timer.py,v $
#																#
#################################################################

import time

class Timer(object):
	'''
	'''
	CORRECTION = 0.0

	def __init__(self) :
		self._start = time.clock()

	def clock(self):
		return time.clock() - self._start - self.CORRECTION

	def __str__(self):
		return str(self.clock())

#def testTimer():
#	t = 
#	return t


N = 10000
Timer.CORRECTION = reduce(lambda s, x: s + Timer().clock(), xrange(N), 0.0) / N 
#print Timer.CORRECTION

def test() :
	print Timer()

if __name__ == '__main__' :
	test()
