import wx

class SplitterWindow(wx.SplitterWindow):
	
	def GetSashPosition(self):
		pos = super(SplitterWindow, self).GetSashPosition()
		if self.GetSashGravity() > 0.5:
			sashDim = [wx.SPLIT_VERTICAL, wx.SPLIT_HORIZONTAL].index(self.GetSplitMode())
			pos -= self.Size[sashDim]
		return pos


if __name__ == '__main__':

	def test():
		def onButton(event):
			self = event.GetEventObject().GetParent()
			self.SetSashPosition(self.GetSashPosition())

			sashDim = [wx.SPLIT_VERTICAL, wx.SPLIT_HORIZONTAL].index(self.GetSplitMode())

			print 'sash pos', self.GetSashPosition()
			print 'w1 size', self.GetWindow1().Size[sashDim]
			print 'w2 size', self.GetWindow2().Size[sashDim]
			print 'sw size', self.Size[sashDim]
			print 'w1+w2 size', self.GetWindow1().Size[sashDim] + self.GetWindow2().Size[sashDim] + self.GetSashSize()

		def oninit(self):
			self.sw = SplitterWindow(self, -1)#, style=wx.NO_BORDER)
			self.sw.SetSashGravity(1)
			self.sw.SplitVertically(wx.TextCtrl(self.sw, -1), wx.Button(self.sw, -1, 'Test'))
			#self.sw.SplitHorizontally(wx.TextCtrl(self.sw, -1), wx.Button(self.sw, -1, 'Test'))

			self.sw.GetWindow2().Bind(wx.EVT_BUTTON, onButton)
			
		def ondestroy(self):
			pass

		def ontimer(self):
			#self.n2.SetSelection(-1,-1)
			#self.n2.SetFocus()
			pass

		from toolib.wx.TestApp import TestApp
		TestApp(oninit, ondestroy, ontimer = ontimer).MainLoop()
	
	test()
