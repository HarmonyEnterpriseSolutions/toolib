import wx
from toolib._ import *

class CheckListBoxWithButons(wx.BoxSizer):

	INDENT = 5

	def __init__(self, parent, *args, **kwargs):
		wx.BoxSizer.__init__(self, wx.VERTICAL)

		#print args, kwargs

		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		b = wx.Button(parent, -1, _("Check all"))
		hsizer.Add(b, 1, wx.RIGHT, self.INDENT)
		b.Bind(
			wx.EVT_BUTTON,
			lambda event: [self._listBox.Check(i) for i in xrange(self._listBox.GetCount())]
		)

		b = wx.Button(parent, -1, _("Uncheck all"))
		hsizer.Add(b, 1)
		b.Bind(
			wx.EVT_BUTTON,
			lambda event: [self._listBox.Check(i, False) for i in xrange(self._listBox.GetCount())]
		)
		self.Add(hsizer, 0, wx.BOTTOM, self.INDENT)

		self._listBox = wx.CheckListBox(parent, *args, **kwargs)
		self.Add(self._listBox, 1, wx.EXPAND)

		if parent.GetSizer() is None:
			parent.SetSizer(self)

	def __getattr__(self, name):
		return getattr(self._listBox, name)


if __name__ == '__main__':
	from toolib.wx.TestApp import TestApp

	def oninit(self):
		CheckListBoxWithButons(self, -1, choices=['one', 'two', 'three'])
		
	def ondestroy(self):
		pass

	TestApp(oninit, ondestroy).MainLoop()
