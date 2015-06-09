from cStringIO import StringIO
from datetime import datetime, time
from toolib import debug


_PARSERS = {}


###############################################################################
# CSV
from csv import reader, Sniffer
def parseCsv(fp, encoding=None):
	
	if hasattr(fp, 'read'):
		text = fp.read()
	else:
		text = fp
	
	if not text:
		return iter(())

	dialect = Sniffer().sniff(text)

	#for i in dir(dialect):
	#	print i, repr(getattr(dialect, i))

	r = reader(StringIO(text), dialect=dialect)

	if encoding:
		r = TupleValuesDecoder(r, encoding)

	return r


class TupleValuesDecoder(object):

	def __init__(self, reader, encoding):
		self._reader = reader
		self._encoding = encoding
			
	def __iter__(self):
		return self
			
	def next(self):
		return tuple((v.decode(self._encoding) for v in self._reader.next()))



_PARSERS['CSV'] = parseCsv
del parseCsv




try:
	import xlrd
except ImportError:
	debug.warning("parsing DBF is not supported, please, install xlrd")
else:

	class XlsRowIterator(object):

		def __init__(self, book, sheet, index=0):
			self._book = book
			self._sheet = sheet
			self._index = index
			
		def __iter__(self):
			return self
			
		def next(self):
			try:
				row = tuple((xlCellValue(cell, self._book) for cell in self._sheet.row(self._index)))
				self._index += 1
				return row
			except IndexError:
				raise StopIteration

	def convDate(value, book):
		t = xlrd.xldate_as_tuple(value, book.datemode)
		if t[0] == 0 and t[1] == 0 and t[2] == 0:
			return time(*t[3:])
		else:
			return datetime(*t)

	def convNumber(value, book):
		if isinstance(value, float):
			v = int(value)
			if v == value:
				value = v
		return value

	xlConv = {
		xlrd.XL_CELL_DATE : convDate,
		xlrd.XL_CELL_NUMBER : convNumber,
	}
	xlConvDefault = lambda value, book: value
	
	def xlCellValue(cell, book):
		return xlConv.get(cell.ctype, xlConvDefault)(cell.value, book)


	def parseXls(fp, encoding=None, sheet_index=0):
		
		if hasattr(fp, 'read'):
			text = fp.read()
		else:
			text = fp
		
		book = xlrd.open_workbook(file_contents=text, encoding_override=encoding)
		sheets = [s for s in book.sheets() if s.sheet_visible]

		sheet = sheets[sheet_index]

		return XlsRowIterator(book, sheet)


	_PARSERS['XLS'] = parseXls
	del parseXls


def parse(format, fp_or_text, **kwargs):
	"""
	fp_or_text: opened file of its content as str
	encoding: encoding to override [csv, xls, dbf]
	sheet_index: sheet index [xls]
	"""
	return _PARSERS[format](fp_or_text, **kwargs)


if __name__ == '__main__':
	#data = open(r'Z:\projects\wm\docs\wm_technotes\wwm\import\klient_bank\export.dbf', 'rb')
	#format = 'DBF'
	#encoding = 'Cp866'

	#data = open(r'Z:\projects\wm\docs\wm_technotes\wwm\import\klient_bank\export.csv', 'rb')
	#format = 'CSV'
	#encoding = 'Cp1251'

	#data = open('''test.dbf''', 'rb')
	#format = 'DBF'
	#encoding = 'Cp866'
	
	data = open(r'Z:\projects\test_xls.xls', 'rb')
	format = 'XLS'
	encoding = None

	#data = open(r'Z:\projects\test_xls.csv', 'rb')
	#format = 'CSV'
	#encoding = 'Cp1251'

	for row in parse(format, data, encoding=encoding):
		print row
