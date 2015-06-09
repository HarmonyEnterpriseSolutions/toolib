
class TNumberDataLines(object):
	"""
	Adapter used in 
		TTableClipboard

	Requires:
		
		getNumberDataRows or GetNumberRows
		getNumberDataCols or GetNumberCols

	Provides:

		_getNumberDataRows
		_getNumberDataCols

		_getBaseDataRow
		_getBaseDataCol
	"""

	def _getBaseDataRow(self):
		if hasattr(self, 'getBaseDataRow'):
			return self.getBaseDataRow()
		else:
			return 0
		
	def _getBaseDataCol(self):
		if hasattr(self, 'getBaseDataCol'):
			return self.getBaseDataCol()
		else:
			return 0

	def _getNumberDataRows(self):
		if hasattr(self, 'getNumberDataRows'):
			return self.getNumberDataRows()
		else:
			return self.GetNumberRows() - self._getBaseDataRow()

	def _getNumberDataCols(self):
		if hasattr(self, 'getNumberDataCols'):
			return self.getNumberDataCols()
		else:
			return self.GetNumberCols() - self._getBaseDataCol()
