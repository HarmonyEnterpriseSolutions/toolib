

class DictIterator(object):
	"""
	converts iterator of sequences to iterator if dicts
	columns is column names, can be infinite iterator
	"""

	def __init__(self, iterator, columns):

		self.iterator = ensure_has_next(iterator)
		self.columns = LazyList(columns)

	
	def __iter__(self):
		return self

	
	def next(self):
		record = self.iterator.next()
		return dict(((self.columns[i], value) for i, value in enumerate(record)))


class LazyList(object):
	"""
	provides __getitem__ to iterator
	"""

	def __init__(self, iterator):
		if isinstance(iterator, (list, tuple)):
			self.iterator = iter(())
			self.data = iterator
		else:				
			self.iterator = ensure_has_next(iterator)
			self.data = []

	def __getitem__(self, i):
		try:
			while i >= len(self.data):
				self.data.append(self.iterator.next())
		
			return self.data[i]
		except StopIteration:
			raise IndexError, "index out of range"
				

class ExcelColumns(object):

	"""
	iterator of excel column names
	"""

	def __init__(self, alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
		self.count = 0
		self.alphabet = alphabet
		self.base = len(self.alphabet)
	
	def __iter__(self):
		return self

	def next(self):

		i = self.count + 1

		self.count += 1

		result = []
		
		while i > 0:
			result.append(self.alphabet[(i+1) % self.base - 2])
			i = (i-1) / self.base
		
		result.reverse()	
		
		return ''.join(result)


def ensure_has_next(iterator):
	"""
	returns iter(object) if object has no method 'next'
	"""
	return iterator if hasattr(iterator, 'next') else iter(iterator)


if __name__ == '__main__':
	data = [
		(1,2,3),
		(4,5,6),
		(7,8,9,10,11),
		(22,33,44),
	]

	for row in DictIterator(data, ExcelColumns()):
		print row


