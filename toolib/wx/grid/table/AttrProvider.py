"""
This is fully pythonic attribute provider
not derived from C

Normally its subclass is used with AbstractGridTable
"""
import wx
import wx.grid

from TAttrCreator import TAttrCreator

#wx.grid.GridCellAttrProvider, 

class AttrProvider(TAttrCreator):

	def __init__(self):
		#wx.grid.GridCellAttrProvider.__init__(self)
		self._table = None

	def init(self):
		"""
		deferred construction until table set
		"""
		pass

	def setTable(self, table):
		self._table = table
		self.init(table)

	def getTable(self):
		return self._table

	def GetAttr(self, row, col, kind):
		"""
		Override this to customize table attributes
		Returns GridCellAttr

		NOTE: call attr.IncRef() before returning cell attribute

		TODO: this is called too often, make some alternative
		e.g. GetRowAttr, GetCollAttr to cache a little and call fewer
		"""
		return None
	
	def SetAttr(self, attr, row, col):
		#raise NotImplementedError, 'abstract'
		pass

	def SetColAttr(self, attr, col):
		raise NotImplementedError, 'abstract'
	
	def SetRowAttr(self, attr, row):
		raise NotImplementedError, 'abstract'
	
	def UpdateAttrRows(self, pos, numrows):
		pass
	
	def UpdateAttrCols(self, pos, numcols):
		pass
	
