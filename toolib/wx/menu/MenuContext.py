import operator

class BaseMenuContext(object):
	"""
	Used to manipulate menu items manually

	Use common (MenuBar, ToolBar) methods:

		def setItemsChecked(self, action, checked):
		def setItemsEnabled(self, action, enabled):
		def disableItems(self, action, disabled=True):

	"""

	def applyMenuContext(self, menu):
		"""
		use menu.disableItems here
		"""
		pass


class ScriptMenuContext(BaseMenuContext):

	def __init__(self, script):
		self.__script = script

	def applyMenuContext(self, menu):
		"""
		use menu.disableItems here
		"""
		self.__script(menu)


class MenuContext(BaseMenuContext):
	"""
	Context is
		TreeNode
		Grid with SelectionContext trait
	"""
	def __init__(self, name, keyGetter):
		"""
		Context name is contet domain to check in
		e.g. 
			selection
			readonlyness
		if domain not present for button it is assumed allways to be in context
		by this domain

		keyGetter: 
			returns context key. E. g. it may be tree node class.
			It is the key to set to menu to enable or disable items.
			Override to customize tree node context key.

		"""
		self.__name = name
		self.__keyGetter = keyGetter

	def applyMenuContext(self, menu):
		menu.applyContext(self)

	def isButtonEnabled(self, buttonResource):
		"""
		Menu or toolbar item
		Override to customize enabling/disabling e.g. for each TreeNode instance
		"""
		contextKeys = buttonResource.getContext(self.__name)
		if contextKeys:
			return self.__keyGetter() in contextKeys
		else:
			return True

