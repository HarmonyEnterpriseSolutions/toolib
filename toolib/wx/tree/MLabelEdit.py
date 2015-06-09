import wx
from toolib._	import *
from errors		import *


class MLabelEdit(object):

	def __init__(self, renameNode=None):
		if self.GetWindowStyleFlag() & wx.TR_EDIT_LABELS:
			wx.EVT_TREE_END_LABEL_EDIT(self, self.GetId(), self.__onEndLabelEdit)

		self.__renameNode = renameNode or (lambda node, text: node.setText(text))

	def onRenameNode(self, eventIgnored=None):
		node = self.getSelectedNode()
		if node:
			self.EditLabel(node._itemId)

	def __onEndLabelEdit(self, event):
		if not event.IsEditCancelled():
			node = self.getNodeForEvent(event)
			if node:
				self.__renameNode(node, event.GetLabel())
				node.fireTextChanged()

			# call veto every time because text set to user object
			# node.setText should call fireTextChanged
			event.Veto()
