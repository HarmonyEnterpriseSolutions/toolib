import wx
from MenuResourcesHolder	import MenuResourcesHolder
from Menu					import Menu
from toolib					import debug

class MenuBar(wx.MenuBar, MenuResourcesHolder):
	def __init__(self, menuResources, config=None):
		#rint "create menu BAR from config", config.get('text')
		wx.MenuBar.__init__(self)
		MenuResourcesHolder.__init__(self, menuResources)
		if config is not None:
			self.loadFromConfig(config)
		self.SetEvtHandlerEnabled(True)

	def loadFromConfig(self, config):
		text = config.get('text', None)
		items = config.get('items', ())
		for item in items:
			# item is action
			text = item.get('text', '')
			self.Append(Menu(self._resources, item), text)

	def applyContexts(self, contexts):
		for i in range(self.GetMenuCount()):
			menu = self.GetMenu(i)
			if isinstance(menu, Menu):
				menu.applyContexts(contexts)

	def setContext(self, context):
		debug.deprecation("use applyContexts")
		self.applyContexts([context])

	def connect(self, window):
		for i in range(self.GetMenuCount()):
			menu = self.GetMenu(i)
			if isinstance(menu, Menu):
				menu.connect(window, connectAccelerators=False)

	def disconnect(self, window):
		for i in range(self.GetMenuCount()):
			menu = self.GetMenu(i)
			if isinstance(menu, Menu):
				menu.disconnect(window)

	def setItemsChecked(self, action, checked):
		items = self.findItems(action)
		for item in items:
			item.Check(checked)

	def findItems(self, action):
		itemList = []
		for i in range(self.GetMenuCount()):
			menu = self.GetMenu(i)
			if isinstance(menu, Menu):
				menu._addItems(action, itemList)
		return itemList

	def setItemsEnabled(self, action, enabled):
		for item in self.findItems(action):
			item.Enable(enabled)
