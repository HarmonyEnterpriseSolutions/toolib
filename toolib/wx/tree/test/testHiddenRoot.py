import wx
from wx.lib.agw.customtreectrl import CustomTreeCtrl

if __name__ == '__main__':
	app = wx.PySimpleApp()
	frame = wx.Frame(None)

	tree = CustomTreeCtrl(frame, -1, style=wx.TR_HIDE_ROOT | wx.TR_EDIT_LABELS | wx.TR_DEFAULT_STYLE)
	root = tree.AddRoot("HIDDEN ROOT")

	for i in range(3):
		tree.AppendItem(root, 'child of the hidden root %s' % i)

	frame.Show()
	app.MainLoop()
	