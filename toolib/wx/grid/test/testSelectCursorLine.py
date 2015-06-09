import wx
from toolib.wx.TestApp import TestApp
from toolib.wx.grid.Grid  import Grid
from toolib.wx.grid.table.List2dTable import List2dTable
from toolib.wx.grid.XSelectCursorLine import XSelectCursorLine

class MyGrid(XSelectCursorLine, Grid):

	def __init__(self, *args, **kwargs):
		super(MyGrid, self).__init__(*args, **kwargs)
		self.SetSelectionMode(Grid.wxGridSelectRows)


if __name__ == '__main__':

	g = None

	def oninit(self):
		self.grid = MyGrid(self, -1)
		self.grid.SetTable(List2dTable())
		self.grid.AppendRows(4)
		self.grid.AppendCols(4)

	def ondestroy(self):
		pass

	TestApp(oninit, ondestroy).MainLoop()
