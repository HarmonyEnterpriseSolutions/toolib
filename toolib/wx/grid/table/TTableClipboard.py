import wx
from MTableMessaging             import MTableMessaging
from toolib.wx.util.clipboard    import TableDataObject, ClipboardError
from TNumberDataLines               import TNumberDataLines
from toolib import debug

try: _
except: _ = lambda s: s


DEBUG = 0

class ClipboardPasteError(ClipboardError):
	_('ClipboardPasteError')
	pass

class ClipboardCopyError(ClipboardError):
	_('ClipboardCopyError')
	pass



class TTableClipboard(TNumberDataLines):
	"""
	Requires:
		
		getValueAsText
		setValueAsText
		
		fireTableUpdated

		getNumberDataRows or GetNumberRows
		getNumberDataCols or GetNumberCols

		AppendRows
		AppendCols


	Provides:

		eraseRect
		copy
		paste

	"""

	def __cellLocationName(self, row, col):
		return _("column '%s', row '%s'" % (self.GetColLabelValue(col) or col, self.GetRowLabelValue(row) or row))

	def __isRectOk(self, rect):
		dataRect = self.getDataRect()
		return dataRect.Contains(rect.getTopLeft()) and dataRect.Contains(rect.getBottomRight())

	def __cantAppend(self, name):
		# try to call Append${name}(0)
		try:
			getattr(self, 'Append' + name)(0)
		except wx.PyAssertionError:
			return True
		else:
			return False

	def eraseRect(self, rect):
		row = rect.GetTop()
		col = rect.GetLeft()
		for r in xrange(row, row + rect.GetHeight()):
			for c in xrange(col, col + rect.GetWidth()):
				try:
					self.setValueAsText(r, c, "")
				except:
					if DEBUG: raise
					pass
		self.fireTableUpdated()

	def copy(self, rect):

		row = rect.GetTop()
		col = rect.GetLeft()

		table = []

		for r in xrange(row, row + rect.GetHeight()):
			row = [None] * rect.GetWidth()
			for i, c in enumerate(xrange(col, col + rect.GetWidth())):
				#rint row + r, col + c
				#rint self.GetValue(row + r, col + c)
				try:
					row[i] = self.getValueAsText(r, c)
				except:
					if DEBUG: raise
					row[i] = ""
			table.append(row)

		TableDataObject.setClipboardData(table)


	def paste(self, row, col):
		if col < 0:
			raise ClipboardPasteError, _("Please, select single cell or column if table is empty")

		if row < 0: 
			# column label selected. assume origin is at first row
			row = 0

		table = TableDataObject.getClipboardData()

		if not table:
			raise ClipboardPasteError, _("Nothing to paste")

		#rint "pasting table %s x %s at (%s, %s)" % (len(table), len(table[0]), row, col)
		#rint "data", table

		height = len(table)
		width  = len(table[0])

		if row + height > self._getBaseDataRow() + self._getNumberDataRows() and self.__cantAppend('Rows'):
			raise ClipboardPasteError, _("Data with %s rows does not fits in %s rows" % (height, self._getBaseDataRow() + self._getNumberDataRows() - row))

		if col + width  > self._getBaseDataCol() + self._getNumberDataCols() and self.__cantAppend('Cols'):
			raise ClipboardPasteError, _("Data with %s columns does not fits in %s columns" % (width, self._getBaseDataCol() + self._getNumberDataCols() - col))

		try:

			for i, r in enumerate(xrange(row, row + height)):

				if r >= self._getBaseDataRow() + self._getNumberDataRows():
					self.AppendRows(1)
					if r >= self._getNumberDataRows():
						debug.error("AppendRows failed")
						break

				for j, c in enumerate(xrange(col, col + width)):

					if c >= self._getBaseDataCol() + self._getNumberDataCols():
						self.AppendCols(1)
						if c >= self._getNumberDataCols():
							debug.error("AppendCols failed")
							break

					try:
						self.setValueAsText(r, c, table[i][j])
					except:
						if DEBUG: raise
						pass

		finally:
			self.fireTableUpdated()

