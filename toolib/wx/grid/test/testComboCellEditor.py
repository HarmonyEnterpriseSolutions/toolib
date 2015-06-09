import wx
from toolib.wx.TestApp import TestApp
from toolib.wx.grid.Grid  import Grid
from toolib.wx.grid.table.List2dTable import List2dTable
from toolib.wx.grid.TSelection import TSelection
from toolib.wx.grid.editors.ComboCellEditor import ComboCellEditor


class MyTable(List2dTable):

	def __init__(self):
		List2dTable.__init__(self)
		
	def GetTypeName(self, row, col):
		return 'my_type'
		

class MyGrid(Grid):

	def __init__(self, *args, **kwargs):
		Grid.__init__(self, *args, **kwargs)

		self.RegisterDataType('my_type', self.GetDefaultRenderer(), ComboCellEditor())


def test():
	def oninit(self):
		
		self.grid = MyGrid(self, -1)
		self.grid.SetTable(MyTable())
		self.grid.AppendRows(10)
		self.grid.AppendCols(10)

		self.Size = (1000, 600)

	def ondestroy(self):
		pass

	def ontimer(self):
		pass

	TestApp(oninit, ondestroy, ontimer=ontimer).MainLoop()

if __name__ == '__main__':
	test()
