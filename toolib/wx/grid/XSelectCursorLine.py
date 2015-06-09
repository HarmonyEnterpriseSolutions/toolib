import wx.grid
from wx.grid import Grid

class XSelectCursorLine(object):

	"""
	affects rows and columns selection mode
	select whole row or column if cell selected

	BUG: when controll pressed can't select multiple rows, event.ControlDown() allways return false
	"""

	def __init__(self, *args, **kwargs):
		super(XSelectCursorLine, self).__init__(*args, **kwargs)
		self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.__on_select_cell, self)	# select whole row/col on cursor move

	def __on_select_cell(self, event):
		if self.GetSelectionMode() == Grid.wxGridSelectRows:
			self.SelectRow(event.GetRow())
		if self.GetSelectionMode() == Grid.wxGridSelectColumns:
			self.SelectCol(event.GetCol())
		event.Skip()
