from Event import Event

class ListenerList(object):
	"""
	use add, remove for java like listeners
	use bind, unbind for method binding
	"""

	def __init__(self, listeners=()):
		self.__listeners = list(listeners)
		self.__bindings = {}

	def __iter__(self):
		return iter(self.__listeners)

	def add(self, listener):
		"""
		add java like listener, will call method onEventName
		"""
		self.__listeners.append(listener)
		
	def remove(self, listener):
		try:
			self.__listeners.remove(listener)
		except ValueError:
			pass

	def bind(self, eventName, method):
		"""
		wxPython like binding
		bind private method to eventName
		"""
		self.__bindings.setdefault(eventName, []).append(method)

	def unbind(self, eventName, method):
		try:
			self.__bindings.get(eventName, []).remove(method)
		except ValueError:
			pass

	def fire(self, event):

		for method in tuple(self.__bindings.get(event.getName(), ())):
			method(event)

		event._send(self)

	def fireEvent(self, source, name, **args):
		self.fire(Event(source, name, **args))

	def firePropertyChanging(self, source, propertyName, value, oldValue):
		self.fire(Event(
			source,
			'propertyChanging',
			propertyName	= propertyName,
			value			= value,
			oldValue		= oldValue,
		))

	def firePropertyChanged(self, source, propertyName, value, oldValue):
		self.fire(Event(
			source,
			'propertyChanged',
			propertyName	= propertyName,
			value			= value,
			oldValue		= oldValue,
		))
