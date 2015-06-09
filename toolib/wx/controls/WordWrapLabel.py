import wx

class WordWrapLabel(wx.TextCtrl):
	def __init__(self, parent, text="", style = wx.TE_MULTILINE | wx.TE_READONLY | wx.NO_BORDER | wx.TE_RICH, *args, **kwargs):
		wx.TextCtrl.__init__(self, parent, -1, style=style, *args, **kwargs)
		self.SetBackgroundColour(parent.GetBackgroundColour())
		if text:
			self.SetValue(text)

	def setText(self, text):
		self.SetValue(text)

	def getText(self):
		return self.GetValue()

