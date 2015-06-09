from toolib.event.ListenerList import ListenerList

class XEditing(object):
	"""
	Adds methods getCellEditor, isEditing
	Editor must fire event editingChanged to editingListeners
	see editors.AbstractCellEditor
	"""

	def __init__(self, *args, **kwargs):
		super(XEditing, self).__init__(*args, **kwargs)

		self.__cellEditor = None
		self.editingListeners = ListenerList()
		self.editingListeners.bind('editingChanged', self.__onEditingChanged)

	def __onEditingChanged(self, event):
		self.__cellEditor = event.getSource() if event.editing else None

	def isEditing(self):
		return self.__cellEditor != None

	def getCellEditor(self):
		"""
		returns currently active cell editor or None if not currently editing
		"""
		return self.__cellEditor