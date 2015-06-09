import wx
from toolib.wx.TestApp import TestApp
import wx.aui

if __name__ == '__main__':

	def oninit(self):
		self.nb = wx.aui.AuiNotebook(self)
		for i in xrange(3):
			page = wx.Panel(self.nb, -1)
			self.nb.AddPage(page, "Page %s" % (i+1) )
			oninit2(page)

	def oninit2(self):
		self.SetSizer(wx.BoxSizer())


		self.nb = wx.Notebook(self, wx.ID_ANY)
		for i in xrange(5):
			page = wx.Button(self.nb, -1, 'test')
			page.Bind(wx.EVT_BUTTON, onbutton)
			self.nb.AddPage(page, "Page %s" % (i+1), True)
		
		self.nb.SetSelection(0)
		self.GetSizer().Add(self.nb, 1)


	def onbutton(event):
		self = event.GetEventObject()

		dlg = wx.Dialog(self, -1)
		dlg.ShowModal()



	def ondestroy(self):
		pass

	TestApp(oninit, ondestroy).MainLoop()
