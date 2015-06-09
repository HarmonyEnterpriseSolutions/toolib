import wx
from toolib.wx.TestApp import TestApp
from toolib.wx.grid.Grid  import Grid
from toolib.wx.grid.table.List2dTable import List2dTable
from toolib.wx.grid.MFindReplace import MFindReplace 

class MyGrid(Grid, MFindReplace):

	def __init__(self, *args, **kwargs):
		Grid.__init__(self, *args, **kwargs)
		MFindReplace.__init__(self, self.getValueAsText)

	def getValueAsText(self, row, col):
		return str(self.GetTable().GetValue(row, col))

def test():

	def oninit(self):
		self.grid = MyGrid(self, -1)
		self.grid.SetTable(List2dTable())
		self.grid.AppendRows(4)
		self.grid.AppendCols(4)

	def ontimer(self):
		self.grid.find()

	def ondestroy(self):
		pass

	TestApp(oninit, ondestroy, ontimer=ontimer).MainLoop()

if __name__ == '__main__':
	test()
