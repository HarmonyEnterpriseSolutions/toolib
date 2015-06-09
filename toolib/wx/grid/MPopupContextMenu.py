import wx
from toolib 								import debug
from toolib.wx.menu.Menu					import Menu
from toolib.wx.menu.TMenuResourcesWindow	import TMenuResourcesWindow
from toolib.wx.menu.MenuContext				import MenuContext
from MPopupMenu                             import MPopupMenu


class MPopupContextMenu(
		MPopupMenu,
		TMenuResourcesWindow,
	):

	"""
	Popup menu 

	-------------------------------------
	| CORNER | COL                      |
	-------------------------------------
	| ROW    | CELL                     |
	|	     |                          |
	|	     |                          |
	-------------------------------------
                  * CELL

	ALL  Select all if not selected 
	ROW  Select Row if not selected
	COL  Select Col if not selected
	CELL Select Cell, row or col depending on selection model
	* CELL Only thrue mouse, select nothing


	Use addContext to register menu context

	Builtin contexts:
		selection
			none

			single-cell
			single-row
			single-column

			multiple-row
			multiple-column
			multiple-cell

		hit
			rowlabel	- row label only
			collabel	- col label only
			cell		- cell only
			corner		- corner only
			space		- space only

			row			- row label or cell
			col			- col label or cell

			any			- hit any place of grid

		hit context works during menu creation so menu items existance depends on hit context
		(we have 5 separate menues for different hit areas)
	"""

	def __init__(self):
		MPopupMenu.__init__(self, self.createDefaultPopupMenu)

		self.__contexts = []
		self.addMenuContext(MenuContext('selection', self.__getSelectionContextKey))
		self.popupListeners.bind('menuPopup', self.__onMenuPopup)

	def __onMenuPopup(self, event):
		event.menu.applyContexts(self.__contexts)

	def getPopupMenuConfig(self):
		"""
		ABSTRACT METHOD
		returns: config, required to create context menu
		can override createDefaultPopupMenu instead anf forget about this method
		"""
		return None

	def createDefaultPopupMenu(self, hitArea):
		"""
		Overrideable
		"""
		menu = Menu(self.getMenuResources(), self.getPopupMenuConfig() or { 'items' : ('--',) }, filterItemsContext = hitArea)
		menu.connect(self)
		return menu

	def addMenuContext(self, context):
		self.__contexts.append(context)

	def __getSelectionContextKey(self):
		rows = self.getRowSelection().getPureSize()
		if rows > 1:
			return 'multiple-row'
		elif rows == 1:
			return 'single-row'
		else:
			cols = self.getColSelection().getPureSize()
			if cols > 1:
				return 'multiple-column'
			elif cols == 1:
				return 'single-column'
			else:
				cells = len(self.getCellSelection())
				if cells > 1:
					return 'multiple-cell'
				elif cells == 1:
					return 'single-cell'
		
		return 'none'


if __name__ == '__main__':
	from toolib.wx.grid.test.testPopupMenu import test
	test()
