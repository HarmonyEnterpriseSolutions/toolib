import wx
from wx.lib.customtreectrl import CustomTreeCtrl

class Test(object):

	def __init__(self):
		app = wx.PySimpleApp()
		frame = wx.Frame(None)
		frame.SetSizer(wx.BoxSizer(wx.VERTICAL))

		button = wx.Button(frame, -1, 'Create root')
		button.Bind(wx.EVT_BUTTON, self.onCreateRoot)
		frame.GetSizer().Add(button, 0, wx.ALL, 5)
	
		button = wx.Button(frame, -1, 'Create child')
		button.Bind(wx.EVT_BUTTON, self.onCreateChild)
		frame.GetSizer().Add(button, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)

		self.tree = CustomTreeCtrl(frame, -1, style=wx.TR_HIDE_ROOT | wx.TR_EDIT_LABELS | wx.TR_DEFAULT_STYLE)
		self.root = self.tree.AddRoot("HIDDEN ROOT")
		frame.GetSizer().Add(self.tree, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)

		frame.Show()
		app.MainLoop()

	def onCreateRoot(self, event):
		self.createChild(self.root)

	def onCreateChild(self, event):
		selectedItem = self.tree.GetSelection()
		if selectedItem:
			self.createChild(selectedItem)
		else:
			print 'Item not selected'

	def createChild(self, parentItem):
		item = self.tree.AppendItem(parentItem, '')
		#parentItem.Expand()
		self.tree.SelectItem(item)

		# fix
		self.tree.CalculatePositions()

		self.tree.EditLabel(item)

if __name__ == '__main__':
	Test()
	