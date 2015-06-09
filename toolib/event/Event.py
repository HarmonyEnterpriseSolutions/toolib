###############################################################################
# Program:	toolib.event
'''
'''
__author__  = "Oleg Noga"
__date__	= "$Date: 2010/03/03 15:05:36 $"
__version__ = "$Revision: 1.10 $"
# $Source: D:/HOME/cvs/toolib/event/Event.py,v $
###############################################################################

import toolib.debug as debug

from EventVetoException import EventVetoException

def capitalize(s):
	return ''.join((s[0].upper(), s[1:]))

class Event(object):
	def __init__(self, source, name, **args):
		self.source = source
		self._init(name, **args)

	def _init(self, name=None, **args):
		if name is not None: 
			self.name = name
		self.__args = args
		return self

	def _send(self, listeners):
		errors = []
		if listeners:						# if any listener registered
			m = self.getMethodName()
			for listener in tuple(listeners):
				if hasattr(listener, m):
					try:
						getattr(listener, m)(self)
					except EventVetoException, e:
						errors.append(e)
				else:
					assert debug.trace("Listener %s has no method: %s" % (listener, m))

		for error in errors:
			raise error.getNestedException()
			

	def __getattr__(self, key):
		try:
			return self.__args[key]
		except KeyError:
			raise AttributeError, key

	def getSource(self):
		"""Returns event source"""
		return self.source

	def setName(self, name):
		self.name = name

	def getName(self):
		"""Returns event name"""
		return self.name

	def getMethodName(self):
		return 'on' + self.name[0].upper() + self.name[1:]

	def raiseVeto(self, nestedException = None):
		''' 
		Raises veto exception
		'''
		raise EventVetoException(self, nestedException)

	def __str__(self):
		args = self.__args.items()
		args.sort()
		args = map(lambda item: "%s=%s" % (item[0], repr(item[1])), args)
		args.insert(0, " '%s' src=%s" % (self.name, repr(self.source)))
		return "<%s%s>" % (self.__class__.__name__, ','.join(args))
