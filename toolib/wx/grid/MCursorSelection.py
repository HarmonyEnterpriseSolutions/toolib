import wx
import wx.grid
from toolib import debug

class MCursorSelection(object):
	"""
	makes cursor allways selected
	"""

	def __init__(self):
		self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.__onGridSelectCell, self)

	def __onGridSelectCell(self, event):
		self.makeCursorSelection(event.GetRow(), event.GetCol())
		event.Skip()

	def makeCursorSelection(self, row=None, col=None):

		if row is None: row = self.GetGridCursorRow()
		if col is None: col = self.GetGridCursorCol()

		#rint "makeCursorSelection(%s, %s)" % (row, col)

		if self.GetSelectionMode() == self.wxGridSelectCells:
			if row >= 0 and col >= 0:
				self.SelectBlock(row, col, row, col)
			else:
				debug.warning("Can't select cell (%s, %s)" % (row, col))

		elif self.GetSelectionMode() == self.wxGridSelectRows:
			if row >= 0:
				self.SelectRow(row)
			else:
				debug.warning("Can't select row %s" % (row,))

		elif self.GetSelectionMode() == self.wxGridSelectColumns:
			if col >= 0:
				self.SelectCol(col)
			else:
				debug.warning("Can't select col %s" % (col,))
		