class TCellRect(object):
	"""
	composes into Grid

	Requires:
		GetColSize
		GetRowSize
		GetColLabelSize
		GetRowLabelSize
		CellToRect

	Provides:
		getColLabelPosition
		getRowLabelPosition
		getColLabelRect
		getRowLabelRect
		getCellRect
	"""
	def __getCellPosition(self, index, fnCellSize):
		x = 0
		for i in xrange(index):
			x += fnCellSize(i)
		return x

	def getColLabelPosition(self, col):
		return self.__getCellPosition(col, self.GetColSize), 0

	def getRowLabelPosition(self, row):
		return 0, self.__getCellPosition(row, self.GetRowSize)

	def getColLabelRect(self, col):
		return self.getColLabelPosition(col) + (self.GetColSize(col), self.GetColLabelSize())

	def getRowLabelRect(self, row):
		return self.getRowLabelPosition(row) + (self.GetRowLabelSize(), self.GetRowSize(row))

	def getCellRect(self, row, col):
		if row < 0:
			return self.getColLabelRect(col)
		elif col < 0:
			return self.getRowLabelRect(row)
		else:
			return self.CellToRect(row, col)
