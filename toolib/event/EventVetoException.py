class EventVetoException(Exception):
	def __init__(self, event, nestedException=None):
		Exception.__init__(self)
		self._event = event
		self._nestedException = nestedException

	def getEvent(self):
		return self._event

	def getNestedException(self):
		return self._nestedException

	def __str__(self):
		return "%s. Nested exception: %s" % (self.__class__.__name__, self._nestedException)
