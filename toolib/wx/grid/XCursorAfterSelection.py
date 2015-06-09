import wx
import wx.grid
from toolib import debug
from TSelection import TSelection

class XCursorAfterSelection(TSelection):
	"""
	moves cursor after selection
	includes TSelection
	modifies TSelection behaviour to treat GridCursor like selected cell
	"""

	def __init__(self, *args, **kwargs):
		super(XCursorAfterSelection, self).__init__(*args, **kwargs)
		self.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.__onGridRangeSelect, self)

	def __onGridRangeSelect(self, event):

		if event.Selecting():
			trow, tcol = event.GetTopLeftCoords()
			brow, bcol = event.GetBottomRightCoords()

			# must call it later because GetGridCursorRow, GetGridCursorCol incorrect now
			# and SetGridCursor called when it must not to be called
			def f():
				oldrow = row = self.GetGridCursorRow()
				oldcol = col = self.GetGridCursorCol()

				if row < trow: row = trow
				if row > brow: row = brow
				if col < tcol: col = tcol
				if col > bcol: col = bcol
		    
				if row != oldrow or col != oldcol:
					try:
						self.SetGridCursor(row, col)
					except wx.PyDeadObjectError:
						pass

			wx.CallAfter(f)

		event.Skip()

	#def getRowSelection(self):
	#	"""
	#	returns list of selected rows and set of selected cells not in rows
	#	"""
	#	sel = super(XCursorAfterSelection, self).getRowSelection()
	#	self.__updateSelectionWithGridCursor(sel)
	#	return sel
	#
	#def getColSelection(self):
	#	"""
	#	returns list of selected cols and set of selected cells not in cols
	#	"""
	#	sel = super(XCursorAfterSelection, self).getColSelection()
	#	self.__updateSelectionWithGridCursor(sel)
	#	return sel
	#
	#def getCellSelection(self):
	#	"""
	#	returns set of selected cells
	#	"""
	#	sel = super(XCursorAfterSelection, self).getCellSelection()
	#	self.__updateSelectionWithGridCursor(sel)
	#	return sel
	# 
	#def __updateSelectionWithGridCursor(self, sel):
	#	# grid cursor is selection
	#	row = self.GetGridCursorRow()
	#	col = self.GetGridCursorCol()
	#	if row >= 0 and col >= 0:
	#		sel._addCell((row, col))
