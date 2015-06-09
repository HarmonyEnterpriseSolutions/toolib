import toolib.debug as debug

from Event 				import Event 
from EventVetoException	import EventVetoException

class EventDispatcher:
	def __init__(self):
		self._listenerDict = {}
		
	def registerListener(self, listenerClass, listener, index=None, forceAdd=0):
		assert debug.trace("%s, class=%s" % (listener.__class__, listenerClass))
		listenerList = self._listenerDict.get(listenerClass)
		if listenerList is None:
			listenerList = []
			self._listenerDict[listenerClass] = listenerList

		if forceAdd or listener not in listenerList:
			if index is None:
				listenerList.append(listener)
			else:
				listenerList.insert(index, listener)
		else:
			debug.warning('Listener <%s> in EventDispatcher already exisit' % listener, 1)

	def unregisterListener(self, listenerClass, listener):
		listeners = self._listenerDict.get(listenerClass)
		if listeners is not None:
			try:
				listeners.remove(listener)
			except ValueError:
				debug.warning('No listener <%s> in EventDispatcher' % listener, 1)

	def fireEvent(self, listenerClass, event):
		listeners = self._listenerDict.get(listenerClass)
		if listeners is not None:
			method = event.getMethodName()
			for listener in listeners:
				if isinstance(listener, EventDispatcher):
					listener.processEvent(event)
				elif hasattr(listener, method):
					getattr(listener, method)(event)

	def append(self, evDisp):
		if isinstance(evDisp, EventDispatcher):
			for listenerClass, listenerList in evDisp._listenerDict.items():
				for listener in listenerList:
					self.registerListener(listenerClass, listener)
		else:
			raise TypeError('Can only append EventDispatcher (not "%s") to EventDispatcher' %type(evDisp).__name__)

	def processEvent(self, event):
		pass

	def __str__(self):
		res = []
		for listenerClass, listeners in self._listenerDict.items():
			res1 = []
			for listener in listeners:
				res1.append('\t%s' %listener)
			res.append('%s: %s' %(listenerClass, '\t\n'.join(res1)))
		return '\n'.join(res)

	def countListeners(self, listenerClass):
		return len(self._listenerDict.get(listenerClass, ()))

