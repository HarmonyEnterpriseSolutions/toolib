import wx
from toolib.wx.TestApp import TestApp
from toolib.wx.grid.Grid  import Grid
from toolib.wx.grid.table.List2dTable import List2dTable
from toolib.wx.grid.MCursorSelection import MCursorSelection

class MyGrid(Grid, MCursorSelection):

	def __init__(self, *args, **kwargs):
		Grid.__init__(self, *args, **kwargs)
		MCursorSelection.__init__(self)


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
