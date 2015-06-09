
class ColumnStateObject(object):

	def __init__(self):
		self.width = None


class MColumnState(object):
	"""
	Requires:
		tableListeners
		GetTable().getColumnId

	"""

	
	def __init__(self):
		self.__columnState = {}
		self.modelListeners.add(self.ModelListener)

	def __getColumnState(self, index):
		id = self.GetTable().getColumnId(index)
		state = self.__columnState.get(id)
		if not state:
			state = self.__columnState[id] = ColumnStateObject()
		return state

	def saveColumnState(self):
		for i in xrange(self.GetNumberCols()):
			try:
				self.__getColumnState(i).width = self.GetColSize(i)
			except IndexError:
				pass

	def restoreColumnState(self):
		for i in xrange(self.GetNumberCols()):
			try:
				w = self.__getColumnState(i).width
			except IndexError:
				pass
			else:
				if w is not None:
					self.SetColSize(i, w)

	class ModelListener(object):

		@staticmethod
		def onModelChanging(event):
			event.getSource().saveColumnState()

		@staticmethod
		def onModelChanged(event):
			event.getSource().restoreColumnState()
	