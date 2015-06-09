from copy import deepcopy

def listxd(*dimensions, **kwargs):
	"""
	generates x-dimensional list of lists (of lists)
	accepts named arg fillValue
	"""
	if len(dimensions) > 1:
		row = listxd(*dimensions[1:], **kwargs)
		res = map(lambda n: deepcopy(row), xrange(dimensions[0]-1))
		res.append(row)
		return res
	else:
		return [kwargs.get('fillValue')] * dimensions[0]

def ensureSize(l, size, fillItem=None):
	"""
	stretches list to size and fills with fillItem
	"""
	if len(l) < size:
		l += [fillItem] * (size - len(l))
	return l
	
def setItemSafe(l, index, item, fillItem=None):
	"""
	stretches list to index and fills with fillItem
	sets [index] to item
	"""
	assert isinstance(l, list), "list expected, got %s %s"  % (l, type(l),)
	ensureSize(l, index+1, fillItem)
	l[index] = item
	return l


def setItemSafe2d(list2d, rowIndex, colIndex, item, fillItem=None):
	"""
	stretches list of lists to index and fills with fillItem
	sets list2d[rowIndex][colIndex] to item
	"""
	ensureSize(list2d, rowIndex+1)
	if list2d[rowIndex] is None:
		list2d[rowIndex] = row = []
	else:
		row = list2d[rowIndex]
	setItemSafe(row, colIndex, item, fillItem)

def fromSequence(sequence, maxSize):
	try:
		l = []
		for i in xrange(maxSize):
			l.append(sequence[i])
	except IndexError:
		pass
	return l

def isListOf(list, value):
	for i in list:
		if i != value:
			return False
	return True

def sorted(l):
	l = list(l)
	l.sort()
	return l

if __name__ == '__main__':
	def testSetItemSafe2d():
		l = []
		setItemSafe2d(l, 3, 4, 'XXX', '-')
		setItemSafe2d(l, 5, 2, 'YYY', '-')
		print l

	testSetItemSafe2d()
