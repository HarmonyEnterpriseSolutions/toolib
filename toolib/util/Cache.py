###############################################################################
# Program:   toolib
"""
	contains Cache, where values for keys in dict
	are loaded by external method
	method can be class bound or static function
	metod must accept at list key argument
"""
__author__  = "Lesha Strashko, Oleg Noga, Sergey Schetinin"
__date__	= "$Date: 2008/09/19 17:35:31 $"
__version__ = "$Revision: 1.8 $"
# $Source: D:/HOME/cvs/toolib/util/Cache.py,v $
###############################################################################

from weakref import WeakKeyDictionary

__all__ = [
	'Cache',
	'cached_method_nogc',
	'cached_method',
	'NotInCache',
]


class NotInCache(object): pass

def cached_method_nogc(m):
	"""
	fastest implementation of cache decorator, read-only cache

	Usage:

	class C:
		@Cache.decorator_nogc
		def getSomething(self, key1, key2, ...):
			return difficult_function(key, key2, ...)
	"""
	cache = {}
	def cached_m_nogc(*args):
		item = cache.get(args, NotInCache)
		if item is NotInCache:
			item = cache[args] = m(*args)
		return item
	return cached_m_nogc


def cached_method(m):
	"""
	cache decorator, read-only cache
	weak references instances
	use if cache holder instances can be destructed from memory

	see cached_method for usage

	TODO: have some problems with WeakKeyDictionary
	WeakKeyDictionary drops selfs actually used
	"""
	cache = WeakKeyDictionary()

	def flush(self):
		cache.pop(self, None)

	def cached_m(self, *args):
		self_cache = cache.get(self, NotInCache)
		if self_cache is NotInCache:
			self_cache = cache[self] = {}
		r = self_cache.get(args, NotInCache)
		if r is NotInCache:
			r = self_cache[args] = m(self, *args) 
		return r

	cached_m.flush = flush

	return cached_m


class Cache(dict):

	decorator_nogc = staticmethod(cached_method_nogc)
	decorator = staticmethod(cached_method)

	def __init__(self, loadMethod, saveMethod=None):
		dict.__init__(self)
		self._loadMethod = loadMethod
		self._saveMethod = saveMethod

	def __getitem__(self, key):
		item = dict.get(self, key, NotInCache)
		if item is NotInCache:
			item = self[key] = self._loadMethod(key)
		return item

	def put(self, key, value, *args, **kwargs):
		dict.__setitem__(self, key, value)
		if self._saveMethod is not None:
			self._saveMethod(key,  value, *args, **kwargs)

	__setitem__ = put

	flush = dict.clear


if __name__ == '__main__':
		
	def testSpeed(N=1000000):
		from timeit import Timer
				
		init = """\
from Cache import Cache


class A(object):

	def __init__(self):
		self._something = Cache(self._getSomething)

	def _getSomething(self, key):
		return "Something about '%s'" % key

	def getSomething(self, key):
		return self._something[key]

class B(object):

	@Cache.decorator_nogc
	def getSomething(self, key):
		return "Something about '%s'" % key

class C(object):

	@Cache.decorator
	def getSomething(self, key):
		return "Something about '%s'" % key

"""


		print "\ntoolib.util.Cache..."
		t1 = Timer("x.getSomething(0)", init + "\nx = A()").timeit(N)
		print t1

		print "\ntoolib.util.Cache with attribute access..."
		t2 = Timer("x._something[0]",   init + "\nx = A()").timeit(N)
		print t2

		print "\nCache.decorator_nogc..."
		t3 = Timer("x.getSomething(0)", init + "\nx = B()").timeit(N)
		print t3

		print "\nCache.decorator..."
		t4 = Timer("x.getSomething(0)", init + "\nx = C()").timeit(N)
		print t4

		print
		print "Cache getter is %s slover than Cache attribute access" % (t1/t2,)
		print "Cache.decorator_nogc is %s faster then Cache getter" % (t1/t3,)
		print "Cache.decorator is %s slover then Cache.decorator_nogc" % (t4/t3,)
		print "Cache.decorator is %s slover then Cache getter" % (t4/t1,)


	def testCache():
		print "------- Test Cache"

		def load(key):
			print ">> load: %s" % key
			return "value of %s" % key

		d = Cache(load)

		print d[1]
		print d[1]
		print d[2]


	def testCachedMethodFlush():
		print "------- Test Cache"

		class C(object):
			#@cached_method
			def load(self, key):
				return "value of %s" % key
			load = cached_method(load)

		c = C()
		print c.load(1)
		print c.load(2)
		print c.load(2)

		c.load.flush(c)

		print c.load(1)
		print c.load(2)
		print c.load(2)
	

	#testSpeed()
	#testCache()
	testCachedMethodFlush()

