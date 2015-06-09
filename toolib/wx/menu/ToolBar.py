import wx
from MenuResourcesHolder	import MenuResourcesHolder
from toolib.util			import lang
from toolib					import debug

class ToolBar(wx.ToolBar, MenuResourcesHolder):

	def __init__(self, parent, menuResources, config):
		#rint "create TOOLBAR from config", config.get('text')
		style = config.get('style', wx.TB_HORIZONTAL | wx.NO_BORDER)
		wx.ToolBar.__init__(self, parent, -1, style=style)
		MenuResourcesHolder.__init__(self, menuResources)
		self.toolIds = []
		self.loadFromConfig(config)
		self.Realize()

	def loadFromConfig(self, config):
		for item in config.get('items', ()):
			try:
				res = self.getButtonResource(item)
			except KeyError:
				continue

			id   = res.getId()
			kind = res.getKind()

			if kind == wx.ITEM_SEPARATOR or id == wx.ID_SEPARATOR:
				self.AddSeparator()
			else:
				bitmap = res.getBitmap() or self._resources.getEmptyBitmap()

				tip = res.getTip()
				help = res.getHelp()
				self.AddTool(id,
							 bitmap,
							 wx.NullBitmap,
							 kind,
							 'label',
							 tip,
							 help,
							 )

				if not res.isEnabled():
					self.EnableTool(id, 0)

				self.toolIds.append(id)

	def iterItems(self):
		"""
		iter tuples (id, buttonResource)
		"""
		for id in self.toolIds:
			if id != wx.ID_SEPARATOR:
				try:
					res = self.getButtonResource(id)
				except KeyError:
					pass
				else:              
					yield id, res
		
	
	def applyContexts(self, contexts):
		self.resetEnabled()
		for context in contexts:
			context.applyMenuContext(self)

	def applyContext(self, context):
		for id, res in self.iterItems():
			self.EnableTool(id, res.isEnabled() and context.isButtonEnabled(res))

	def setContext(self, context):
		debug.deprecation("use applyContexts")
		self.applyContexts([context])

	def connect(self, window):
		for id, res in self.iterItems():
			res.connect(window, wx.wxEVT_COMMAND_TOOL_CLICKED)

	def disconnect(self, window):
		for id in self.toolIds:
			if id != wx.ID_SEPARATOR:
				window.Disconnect(id, -1, wx.wxEVT_COMMAND_TOOL_CLICKED)

	def getToolId(self, action):
		return self.getButtonResource(action).getId()

	def setItemsChecked(self, action, checked):
		self.ToggleTool(self.getToolId(action), checked)

	def setItemsEnabled(self, action, enabled):
		self.EnableTool(id, enabled)

	def disableItems(self, action, disabled=True):
		"""
		can't enable
		"""
		id = self.getToolId(action)
		self.EnableTool(id, self.GetToolEnabled(id) and not lang.leval(disabled))

	def resetEnabled(self):
		for id, res in self.iterItems():
			self.EnableTool(id, res.isEnabled())
