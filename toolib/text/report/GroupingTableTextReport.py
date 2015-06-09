from TextReport import TextReport, TextReportIterator


class GroupingTableTextReport(TextReport):

	def getIteratorClass(self):
		return GroupingTableTextReportIterator


class GroupingTableTextReportIterator(TextReportIterator):

	def __init__(self, data):
	    # blocks, from inner to outer
		self._iterator = iter(data)
		self._prevRow = {}		# block : row
		self._row = None		# block : row
		self._prevBlock = None
		self._keepRow = False

	def nextRow(self, block):
		#rint "NEXT ROW", block.getId()
		try:
			if self._row is None or not self._keepRow and self._prevBlock is not block.getParent():
				#rint "FETCH ROW"
				self._row = self._iterator.next()
			if self._isEndOfGrouping(block):
				row = None
			else:
				row = self._row
		except StopIteration:
			#rint "STOP"
			self._row = None
			row = None

		self._keepRow = row is None
		self._prevRow[block] = row
		self._prevBlock = block

		#print "RETURN", row
		return row

	def _isEndOfGrouping(self, block):
		oldRow = self._prevRow.get(block)
		if oldRow:
			fields = block.getGroupingFields()
			oldData = tuple((   oldRow.get(field) for field in fields))
			data    = tuple((self._row.get(field) for field in fields))
			return data != oldData
		else:
			return False
	
