
class ForkDict(object):
	"""
	Forks many dicts into one dict interface

	"""
	def __init__(self, dicts, defaultDictIndex=0):
		self.__dicts = tuple(dicts)
		self.__dictChanged = [0]*len(dicts)
		self.__keys = None
		self.__defaultDictIndex = defaultDictIndex

	def __contains__(self, x):
		for d in self.__dicts:
			if x in d:
				return 1
		return 0

	def has_key(self, key):
		for d in self.__dicts:
			if d.has_key(key):
				return 1
		return 0

	def __getitem__(self, key):
		for d in self.__dicts:
			if d.has_key(key):
				return d[key]
		raise KeyError, key

	def __setitem__(self, key, value):
		for i, d in enumerate(self.__dicts):
			oldval = d.get(key, NotImplemented)
			if oldval is not NotImplemented:
				if value != oldval:
					d[key] = value
					self.__dictChanged[i] = True
				return

		# no dictionary have such key, write to default dictionary
		self.__dicts[self.__defaultDictIndex][key] = value
		self.__dictChanged[self.__defaultDictIndex] = True


	def get(self, key, default):
		for d in self.__dicts:
			if d.has_key(key):
				return d[key]
		return default

	def keys(self):
		if self.__keys is None:
			d = {}
			n = len(self.__dicts)
			for i in range(n-1, -1 ,-1):
				d.update(self.__dicts[i])
			self.__keys = tuple(d.iterkeys())
		return self.__keys

	def iterkeys(self):
		return iter(self.keys())

	def values(self):
		values = []
		for key in self.keys():
			values.append(self[key])
		return values

	def itervalues(self):
		"""
		TODO: create iterator for this
		"""
		return iter(self.values())

	def update(self, dict):
		for key, value in dict.iteritems():
			self[key] = value

	def dictCount(self):
		return len(self.__dicts)

	def isDictChangedAt(self, index):
		return self.__dictChanged[index]

	def dicts(self):
		return self.__dicts

	def dictAt(self, index):
		return self.__dicts[index]

	def __str__(self):
		s = ['{']
		for key in self.keys():
			s.append(key.__repr__())
			s.append(': ')
			s.append(self[key].__repr__())
			s.append(', ')
		s.append('}')
		return ''.join(s)

	def __len__(self):
		return len(self.keys())

	def iteritems(self):
		for k in self.keys():
			yield k, self[k]

	def items(self):
		return list(self.iteritems())

##__delattr__:
##x.__delattr__('name') <==> del x.name
##
##
##__delitem__:
##x.__delitem__(y) <==> del x[y]
##
##
##__doc__:
##str(object) -> string
##
##Return a nice string representation of the object.
##If the argument is a string, the return value is the same object.
##
##
##__eq__:
##x.__eq__(y) <==> x==y
##
##
##__ge__:
##x.__ge__(y) <==> x>=y
##
##
##__getattribute__:
##x.__getattribute__('name') <==> x.name
##
##
##__getitem__:
##x.__getitem__(y) <==> x[y]
##
##
##__gt__:
##x.__gt__(y) <==> x>y
##
##
##__hash__:
##x.__hash__() <==> hash(x)
##
##
##__init__:
##x.__init__(...) initializes x; see x.__class__.__doc__ for signature
##
##
##__iter__:
##x.__iter__() <==> iter(x)
##
##
##__le__:
##x.__le__(y) <==> x<=y
##
##
##__len__:
##x.__len__() <==> len(x)
##
##
##__lt__:
##x.__lt__(y) <==> x<y
##
##
##__ne__:
##x.__ne__(y) <==> x!=y
##
##
##__new__:
##T.__new__(S, ...) -> a new object with type S, a subtype of T
##
##
##__reduce__:
##helper for pickle
##
##
##__repr__:
##x.__repr__() <==> repr(x)
##
##
##__setattr__:
##x.__setattr__('name', value) <==> x.name = value
##
##
##__setitem__:
##x.__setitem__(i, y) <==> x[i]=y
##
##
##__str__:
##x.__str__() <==> str(x)
##
##
##clear:
##D.clear() -> None.  Remove all items from D.
##
##
##copy:
##D.copy() -> a shallow copy of D
##
##
##get:
##D.get(k[,d]) -> D[k] if D.has_key(k), else d.  d defaults to None.
##
##
##has_key:
##D.has_key(k) -> 1 if D has a key k, else 0
##
##
##items:
##D.items() -> list of D's (key, value) pairs, as 2-tuples
##
##
##iteritems:
##D.iteritems() -> an iterator over the (key, value) items of D
##
##
##iterkeys:
##D.iterkeys() -> an iterator over the keys of D
##
##
##itervalues:
##D.itervalues() -> an iterator over the values of D
##
##
##keys:
##D.keys() -> list of D's keys
##
##
##popitem:
##D.popitem() -> (k, v), remove and return some (key, value) pair as a
##2-tuple; but raise KeyError if D is empty
##
##
##setdefault:
##D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if not D.has_key(k)
##
##
##update:
##D.update(E) -> None.  Update D from E: for k in E.keys(): D[k] = E[k]
##
##
##values:
##D.values() -> list of D's values

