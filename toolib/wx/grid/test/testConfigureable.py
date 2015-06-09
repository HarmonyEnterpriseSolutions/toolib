import wx
from toolib.wx.TestApp import TestApp
from toolib.wx.grid.Grid  import Grid
from toolib.wx.grid.table.List2dTable import List2dTable
from toolib.wx.grid.TConfigurable import TConfigurable

class MyGrid(Grid, TConfigurable):

	def __init__(self, *args, **kwargs):
		Grid.__init__(self, *args, **kwargs)

	def getProjectPath(self):
		return '.'
		
	def getDomain(self):
		return 'TestConfigurableGrid'


if __name__ == '__main__':

	g = None

	def oninit(self):
		self.grid = MyGrid(self, -1)
		self.grid.SetTable(List2dTable())
		self.grid.AppendRows(4)
		self.grid.AppendCols(4)

		self.grid.applyConfig()

	def ondestroy(self):
		self.grid.saveConfig()

	TestApp(oninit, ondestroy).MainLoop()
