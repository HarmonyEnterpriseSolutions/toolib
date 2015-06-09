
class TNumberDataLines(object):
	"""
	Adapter used in 
		TTableClipboard

	Requires:

		GetTable	

	Provides:

		getBaseDataRow
		getBaseDataCol
		getNumberDataRows
		getNumberDataCols

	"""

	def getBaseDataRow(self):
		t = self.GetTable()
		if hasattr(t, 'getBaseDataRow'):
			return t.getBaseDataRow()
		else:
			return 0
		
	def getBaseDataCol(self):
		t = self.GetTable()
		if hasattr(t, 'getBaseDataCol'):
			return t.getBaseDataCol()
		else:
			return 0

	def getNumberDataRows(self):
		t = self.GetTable()
		if hasattr(t, 'getNumberDataRows'):
			return t.getNumberDataRows()
		else:
			return t.GetNumberRows()

	def getNumberDataCols(self):
		t = self.GetTable()
		if hasattr(t, 'getNumberDataCols'):
			return t.getNumberDataCols()
		else:
			return t.GetNumberCols()
