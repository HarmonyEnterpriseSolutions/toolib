import wx
from toolib.wx.TestApp import TestApp
from toolib.wx.grid.Grid  import Grid
from toolib.wx.grid.table.List2dTable import List2dTable
from toolib.wx.grid.XTips import XTips

class MyGrid(XTips, Grid):

	def getTipValue(self, row, col):
		return "A tip for %s, %s" % (self.GetRowLabelValue(row), self.GetColLabelValue(col))
	

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
