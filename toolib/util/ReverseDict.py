###############################################################################
# Program:   Toolib
"""
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2009/05/14 15:20:54 $"
__version__ = "$Revision: 1.3 $"
# $Source: D:/HOME/cvs/toolib/util/ReverseDict.py,v $
###############################################################################
class ReverseDict(dict):
	"""
	Like dictionary but have .reverse member, the instance of reverse dictionary

	{values : keys}

	.revers dictionary is ReversDict instanse itself and automatically holds changes of pair.

	So system is pretty symmetric

	Note:
		pop, popitem is not supported yet

	"""

	def __init__(self, values=None, __reverse__=None):
		if values:
			dict.__init__(self, values)
		else:
			dict.__init__(self)

		if __reverse__ is not None:
			self.reverse = __reverse__
		else:
			self.reverse = ReverseDict(__reverse__=self)

	def update(self, d):
		dict.update(self, d)
		for k, v in d.iteritems():
			dict.__setitem__(self.reverse, v, k)

	def clear(self):
		dict.clear(self)
		dict.clear(self.reverse)

	def __delitem__(self, key):
		try:
			dict.__delitem__(self.reverse, self[key])
		except KeyError:
			pass
		dict.__delitem__(self, key)

	def __setitem__(self, key, value):
		try:
			dict.__delitem__(self.reverse, self[key])
		except KeyError:
			pass
		dict.__setitem__(self, key, value)
		dict.__setitem__(self.reverse, value, key)
	
	def __str__(self):
		return "%s, %s" % (dict.__str__(self), dict.__str__(self.reverse))

	def copy(self):
		d = ReverseDict()
		d.update(self)
		return d

	def setdefault(self, k, d=None):
		if self.has_key(k):
			return self[k]
		else:
			self[k]=d
			return d

	def pop(self, *p, **pp):
		raise NotImplementedError

	def popitem(self, *p, **pp):
		raise NotImplementedError
			

if __name__ == '__main__':
	d = ReverseDict({0 : "000"})

	d[1] = "A"
	d[1] = "AA"
	d.update({2:"B", 3:"C"})
	d.reverse['E'] = 5

	del d.reverse['E']

	print d.setdefault(4, "D")
	print d

	assert id(d) == id(d.reverse.reverse)

