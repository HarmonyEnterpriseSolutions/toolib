#################################################################
# Program: Toolib
"""

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2008/05/19 16:36:00 $"
__version__ = "$Revision: 1.21 $"
# $Source: D:/HOME/cvs/toolib/wx/tree/Tree.py,v $
#
#################################################################

import wx
from MultiRootTree                   import MultiRootTree
from toolib.wx.mixin.TWindowProperty import TWindowProperty
from toolib                          import debug
from _base                           import TExpansion
from toolib.wx.imagecaches           import CachedImageListStub


class Tree(MultiRootTree, TWindowProperty, TExpansion):
	'''
	it only adds items to the tree view when they are needed.
	'''
	
	def __init__(self, *p, **pp):
		rootNode = pp.pop('rootNode', None)
		super(Tree, self).__init__(*p, **pp)

		res = self.getParentWindowProperty('resources', None)

		# look for cachedImageList, then for resources attribute
		try:
			self.__imageList = self.getWindowProperty('cachedImageList')
		except AttributeError:
			try:
				self.__imageList = self.getWindowProperty('resources').getIconCache()
			except AttributeError:
				debug.warning("Tree has no resources")
				self.__imageList = CachedImageListStub()

		if self.__imageList:
			self.SetImageList(self.__imageList)

		if rootNode is not None:
			self.addRoot(rootNode)

		self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.__onExpandNode)

	def getImageIndex(self, imageName):
		# wxPython bug: GetImageList not returns CachedImageList but wx.ImageList
		return self.__imageList.getImageIndex(imageName)

	def __onExpandNode(self, event):
		wx.BeginBusyCursor()
		try:
			# the lazy tree deals with python objects,
			# we call them node here...
			node = self.getNodeForEvent(event)

			## assert node, '''An unknown node was expanded in the LazyTree''' this check is too broad...
			if not self.GetFirstChild(node._itemId)[0].IsOk():
				# we have no children currently in the tree...
				childCount = 0
				for child in node.children():
					childCount = childCount + 1
					node.addAsChild(child)

				node._childCount = childCount
				node.fireExpandableChanged()
				node.fireTextChanged()
		finally:
			wx.EndBusyCursor()
			event.Skip()

	def getRoot(self):
		item = self.GetRootItem()
		if item.IsOk():
			return self.GetPyData(item)

	def setRoot(self, node):
		self.DeleteAllItems()
		self.addRoot(node)

	# primary customisation points...
	def addRoot(self, node):
		node.addAsRoot(self)

	def iterRoots(self):
		item = self.GetRootItem()
		while item.IsOk():
			yield self.GetPyData(item)
			item = self.GetNextSibling(item)

	def iterNodes(self):
		for root in self.iterRoots():
			for node in root.iterNodes():
				yield node
	
	def refresh(self):
		"""
		if roots overrided, removes all nodes from tree
		else, reloads all root children
		"""
		ids = self.getExpandedNodeIds()
		selectedNode = self.getSelectedNode()
		
		if hasattr(self, 'roots'):
			self.DeleteAllItems()
			for root in self.roots():
				self.addRoot(root)
		else:
			for root in self.iterRoots():
				root.refreshChildren()
				root.fireNodeChanged()

		self.setExpandedNodeIds(ids)
		if selectedNode:
			self.selectNode(self.findNode(selectedNode.getId()))

	def getSelectedNode(self):
		itemId = self.GetSelection()
		if itemId.IsOk():
			return self.GetPyData(itemId)

	def selectNode(self, node):
		# this check allows selectNode(findNode()) constructions
		if node:
			self.SelectItem(node._itemId)

	def selectIdPath(self, idPath):
		if idPath:
			self.setExpandedNodeIds(idPath[:-1])
			self.selectNode(self.findNode(idPath[-1]))

	def getNodeForEvent(self, event):
		""" For events, supporting GetItem, returns node through GetItem() method"""
		if hasattr(event, 'GetItem'):
			item = event.GetItem()
			if item.IsOk():
				return self.GetPyData(item)

	#######################################################
	# correct Delete

	def __invalidateChildren(self, itemId):
		for node in tuple(self.GetPyData(itemId).iterNodes(includeSelf = False)):
			node._invalidate()

	def CollapseAndReset(self, itemId):
		# invalidate all child treenodes first
		self.__invalidateChildren(itemId)
		return super(Tree, self).CollapseAndReset(itemId)

	def DeleteChildren(self, itemId):
		"""
		Not tested!
		"""
		# invalidate all child treenodes first
		self.__invalidateChildren(itemId)
		return super(Tree, self).DeleteChildren(itemId)

	def DeleteAllItems(self):
		# invalidate all treenodes first
		for node in tuple(self.iterNodes()):
			node._invalidate()
		return super(Tree, self).DeleteAllItems()

	def Delete(self, itemId):
		self.GetPyData(itemId)._invalidate()
		return super(Tree, self).Delete(itemId)


if __name__ == '__main__':
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
	
		class MyTree(Tree):
	
			def __init__(self, *p, **pp):
				Tree.__init__(self, *p, **pp)
	
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
	
	test()

