import wx
from testGrid import TestGrid, TestApp
from toolib.wx.grid.XCursorAfterSelection import XCursorAfterSelection

class MyGrid(XCursorAfterSelection, TestGrid):
	pass

if __name__ == '__main__':
	
	def oninit(self):
		self.grid = MyGrid(self, -1)

	def ondestroy(self):
		pass

	TestApp(oninit, ondestroy).MainLoop()
