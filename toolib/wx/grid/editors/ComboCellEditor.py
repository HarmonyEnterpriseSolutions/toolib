"""
DEPRECATED
Use ObjectChoiceCellEditor
TODO: Make ChoiceCellEditor to use instead this
"""
import wx
import wx.combo
from AbstractCellEditor	import AbstractCellEditor
from toolib				import debug

class ComboCellEditor(AbstractCellEditor):
	def __init__(self):
		AbstractCellEditor.__init__(self)

	def createControl(self, parent, id):
		return wx.ComboBox(parent, id, style = wx.CB_DROPDOWN | wx.CB_READONLY)
		#return wx.combo.ComboCtrl(parent, id, style = wx.CB_DROPDOWN)

	def getValues(self, grid, row, col):
		""" override to return enum values """
		return ("One","Two","Three")

	def setControlValue(self, value):
		"""
		called in BeginEdit, after startEdit
		start value passed
		mission is init control with start value
		"""
		self.GetControl().SetValue(value or "")

	def startEdit(self, grid, row, col):
		self.GetControl().Clear()
		values = self.getValues(grid, row, col)
		for v in values:
			self.GetControl().Append(v)
		#
		#value = self.getValueAsText(grid, row, col)
		#try:
		#	debug.trace("set initial value: %s" % value)
		#	self.GetControl().SetValue(value)
		#except:
		#	debug.error("invalid enum value: '%s'. Setting first one." % value)
		#	if len(values) > 0:
		#		self.GetControl().SetValue(values[0])
		#return value
		return grid.GetTable().GetValue(row, col)
	
	def stopEdit(self, grid, row, col):
		"""
		get control value and set to grid
		"""
		value = self.GetControl().GetValue()
		if value != self.getStartValue():
			grid.GetTable().SetValue(row, col, value)
			return True
		return False

	def cleanControl(self):
		self.GetControl().Clear()
