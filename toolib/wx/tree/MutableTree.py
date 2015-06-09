import wx
from Tree		import Tree
from toolib._	import *
from errors		import *
from MTreePopupContextMenu		import MTreePopupContextMenu


class CutedTreeNodeDesign(object):
	"""
	Mixin to make tree node gray when cut
		In:  TreeNode::COLOUR_TEXT_DEFAULT 
		Out: getTextColour
	"""
	
	COLOUR_TEXT_CUT = "grey"

	def getTextColour(self):
		if self.getTree().getCuttedNode() is self:
			return self.COLOUR_TEXT_CUT
		else:
			return self.getTree().getDefaultItemTextColour()

class MutableTree(Tree, MTreePopupContextMenu):

	def __init__(self, *args, **kwargs):
		self.__readOnly = kwargs.pop('readOnly', False)

		Tree.__init__(self, *args, **kwargs)
		MTreePopupContextMenu.__init__(self)

		#wx.EVT_TREE_BEGIN_DRAG(id, func)
		self.__cuttedNode = None
		self.__copiedNode = None

		# add label edit handler
		if self.GetWindowStyleFlag() & wx.TR_EDIT_LABELS:
			wx.EVT_TREE_END_LABEL_EDIT(self, self.GetId(), self.OnEndLabelEdit)

		self.popupListeners.bind('menuPopup', self.__onMenuPopup)


	def setReadOnly(self, readOnly):
		self.__readOnly = readOnly

	def isReadOnly(self):
		return self.__readOnly

	def OnRenameNode(self, event):
		node = self.getSelectedNode()
		if node is not None:
			self.EditLabel(node._itemId)

	def OnEndLabelEdit(self, event):
		if not event.IsEditCancelled():
			if not self.isReadOnly():
				node = self.getNodeForEvent(event)
				if node:
					node.setText(event.GetLabel())

			# call veto every time because text set to user object
			# node.setText should call fireTextChanged
			event.Veto()

	def setCuttedNode(self, node):
		prev = self.__cuttedNode
		self.__cuttedNode = node
		if prev: prev.fireNodeChanged()
		if node: node.fireNodeChanged()

	def getCuttedNode(self):
		return self.__cuttedNode

	def setCopiedNode(self, node):
		self.__copiedNode = node

	def getCopiedNode(self):
		return self.__copiedNode

	def OnCutNode(self, event):
		self.setCopiedNode(None)
		self.setCuttedNode(self.getSelectedNode())

	def OnCopyNode(self, event):
		self.setCuttedNode(None)
		self.setCopiedNode(self.getSelectedNode())

	def OnRefreshChildren(self, event):
		self.getSelectedNode().refreshChildren()

	def OnPasteNode(self, event):
		cutted = self.getCuttedNode()
		copied = self.getCopiedNode()
		target = self.getSelectedNode()

		try:
			if cutted:
				if cutted.isDescendant(target):
					self.setCuttedNode(None)
					raise TreePasteError, _("Can't paste node into self or child")
				else:
					idPath = target.getIdPath() + [cutted.getId()]
					try:
						target.move(cutted)
					except TreeOperationError:
						self.setCuttedNode(None)
						raise
					else:
						node = target.getCommonAncestor(cutted)
						if node:
							node.refreshChildren()
						else:
							self.refresh()
						self.selectIdPath(idPath)
			elif copied:
				id = target.copy(copied)
				idPath = target.getIdPath() + [id]
			
				target.refreshChildren()
				self.selectIdPath(idPath)
				self.setCopiedNode(None)

		except TreeOperationError, e:
			d = wx.MessageDialog(self, str(e), _("Paste operation failed"), wx.ICON_HAND)
			d.ShowModal()
			d.Destroy()

	def OnRemoveNode(self, event):
		self.getSelectedNode().remove()

	def OnCreateNode(self, event):
		raise NotImplementedError, 'abstract'

	def __onMenuPopup(self, event):
		"""
		Enables remove, cut, paste
		"""
		event.menu.disableItems('newNode',    self.isReadOnly())
		event.menu.disableItems('renameNode', self.isReadOnly() or not self.GetWindowStyle() & wx.TR_EDIT_LABELS)
		event.menu.disableItems('removeNode', self.isReadOnly() or event.node.isRoot())
		event.menu.disableItems('cutNode',    self.isReadOnly() or event.node.isRoot())
		event.menu.disableItems('pasteNode',  self.isReadOnly() or self.getCuttedNode() is None and self.getCopiedNode() is None)


	def getContextMenuConfig(self):
		c = {
			'items' : [
				'refreshChildren',
				'--',
				'newNode',
				'--',
				'cutNode',
				'copyNode',
				'pasteNode',
				'--',
				'removeNode',
			]
		}

		if self.GetWindowStyle() & wx.TR_EDIT_LABELS:
			c['items'].insert(3, 'renameNode')

		return c

	def getDefaultItemTextColour(self):
		return wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWTEXT)	
