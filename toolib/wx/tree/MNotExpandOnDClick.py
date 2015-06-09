import wx
from Tree import Tree
from wx.lib.customtreectrl import wxEVT_TREE_ITEM_ACTIVATED

class MNotExpandOnDClick(object):

	def __init__(self):
		self.Bind(wx.EVT_LEFT_DCLICK, self.__on_left_dclick)

	def __on_left_dclick(self, event):	
		itemId, flags = self.HitTest(event.GetPosition()) 
		if flags & (wx.TREE_HITTEST_ONITEMLABEL | wx.TREE_HITTEST_ONITEMICON):
			self.AddPendingEvent(wx.TreeEvent(wxEVT_TREE_ITEM_ACTIVATED, self, self.GetSelection()))
		else:
			event.Skip()

"""
def test():

	from TreeNode import TreeNode

	class MyTreeNode(TreeNode):

		def __init__(self, id):
			TreeNode.__init__(self)
			self.id = id

		def getId(self):
			return self.id

		def children(self):
			return (MyTreeNode(self.id*10+1), MyTreeNode(self.id*10+2), MyTreeNode(self.id*10+3))

		def getText(self):
			return str(self.id)

	class MyTree(Tree, MNotExpandOnDClick):

		def __init__(self, *p, **pp):
			Tree.__init__(self, *p, **pp)
			MNotExpandOnDClick.__init__(self)

			self.Bind(wx.EVT_TREE_SEL_CHANGED, self.__onSelectionChanged)

		def __onSelectionChanged(self, event):
			print "SEL CHANGED:", self.getNodeForEvent(event).getId()

		def roots(self):
			return (MyTreeNode(1), MyTreeNode(2), MyTreeNode(3))

	def oninit(self):
		self.t = MyTree(self)
		self.t.refresh()

	def ondestroy(self):
		pass

	def ontimer(self):
		#self.t.selectIdPath([1, 12])
		pass

	from toolib.wx.TestApp import TestApp
	TestApp(oninit, ondestroy, ontimer=ontimer).MainLoop()


if __name__ == '__main__':
	test()
"""