import wx

class TestDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, -1, 'modal dialog')
		self.b = wx.Button(self, -1, 'Show modeless window')

		def onButton(event):
			frame = wx.MiniFrame(self, -1, "modeless frame")
			frame.MakeModal(False)
			frame.Show()

		self.b.Bind(wx.EVT_BUTTON, onButton)


def test():

	def oninit(self):
		self.b = wx.Button(self, -1, 'Show modal dialog')

		def onButton(event):
			dlg = TestDialog(self)
			dlg.Fit()
			dlg.CenterOnParent()
			dlg.ShowModal()
		
		self.b.Bind(wx.EVT_BUTTON, onButton)

		
	def ondestroy(self):
		pass

	def ontimer(self):
		pass

	from toolib.wx.TestApp import TestApp
	TestApp(oninit, ondestroy, ontimer = ontimer).MainLoop()

if __name__ == '__main__':
	test()
