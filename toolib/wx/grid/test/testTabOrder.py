import wx
from toolib.wx.TestApp import TestApp
from toolib.wx.grid.Grid  import Grid
from toolib.wx.grid.table.List2dTable import List2dTable
from toolib.wx.grid.MTabOrder import MTabOrder_reading as MTabOrder

class MyGrid(Grid, MTabOrder):

	def __init__(self, *args, **kwargs):
		Grid.__init__(self, *args, **kwargs)
		MTabOrder.__init__(self)

def test():

	def oninit(self):
		self.grid = MyGrid(self, -1)
		self.grid.SetTable(List2dTable())
		self.grid.AppendRows(4)
		self.grid.AppendCols(4)

	def ondestroy(self):
		pass

	TestApp(oninit, ondestroy).MainLoop()

if __name__ == '__main__':
	test()
