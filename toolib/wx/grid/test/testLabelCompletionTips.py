import wx
from toolib.wx.TestApp import TestApp
from toolib.wx.grid.Grid  import Grid
from toolib.wx.grid.table.List2dTable import List2dTable
from toolib.wx.grid.MLabelCompletionTips import MLabelCompletionTips

class MyGrid(Grid, MLabelCompletionTips):

	def __init__(self, *args, **kwargs):
		Grid.__init__(self, *args, **kwargs)
		MLabelCompletionTips.__init__(self, True, True)
		


if __name__ == '__main__':

	def oninit(self):
		g = MyGrid(self, -1)
		g.SetTable(List2dTable())
		g.AppendRows(4)
		g.AppendCols(4)

	TestApp(oninit).MainLoop()
