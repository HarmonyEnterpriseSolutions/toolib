###############################################################################
# Program:   Sula 0.7
'''
	Helper class for event fire. Supports toolib.event.Dispatcher-like events.
	Usage :
		## inherit it first
		SomeClassWhantsToFireEvents(EventSupport):
			def __init__(self):
				EventSupport.__init__(
					self,
					'eventClass',	 ## eventClass name for listeners
					dispatcher		 ## type:toolib.event.Dispatcher.Dispatcher()
				)
				self.name = 'askdjalskjd'
			## to fire events use fireEvent(eventName, **namedParams)
			## named params are included into event as attributes
			## fireEvent supports EventVetoException, so there is no need to catch
			## it, because user exception(by event listener) is thrown automatically.
			def doSmth(self):
				self.fireEvent('doSmth', name = self.name, flag = 3)
'''

__author__  = "Lesha Strashko, Oleg Noga"
__date__	= "$Date: 2006/11/22 17:58:17 $"
__version__ = "$Revision: 1.5 $"
# $Source: D:/HOME/cvs/toolib/event/EventSupport.py,v $
###############################################################################

import sys
from Event					import Event
from EventVetoException		import EventVetoException

class AbstractEventSupport:

	def getEventDispatcher(self):
		raise NotImplementedError, 'abstract'

	def getEventClass(self):
		raise NotImplementedError, 'abstract'

	def fireEvent(self, eventName, **params):
		"""
		Fires event with source=self
		named parameters will be passed into Event constructor
		excluding source parameter
		source named parameter still can override it
		"""
		#rint ">>> in fireEvent. EventClass=%s. Listeners: %s" % (self.getEventClass(), self.getEventDispatcher()._listenerDict)
		if params.has_key("source"):
			source = params["source"]
			del params["source"]
		else:
			source = self
		event = Event(source, eventName, **params)
		disp = self.getEventDispatcher()
		if disp is not None:
			try:
				disp.fireEvent(self.getEventClass(), event)
			except EventVetoException:
				ex_class, ex, tb = sys.exc_info()
				raise ex.getNestedException().__class__, ex.getNestedException(), tb
		# @Oleg why it returns event?	
		return event


class EventSupport(AbstractEventSupport):

	def __init__(self, eventClass, dispatcher = None):
		self._eventDispatcher = dispatcher
		self._eventClass = eventClass

	def getEventDispatcher(self):
		return self._eventDispatcher

	def setEventDispatcher(self, eventDispatcher):
		self._eventDispatcher = eventDispatcher

	def getEventClass(self):
		return self._eventClass

	def hasEventDispatcher(self):
		return self._eventDispatcher is not None

