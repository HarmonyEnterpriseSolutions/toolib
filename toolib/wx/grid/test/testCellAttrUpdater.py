import wx
from toolib.wx.TestApp import TestApp
from toolib.wx.grid.Grid  import Grid
from toolib.wx.grid.table.List2dTable import List2dTable
from toolib.wx.grid.TSelection import TSelection


class MyTable(List2dTable):

	dc = (50, 100, 256-50)
	c = [255, 255, 255]

	def __init__(self):
		List2dTable.__init__(self)
		#self.addAttrUpdater('RowTopAnchored')
		self.addAttrUpdater('RowBottomAnchored')

	def colorMyWorld(self):
		if self.CanHaveAttributes():
			ap = self.GetAttrProvider()

			for r in xrange(self.GetNumberRows()):
				for c in xrange(self.GetNumberCols()):
					self.SetValue(r, c, '%s, %s' % (r, c))
		
				for i in range(3):
					self.c[i] = (self.c[i] + self.dc[i]) % 256

				#if (r == self.GetNumberRows()-1):
				ap.SetRowAttr(self.newAttr(backgroundColour = self.c), r)


		

class MyGrid(Grid, TSelection):

	def __init__(self, *args, **kwargs):
		Grid.__init__(self, *args, **kwargs)

	def getPopupMenuConfig(self):
		return { 
			'items' : [
				'insertColumn',
				'appendColumn',
				'removeColumn',
				'--',
				'insertRow',
				'appendRow',
				'removeRow',
			],
		}

	def OnInsertRow(self, event):
		self.GetTable().InsertRows(self.getRowSelection()[0], 1)

	def OnAppendRow(self, event):
		self.GetTable().AppendRows(1)

	def OnRemoveRow(self, event):
		s = self.getRowSelection().getRows()
		s.reverse()
		for i in s:
			self.GetTable().DeleteRows(i, 1)


def test():
	def oninit(self):
		
		self.grid = MyGrid(self, -1)
		self.grid.SetTable(MyTable())
		self.grid.AppendRows(10)
		self.grid.AppendCols(10)

		self.grid.GetTable().colorMyWorld()

		self.Size = (1000, 600)

	def ondestroy(self):
		pass

	def ontimer(self):
		t = self.grid.GetTable()
		t.fireTableStructureChanging()

		#if len(t._data) == 101:
		#	for i in range(100):
		#		del t._data[0]
		#else:
		#	for i in range(10):
		#		t._data.insert(0, [])

		try:
			del t._data[7]
		except:
			for i in xrange(3):
				t._data.insert(2, [])

		t.fireTableStructureChanged()

	TestApp(oninit, ondestroy, ontimer=ontimer).MainLoop()

if __name__ == '__main__':
	test()
