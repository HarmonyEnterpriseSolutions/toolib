import sys
import xlrd
from datetime import datetime

xlConv = {
	xlrd.XL_CELL_DATE : lambda value, book: datetime(*xlrd.xldate_as_tuple(value, book.datemode)),
}
xlConvDefault = lambda value, book: value
	
class Book(object):

	def __init__(self, filename):
		self._book = xlrd.open_workbook(filename)

	def __getitem__(self, index):
		return Sheet(self, self._book.sheets()[index])

	def __len__(self):
		return len(self._book.sheets())


class Sheet(object):

	def __init__(self, book, sheet):
		self.book = book
		self._sheet = sheet

	def __getitem__(self, row):
		return Row(self, self._sheet.row(row))

	def __len__(self):
		return self._sheet.nrows

	def __getattr__(self, name):
		return getattr(self._sheet, name)


class Row(object):

	def __init__(self, sheet, row):
		self.sheet = sheet
		self._row = row

	def __getitem__(self, col):
		return Cell(self, self._row[col])

	def __len__(self):
		return len(self._row)


class Cell(object):

	def __init__(self, row, cell):
		self.row = row
		self._cell = cell
		
	value = property(lambda self: xlConv.get(self._cell.ctype, xlConvDefault)(self._cell.value, self.row.sheet.book._book))
		
	def __unicode__(self):
		return unicode(self.value)


def main(filename, delimiter='\t', encoding='cp1251'):
	book = Book(filename)
	for sheet in book:
		f = open(sheet.name + u'.csv', 'wt')
		for row in sheet:
			print >>f, delimiter.join((unicode(cell).encode(encoding) for cell in row))
		f.close()


if __name__ == '__main__':
	main(*sys.argv[1:])