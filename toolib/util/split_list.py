import itertools


def split_list_by(l, n):
	for i in range(len(l)/n + 1):
		p = l[i*n:(i+1)*n]
		if p:
			yield p


class CountingIterator(object):
	def __init__(self, iterator):
		self.iterator = iterator
		self.count = 0

	def __iter__(self):
		return self
	
	def next(self):
		next = self.iterator.next()
		self.count += 1
		return next


def isplit_list_by(il, n):
	"""
	returns iterator of iterator2
	each iterator2 will return n element of il
	"""
	il = iter(il) # to forget about length
	while True:
		p = CountingIterator(itertools.islice(il, n))
		yield p
		if p.count < n:
			return


if __name__ == '__main__':
	for x in isplit_list_by(xrange(400), 30):
		print "------------"
		for z in x:
			print repr(z),
		print


