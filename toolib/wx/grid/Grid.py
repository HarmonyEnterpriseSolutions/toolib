#################################################################
# Program: Toolib
"""
Grid implementation

Grid 
	Control(View) itselfs. Can be used with only Table classes.


"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2012/10/09 09:56:14 $"
__version__ = "$Revision: 1.31 $"
# $Source: D:/HOME/cvs/toolib/wx/grid/Grid.py,v $
#
#################################################################

import wx

from toolib.util import lang

from MGridMessaging			import MGridMessaging
from MGridModelListeners	import MGridModelListeners
from TCellEditing			import TCellEditing
from TCellRect				import TCellRect
from TCursor				import TCursor
from THitTest				import THitTest		# includes ScrollTranslation
from TSelectedRect			import TSelectedRect
from TSelection				import TSelection
from TColumnExtraWidth		import TColumnExtraWidth

from wxGrid import wxGrid as __super__

class Grid(
		MGridModelListeners,
		MGridMessaging,
		__super__,
		TCellEditing,
		TCellRect,
		TCursor,
		THitTest,
		TSelectedRect,
		#TSelection,	# already in TSelectedRect
		TColumnExtraWidth,
	):
	"""
	1. Messaging Table support
	2. modelListeners
		onModelChanging (model, oldModel)
		onModelChanged  (model, oldModel)
	"""
	__INITARGS__ = ('parent', 'id', 'pos', 'size', 'style', 'name')

	def __init__(self, *args, **kwargs):
		args, kwargs = lang.normalize_args(args, kwargs, self.__INITARGS__)
		kwargs['style'] = kwargs.get('style', 0) | wx.WANTS_CHARS
		__super__.__init__(self, *args, **kwargs)
		MGridModelListeners.__init__(self)
	


if __name__ == '__main__':

	def oninit(self):
		from Grid import Grid
		g = Grid(self, -1)

		from table.Table import Table
		class MyTable(Table):
			def GetNumberRows(self):
				return 3

			def GetNumberCols(self):
				return 3
		
		g.SetTable(MyTable())
		#g.AppendRows(1)
		#g.AppendCols(1)
		self.grid = g

	def ondestroy(self):
		self.grid.Destroy()

	from toolib.wx.TestApp import TestApp
	TestApp(oninit, ondestroy).MainLoop()
