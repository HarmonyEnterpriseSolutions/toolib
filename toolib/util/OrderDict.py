###############################################################################
# Program:   Toolib
"""
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2008/03/20 19:03:15 $"
__version__ = "$Revision: 1.6 $"
# $Source: D:/HOME/cvs/toolib/util/OrderDict.py,v $
###############################################################################
class OrderDictIterator(object):
	"""
	Iteration in dictionary ordered by list of keys.
	next returns value
	"""
	def __init__(self, dict, orderList):
		self.dict = dict
		self.order = orderList
		self.index = 0

	def __iter__(self):
		self.index = 0
		return self

	def next(self):
		try:
			value = self.dict[self.order[self.index]]
			self.index += 1
			return value
		except IndexError:
			raise StopIteration


class OrderDictItemsIterator(OrderDictIterator):
	"""
	Iteration in dictionary ordered by list of keys.
	next returns tuple (key, value)
	"""
	def next(self):
		try:
			key = self.order[self.index]
			value = self.dict[key]
			self.index += 1
			return key, value
		except IndexError:
			raise StopIteration

class OrderDict(dict):
	def __init__(self, data=()):
		dict.__init__(self)
		self.order = []
		for key, value in data:
			self[key] = value

	def __setitem__(self, key, value):
		"""
		if value already exists in dict position remains the same
		else key and value appended to the end
		"""
		try:
			self.order.index(key)
		except ValueError:
			self.order.append(key)
		dict.__setitem__(self, key, value)

	def __delitem__(self, key):
		dict.__delitem__(self, key)
		self.order.remove(key)
	
	def keys(self):
		return list(self.order)

	def iterkeys(self):
		return iter(self.order)

	def values(self):
		return map(self.__getitem__, self.order)

	def itervalues(self):
		"""
		returns generator of tuples (key, value)
		"""
		return OrderDictIterator(self, self.order)

	def items(self):
		"""
		returns list of tuples (key, value)
		"""
		return list(self.iteritems())

	def iteritems(self):
		return OrderDictItemsIterator(self, self.order)

	def reverse(self):
		self.order.reverse()

	def insert(self, index, key, value):
		try:
			self.order.remove(key)
		except:
			pass
		self.order.insert(index, key)
		dict.__setitem__(self, key, value)


	def clear(self):
		del self.order[:]
		return dict.clear(self)


if __name__ == "__main__":
	def test():
		d = OrderDict()
		print d.order

		d['a'] = 1
		d['c'] = 2
		d['b'] = 3
		d['e'] = 4

		del d['c']

		for i in d.itervalues():
			print i

		for i in d.iteritems():
			print i

	test()
