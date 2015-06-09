import wx
from toolib 					import debug
from toolib.event.ListenerList	import ListenerList
from toolib.util				import lang

from errors						import GridHitSpace

from TSelection					import TSelection
from THitTest					import THitTest
from TCellEditing				import TCellEditing
from TClickSelection			import TClickSelection


class HitArea(frozenset):

	def __eq__(self, other):
		return other in self

class MPopupMenu(
		TCellEditing,
		TClickSelection,
		THitTest,
		TSelection,
	):

	"""
	Popup menu 

	---------------------------------------
	| CORNER   | COLLABEL                 |
	---------------------------------------
	| ROWLABEL | CELL                     |
	|	       |                          |
	|	       |                          |
	---------------------------------------
                  * SPACE

	ALL       Select all if not selected 
	ROWLABEL  Select Row if not selected
	COLLABEL  Select Col if not selected
	CELL      Select Cell, row or col depending on selection model
	SPACE     Only thrue mouse, select nothing


	Use addContext to register menu context

	Builtin contexts:

		hit
			rowlabel	- row label only
			collabel	- col label only
			cell		- cell only
			corner		- corner only
			space		- space only

			row			- row label or cell
			col			- col label or cell

			any			- hit any place of grid

	"""

	HIT_CORNER		= HitArea(('any', 'corner'))
	HIT_ROWLABEL	= HitArea(('any', 'rowlabel', 'row'))
	HIT_COLLABEL	= HitArea(('any', 'collabel', 'col'))
	HIT_CELL		= HitArea(('any', 'row', 'col', 'cell'))
	HIT_SPACE		= HitArea(('any', 'space'))

	def __init__(self, menuFactory):
		self.__menuFactory = menuFactory
		self.__menu = {}

		self.popupListeners = ListenerList()
		self.GetGridWindow().Bind(wx.EVT_MOUSE_EVENTS, self.__onMouseEvent, self.GetGridWindow())
		self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.__onLabelClick, self)
	
	###########################################################################
	# Popup menu

	def __onMouseEvent(self, event):
		if event.RightDown():
			pos = (
				event.GetPosition()[0] + self.GetRowLabelSize(), 
				event.GetPosition()[1] + self.GetColLabelSize(),
			)

			try:
				self.__popup(self.HIT_CELL, pos, *self.hitTest(event.GetPosition()))
			except GridHitSpace:
				self.stopCellEditing()
				self.__popup(self.HIT_SPACE, pos, -1, -1)

		elif event.RightUp():
			pass

		else:
			event.Skip()

	def __onLabelClick(self, event):
		if not self.__popup(
				lang.iif(
					event.GetRow() == -1, 
					lang.iif(
						event.GetCol() == -1, 
						self.HIT_CORNER, 
						self.HIT_COLLABEL
					), 
					self.HIT_ROWLABEL
				),
				event.GetPosition(), 
				event.GetRow(), 
				event.GetCol(),
			):

			event.Skip()


	def __popup(self, hitArea, pos, row = -1, col = -1):
		assert isinstance(row, int), row
		assert isinstance(col, int), col

		#rint "popup(hitArea=%s, pos=%s, row=%s, col=%s)" % (hitArea, pos, row, col)
		if hitArea is not self.HIT_SPACE and not self.isInSelection(row, col):
			self.makeClickSelection(row, col)
	
		menu = self.getPopupMenu(hitArea)

		if menu is not None:
			self.popupListeners.fireEvent(self, 'menuPopup', menu=menu, pos=pos, hitArea=hitArea, row=row, col=col)
			self.PopupMenu(menu, pos)

		return bool(menu)


	def getPopupMenu(self, hitArea):
		if not self.__menu.has_key(hitArea):
			self.__menu[hitArea] = self.__menuFactory(hitArea)
		return self.__menu[hitArea]


if __name__ == '__main__':
	from toolib.wx.grid.test.testPopupMenu import test
	test()
