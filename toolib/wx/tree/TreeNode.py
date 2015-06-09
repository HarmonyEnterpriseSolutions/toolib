import wx
from toolib.wx.menu.MenuContext		import MenuContext
from _base import TExpansion

class TreeNode(MenuContext, TExpansion):

	def __init__(self, childCount=-1):
		MenuContext.__init__(self, 'node', self.getNodeContextKey)
		self._itemId = None
		self._tree = None
		self._childCount = childCount

	def getTree(self):
		return self._tree


	### FIRE ################################
	
	def fireTextChanged(self):
		if self:
			self._tree.SetItemText(self._itemId, self.getText())

	def fireTextColourChanged(self):
		if self:
			colour = self.getTextColour()
			if colour is not None:
				self._tree.SetItemTextColour(self._itemId, colour)

	def fireIconChanged(self):
		if self:
			self._tree.SetItemImage(self._itemId, self._imageIndex())
			self._tree.SetItemImage(self._itemId, self._selectedImageIndex(), wx.TreeItemIcon_Selected)
			#self._tree.SetItemSelectedImage(self._itemId, self._selectedImageIndex())

	def fireExpandableChanged(self):
		if self:
			self._tree.SetItemHasChildren(self._itemId, self.isExpandable())

	def fireNodeChanged(self):
		self.fireTextChanged()
		self.fireTextColourChanged()
		self.fireIconChanged()

	### Menu Context ########################

	def getNodeContextKey(self):
		"""
		context name is "node"
		override to return popup menu context key, e.g. tree node class
		"""
		return None

	### Overridables ################################

	def getId(self):
		return NotImplemented

	def getImageName(self):
		return None

	def getSelectedImageName(self):
		return self.getImageName()

	def _imageIndex(self):
		return self._tree.getImageIndex(self.getImageName())

	def _selectedImageIndex(self):
		return self._tree.getImageIndex(self.getSelectedImageName())

	def getText(self):
		return "Generic item"

	def getTextColour(self):
		return wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWTEXT)

	def isExpandable(self):
		return self._childCount != 0

	def children(self):
		"""
		Override to load children
		Return: enumeration of TreeNodes, not atached to the tree
		"""
		return ()

	##----------------------------------------------
	def isExpanded(self):
		try:
			return self._tree.IsExpanded(self._itemId)
		except:
			return True

	def setExpanded(self, expanded):
		try:
			if expanded:
				self._tree.Expand(self._itemId)
			else:
				self._tree.Collapse(self._itemId)
		except:
			pass
	##----------------------------------------------

	def isDescendant(self, node):
		""" returns nonzero if node is descendant of this node """
		while node:
			if node == self:
				return 1
			node = node.getParent()
		return 0

	def remove(self):
		""" removes node fom tree. """
		self._tree.Delete(self._itemId)

	def _invalidate(self):
		""" used in Tree node remove methods to invalidate this node """
		self._itemId = None
		self._tree = None

	def addAsRoot(self, tree):
		self._tree = tree
		self._itemId = self._tree.AddRoot(
			self.getText(),
			self._imageIndex(),
			self._selectedImageIndex(),
			wx.TreeItemData(self)
		)

		self.fireTextColourChanged()		#
		self.fireExpandableChanged()		# not changed, but initialization need

	def addAsChild(self, node):
		node._tree = self._tree
		node._itemId = self._tree.AppendItem(
			self._itemId,
			node.getText(),
			node._imageIndex(),
			node._selectedImageIndex(),
			wx.TreeItemData(node)
		)
		node.fireTextColourChanged()		# 
		node.fireExpandableChanged()		# not changed, but initialization need

	def getParent(self):
		item = self._tree.GetItemParent(self._itemId)
		if item.IsOk():
			return self._tree.GetPyData(item)

	def isRoot(self):
		return self.getParent() is None

	def getChildNodes(self):
		list = []
		childItem, cookie = self._tree.GetFirstChild(self._itemId)
		while childItem.IsOk():
			node = self._tree.GetPyData(childItem)
			list.append(node)
			childItem, cookie = self._tree.GetNextChild(self._itemId, cookie)
		return list

	def iterNodes(self, includeSelf=True):
		"""
		Iterates all subnodes recursive, including self
		"""
		if includeSelf:
			yield self
		childItem, cookie = self._tree.GetFirstChild(self._itemId)
		while childItem.IsOk():
			node = self._tree.GetPyData(childItem)
			for node in node.iterNodes():
				yield node
			childItem, cookie = self._tree.GetNextChild(self._itemId, cookie)

	def refresh(self):
		self.fireNodeChanged()
		self.fireExpandableChanged()

	def refreshChildren(self):
		if self:
			selectedNode = self._tree.getSelectedNode()
			if not selectedNode.isDescendant(self):
				selectedNode = None

			ids = self.getExpandedNodeIds()

			self._tree.CollapseAndReset(self._itemId)

			self.setExpandedNodeIds(ids)
			if selectedNode:
				self._tree.selectNode(self._tree.findNode(selectedNode.getId()))

			self._childCount = -1
			self.fireExpandableChanged()

	def getTreePath(self):
		l = [self]
		parent = self.getParent()
		while parent:
			l.append(parent)
			parent = parent.getParent()
		l.reverse()
		return l

	def getCommonTreePath(self, node):
		selfPath = self.getTreePath()[:-1]
		nodePath = node.getTreePath()[:-1]
		i = 0
		n = min(len(selfPath), len(nodePath))
		while i<n and selfPath[i] is nodePath[i]:
			i += 1
		return selfPath[:i]

	def getIdPath(self):
		return [i.getId() for i in self.getTreePath()]

	def getCommonIdPath(self, node):
		return [i.getId() for i in self.getCommonTreePath(node)]

	def getCommonAncestor(self, node):
		try:
			return self.getCommonTreePath(node)[-1]
		except IndexError:
			return None
	
	#def __del__(self):
	#	self.remove()

	def __nonzero__(self):
		return self._itemId is not None and self._itemId.IsOk() and self._tree is not None
