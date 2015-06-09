import wx
from toolib.wx.TestApp import TestApp
from toolib.wx.grid.Grid  import Grid
from toolib.wx.grid.table.List2dTable import List2dTable
from toolib.wx.grid.MColumnSizer import MColumnSizer_oneGrows

class MyGrid(Grid, MColumnSizer_oneGrows):

	def __init__(self, *args, **kwargs):
		Grid.__init__(self, *args, **kwargs)
		MColumnSizer_oneGrows.__init__(self, 1)


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
