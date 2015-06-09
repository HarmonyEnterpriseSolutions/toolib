import wx
import wx.lib.flatnotebook as fnb
from toolib.wx.TestApp import TestApp

if __name__ == '__main__':

	def oninit(self):
		self.nb = wx.lib.flatnotebook.FlatNotebook(self, wx.ID_ANY, style=fnb.FNB_X_ON_TAB | fnb.FNB_FF2 | fnb.FNB_NO_X_BUTTON)
		for i in xrange(3):
			page = wx.Panel(self, -1)
			self.nb.AddPage(page, "Page %s" % (i+1), True)

	def ondestroy(self):
		pass

	TestApp(oninit, ondestroy).MainLoop()
