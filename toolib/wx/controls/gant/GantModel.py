from toolib.event.ListenerList import ListenerList
from Activity import Activity


class GantModel(object):
	
	def __init__(self, scaleFactor=1):
		self._activities = []
		self.listeners = ListenerList()
		self.__scaleFactor = scaleFactor

	def getScaleFactor(self):
		return self.__scaleFactor

	def setScaleFactor(self):
		if scaleFactor != self.__scaleFactor:
			oldValue = self.__scaleFactor
			self.__scaleFactor = scaleFactor
			self.listeners.firePropertyChanged(self, 'scaleFactor', scaleFactor, oldValue)

	def addActivity(self, *args, **kwargs):
		return Activity(self, *args, **kwargs)

	#def _moveActivity(self, index, deltaIndex):
	#	"""
	#	Moves activity at index down or up depending on deltaIndex
	#	actually changes this activity in places with another
	#	"""
	#	index2 = min(max(0, index + deltaIndex), len(self._activities) - 1)
	#
	#	if index != index2:
	#		affectedActivities = [self._activities[i] for i in xrange(min(index, index2), max(index, index2)+1)]
	#		oldIndex = [a.getRow() for a in affectedActivities]
	#	
	#		a  = self._activities[index]
	#		del self._activities[index]
	#		self._activities.insert(index2, a)
	#
	#		for i, a in enumerate(affectedActivities):
	#			self.listeners.firePropertyChanged(a, 'index', a.getRow(), oldIndex[i])
	# 
	#	return index2 - index

	def __iter__(self):
		return iter(self._activities)

	def __getitem__(self, index):
		return self._activities[index]

	def __len__(self):
		return len(self._activities)

	def _getFreeRow(self):
		rows = [a.getRow() for a in self._activities]
		freeRows = list(set(xrange(0, (max(rows) if rows else 0) + 2)).difference(rows))
		freeRows.sort()
		return freeRows[0]


if __name__ == '__main__':
	from test import test
	test()
