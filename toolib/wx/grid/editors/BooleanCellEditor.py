import wx

from AbstractCellEditor import AbstractCellEditor

class BooleanCellEditor(AbstractCellEditor):
	def __init__(self, choices=None, strfunc=None, setfunc=None):
		AbstractCellEditor.__init__(self)

	def createControl(self, parent, id):
		return wx.CheckBox(parent, id)

	def startEdit(self, grid, row, col):
		#rint "startEditor", grid.GetTable().GetValue(row, col)
		return not grid.GetTable().GetValue(row, col)

	def setControlValue(self, value):
		"""
		value is id
		"""
		self.GetControl().SetValue(bool(value))

	def stopEdit(self, grid, row, col):
		"""
		get control value and set to grid
		"""
		value = self.GetControl().GetValue()
		#rint "stopEdit", value
		grid.GetTable().SetValue(row, col, bool(value))
		return True

	def SetSize(self, rect):
		"""
		Called to position/size the edit control within the cell rectangle.
		If you don't fill the cell (the rect) then be sure to override
		PaintBackground and do something meaningful there.
		"""
		w, h = self.GetControl().Size
		self.GetControl().SetDimensions(rect.x + (rect.width - w)/2 + 2, rect.y + (rect.height-h)/2 + 2, w, h)
