import wx
from AbstractCellEditor					import AbstractCellEditor
from toolib								import debug
from toolib.wx.controls.ObjectChoice	import ObjectChoice

class ObjectChoiceCellEditor(AbstractCellEditor):
	def __init__(self, choices=None, strfunc=None, setfunc=None):
		"""
		choices is static choices
		strfunc is string representator for choice
		setfunc is value converter to set
		also GridTable can define getChoices(self, row, col) method
		"""
		AbstractCellEditor.__init__(self)
		self._choices = choices
		self._strfunc = strfunc or str
		self._setfunc = setfunc or (lambda x: x)

	def createControl(self, parent, id):
		return ObjectChoice(parent, id, strfunc=self._strfunc)

	def startEdit(self, grid, row, col):
		self.GetControl().Clear()
		if self._choices:
			self.GetControl().Set(self._choices)
		elif hasattr(grid.GetTable(), 'getChoices'):
			self.GetControl().Set(grid.GetTable().getChoices(row, col))
		return grid.GetTable().GetValue(row, col)

	def setControlValue(self, value):
		"""
		value is id
		"""
		#rint "setControlValue", value, type(value)
		try:
			self.GetControl().setSelectedObject(value)
		except:
			if len(self.GetControl()) > 0:
				self.GetControl().SetSelection(0)

	
	def stopEdit(self, grid, row, col):
		"""
		get control value and set to grid
		"""
		value = self.GetControl().getSelectedObject()
		if value != self.getStartValue():
			grid.GetTable().SetValue(row, col, self._setfunc(value))
			return True
		return False

	def cleanControl(self):
		self.GetControl().clear()
