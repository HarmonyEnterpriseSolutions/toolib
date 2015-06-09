###############################################################################
# Program:   toolib
"""
	contains sequence Cache, where values for keys in dict
	are loaded by external method
	method can be class bound or static function
	metod must accept at list key argument
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2006/05/18 14:59:12 $"
__version__ = "$Revision: 1.4 $"
# $Source: D:/HOME/cvs/toolib/util/SequenceCache.py,v $
###############################################################################

__all__ = ['SequenceCache']

class SequenceCache(object):
	def __init__(self, size, loadMethod, saveMethod=None):
		self._data = [NotImplemented] * size
		self._loadMethod = loadMethod
		self._saveMethod = saveMethod

	def isItemLoaded(self, index):
		return self._data[index] is not NotImplemented

	def __len__(self):
		return len(self._data)

	def __getitem__(self, index):
		item = self._data[index]
		if item is NotImplemented:
			item = self._loadMethod(index)
			self._data[index] = item
		return item

	def put(self, index, value, *args, **kwargs):
		self._data[index] = value
		if self._saveMethod is not None:
			self._saveMethod(index,  value, *args, **kwargs)

	__setitem__ = put

	def flush(self):
		for i in xrange(len(self._data)):
			self._data[i] = NotImplemented


if __name__ == '__main__':

	print "------- Test ListCache"

	def load(key):
		print ">> load: %s" % key
		return "value of %s" % key

	d = SequenceCache(5, load)
	print d[1]
	print d[1]
	print d[2]
	print d._data

