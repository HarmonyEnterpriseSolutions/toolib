###############################################################################
# Program:   toolib
"""
Dictionary wrapper, allows to use it as key of dictionary
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2006/08/03 18:39:40 $"
__version__ = "$Revision: 1.2 $"
# $Source: D:/HOME/cvs/toolib/util/iterators.py,v $
###############################################################################

def iterContinuousRanges(integers):
	integers = iter(integers)
	start = prev = integers.next()
	for item in integers:
		if item - 1 != prev:
			yield start, prev-start+1
			start = item
		prev = item						
	yield start, prev-start+1


def iterRecursiveWithGetChildren(
		object, 
		childrenGetter = 'getChildren',
		includeThis = False
	):

	if includeThis:
		yield object

	try:
		for child in getattr(object, childrenGetter)() or ():
			yield child

			for i in iterRecursiveWithGetChildren(child, childrenGetter):
				yield i

	except AttributeError:
		pass


def iterRecursiveWithGetItem(
		object, 
		itemGetter = '__getitem__',
		lengthGetter = '__len__',
		includeThis = False
	):

	if includeThis:
		yield object

	try:
		for index in xrange(getattr(object, lengthGetter)() or 0):
			child = getattr(object, itemGetter)(index)

			yield child

			for i in iterRecursiveWithGetItem(child, itemGetter, lengthGetter):
				yield i

	except AttributeError:
		pass


if __name__ == '__main__':
	tree = [
		[1,2,3,4,5],
		[
			[6,7,8],
			[9],
		],
		10,
		11,
	]

	#for i in iterRecursiveWithGetItem(tree):
	#	print i

	for i, j in iterContinuousRanges([1,2,3,4,5,  7,  9,10,11,    15,   23,  26,  28]):
		print i, j
