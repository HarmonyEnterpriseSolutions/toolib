import wx

class TextCtrl(wx.TextCtrl):

	def setText(self, text):
		self.SetValue(text)

	def getText(self):
		return self.GetValue()

	def getLineHeight(self):
		return self.GetTextExtent('A')[1]

	def getHeightInLines(self):
		return float(self.GetClientSize()[1]) / float(self.getLineHeight()+1)	# seems to be 1 pixel between lines
