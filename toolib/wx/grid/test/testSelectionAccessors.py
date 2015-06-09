import wx
from toolib.wx.TestApp import TestApp
from toolib.wx.grid.Grid  import Grid
from toolib.wx.grid.table.List2dTable import List2dTable

from toolib.wx.grid.XCursorAfterSelection import XCursorAfterSelection

class MyGrid(XCursorAfterSelection, Grid):

	def __init__(self, *args, **kwargs):
		super(MyGrid, self).__init__(*args, **kwargs)
		self.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.OnGridRangeSelect, self)
		self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.OnGridSelectCell, self)
		#self.SetSelectionMode(self.wxGridSelectRows)
		
	def	OnGridRangeSelect(self, event):
		def f():

			print "----------------------------------------------------------------------"
			print "X cells:", self.GetSelectedCells()
			print "X rows: ", self.GetSelectedRows()
			print "X cols: ", self.GetSelectedCols()
			print "X blocks: ", self.GetSelectionBlockTopLeft(), self.GetSelectionBlockBottomRight()
			print
			print "rows: ", self.getRowSelection()
			print "cols: ", self.getColSelection()
			print "cells:", self.getCellSelection()

		wx.CallAfter(f)
		event.Skip()

	def	OnGridSelectCell(self, event):
		def f():
			print "----------------------------------------------------------------------"
			print "rows: ", self.getRowSelection()
			print "cols: ", self.getColSelection()
			print "cells:", self.getCellSelection()
		wx.CallAfter(f)
		event.Skip()

if __name__ == '__main__':

	def oninit(self):
			

		g = MyGrid(self, -1)


		g.SetTable(List2dTable())

		g.AppendRows(4)
		g.AppendCols(4)

		#g.SetSelectionMode(g.wxGridSelectCells)
		#g.SetSelectionMode(g.wxGridSelectRows)
		#g.SetSelectionMode(g.wxGridSelectColumns)

	TestApp(oninit).MainLoop()
