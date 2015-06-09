import wx
from toolib.wx.TestApp import TestApp
from toolib.wx.grid.Grid  import Grid
from toolib.wx.grid.table.List2dTable import List2dTable
from toolib.wx.grid.THitTest import THitTest, GridHitSpace

class MyGrid(Grid, THitTest):

	def __init__(self, *args, **kwargs):
		Grid.__init__(self, *args, **kwargs)
		self.EnableEditing(False)
		self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.__on_cell_left_dclick)			#GetGridWindow().

	def __on_cell_left_dclick(self, event):
		x, y = event.GetPosition()
		x -= self.GetRowLabelSize()
		y -= self.GetColLabelSize()
		print 'dclick at (%s, %s):' % (x, y),
		try:
			row, col = self.hitTest((x,y))
			print "(%s, %s)" % (row, col)
		except GridHitSpace: 
			print 'space'

		event.Skip()

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
