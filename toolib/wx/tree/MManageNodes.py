import wx
from toolib._	import *
from errors		import *


class MManagedNode(object):
	"""
	Mixin to make tree node gray when cut
		overrides TreeNode::getTextColour
	"""
	
	COLOUR_TEXT_CUT = "grey"

	def getTextColour(self):
		if self.getTree().getCuttedNode() is self:
			return self.COLOUR_TEXT_CUT
		else:
			return super(MManagedNode, self).getTextColour()

	def move(self, cutted):
		"""
		Override to implement Paste Cutted node here 
			or pass moveNode to MManageNodes constructor
		Return True if ok False if imposible
		Can throw TreeOperationError
		"""
		raise NotImplementedError, 'abstract'

	def copy(self, copied):
		"""
		Override to implement Paste Copied node here 
			or pass copyNode to MManageNodes constructor
		Can throw TreeOperationError
		"""
		raise NotImplementedError, 'abstract'


class MManageNodes(object):

	def __init__(self, moveNode = None, copyNode = None):
		self.__cuttedNode = None
		self.__copiedNode = None
		self.__moveNode = moveNode or (lambda target, source: target.move(source))
		self.__copyNode = copyNode or (lambda target, source: target.copy(source))

	def __setCuttedNode(self, node):
		prev = self.__cuttedNode
		self.__cuttedNode = node
		if prev: prev.fireNodeChanged()
		if node: node.fireNodeChanged()

	def getCuttedNode(self):
		return self.__cuttedNode

	def __setCopiedNode(self, node):
		self.__copiedNode = node

	def getCopiedNode(self):
		return self.__copiedNode

	def onCutNode(self, eventIgnored=None):
		self.__setCopiedNode(None)
		self.__setCuttedNode(self.getSelectedNode())

	def onCopyNode(self, eventIgnored=None):
		self.__setCuttedNode(None)
		self.__setCopiedNode(self.getSelectedNode())

	def onPasteNode(self, eventIgnored=None):
		cutted = self.getCuttedNode()
		copied = self.getCopiedNode()
		target = self.getSelectedNode()

		try:
			if cutted:
				if cutted.isDescendant(target):
					self.__setCuttedNode(None)
					raise TreePasteError, _("Can't paste node into self or child")
				else:
					idPath = target.getIdPath() + [cutted.getId()]
					try:
						self.__moveNode(target, cutted)
					except TreeOperationError:
						self.__setCuttedNode(None)
						raise
					else:
						node = target.getCommonAncestor(cutted)
						if node:
							node.refreshChildren()
						else:
							self.refresh()
						self.selectIdPath(idPath)
			elif copied:
				id = self.__copyNode(target, copied)
				idPath = target.getIdPath() + [id]
			
				target.refreshChildren()
				self.selectIdPath(idPath)
				self.__setCopiedNode(None)

		except TreeOperationError, e:
			d = wx.MessageDialog(self, str(e), _("Paste operation failed"), wx.ICON_HAND)
			d.ShowModal()
			d.Destroy()

	#def __onMenuPopup(self, event):
	#	"""
	#	Enables remove, cut, paste
	#	"""
	#	event.menu.disableItems('cutNode',    self.isReadOnly() or event.node.isRoot())
	#	event.menu.disableItems('pasteNode',  self.isReadOnly() or self.getCuttedNode() is None and self.getCopiedNode() is None)
	 

