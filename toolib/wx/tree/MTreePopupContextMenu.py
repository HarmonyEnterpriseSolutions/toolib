#################################################################
# Program: Toolib
"""
toolib.wx.menu dependent popup menu mixin
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2007/09/17 13:19:43 $"
__version__ = "$Revision: 1.1 $"
# $Source: D:/HOME/cvs/toolib/wx/tree/MTreePopupContextMenu.py,v $
#
#################################################################

from toolib.wx.menu.Menu                 import Menu
from toolib.wx.mixin.TWindowProperty     import TWindowProperty
from toolib                              import debug
from MTreePopupMenu                      import MTreePopupMenu
from toolib.wx.menu.TMenuResourcesWindow import TMenuResourcesWindow


class MTreePopupContextMenu(MTreePopupMenu, TMenuResourcesWindow):

	def __init__(self):
		MTreePopupMenu.__init__(self, self.createDefaultContextMenu)
		self.__contexts = []
		self.popupListeners.bind('menuPopup', self.__onMenuPopup)

	def addMenuContext(self, context):
		self.__contexts.append(context)

	def __onMenuPopup(self, event):
		if isinstance(event.menu, Menu):
			contexts = list(self.__contexts)
			if event.node:
				# node is menu context too (named 'node')
				contexts.append(event.node)
			event.menu.applyContexts(contexts)

	def getContextMenuConfig(self):
		"""
		ABSTRACT METHOD
		returns: config, required to create context menu
		"""
		raise NotImplementedError
		#return {'items' : ["one", "two"] }

	def createDefaultContextMenu(self):
		try:
			conf = self.getContextMenuConfig()
		except NotImplementedError:
			debug.warning("Tree::getContextMenuConfig() is not implemented")
		else:
			resources = self.getMenuResources()
			if resources is not None:
				menu = Menu(resources, conf)
				menu.connect(self)
				return menu
			else:
				debug.error("No resources to create default context menu")
