import wx
import wx.aui
from toolib.wx.TestApp import TestApp

if __name__ == '__main__':

	def onMotion(event):
		tabCtrl = event.GetEventObject()
		nb = tabCtrl.GetParent()
		x, y = event.GetPosition()
		print tabCtrl.GetChildren()
		print event.GetPosition(), tabCtrl.TabHitTest(x, y, None), tabCtrl.HitTest((x, y))
		#tabCtrl.SetToolTipString('Beeeeee: %s' % (tabCtrl.HitTest(event.GetPosition()),))

		event.Skip()

	def oninit(self):
		self.nb = wx.aui.AuiNotebook(self)
		for i in xrange(3):
			page = wx.Panel(self, -1)
			self.nb.AddPage(page, "Page %s" % (i+1) )

		for i, w in enumerate(self.nb.GetChildren()):
			if isinstance(w, wx.aui.AuiTabCtrl):
				tabCtrl = w

		for i in dir(tabCtrl):
			print i
				

		tabCtrl.Bind(wx.EVT_MOTION, onMotion, tabCtrl)


		print tabCtrl.HitTest((1,1))

	def ondestroy(self):
		pass

	TestApp(oninit, ondestroy).MainLoop()

