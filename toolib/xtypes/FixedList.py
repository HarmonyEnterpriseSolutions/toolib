#################################################################
# Program: Rata
"""

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2003/11/18 13:02:07 $"
__version__ = "$Revision: 1.4 $"
# $Source: D:/HOME/cvs/toolib/xtypes/FixedList.py,v $
#
#################################################################
from types import ListType
import types
from toolib.utility.MethodDisabler import MethodDisabler

class FixedList(ListType, MethodDisabler):
	"""
		'__add__',		# x.__add__(y) <==> x+y
		'__contains__',		# x.__contains__(y) <==> y in x
		'__delattr__',		# x.__delattr__('name') <==> del x.name
		'__delitem__',		# x.__delitem__(y) <==> del x[y]
		'__delslice__',		# x.__delslice__(i, j) <==> del x[i:j]
		'__eq__',		# x.__eq__(y) <==> x==y
		'__ge__',		# x.__ge__(y) <==> x>=y
		'__getattribute__',		# x.__getattribute__('name') <==> x.name
		'__getitem__',		# x.__getitem__(y) <==> x[y]
		'__getslice__',		# x.__getslice__(i, j) <==> x[i:j]
		'__gt__',		# x.__gt__(y) <==> x>y
		'__hash__',		# x.__hash__() <==> hash(x)
		'__iadd__',		# x.__iadd__(y) <==> x+=y
		'__imul__',		# x.__imul__(y) <==> x*=y
		'__init__',		# x.__init__(...) initializes x; see x.__class__.__doc__ for signature
		'__le__',		# x.__le__(y) <==> x<=y
		'__len__',		# x.__len__() <==> len(x)
		'__lt__',		# x.__lt__(y) <==> x<y
		'__mul__',		# x.__mul__(n) <==> x*n
		'__ne__',		# x.__ne__(y) <==> x!=y
		'__new__',		# T.__new__(S, ...) -> a new object with type S, a subtype of T
		'__reduce__',		# helper for pickle
		'__repr__',		# x.__repr__() <==> repr(x)
		'__rmul__',		# x.__rmul__(n) <==> n*x
		'__setattr__',		# x.__setattr__('name', value) <==> x.name = value
		'__setitem__',		# x.__setitem__(i, y) <==> x[i]=y
		'__setslice__',		# x.__setslice__(i, j, y) <==> x[i:j]=y
		'__str__',		# x.__str__() <==> str(x)
		'append',		# L.append(object) -- append object to end
		'count',		# L.count(value) -> integer -- return number of occurrences of value
		'extend',		# L.extend(list) -- extend list by appending list elements
		'index',		# L.index(value) -> integer -- return index of first occurrence of value
		'insert',		# L.insert(index, object) -- insert object before index
		'pop',		# L.pop([index]) -> item -- remove and return item at index (default last)
		'remove',		# L.remove(value) -- remove first occurrence of value
		'reverse',		# L.reverse() -- reverse *IN PLACE*
		'sort',		# L.sort([cmpfunc]) -- sort *IN PLACE*; if given, cmpfunc(x, y) -> -1, 0, 1
	"""
	__disabled_methods__ = (
		'__delitem__',		# x.__delitem__(y) <==> del x[y]
		'__delslice__',		# x.__delslice__(i, j) <==> del x[i:j]

		'__iadd__',		# x.__iadd__(y) <==> x+=y
		'__imul__',		# x.__imul__(y) <==> x*=y

		'append',		# L.append(object) -- append object to end
		'extend',		# L.extend(list) -- extend list by appending list elements
		'insert',		# L.insert(index, object) -- insert object before index
		'pop',			# L.pop([index]) -> item -- remove and return item at index (default last)
		'remove',		# L.remove(value) -- remove first occurrence of value
	)

	def __init__(self, size_or_iterable, itemClass=None):
		"""
		size:		Array size
		itemClass:  Item class to check in setter
		"""
		MethodDisabler.__init__(self)
		self.__itemClass = itemClass

		if isinstance(size_or_iterable, (types.IntType, types.LongType)):
			ListType.extend(self, [None]*size_or_iterable)
		else:
			ListType.extend(self, list(size_or_iterable))

	def __setslice__(self, i, j, y):
		if j-i == len(y):
			ListType.__setslice__(self, i, j, y)
		else:
			raise IndexError, "Length change requested in list slice assignment: %d-%d != %d" % (j, i, len(y))

	def __setitem__(self, i, item):
		if self.__itemClass is None or item is None or isinstance(item, self.__itemClass):
			ListType.__setitem__(self, i, item)
		else:
			raise TypeError, "List assignment item type missmatch, expected %s, got %s" % ( self.__itemClass, item.__class__,)

if __name__ == '__main__':
	import sys
	def test():
		import types
		a = FixedList((1,2,3,4))
		a[3:4] = [3]
		try:
			a[3:4] = [3,4]
		except:
			e = sys.exc_info()
			sys.excepthook(e[0], e[1], e[2])

		b = FixedList(3, types.IntType)
		b[2] = 3
		try:
			b[2] = "Hello Wo-ry-ly-dy"
		except:
			e = sys.exc_info()
			sys.excepthook(e[0], e[1], e[2])
		print a
		print b
	test()
