#################################################################
# Program: toolib
"""
StackIterator
	Iterator wrapper
	Iterates thrue iterator
	can push back values to get them on next iterations
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2005/08/03 13:42:41 $"
__version__ = "$Revision: 1.3 $"
# $Source: D:/HOME/cvs/toolib/util/StackIterator.py,v $
#
#################################################################

class StackIterator(object):
	__doc__ = __doc__

	def __init__(self, iterator):
		self._iterator = iterator
		self._stack = []

	def next(self):
		if not self._stack:
			return self._iterator.next()
		else:
			try:
				return self._stack.pop()
			except IndexError:
				raise StopIteration

	def back(self, object):
		"""
		pushes back value to get it on next iteration
		can push many values
		"""
		self._stack.append(object)

