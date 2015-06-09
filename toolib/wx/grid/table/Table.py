#################################################################
# Program: Toolib
"""
	Grid model.
	Extension of PyGridTableBase, defines listener support and helper methods to generate evenrs.
	You can add Grids as listeners to notify them about table changes.

		def addGridTableListener(self, l):		\ registers wx.grid.Grid as listener
		def removeGridTableListener(self, l):	/ 

		def fireRowsAppended(self, count):		\
		def fireRowsInserted(self, pos, count):	 \
		def fireRowsDeleted(self, pos, count):	  \  	call on any rows or cols add/remove operation
		def fireColsAppended(self, count):		  /		(without data changing) Causes grid::Redimension
		def fireColsInserted(self, pos, count):	 /
		def fireColsDeleted(self, pos, count):	/
		def fireTableUpdated(self):				call to force listeners reload table values
		
		def fireTableStructureChanging(self):	call before table dimensions and data changed
		def fireTableStructureChanged(self):	call after table dimensions and data changed
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2008/05/22 15:31:06 $"
__version__ = "$Revision: 1.4 $"
# $Source: D:/HOME/cvs/toolib/wx/grid/table/Table.py,v $
#
#################################################################
from wxGridTableBase	import wxGridTableBase
from MTableMessaging	import MTableMessaging
from TAttrCreator		import TAttrCreator
from toolib				import debug


class Table(wxGridTableBase, MTableMessaging, TAttrCreator):
	def __init__(self):
		wxGridTableBase.__init__(self)
		MTableMessaging.__init__(self)

	def getColumnId(self, index):
		# used in TConfigurable, MColumnState
		return str(index)
