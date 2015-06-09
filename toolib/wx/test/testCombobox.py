import wx
from toolib.wx.TestApp import TestApp
import wx.aui

if __name__ == '__main__':

	def oninit(self):
		self.cb = wx.ComboBox(self, wx.ID_ANY, choices=["One", 'Two', 'Three'])
		self.cb.SetEditable(False)
		self.cb.Enable(False)
		self.cb.SetItems(['bebe'])

	def on_combobox(event):
		print event
		event.Skip()
		pass

	def ondestroy(self):
		pass

	TestApp(oninit, ondestroy).MainLoop()
