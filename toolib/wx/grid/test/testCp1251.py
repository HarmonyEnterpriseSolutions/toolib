import wx
from toolib.wx.TestApp import TestApp
from toolib.wx.grid.Grid  import Grid
from toolib.wx.grid.table.List2dTable import List2dTable

class MyGrid(Grid):
	pass

def test():

	def oninit(self):
		self.grid = MyGrid(self, -1)
		self.grid.SetTable(List2dTable())
		self.grid.AppendRows(16)
		self.grid.AppendCols(16)

		for i in xrange(256):
			self.grid.GetTable().SetValue(i/16, i % 16, chr(i))#"0x%02X: %s" % (i, chr(i)))

		for i in xrange(16):
			self.grid.SetColSize(i, 20)

	def ondestroy(self):
		pass

	TestApp(oninit, ondestroy).MainLoop()

if __name__ == '__main__':
	test()
