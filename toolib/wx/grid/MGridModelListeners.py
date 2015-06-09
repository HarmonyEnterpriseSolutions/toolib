from toolib.event.ListenerList	import ListenerList


class MGridModelListeners(object):

	def __init__(self):
		self.modelListeners = ListenerList()


	def SetTable(self, table, takeOwnership=False):
		"""
		Messaging
		"""
		oldTable = self.GetTable()
		self.modelListeners.fireEvent(self, 'modelChanging', model = table, oldModel = oldTable)
		super(MGridModelListeners, self).SetTable(table, takeOwnership)
		self.modelListeners.fireEvent(self, 'modelChanged',  model = table, oldModel = oldTable)
