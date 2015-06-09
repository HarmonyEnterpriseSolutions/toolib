class Link(object):

	def __init__(self, activityFrom, activityTo, name="", lag=0):

		#if predecessor in self._linksFrom:
		#	raise ValueError, "Link already exists"

		assert activityFrom is not None
		assert activityTo   is not None

		assert activityFrom is not activityTo

		self.__activityFrom = activityFrom
		self.__activityTo   = activityTo
		self.__name = name or ''
		self.__lag  = lag  or 0

		self.__activityTo._linksTo[self.__activityFrom] = self
		self.__activityFrom._linksFrom[self.__activityTo]   = self
		self.__activityTo._updateStart()
		self.__activityFrom._model.listeners.fireEvent(self, 'objectCreated')


	def getActivityFrom(self):
		return self.__activityFrom

	def getActivityTo(self):
		return self.__activityTo

	def remove(self):
		#rint "-----------------"
		#rint self
		#rint self.__activityFrom, self.__activityFrom._linksFrom
		#rint self.__activityTo, self.__activityTo._linksTo
		del self.__activityFrom._linksFrom[self.__activityTo]
		del self.__activityTo._linksTo[self.__activityFrom]
		self.__activityFrom._model.listeners.fireEvent(self, 'objectRemoved')
		self.__activityTo._updateStart()

	def _setStart(self, start):
		self.__activityTo._setStart(start + self.__lag)

	def setLag(self, lag):
		assert lag is not None
		if self.__lag != lag:
			oldValue = self.__lag
			self.__lag = lag
			self.__activityTo._setStart(start + self.__lag)
			#self.__activityFrom._model.listeners.firePropertyChanged(self, 'lag', lag, oldValue)
			
	def getEnd(self):
		return self.__activityFrom.getEnd() + self.__lag
	
	def __repr__(self):
		return "<Link from %s to %s>" % (self.__activityFrom.getRow(), self.__activityTo.getRow())


if __name__ == '__main__':
	from test import test
	test()
