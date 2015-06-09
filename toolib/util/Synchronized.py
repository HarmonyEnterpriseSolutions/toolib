#################################################################
# Program:   toolib
"""
Base class for all classes, that uses __synchronized__ attribute
usage:

	class MyClass(MyParents, Synchronized):
		__synchronized__ = ('addItem', 'removeItem')
		...

and methods 'addItem' and 'removeItem' will be synchronized (like a Java)
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2005/08/03 12:24:18 $"
__version__ = "$Revision: 1.1 $"
# $Source: D:/HOME/cvs/toolib/util/Synchronized.py,v $
#
#################################################################
from threading import currentThread

VERBOSE = 0

class CallHook:
	"""function hook"""
	def __init__(self, object, method):
		self.object = object
		self.method = method

	def __call__(self, *argTuple, **argDict):
		if self.object.ownerThread() != currentThread():	# allow secondary entry
			self.object.acquireInstance()
			acquired = 1
		else:
			acquired = 0
		self.object.__owner__ = None
		res = apply(self.method, (self.object,) + argTuple, argDict)
		if acquired:
			self.object.releaseInstance()
		return res

	def __str__(self):
		return "<synchronized function %s>" % (self.method.__name__,)


class Synchronized:
	def __init__(self):
		from threading import Semaphore
		self.__lock = Semaphore()
		self.__ownerThread = None
		classdict = self.__class__.__dict__
		for attr in classdict.get("__synchronized__", ()):
			try:
				method = classdict[attr]
				if callable(method):
					self.__dict__[attr] = CallHook(self, method)
				else:
					if VERBOSE: print "! Synchronized: Object is not callable: %s" % (attr,)
			except KeyError:
				if VERBOSE: print "! Synchronized: Method not found: %s" % (attr,)

	def releaseInstance(self):
		self.__ownerThread = None
		self.__lock.release()

	def acquireInstance(self):
		self.__lock.acquire()
		self.__ownerThread = currentThread()

	def ownerThread(self):
		return self.__ownerThread
