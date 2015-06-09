class CacheByClass(dict):
	"""
	dynamically extends
	"""

	def __init__(self, *p):
		dict.__init__(self, *p)	# pass initial dict if any

	def __getitem__(self, pyClass):
		try:
			return dict.__getitem__(self, pyClass.__name__)
		except KeyError:
			for base in getattr(pyClass, '__bases__', ()):
				try:
					res = dict.__getitem__(self, base.__name__)
				except KeyError:
					try:
						return self[base]
					except KeyError:
						pass
				else:
					self[pyClass.__name__] = res
					return res
			raise KeyError, pyClass.__name__

	def get(self, pyClass, default=None):
		"""
		Note: caches default value
		"""
		try:
			return self[pyClass]
		except KeyError:
			self[pyClass.__name__] = default
			return default

if __name__ == '__main__':
	class A:
		pass
		x = 'a'

	class BB(object):
		#x = 'bb'
		pass

	class B(BB):
		pass

		#x = 'b'

	class C(A):
		pass

		#x = 'c'

	class D(B, C):
		pass


	d = CacheByClass({ 'A' : 'aaa', 'B': 'bbb'})

	print D().x

	print d
	print 'A', d[A]
	print 'C', d[C]
	print 'D', d[D]
	print d
