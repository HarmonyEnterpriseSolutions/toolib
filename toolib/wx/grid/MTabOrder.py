import wx
from toolib  import debug
from TCursor import TCursor
from TNumberDataLines import TNumberDataLines

class MTabOrder(TNumberDataLines):

	def __init__(self):
		self.Bind(wx.EVT_KEY_DOWN, self.__onKeyDown)

	def __onKeyDown(self, event):
		if event.GetKeyCode() in (wx.WXK_TAB, wx.WXK_RETURN) and not event.ControlDown():
			self.OnTabKeyDown(event)
		else:
			event.Skip()

	def OnTabKeyDown(self, event):
		event.Skip()


class MTabOrder_reading(MTabOrder, TCursor):
	"""
	Make tab move cursor like reading a book
	Shift-Tab works backward

	Tab at right-bottomm cell will append row if Table::AppendRows defined
	"""

	def OnTabKeyDown(self, event):
		if event.ShiftDown():
			col = self.GetGridCursorCol()
			if col <= self.getBaseDataCol():
				row = self.GetGridCursorRow()
				if row > 0:
					self.setGridCursor(row-1, self.getNumberDataCols()-1)
			else:
				self.MoveCursorLeft(0)
		else:
			if not self.MoveCursorRight(0):	
				row = self.GetGridCursorRow()
				if row < self.getNumberDataRows()-1:
					self.setGridCursor(row+1, self.getBaseDataCol())
				else:
					row = self.GetGridCursorRow()
					try:
						self.AppendRows(1)
					except wx.PyAssertionError:
						assert debug.trace("Tab requested to append row but AppendRows seems not to be implemented")
						pass
					else:
						#while self.MoveCursorLeft(0):
						#	pass
						self.setGridCursor(self.getNumberDataRows()-1, self.getBaseDataCol())




class MTabOrder_rightmost(MTabOrder):
	"""
	Make tab move cursor to right an then down
	Shift-Tab works backward
	"""

	def OnTabKeyDown(self, event):
		if event.ShiftDown():
			if not self.MoveCursorUp(0):	self.MoveCursorLeft(0)
		else:
			if not self.MoveCursorRight(0):	self.MoveCursorDown(0)


if __name__ == '__main__':
	from toolib.wx.grid.test.testTabOrder import test
	test()