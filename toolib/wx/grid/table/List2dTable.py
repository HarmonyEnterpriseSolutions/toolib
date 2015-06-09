#################################################################
# Program: Toolib
"""
	Implementation of Table
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2007/08/06 16:03:37 $"
__version__ = "$Revision: 1.1 $"
# $Source: D:/HOME/cvs/toolib/wx/grid/table/List2dTable.py,v $
#
#################################################################
import wx
from Table import Table
import toolib.util.lists as lists

class NativeRowLabelSequence(object):
	def __init__(self, table):
		self._table = table
	def __getitem__(self, index):
		return Table.GetRowLabelValue(self._table, index)
		       
class NativeColLabelSequence(object):
	def __init__(self, table):
		self._table = table
	def __getitem__(self, index):
		return Table.GetColLabelValue(self._table, index)

class EmptyStringSequence(object):
	def __getitem__(self, index):
		return ""

LABELS_NATIVE = NotImplemented
LABELS_EMPTY  = None

class List2dTable(Table):
	"""
	Implements simple Grid table with internal data

	User can install background row label sequences

	.getRowLabelSequence \  
	.setRowLabelSequence /

	.getColLabelSequence \
	.setColLabelSequence /

	SetRowLabelValue, SetColLabelValue will superseed background sequence.
	GetRowLabelValue, GetColLabelValue will return previous set value or value returned by sequence
	"""

	LABELS_NATIVE = LABELS_NATIVE
	LABELS_EMPTY  = LABELS_EMPTY

	def __init__(self, *p, **pp):
		"""
		See _init for arguments
		"""
		Table.__init__(self)
		self._init(*p, **pp)

	def _init(self, data=[], rowLabelSequence=LABELS_NATIVE, colLabelSequence=LABELS_NATIVE):
		"""
		rowLabels \ list or sequence, including infinite
		colLabels / None in sequence forces basic value

		"""
		self._data = data
		if rowLabelSequence == self.LABELS_EMPTY: 
			rowLabelSequence = EmptyStringSequence()
		elif rowLabelSequence == self.LABELS_NATIVE: 
			rowLabelSequence = NativeRowLabelSequence(self)

		if colLabelSequence == self.LABELS_EMPTY: 
			colLabelSequence = EmptyStringSequence()
		elif colLabelSequence == self.LABELS_NATIVE: 
			colLabelSequence = NativeColLabelSequence(self)

		self._rowLabelSequence = rowLabelSequence
		self._colLabelSequence = colLabelSequence

		self._rowLabels = []
		self._colLabels = []

	def getRowLabelSequence(self):	return self._rowLabelSequence
	def getColLabelSequence(self):	return self._colLabelSequence
	def setRowLabelSequence(self, seq):	self._rowLabelSequence = seq
	def setColLabelSequence(self, seq):	self._colLabelSequence = seq

	def GetNumberRows(self):
		return len(self._data)

	def GetNumberCols(self):
		return max(map(len, self._data)+[0])

	def IsEmptyCell(self, row, col):
		try:
			return self._data[row][col] is None
		except IndexError:
			return True

	def GetValue(self, row, col):
		try:
			return self._data[row][col]
		except IndexError:
			return None

	def SetValue(self, row, col, value):
		#rint "list2dtable.SetValue", row, col, value
		lists.setItemSafe(self._data[row], col, value)

	def AppendRows(self, count):
		for i in xrange(count):
			self._data.append([])
		self.fireRowsAppended(count)

	def InsertRows(self, pos, count):
		for i in xrange(count):
			self._data.insert(pos, [])
		self.fireRowsInserted(pos, count)

	def DeleteRows(self, pos, count):
		self._data = self._data[:pos] + self._data[pos+count:]
		self.fireRowsDeleted(pos, count)

	def AppendCols(self, count):
		self._data = [row + [None] * count for row in self._data]
		self.fireColsAppended(count)

	def InsertCols(self, pos, count):
		self._data = [row[:pos] + ([None]*count) + row[pos:] for row in self._data]
		self.fireColsInserted(pos, count)

	def DeleteCols(self, pos, count):
		self._data = [row[:pos] + row[pos+count:] for row in self._data]
		self.fireColsDeleted(pos, count)

	def _setData(self, data):
		"""
		see init for arguments
		"""
		self.fireTableStructureChanging()
		self._data = data
		self.fireTableStructureChanged()

	def _getData(self):
		return self._data

	def GetRowLabelValue(self, index):
		try:
			if self._rowLabels[index] is None: return self._rowLabelSequence[index]
			return self._rowLabels[index]
		except IndexError:
			return self._rowLabelSequence[index]

	def GetColLabelValue(self, index):
		try:
			if self._colLabels[index] is None: self._colLabelSequence[index]
			return self._colLabels[index]
		except IndexError:
			return self._colLabelSequence[index]

	def SetRowLabelValue(self, index, value):
		lists.setItemSafe(self._rowLabels, index, value)

	def SetColLabelValue(self, index, value):
		lists.setItemSafe(self._colLabels, index, value)

	# now really usefull methods
	def clear(self):
		self.removeRows(range(len(self._rows)-1, -1, -1))

	def appendRows(self, rows):
		self._data.extend(rows)
		self.fireRowsAppended(len(rows))
		


if __name__ == '__main__':
	
	def oninit(self):
		from toolib.wx.grid.Grid import Grid
		
		g = Grid(self, -1)

		m = List2dTable([
			[11,12,13,14,15],# * 10,
			[21,22,23,24,25],# * 10,
			[31,32,33,34,35],# * 10,
			[41,42,43,44,45],# * 10,
			[51,52,53,54],# * 10,
		], None, None)

		g.SetTable(m)

		g.InsertRows(1,2)
		g.InsertCols(1,2)

		g.DeleteRows(1,2)
		g.DeleteCols(1,2)

		g.AppendRows(1)
		g.AppendCols(1)

		#m._setData([[1,2,3], [3,4,5]])

		g.SetColLabelValue(0, 'AAA')
		g.SetRowLabelValue(1, 'BBB')

		#g.AppendRows(10)
		#g.AppendCols(1000)

	from toolib.wx.TestApp import TestApp
	TestApp(oninit).MainLoop()
