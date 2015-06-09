import wx
from toolib.wx.TestApp import TestApp
from toolib.wx.grid.Grid  import Grid
from toolib.wx.grid.table.List2dTable import List2dTable
from toolib.wx.grid.MPopupContextMenu import MPopupContextMenu

class MyGrid(Grid, MPopupContextMenu):

	def __init__(self, *args, **kwargs):
		Grid.__init__(self, *args, **kwargs)
		MPopupContextMenu.__init__(self)

	def getPopupMenuConfig(self):
		return { 
			'items' : [
				'corner',
				'--',
				'sortColumn',
				'--',
				'insertColumn',
				'appendColumn',
				'removeColumn',
				'--',
				'insertRow',
				'appendRow',
				'removeRow',
				'--',
				'excelExport',
			],
		}

def test(selectionMode):
	def oninit(self):
		
		self.actions = {
			'--' : {
				'kind'		: wx.ITEM_SEPARATOR,
			},
				
			'corner' : {
				'text'	: 'Corner',
				'context' : {
					'hit' : ['corner'],
				}
			},
			'sortColumn' : {
				'text'	: 'Sort Column',
				'context' : {
					'hit' : ['collabel'],
				}
			},
			'insertColumn' : {
				'text'	: 'Insert Column',
				'context' : {
					'hit' : ['collabel'],
				}
			},
			'appendColumn' : {
				'text'	: 'Append Column',
				'context' : {
					'hit' : ['collabel', 'space'],
				}
			},
			'removeColumn' : {
				'text'	: 'Remove Column',
				'context' : {
					'hit' : ['collabel'],
				}
			},
			'insertRow' : {
				'text'	: 'Insert Row',
				'context' : {
					'hit' : ['row'],
				}
			},
			'appendRow' : {
				'text'	: 'Append Row',
				'context' : {
					'hit' : ['row', 'space'],
				}
			},
			'removeRow' : {
				'text'	: 'Remove Row',
				'context' : {
					'hit' : ['row'],
					'selection' : ['single-row', 'single-cell'],
				},
			},
			'excelExport' : {
				'text'	: 'Export to Excel',
			},

		}

		self.grid = MyGrid(self, -1)
		self.grid.SetTable(List2dTable())
		self.grid.AppendRows(4)
		self.grid.AppendCols(4)
		self.grid.SetSelectionMode(selectionMode)

		#self.grid.SetSelectionMode(self.grid.wxGridSelectCells)
		#self.grid.SetSelectionMode(self.grid.wxGridSelectRows)
		#self.grid.SetSelectionMode(self.grid.wxGridSelectColumns)

	def ondestroy(self):
		pass

	TestApp(oninit, ondestroy).MainLoop()

if __name__ == '__main__':
	test(Grid.wxGridSelectCells)
