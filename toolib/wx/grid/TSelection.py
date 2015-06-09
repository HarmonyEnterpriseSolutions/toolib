from toolib.util import lang
import wx.grid

try: _
except NameError: _ = lambda x: x


__all__ = ['TSelection', 'SelectionError']


class SelectionError(Exception):
	_('SelectionError')
	pass


class TSelection(object):
	"""
	Requires:
		GetNumberRows
		GetNumberCols

		GetSelectedRows
		GetSelectedCols
		GetSelectedCells

		GetSelectionBlockBottomRight
		GetSelectionBlockTopLeft
		GetSelectionMode

	Provides:
		getRowSelection		--> returns LineSelection
		getColSelection		--> returns LineSelection
		getCellSelection	--> returns CellSelection
		isInSelection
	"""

	def getRowSelection(self):
		"""
		returns list of selected rows and set of selected cells not in rows
		"""
		rows = set(self.GetSelectedRows())

		blocks = self.__getSelectedBlocks()

		for i in xrange(len(blocks)-1, -1, -1):
			(top, left), (bottom, right) = blocks[i]
			if left == 0 and right  == self.GetNumberCols() - 1:
				rows.update( range(top, bottom + 1) )
				del blocks[i]	# remove block because it is already in rows
		
		cells = self.__getCellSetOfSelectedBlocksAndCells(blocks)
		self.__updateCellSetWithSelectedCols(cells)

		for i in self.__iterPureRows(cells, self.GetNumberCols(), 0):
			rows.add(i)
		
		return LineSelection(rows, cells, 0)


	def getColSelection(self):
		"""
		returns list of selected cols and set of selected cells not in cols
		"""
		cols = set(self.GetSelectedCols())

		blocks = self.__getSelectedBlocks()

		for i in xrange(len(blocks)-1, -1, -1):
			(top, left), (bottom, right) = blocks[i]
			if top  == 0 and bottom == self.GetNumberRows() - 1:
				cols.update( range(left, right + 1) )
				del blocks[i]	# remove block because it is already in cols

		cells = self.__getCellSetOfSelectedBlocksAndCells(blocks)
		self.__updateCellSetWithSelectedRows(cells)

		for i in self.__iterPureRows(cells, self.GetNumberRows(), 1):
			cols.add(i)

		return LineSelection(cols, cells, 1)


	def getCellSelection(self):
		"""
		returns set of selected cells
		"""
		cells = self.__getCellSetOfSelectedBlocksAndCells(self.__getSelectedBlocks())
		self.__updateCellSetWithSelectedRows(cells)
		self.__updateCellSetWithSelectedCols(cells)
		return CellSelection(cells)


	def isInSelection(self, row=-1, col=-1):
		"""
		if row or col >=0
		returns True if this cell, row or column selected
		"""
		if row >= 0 and row in self.getRowSelection():
			return True
		if col >= 0:
			if col in self.getColSelection():
				return True
			if row >= 0:
				if (row, col) in self.getCellSelection():
					return True
		return False

	__modeSelectionGetter = {
		wx.grid.Grid.wxGridSelectRows    : getRowSelection,
		wx.grid.Grid.wxGridSelectColumns : getColSelection,
		wx.grid.Grid.wxGridSelectCells   : getCellSelection,
	}

	def getModeSelection(self):
		return self.__modeSelectionGetter[self.GetSelectionMode()](self)

	def __getSelectedBlocks(self):
		return zip(self.GetSelectionBlockTopLeft(), self.GetSelectionBlockBottomRight())

	
	#def estimateCellSelectionSize(self):
	#	"""
	#	Retured value allways >= real
	#	"""
	#	n = (
	#		  len(self.GetSelectedCols()) * self.GetNumberRows()
	#		+ len(self.GetSelectedRows()) * self.GetNumberCols()
	#		+ len(self.GetSelectedCells())
	#	)
	#
	#	for (top, left), (bottom, right) in self.__getSelectedBlocks():
	#		n += (right - left + 1) * (bottom - top + 1)
	#	
	#	return min(n, self.GetNumberRows() * self.GetNumberCols())


	def __iterPureRows(self, cells, colCount, rowDimension):
		"""
		generates row numbers
		excludes cells from cells
		"""

		d = {}
		for cell in cells:
			x = cell[rowDimension]
			d[x] = d.get(x, 0) + 1

		for i, count in d.iteritems():
			if count == colCount:
				for j in xrange(colCount):
					cells.remove(lang.iif(rowDimension, (j, i), (i, j)))
				yield i
	

	################################################
	# Cell set created with this 3 methods
	#

	def __getCellSetOfSelectedBlocksAndCells(self, blocks):
		cells = set(self.GetSelectedCells())
		for (top, left), (bottom, right) in blocks:
			for i in xrange(top, bottom+1):
				for j in xrange(left, right+1):
					cells.add((i, j))
		return cells

	def __updateCellSetWithSelectedRows(self, cells):
		for i in self.GetSelectedRows():
			for j in xrange(self.GetNumberCols()):
				cells.add((i, j))

	def __updateCellSetWithSelectedCols(self, cells):
		for j in self.GetSelectedCols():
			for i in xrange(self.GetNumberRows()):
				cells.add((i, j))


##############################################################################
# 
#
class CellSelection(object):
	"""
	returned with getCellSelection
	"""
	def __init__(self, cells):
		self.__cellSet = cells
		self.__cells = None

	def getCellSet(self):
		return self.__cellSet

	def getCells(self):
		if self.__cells == None:
			self.__cells = list(self.__cellSet)
			self.__cells.sort()
		return self.__cells

	def getSingleCell(self):
		if len(self.__cellSet) == 1:
			return tuple(self.__cellSet)[0]
		else:
			raise SelectionError, _("Single cell selection expected")

	def __len__(self):
		return len(self.__cellSet)

	def __nonzero__(self):
		return bool(self.__cellSet)

	def __getitem__(self, i):
		return self.getCells()[i]

	def __str__(self):
		return "<CellSelection %s>" % (self.getCells() ,)

	def __contains__(self, cell):
		return tuple(cell) in self.__cellSet

	def _addCell(self, cell):
		self.__cellSet.add(cell)
		self.__cells = None

class LineSelection(CellSelection):
	"""
	returned with getRowSelection
	returned with getColSelection
	"""

	def __init__(self, lineSet, cells, dimension):
		"""
		dimenstion is 0 for row and 1 for col selection
		"""
		CellSelection.__init__(self, cells)
		self.__dimension = dimension
		self.__lineSet = lineSet
		self.__lines = None

	def getLineSet(self):
		return self.__lineSet

	def getLines(self):
		if self.__lines == None:
			self.__lines = list(self.__lineSet)
			self.__lines.sort()
		return self.__lines

	def getSingleLine(self):
		if len(self.__lineSet) == 1:
			return tuple(self.__lineSet)[0]
		else:
			raise SelectionError, (
				_("Single row selection expected"), 
				_("Single column selection expected")
			)[self.__dimension]

	def getPureLines(self):
		if self.isPure():
			return self.getLines()
		else:
			raise SelectionError, (
				_("Pure row selection expected"), 
				_("Pure column selection expected")
			)[self.__dimension]

	def getSingleLineOrCell(self):
		try:
			return self.getSingleLine()
		except SelectionError:
			try:
				return self.getSingleCell()[self.__dimension]
			except SelectionError:
				raise SelectionError, (
					_("Single row or cell selection expected"), 
					_("Single column or cell selection expected")
				)[self.__dimension]

	def __len__(self):
		return len(self.__lineSet)

	def __getitem__(self, i):
		return self.getLines()[i]

	def isPure(self):
		"""
		If only lines selected
		"""
		return not self.getCellSet()

	def getPureSize(self):
		"""
		if only lines selected:
			count of lines selected
		else:
			0
		"""
		if self.isPure():
			return len(self)
		else:
			return 0

	def __str__(self):
		return "<LineSelection %s, except cells %s>" % (self.getLines(), self.getCells())

	def __contains__(self, line):
		return line in self.__lineSet

	def _addCell(self, cell):
		if cell[self.__dimension] not in self.__lineSet:
			super(LineSelection, self)._addCell(cell)

if __name__ == '__main__':

	cells = set([
		(0,0),		(0,1),					(0,3),
		(1,0),		(1,1),		(1,2),		(1,3),
								(2,2),		(2,3),
	])

	for row in TSelection()._Selection__iterPureRows(cells, 4, 0):
		print row

	cells = list(cells)
	cells.sort()
	print cells

	print "--------------------"

	cells = set([
		(0,0),		(0,1),					(0,3),
		(1,0),		(1,1),		(1,2),		(1,3),
								(2,2),		(2,3),
	])

	for row in TSelection()._Selection__iterPureRows(cells, 3, 1):
		print row

	cells = list(cells)
	cells.sort()
	print cells

