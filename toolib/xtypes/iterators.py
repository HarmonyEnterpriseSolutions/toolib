###############################################################################
# Program:   Sula 0.7
"""
	iterator types module, contain special types of iterators.
"""
__author__  = "Lesha Strashko"
__date__	= "$Date: 2007/03/05 17:35:49 $"
__version__ = "$Revision: 1.9 $"
__credits__ = "No credits today"
# $Source: D:/HOME/cvs/toolib/xtypes/iterators.py,v $
###############################################################################


class OrderDictSequence:
	"""
	Sequence over objects from objectDict with order form orderList
	"""
	def __init__(self, objectDict, orderList):
		self._objects = objectDict
		self._order = orderList

	def __len__(self):
		return len(self._order)

	def __getitem__(self, i):
		return self._objects[self._order[i]]


from toolib.util.OrderDict import OrderDictIterator, OrderDictTupleIterator

class ReverseIterator:
	
	"Iterator for looping over a sequence backwards"
	
	def __init__(self, data):
		self.data = data
		self.index = len(data)
	
	def __iter__(self):
		return self

	def next(self):
		if self.index == 0:
			raise StopIteration
		self.index -= 1
		return self.data[self.index]
