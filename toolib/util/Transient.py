#################################################################
# Program:   toolib
"""
Base class for all classes, that uses __transient__ attribute
usage:

	class MyClass(MyParents, Transient):
		__transient__ = ('d', 'e')
		...

and attributes d, e will be pickled with None value
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2014/12/24 13:36:42 $"
__version__ = "$Revision: 1.2 $"
# $Source: C:/HOME/cvs/toolib/util/Transient.py,v $
#																#
#################################################################
from types import ClassType
from copy import copy
from toolib.debug import *

VERBOSE=0

def _setTransientsToNone(stuff, klass):
	##print "__setTransientsToNone in", klass.__name__
	if hasattr(klass, '__transient__') and klass.__transient__:
		for name in klass.__transient__:
			##print "deal with", name
			if name.startswith('__'):
				name = '_%s%s' % (klass.__name__, name,)
			if stuff.has_key(name):
				stuff[name] = None
			else:
				warning('No transient member "%s" in __dict__ for class %s' % (name, klass.__name__))

	if hasattr(klass, '__bases__'):
		for base in klass.__bases__:
			_setTransientsToNone(stuff, base)


class Transient(object):
	def __getstate__(self):
		stuff = copy(self.__dict__)
		_setTransientsToNone(stuff, self.__class__)
		return stuff

if __name__ == '__main__':
	print "\n>>> START ---------------------------------"
	class cap(Transient):
		__transient__ = ('pd', 'pe', '__private')
		def __init__(self):
			self.pa = "aaa"
			self.pb = "bbb"
			self.pc = "ccc"
			self.pd = "ddd"
			self.pe = "eee"
			self.__private = "cap private"

	class ca(cap):
		__transient__ = ('d', 'e', 'f', 'g')
		def __init__(self):
			cap.__init__(self)
			self.a = "aaa"
			self.b = "bbb"
			self.c = "ccc"
			self.d = "ddd"
			self.e = "eee"
			self.__private = "ca private member"

	capp = cap()
	o = ca()
	print o.__dict__
	import pickle
	s = pickle.dumps(o)
	o2 = pickle.loads(s)
	print o2.__dict__


## Old version, not deals with base classes
##class Transient:
##  def __getstate__(self):
##		stuff = self.__dict__
##		try:
##			transient = self.__class__.__transient__
##			if transient:
##				stuff = {}
##				prefix = "_%s__" % self.__class__.__name__
##				prefix_len = len(prefix) - 2
##				for attr in self.__dict__.keys():
##					# remove __ClassName_ before private fields for comparation
##					if attr.startswith(prefix):
##						attr_name = attr[ prefix_len : ]
##					else:
##						attr_name = attr
##
##					if transient.__contains__(attr_name):
##						stuff[attr] = None
##					else:
##						stuff[attr] = self.__dict__[attr]
##		except AttributeError:		# no __transient__ field in class
##			pass
##		if VERBOSE:
##			print "Transient: class=%s, state=%s" % (self.__class__, stuff)
##		return stuff

