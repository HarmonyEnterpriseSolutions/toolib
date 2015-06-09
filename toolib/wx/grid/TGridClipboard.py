import wx
from TSelectedRect import TSelectedRect

class TGridClipboard(TSelectedRect):
	
	def cut(self):
		rect = self.getSelectedRect()
		if rect:
			self.GetTable().copy(rect)
			self.GetTable().eraseRect(rect)

	def copy(self):
		rect = self.getSelectedRect()
		if rect:
			self.GetTable().copy(rect)

	def paste(self):
		row, col = self.getGridCursor()
		try:
			wx.BeginBusyCursor()
			self.GetTable().paste(row, col)
		finally:
			wx.EndBusyCursor()
