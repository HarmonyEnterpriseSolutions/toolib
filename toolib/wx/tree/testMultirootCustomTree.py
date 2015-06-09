import wx
from CustomTreeCtrl import CustomTreeCtrl
from MMultiRootTree import MMultiRootTree

if __name__ == '__main__':

	class MultiRootTree(MMultiRootTree, CustomTreeCtrl):
		def __init__(self, parent):
			CustomTreeCtrl.__init__(self, parent, -1, style = wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
			MMultiRootTree.__init__(self)


	def test():

		def oninit(self):
			t = MultiRootTree(self)
			
			for i in xrange(3):
				root = t.AddRoot('Root ' + str(i+1))
				for j in xrange(3):
					t.AppendItem(root, str((i+1)*10+j))

			t.Bind(wx.EVT_TREE_SEL_CHANGED, __onSelectionChanged)

		def __onSelectionChanged(event):
			t = event.GetEventObject()
			print "SEL CHANGED:", t.GetItemText(event.GetItem()), event.GetItem().IsOk()

		def ondestroy(self):
			pass

		from toolib.wx.TestApp import TestApp
		TestApp(oninit, ondestroy).MainLoop()


	def testBase():

		def oninit(self):
			self.t = t = wx.TreeCtrl(self, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)

			p = t

			while p.GetParent():
				p = p.GetParent()
			
			vroot = t.AddRoot("ROOT")

			for i in xrange(3):
				root = t.AppendItem(vroot, str((i+1)))
				for j in xrange(3):
					t.AppendItem(root, str((i+1)*10+j))

			t.Bind(wx.EVT_TREE_SEL_CHANGED, __onSelectionChanged)

		def __onSelectionChanged(event):
			t = event.GetEventObject()
			print "SEL CHANGED:", t.GetItemText(event.GetItem()), event.GetItem().IsOk()
			event.Skip()

		def ondestroy(self):
			pass

		from toolib.wx.TestApp import TestApp
		TestApp(oninit, ondestroy).MainLoop()


	test()

