#################################################################
# Program:   Business time logger
"""
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2004/03/24 12:36:39 $"
__version__ = "$Revision: 1.2 $"
# $Source: D:/HOME/cvs/toolib/scripts/businesstime.py,v $
#																#
#################################################################

from mx import DateTime
import sys, os
from toolib.win32.excel import *

FILE_PATH = r"\\PAVEL2\public\Abrisola\Hours Of Business\${USER_NAME}\log.xls"

FROM = "start"
TILL = "stop"

TARGET_WORK		= "work"
TARGET_DINNER	= "dinner"

DATE_LOOKUP_RANGE = xrange(2, 100)



class BusinessTimeDocumentTemplate:
	def __init__(self):
		self._columns = {}
		self._sheetName = 1

	def setSheetName(self, sheetName):
		self._sheetName = sheetName

	def getSheetName(self):
		return self._sheetName

	def addColumn(self, target, index):
		self._columns[target] = index

	def getColumn(self, target):
		return self._columns[target]
		

class BusinessTimeDocument:

	def __init__(self, template, path):
		self._path = path
		self._template = template
		self._xlSheet = None
		
		self._date = None
		self._dateIndex = None

		self._recognize()

	def _recognize(self):
		sheet = self.getExcelSheet()
		for i in DATE_LOOKUP_RANGE:
			value = sheet.getCell(i, self._template.getColumn("index"))
			if value is not None:
				try:
					self._date = DateTime.DateTimeFromCOMDate(value)
					self._dateIndex = i
					return
				except:
					print "* Error reading date:", value, type(value)
					continue
		raise "Bad document"
		
	def getRowForDate(self, date):
		return self._dateIndex + int(round((date - self._date).days))

	def setTime(self, target, from_or_till):
		today = DateTime.today()
		col = self._template.getColumn((target, from_or_till))
		row = self.getRowForDate(today)
		now = DateTime.now()
		value = now.abstime / 60 / 60 / 24
		print "+ %s %s: Setting time at (%s, %s) to %s" % (from_or_till, target, row, col, now)
		self._xlSheet.setCell(row, col, value)

	def save(self):
		self.getExcelSheet().getBook().save()

	def getExcelSheet(self):
		if self._xlSheet is None:
			try:
				self._xlSheet = ExcelBook(self._path).getSheet(self._template.getSheetName())
			except:
				raise "Excel file not found: " + self._path
		return self._xlSheet

	def __del__(self):
		if self._xlSheet:
			self.getExcelSheet().getBook().close()


def getTemplate():
	template = BusinessTimeDocumentTemplate()
	template.addColumn("index",               1)
	template.addColumn((TARGET_WORK,   FROM), 3)
	template.addColumn((TARGET_WORK,   TILL), 4)
	template.addColumn((TARGET_DINNER, FROM), 5)
	template.addColumn((TARGET_DINNER, TILL), 6)
	return template
	

def usage(args):
	print "  Usage: %s < %s | %s > < %s | %s >" % (args[0], FROM, TILL, TARGET_WORK, TARGET_DINNER)

def main(args):
	try:
		from_or_till = args[1]
		target = args[2]
	except IndexError:
		print "! Wrong arguments"
		usage(args)
		return 1
	
	file = FILE_PATH.replace("${USER_NAME}", os.getenv("USERNAME"))

	doc = BusinessTimeDocument(getTemplate(), file)
	doc.setTime(target, from_or_till)
	doc.save()
	return 0

if __name__ == "__main__":
	try:
		sys.exit(main(sys.argv))
	except SystemExit:
		raise
	except:
		apply(sys.excepthook, sys.exc_info())
		sys.exit(1)

