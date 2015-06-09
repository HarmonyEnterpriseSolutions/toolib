#################################################################
# Program: Toolib
"""

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2007/04/23 16:34:31 $"
__version__ = "$Revision: 1.18 $"
# $Source: D:/HOME/cvs/toolib/wx/menu/Menu.py,v $
#
#################################################################

import wx
from toolib.debug	  		import *
from MenuResources			import MenuResources
from MenuResourcesHolder	import MenuResourcesHolder
from toolib.util 			import lang
from sets					import Set as set

EMPTY_DICT = {}


class Menu(wx.Menu, MenuResourcesHolder):
	def __init__(self, menuResources, config, filterItemsContext=None):
		#rint "create menu from config", config.get('text')
		assert isinstance(menuResources, MenuResources), 'arg 2 must be instance of MenuResources, have %s' % menuResources.__class__
		wx.Menu.__init__(self)
		MenuResourcesHolder.__init__(self, menuResources)
		if config is not None:
			self.loadFromConfig(config, filterItemsContext)

		#self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI)

	def loadFromConfig(self, config, filterItemsContext=None):
		items = config.get('items', ())
		haveSeparator = False
		for item in items:
			if isinstance(item, dict):
				# it is inline submenu config (new style)
				inlineSubmenuConf = item.copy()
				item = inlineSubmenuConf.pop('id')
			else:
				inlineSubmenuConf = None

			res = self.getButtonResource(item)

			if res.getKind() != wx.ITEM_SEPARATOR:

				if res.getContext('hit') is None or filterItemsContext in res.getContext('hit'):

					submenuConf = res.getSubmenuConfig()
					if submenuConf or inlineSubmenuConf:
						if inlineSubmenuConf:
							submenuConf = (submenuConf or {}).copy()
							submenuConf.update(inlineSubmenuConf)

						submenu = Menu(self._resources, submenuConf)		# wrap config into menu
					else:
						submenu = None

					menuitem = wx.MenuItem(self, res.getId(), res.getText(), res.getHelp(), res.getKind(), submenu)

					icon = res.getBitmap()
					if icon:
						menuitem.SetBitmap(icon)

					if haveSeparator:
						self.AppendSeparator()
						haveSeparator = False

					self.AppendItem(menuitem)

					if not res.isEnabled():
						menuitem.Enable(0)

					if res.getKind() in (wx.ITEM_CHECK, wx.ITEM_RADIO):
						menuitem.Check(res.getState())
			
			elif self.GetMenuItemCount() > 0:
				haveSeparator = True


	def connect(self, window, connectAccelerators=True):
		for res in self.getButtonResourcesRecursive():
			res.connect(window, wx.wxEVT_COMMAND_MENU_SELECTED)

		if connectAccelerators:
			self.connectAccelerators(window)

	def connectAccelerators(self, window):
		aEntries = self.getAcceleratorEntries()
		if aEntries:
			aTable = wx.AcceleratorTable(aEntries)
			if window.GetAcceleratorTable() != aTable:
				window.SetAcceleratorTable(aTable)

	def disconnect(self, window):
		for id in self.getIdsRecursive():
			ok = window.Disconnect(id, -1, wx.wxEVT_COMMAND_MENU_SELECTED)
			if ok:
				try:
					assert trace("disconnected: %s" % (self.getButtonResource(id).getCommand()))
				except KeyError:
					assert trace("disconnected: %s" % id)

	def setItemsChecked(self, action, checked):
		items = self.findItems(action)
		for item in items:
			item.Check(checked)

	def findItems(self, action):
		"""
		looks for items Recursive
		"""
		l = []
		self._addItems(action, l)
		return l

	def _addItems(self, action, itemList):
		id = self.getButtonResource(action).getId()
		item = self.FindItemById(id)
		if item:
			itemList.append(item)
		for item in self.GetMenuItems():
			submenu = item.GetSubMenu()
			if isinstance(submenu, Menu):
				submenu._addItems(action, itemList)

	def applyContexts(self, contexts):
		self.resetEnabled()
		for context in contexts:
			context.applyMenuContext(self)

	def applyContext(self, context):
		for item in self.GetMenuItems():
			id = item.GetId()
			if id != wx.ID_SEPARATOR:
				try:
					res = self.getButtonResource(id)
				except KeyError:
					pass
				else:
					submenu = item.GetSubMenu()
					enabled = context.isButtonEnabled(res)
					if submenu:
						enabled = enabled and submenu.GetMenuItemCount() > 0
						if isinstance(submenu, Menu):
							submenu.applyContext(context)
					self.Enable(id, self.IsEnabled(id) and enabled)

	def setItemsEnabled(self, action, enabled):
		i = 0
		for item in self.findItems(action):
			i += 1
			item.Enable(enabled)
		return i

	def disableItems(self, action, disabled=True):
		"""
		can't enable
		"""
		for item in self.findItems(action):
			item.Enable(item.IsEnabled() and not lang.leval(disabled))

	def resetEnabled(self):
		for item in self.iterItemsRecursive():
			try:
				enabled = self.getButtonResource(item).isEnabled()
			except KeyError:
				enabled = True

			if item.GetSubMenu() and not item.GetSubMenu().GetMenuItems():
				enabled = False

			item.Enable(enabled)

	def iterItemsRecursive(self):
		"""
		iters items of Menu and sub Menu'es excluding SEPARATORs
		"""
		for item in self.GetMenuItems():
			if item.GetId() != wx.ID_SEPARATOR:
				submenu = item.GetSubMenu()
				if isinstance(submenu, Menu):
					for i in submenu.iterItemsRecursive():	yield i
				#else:
				yield item

	def getIdsRecursive(self, itemFilter=lambda item: True):
		"""
		return list of ids from Menu and sub Menu'es, excluding ID_SEPARATOR
		"""
		return list(set([item.GetId() for item in self.iterItemsRecursive() if itemFilter(item)]))

	#def getMenuItem(self, id):
	#	for item in self.GetMenuItems():
	#		if item.GetId() == id:
	#			return item
	#	raise KeyError, id

	def getButtonResourcesRecursive(self, itemFilter=lambda item: True):
		"""
		return list of ids from Menu and sub Menu'es, excluding ID_SEPARATOR
		"""
		res = []
		for id in self.getIdsRecursive(itemFilter):
			try:
				res.append(self.getButtonResource(id))
			except KeyError:
				pass
		return res

	def getAcceleratorEntries(self):
		"""
		returns enries from menu and submenues
		"""
		return filter(None, 
			map(
				lambda res: res.getAcceleratorEntry(), 
				self.getButtonResourcesRecursive()		#lambda item: item.IsEnabled())
			)
		)

if __name__ == '__main__':
	from test import test
	test()
