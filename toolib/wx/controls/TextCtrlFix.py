import wx

"""
Monkey Patch for wx.TextCtrl
Fixes incorrect text hscroll after resize
"""

__super__ = wx.TextCtrl

class TextCtrlFix(wx.TextCtrl):
	def __init__(self, parent, id=-1, value = "", pos = wx.DefaultPosition, size = wx.DefaultSize, style = 0, validator = wx.DefaultValidator, name = wx.TextCtrlNameStr):
		__super__.__init__(self, parent, id, value, pos, size, style, validator, name)

		if (style & (wx.TE_MULTILINE | wx.TE_RICH | wx.TE_RICH2 | wx.TE_AUTO_URL)) == 0:
			self.Bind(wx.EVT_SIZE, _onSize)
			

def _onSize(event):
	
	wx.CallAfter(_afterOnSize, event.GetEventObject())
	event.Skip()


def _afterOnSize(control):

	s1, s2 = control.GetSelection()
	ip = control.GetInsertionPoint()

	if s1 != s2 or ip > 0:
		# force to scroll text left
		control.SetInsertionPoint(0)

		# restore insertion point and selection
		if ip > 0:
			control.SetInsertionPoint(ip)

		if s1 != s2:
			control.SetSelection(s1, s2)


wx.TextCtrl = TextCtrlFix


def test():

	def oninit(self):
		self.SetSizer(wx.BoxSizer(wx.VERTICAL))
		self.c = wx.TextCtrl(self, -1, ('1 12 123 12345 123456 1234567 12345678 123456789 1234567890 12345678901 123456789012'), style=0)
		self.GetSizer().Add(self.c, 0, wx.GROW)

		self.Fit()
	
	def ondestroy(self):
		pass

	def ontimer(self):
		#self.c.SetSize(self.c.GetSize())
		#self.c.Refresh()
		#print "timer"
		self.SetSize((600,100))


	from toolib.wx.TestApp import TestApp
	TestApp(oninit, ondestroy, ontimer = ontimer).MainLoop()

if __name__ == '__main__':
	test()
