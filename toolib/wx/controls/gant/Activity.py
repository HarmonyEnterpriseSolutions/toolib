from Link import Link

class Activity(object):

	def __init__(self, model, duration = 1, name='', row=None, startMin=0):

		self._model = model
		
		self.__row      = row if row is not None else self._model._getFreeRow()
		self.__duration = duration or 1
		self.__name     = name     or ''
		self.__startMin = startMin or 0

		self._linksFrom = {}
		self._linksTo = {}

		self.__start = startMin

		self.__selected = False

		self._model._activities.append(self)

		self._model.listeners.fireEvent(self, 'objectCreated')


	def addPredecessor(self, predecessor, linkName="", lag=0):
		"""
		add predecessor activity
		"""
		link = Link(predecessor, self, linkName, lag)
		
	def getLinkFrom(activity):
		return self._linksFrom[activity]

	def getLinkTo(self, activity):
		return self._linksTo[activity]

	def getLinksFrom(self):
		return self._linksFrom.values()

	def getLinksTo(self):
		return self._linksTo.values()

	def setDuration(self, duration):
		assert duration is not None
		if duration != self.__duration:
			oldValue = self.__duration
			self.__duration = duration
			self._fireEndChanged()
			self._model.listeners.firePropertyChanged(self, 'duration', duration, oldValue)

	def setName(self, name):
		assert name is not None
		if name != self.__name:
			oldValue = self.__name
			self.__name = name
			self._model.listeners.firePropertyChanged(self, 'name', name, oldValue)

	def _setStart(self, start):
		assert start is not None
		#rint "SET START", repr(self), start, self.__start
		if start != self.__start:
			oldValue = self.__start
			self.__start = max(start, self.__startMin)
			self._fireEndChanged()
			self._model.listeners.firePropertyChanged(self, 'start', start, oldValue)

	def setStartMin(self, startMin):
		assert startMin is not None
		if startMin != self.__startMin:
			self.__startMin = startMin
			self._setStart(max(self.__start, self.__startMin))

	def setRow(self, row):
		assert row is not None
		if row != self.__row:
			oldValue = self.__row
			self.__row = row
			self._model.listeners.firePropertyChanged(self, 'row', row, oldValue)
	
	def _fireEndChanged(self):
		for link in self._linksFrom.itervalues():
			#link._setStart(self.__start + self.__duration)
			link.getActivityTo()._updateStart()

	def getRow(self):		return self.__row
	def getDuration(self):	return self.__duration
	def getName(self):		return self.__name
	def getStartMin(self):	return self.__startMin

	def getStart(self):		return self.__start
	def getEnd(self):		return self.__start + self.__duration

	def _updateStart(self):
		#rint "+ update start of", self
		#rint "+ incoming links:", self._linksTo.values()
		#rint "+ out links:", self._linksFrom.values()
		self._setStart(max([self.__startMin] + [link.getEnd() for link in self._linksTo.itervalues()]))
			
	def remove(self):
		for link in self.getLinksTo():
			link.remove()
		for link in self.getLinksFrom():
			link.remove()
		self._model.listeners.fireEvent(self, 'objectRemoved')
		self._model._activities.remove(self)

	def move(self, deltaIndex):
		self._model._moveActivity(self.getRow(), deltaIndex)

	def __repr__(self):
		return "<Activity %s>" % self.getRow()

	def setSelected(self, selected):
		if selected != self.__selected:
			
			if selected:
				# deselect all activities before
				for activity in self._model._activities:
					activity.setSelected(False)

			oldValue = self.__selected
			self.__selected = selected
			self._model.listeners.firePropertyChanged(self, 'selected', selected, oldValue)

	def isSelected(self):
		return self.__selected


if __name__ == '__main__':
	from test import test
	test()
