#################################################################
# Program: Toolib
"""
minimal tree popup menu mixin

when tree node clicked to popup 
creates menu with menuFactory for a first time and popups it
any registered popupListener will receive menuPopup event with
	event.item
	event.menu
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2010/03/12 16:49:04 $"
__version__ = "$Revision: 1.7 $"
# $Source: D:/HOME/cvs/toolib/wx/tree/MTreePopupMenu.py,v $
#
#################################################################

import wx
from toolib.event.ListenerList			import ListenerList
from toolib								import debug

class MTreePopupMenu(object):

	def __init__(self, menuFactory, popupNowhere=False):
		self.__menuFactory = menuFactory
		self.__menu = NotImplemented
		self.__popupNowhere = popupNowhere
		self.popupListeners = ListenerList()
		window = self.GetMainWindow() if hasattr(self, 'GetMainWindow') else self
		window.Bind(wx.EVT_RIGHT_UP, self.__onItemPopup, window)

	def __onItemPopup(self, event):
		window = event.GetEventObject()
		pos = event.GetPosition()

		item, flags = window.HitTest(pos)[:2]

		if item is not None and item.IsOk() and (flags & (wx.TREE_HITTEST_ONITEMICON | wx.TREE_HITTEST_ONITEMLABEL)):
			self.SelectItem(item)
			data = item.GetData()
		else:
			item = None
			data = None

		if item or flags & (wx.TREE_HITTEST_NOWHERE | wx.TREE_HITTEST_ONITEMRIGHT) and self.__popupNowhere:
			menu = self.getPopupMenu()
			if menu is not None:
				# fire after contexts apply because menu.applyContexts resets disabled
				self.popupListeners.fireEvent(self, 'menuPopup', 
					menu = menu,
					item = item,
					data = data,
				)
				window.PopupMenu(menu, pos)
				return

		event.Skip()

	def getPopupMenu(self):
		if self.__menu is NotImplemented:
			self.__menu = self.__menuFactory()
		return self.__menu
