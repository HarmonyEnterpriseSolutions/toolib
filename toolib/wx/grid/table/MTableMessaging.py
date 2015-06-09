import wx.grid
from AttrUpdater               import AttrUpdater
from toolib                    import debug
from toolib.event.ListenerList import ListenerList


class MTableMessaging(object):
	"""
	Requires:
		getWxTable			returns self if not defined in base class
		GetNumberRows
		GetNumberCols

	Messages:
	    GRIDTABLE_REQUEST_VIEW_GET_VALUES		(), calls Grid::GetModelValues()
	    GRIDTABLE_REQUEST_VIEW_SEND_VALUES		(), calls Grid::SetModelValues()
	
	    GRIDTABLE_NOTIFY_ROWS_INSERTED          (pos, count) \
	    GRIDTABLE_NOTIFY_ROWS_APPENDED          (count)       \
	    GRIDTABLE_NOTIFY_ROWS_DELETED           (pos, count)   \
	                                                            > calls Grid::Redimension(msg)
	    GRIDTABLE_NOTIFY_COLS_INSERTED          (pos, count)   /
	    GRIDTABLE_NOTIFY_COLS_APPENDED          (count)       /
	    GRIDTABLE_NOTIFY_COLS_DELETED           (pos, count) /
	"""
	def __init__(self):
		self.__listeners = []
		self.__oldSize = None
		self.__attrUpdaters = []
		
		self.attrUpdateListeners = ListenerList()

	def addAttrUpdater(self, kind):
		self.__attrUpdaters.append(AttrUpdater(self, kind))

	def getWxTable(self):
		return self
	
	def addGridTableListener(self, l):
		self.__listeners.append(l)

	def removeGridTableListener(self, l):
		try:
			self.__listeners.remove(l)
		except ValueError:
			pass

	def __fireMessage(self, message, tableUpdate=False):
		"""
		tableUpdate is True only when fired from fireTableStructureChanged
		"""
		assert message.Id != wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES
		
		if message.Id == wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED:
			# do DELETE before ProcessTableMessage
			for au in self.__attrUpdaters:
				au.processTableMessage(message, tableUpdate)
		
		for l in self.__listeners:
			l.ProcessTableMessage(message)

		# remember oldSize for the next fireTableStructureChanged call
		#self.__oldSize = self.GetNumberRows(), self.GetNumberCols()

		if message.Id != wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED:
			# do APPEND, INSERT after ProcessTableMessage
			for au in self.__attrUpdaters:
				au.processTableMessage(message, tableUpdate)


		# partial attributes update in case of fireRowsXXX, fireColsXXX
		if not tableUpdate:
			for au in self.__attrUpdaters:
				au.fireTableResize(message)


	def fireRowsAppended(self, count):
		assert debug.trace("rows appended: %s" % count)
		self.__fireMessage(wx.grid.GridTableMessage(self.getWxTable(), wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, count))

	def fireRowsInserted(self, pos, count):
		assert debug.trace("rows inserted: %s, %s" % (pos, count))
		self.__fireMessage(wx.grid.GridTableMessage(self.getWxTable(), wx.grid.GRIDTABLE_NOTIFY_ROWS_INSERTED, pos, count))

	def fireRowsDeleted(self, pos, count):
		assert debug.trace("rows deleted: %s, %s" % (pos, count))
		self.__fireMessage(wx.grid.GridTableMessage(self.getWxTable(), wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED, pos, count))

	def fireColsAppended(self, count):
		assert debug.trace("cols appended: %s" % count)
		self.__fireMessage(wx.grid.GridTableMessage(self.getWxTable(), wx.grid.GRIDTABLE_NOTIFY_COLS_APPENDED, count))

	def fireColsInserted(self, pos, count):
		assert debug.trace("cols inserted: %s, %s" % (pos, count))
		self.__fireMessage(wx.grid.GridTableMessage(self.getWxTable(), wx.grid.GRIDTABLE_NOTIFY_COLS_INSERTED, pos, count))

	def fireColsDeleted(self, pos, count):
		assert debug.trace("cols deleted: %s, %s" % (pos, count))
		self.__fireMessage(wx.grid.GridTableMessage(self.getWxTable(), wx.grid.GRIDTABLE_NOTIFY_COLS_DELETED, pos, count))

	def fireTableUpdated(self):
		"""
		Table values was updated
		attrUpdateMessage is for internal use
		"""
		assert debug.trace("table updated")
		
		message = wx.grid.GridTableMessage(self.getWxTable(), wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)

		for l in self.__listeners:
			l.ProcessTableMessage(message)

		for au in self.__attrUpdaters:
			au.fireFullUpdate()


	def fireTableStructureChanging(self):
		"""
		Call before major table data changing
		"""
		assert debug.trace("structure changing")
		assert self.__oldSize is None
		self.__oldSize = self.GetNumberRows(), self.GetNumberCols()


	def fireTableStructureChanged(self):
		"""
		Call after major table data changing
		"""
		assert debug.trace("structure changed")
		assert self.__oldSize is not None

		oldRows, oldCols = self.__oldSize
		self.__oldSize = None

		for old, new, delmsg, addmsg in (
			(oldRows, self.GetNumberRows(), wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED, wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED),
			(oldCols, self.GetNumberCols(), wx.grid.GRIDTABLE_NOTIFY_COLS_DELETED, wx.grid.GRIDTABLE_NOTIFY_COLS_APPENDED),
		):
			if new < old:
				self.__fireMessage(wx.grid.GridTableMessage(self.getWxTable(), delmsg, new, old-new), True)
			elif new > old:
				self.__fireMessage(wx.grid.GridTableMessage(self.getWxTable(), addmsg, new-old), True)

		self.fireTableUpdated()

		self.__oldSize = None
