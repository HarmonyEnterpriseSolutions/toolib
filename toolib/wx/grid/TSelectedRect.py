import wx
from TSelection import TSelection, SelectionError
from toolib._ import *

class TSelectedRect(TSelection):	
	"""
	Requires:
		GetGridCursorCol
		GetGridCursorRow
		GetNumberCols
		GetNumberRows
		GetSelectedCells
		GetSelectedCols
		GetSelectedRows
		GetSelectionBlockBottomRight
		GetSelectionBlockTopLeft

	Provides:
		getSelectedRect

	"""
	

	def getSelectedRect(self):
		"""
		analyze if selected cells is rectangle range
		return wx.Rect if so
		works only in single selection mode

		if none selected, returns cursor rect if cursor valid
		"""
		cells = self.getCellSelection()
		if cells:
		
			row1, col1 = cells[ 0]
			row2, col2 = cells[-1]

			minrow = reduce(lambda value, cell: min(cell[0], value), cells, row1)
			mincol = reduce(lambda value, cell: min(cell[1], value), cells, col1)
			maxrow = reduce(lambda value, cell: max(cell[0], value), cells, row2)
			maxcol = reduce(lambda value, cell: max(cell[1], value), cells, col2)
		
			if (maxcol - mincol + 1) * (maxrow - minrow + 1) == len(cells):
				return wx.Rect(mincol, minrow, maxcol - mincol + 1, maxrow - minrow + 1)
			else:
				raise SelectionError, _('Rectangular selection expected')
		else:
			row = self.GetGridCursorRow()
			col = self.GetGridCursorCol()
			if row >= 0 and col >= 0:
				return wx.Rect(col, row, 1, 1)
