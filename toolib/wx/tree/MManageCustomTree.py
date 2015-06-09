import wx
from toolib._	import *
from errors		import *
from wx.lib.customtreectrl import TreeItemAttr


class MManageCustomTree(object):

	def __init__(self, moveItem, copyItem):
		"""
		@param moveItem callback to move node
		@param moveItem callback to copy node
		"""
		self.__cuttedItem = None
		self.__copiedItem = None
		self.__copiedItemData = None
		self.__cuttedItemData = None
		self.__moveItem = moveItem
		self.__copyItem = copyItem

		self.__attrNormal = TreeItemAttr()
		self.__attrCutted = TreeItemAttr(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))

		self.Bind(wx.EVT_TREE_DELETE_ITEM, self.__on_tree_delete_item, self)

	def __on_tree_delete_item(self, event):
		item = event.GetItem()
		if item is self.__cuttedItem:
			self.__cuttedItem = None
		if item is self.__copiedItem:
			self.__copiedItem = None

	def __setCuttedItem(self, item):
		if self.__cuttedItem is not item:
			
			if self.__cuttedItem:
				self.__cuttedItem.SetAttributes(self.__attrNormal)
			
			self.__cuttedItem = item
			self.__cuttedItemData = item.GetData() if item is not None else None

			if self.__cuttedItem:
				self.__cuttedItem.SetAttributes(self.__attrCutted)

			self.Refresh()

	def getCuttedItem(self):
		return self.__cuttedItem

	def getCuttedItemData(self, force=False):
		"""
		if force, returns item data, even if cutted item was removedfrom tree
		if not force, words like getCuttedItem().GetData()
		"""
		if force:
			return self.__cuttedItemData
		else:
			return self.__cuttedItem.GetData() if self.__cuttedItem else None

	def __setCopiedItem(self, item):
		self.__copiedItem = item
		self.__copiedItemData = item.GetData() if item is not None else None

	def getCopiedItem(self):
		return self.__copiedItem

	def getCopiedItemData(self, force=False):
		"""
		if force, returns item data, even if copied item was removedfrom tree
		if not force, words like getCopiedItem().GetData()
		"""
		if force:
			return self.__copiedItemData
		else:
			return self.__copiedItem.GetData() if self.__copiedItem else None

	def onCutItem(self, eventIgnored=None):
		self.__setCopiedItem(None)
		self.__setCuttedItem(self.GetSelection())

	def onCopyItem(self, eventIgnored=None):
		self.__setCuttedItem(None)
		self.__setCopiedItem(self.GetSelection())

	def onPasteItem(self, eventIgnored=None):
		cutted = self.getCuttedItem()
		copied = self.getCopiedItem()
		target = self.GetSelection()

		try:
			if cutted:
				if self.isDescendant(cutted, target):
					self.__setCuttedItem(None)
					raise TreePasteError, _("Can't paste item into self or child")
				else:
					#idPath = self.getIdPath(target) + [cutted.GetData()]
					try:
						self.__moveItem(target, cutted)
					except TreeOperationError:
						self.__setCuttedItem(None)
						raise
					else:
						#item = self.getCommonAncestor(target, cutted)
						#if item:
						#	item.refreshChildren()
						#else:
						#	self.refresh()
						#self.selectIdPath(idPath)
						pass
			elif copied:
				id = self.__copyItem(target, copied)
				#idPath = target.getIdPath() + [id]
			
				#target.refreshChildren()
				#self.selectIdPath(idPath)
				#self.__setCopiedItem(None)

		except TreeOperationError, e:
			d = wx.MessageDialog(self, str(e), _("Paste operation failed"), wx.ICON_HAND)
			d.ShowModal()
			d.Destroy()
	 

	# it is ported TreeNode methods

	def isDescendant(tree, self, node):
		""" returns nonzero if node is descendant of this node """
		while node and node.IsOk():
			if node is self:
				return True
			node = node.GetParent()
		return False
	
	def getTreePath(tree, self):
		l = [self]
		parent = self.GetParent()
		while parent:
			l.append(parent)
			parent = parent.GetParent()
		l.reverse()
		return l

	#def getIdPath(tree, self):
	#	return [i.GetData() for i in tree.getTreePath(self)]

	#def getCommonTreePath(tree, self, node):
	#	selfPath = tree.getTreePath(self)[:-1]
	#	nodePath = tree.getTreePath(node)[:-1]
	#	i = 0
	#	n = min(len(selfPath), len(nodePath))
	#	while i<n and selfPath[i] is nodePath[i]:
	#		i += 1
	#	return selfPath[:i]

	#def getCommonAncestor(tree, self, node):
	#	try:
	#		return tree.getCommonTreePath(self, node)[-1]
	#	except IndexError:
	#		return None
