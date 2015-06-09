import wx

class Choice(wx.Choice):
	def GetValue(self):
		return self.GetSelection()
