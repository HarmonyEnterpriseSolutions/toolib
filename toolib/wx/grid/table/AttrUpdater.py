import wx
import wx.grid
from toolib.event import *

DEBUG = 0
if DEBUG:
	MSG = {
		wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES	: 'REQUEST_VIEW_GET_VALUES',
		wx.grid.GRIDTABLE_NOTIFY_ROWS_INSERTED		: 'NOTIFY_ROWS_INSERTED',
		wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED		: 'NOTIFY_ROWS_APPENDED',
		wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED		: 'NOTIFY_ROWS_DELETED',
		wx.grid.GRIDTABLE_NOTIFY_COLS_INSERTED		: 'NOTIFY_COLS_INSERTED',
		wx.grid.GRIDTABLE_NOTIFY_COLS_APPENDED		: 'NOTIFY_COLS_APPENDED',
		wx.grid.GRIDTABLE_NOTIFY_COLS_DELETED		: 'NOTIFY_COLS_DELETED',
	}

def AttrUpdater(table, kind):
	"""
	Factory
	"""
	return eval(kind)(table)


class BaseAttrUpdater(object):

	TABLE_UPDATED = wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES

	def __init__(self, table):
		assert table

		self.table = table
		if table.CanHaveAttributes():
			self.ap = table.GetAttrProvider()
		else:
			raise NotImplementedError, 'Table not support attributes'

	def fireFullUpdate(self):
		self.fireUpdate(0, self.getNumberLines())
	
	def processTableMessage(self, message, tableUpdate):
		if tableUpdate:
			self.processTableUpdateMessage(message)
		else:
			self.processTableResizeMessage(message)


class TTopAnchored(object):
	"""
	Provides:
		processTableResizeMessage
		processTableUpdateMessage

	Requires:
		fireUpdate
		updateAttrLines
		getNumberLines
		INSERTED
		APPENDED
		DELETED
	"""
	
	def processTableResizeMessage(self, message):
		if DEBUG: print 'TTopAnchored::processTableResizeMessage', MSG[message.Id], message.CommandInt, message.CommandInt2
		if   message.Id == self.INSERTED and message.CommandInt2 > 0:
			self.updateAttrLines(message.CommandInt, message.CommandInt2)
		elif message.Id == self.DELETED and message.CommandInt2 > 0:
			self.updateAttrLines(message.CommandInt, -message.CommandInt2)

	def processTableUpdateMessage(self, message):
		"""
		simmilar to processTableResizeMessage
		but used in 
			fireTableStructureChanging
			fireTableStructureChanged
		cycle
		"""
		if DEBUG: print 'TTopAnchored::processTableUpdateMessage', MSG[message.Id], message.CommandInt, message.CommandInt2
		if message.Id == self.DELETED:
			self.processTableResizeMessage(message)

	def fireTableResize(self, message):
		if DEBUG: print 'TTopAnchored::fireUpdate', MSG[message.Id], message.CommandInt, message.CommandInt2
		if   message.Id == self.INSERTED and message.CommandInt2 > 0:
			self.fireUpdate(message.CommandInt, message.CommandInt2)
		
		elif message.Id == self.APPENDED and message.CommandInt > 0:
			self.fireUpdate(self.getNumberLines() - message.CommandInt, message.CommandInt)
		


class TBottomAnchored(TTopAnchored):
	"""
	Provides:
		processTableResizeMessage
		processTableUpdateMessage

	Requires:
		fireUpdate
		updateAttrLines
		getNumberLines
		INSERTED
		APPENDED
		DELETED
	"""
	
	def processTableUpdateMessage(self, message):
		if DEBUG: print 'TBottomAnchored::processTableUpdateMessage', MSG[message.Id], message.CommandInt, message.CommandInt2

		if   message.Id == self.INSERTED and message.CommandInt2 > 0:
			# insert empty attrs from start
			self.updateAttrLines(0, message.CommandInt2)
		
		elif message.Id == self.APPENDED and message.CommandInt > 0:
			# insert empty attrs from start
			self.updateAttrLines(0, message.CommandInt)
		
		elif message.Id == self.DELETED and message.CommandInt2 > 0:
			# remove from start
			self.updateAttrLines(0, -message.CommandInt2)
			pass


class Row(BaseAttrUpdater):
	"""
	Provides:
		INSERTED
		APPENDED
		DELETED

		fireUpdate
		updateAttrLines
		getNumberLines
	"""

	INSERTED = wx.grid.GRIDTABLE_NOTIFY_ROWS_INSERTED
	APPENDED = wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED
	DELETED  = wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED

	def updateAttrLines(self, pos, count):
		if DEBUG: print 'UpdateAttrRows', pos, count
		self.ap.UpdateAttrRows(pos, count)

	def getNumberLines(self):
		return self.table.GetNumberRows()

	def fireUpdate(self, pos, count):
		self.table.attrUpdateListeners.fireEvent(self.table, 'updateRowAttrs', pos=pos, count=count)


class Col(BaseAttrUpdater):
	"""
	Provides:
		INSERTED
		APPENDED
		DELETED

		fireUpdate
		updateAttrLines
		getNumberLines
	"""

	INSERTED = wx.grid.GRIDTABLE_NOTIFY_COLS_INSERTED
	APPENDED = wx.grid.GRIDTABLE_NOTIFY_COLS_APPENDED
	DELETED  = wx.grid.GRIDTABLE_NOTIFY_COLS_DELETED

	def updateAttrLines(pos, count):
		self.ap.UpdateAttrCols(self, pos, count)

	def getNumberLines(self):
		return self.table.GetNumberCols()

	def fireUpdate(self, pos, count):
		self.table.attrUpdateListeners.fireEvent(self.table, 'updateColAttrs', pos=pos, count=count)
			

#########################################################
# Implementations

class RowTopAnchored   (Row, TTopAnchored):
	pass

class ColLeftAnchored  (Col, TTopAnchored):
	pass

class RowBottomAnchored(Row, TBottomAnchored):
	pass

class ColRightAnchored (Col, TBottomAnchored):
	pass
