import wx
from TSelection import TSelection


class MDeleteSelection(TSelection):
	
	"""
	On Delete: SetValue None to selected cells, works only in cell selection mode
	On Shift+Delete: does nothing

	Recommended to use with CursorSelection
	"""
	
	def __init__(self):
		self.Bind(wx.EVT_CHAR,		self.__onChar)

	def __onChar(self, event):
		#rint "char", event.GetKeyCode(), wx.WXK_DELETE
		if event.GetKeyCode() == wx.WXK_DELETE:
			if not event.AltDown() and not event.ShiftDown() and not event.ControlDown():
				self.OnDeleteSelection(event)
			else:
				pass # do not skip, block this events
		else:
			event.Skip()

	def OnDeleteSelection(self, event):
		if self.GetSelectionMode() == self.wxGridSelectCells:
			table = self.GetTable()
			cells = self.getCellSelection()
			if cells:
				for row, col in cells:
					#rint "table.SetValue(%s, %s, None)" %  (row, col)
					table.SetValue(row, col, None)
				table.fireTableUpdated()
			else:
				event.Skip()
		else:
			event.Skip()
