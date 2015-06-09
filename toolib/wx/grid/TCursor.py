class TCursor(object):
	"""
	Adds cursor-handling convenient methods

	Requires:
		GetGridCursorCol
		GetGridCursorRow
		
		SetGridCursor

	Provides:
		getGridCursor
		setGridCursor
	"""

	def getGridCursor(self):
		"""
		Convenience python method
		"""
		return self.GetGridCursorRow(), self.GetGridCursorCol()

	def setGridCursor(self, row=-1, col=-1, scrollToCursor=True):
		"""
		can preserve row or col if row == -1 or col == -1
		also can scroll to cursor
		"""
		oldRow, oldCol = self.getGridCursor()

		if row == -1:
			row = oldRow

		if col == -1:
			col = oldCol

		if oldRow != row or oldCol != col:
			self.SetGridCursor(row, col)

		if scrollToCursor:
			self.MakeCellVisible(row, col)
