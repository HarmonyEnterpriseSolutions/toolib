# -*- coding: Cp1251 -*-
#################################################################
# Program:   common
"""
	Excel access from python

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2006/11/22 17:58:19 $"
__version__ = "$Revision: 1.13 $"
# $Source: D:/HOME/cvs/toolib/win32/excel.py,v $
#																#
#################################################################

# Calculating:
#All open workbooks		Application.Calculate (or just Calculate)
#A specific worksheet   Worksheets(1).Calculate
#A specified range		Worksheets(1).Rows(2).Calculate


import win32api
import win32com.client
import pywintypes
import types
import os
import sys
import time
import toolib.amath as amath
from toolib			import debug
from toolib._		import *
from toolib			import amath

MAIN_WINDOW_CLASS = 'XLMAIN'
DESK_WINDOW_CLASS = 'XLDESK'

xlNormal	= -4143
xlMinimized = -4140
xlMaximized = -4137

A = ord('A')

##__all__ = ('getExcelApplication', 'releaseExcelApplication', 'ExcelBook', 'ExcelSheet', 'ExcelSheetRegion')

__excelApp = None

def getExcelApplication():
	global __excelApp
	if __excelApp == None:
		__excelApp = win32com.client.DispatchEx("Excel.Application")
		#__excelApp.Visible = 0

	#try:
	#   __excelApp.Visible		# simplest NOP, poll RPC server
	#except pywintypes.com_error, e:
	#   if e[0] == 0x800706BA:
	#		debug.warning('Excel RPC Server lost! Creating a new one')
	#		__excelApp = win32com.client.DispatchEx("Excel.Application")
	#   else:
	#		raise
	return __excelApp


def releaseExcelApplication():
	global __excelApp
	if __excelApp:
		del __excelApp


def getExcelHwnd(excelApp=None):
	import win32gui, random
	if excelApp is None:
		excelApp = getExcelApplication()

	excelApp.Caption = str(random.random())

	try:
		hwnd = win32gui.FindWindow(MAIN_WINDOW_CLASS, excelApp.Caption)
	except win32api.error:
		hwnd = 0

	excelApp.Caption = ""
	return hwnd

def getExcelDeskHwnd(excelApp=None):
	import win32gui
	hwnd = getExcelHwnd(excelApp)
	if hwnd:
		return win32gui.FindWindowEx(hwnd, 0, DESK_WINDOW_CLASS, None)
	else:
		return 0

def hideExcel(xlApp=None, parentWindow=None):
	if xlApp is None: xlApp = getExcelApplication()
	while 1:
		try:
			xlApp.Visible = 0
			return
		except pywintypes.com_error:
			#@TODO: use winapi dialog here
			import wx
			import toolib.wx.wxutils as wxutils
			wxutils.messageBox(parentWindow, _("Can't hide Excel, ensure that no dialogs opened in Excel and press ok."), _("Problem with Excel"), wx.OK | wx.ICON_EXCLAMATION)


def colName(n):
	if not isinstance(n, (int, long)): debug.warning("Input argument type is not int: %s (%s)" % (n, type(n)))
	h, l = divmod(n-1, 26)
	h -= 1
	if h >= 0:  hc = chr(A + h)
	else:		hc = ""
	lc = chr(A + l)
	return hc + lc

def cellName(row, col):
	return "%s%d" % (colName(col), row)

class ExcelBook:
	def __init__(self, filename=None, active=False):
		"""Opens Book from file"""
		if active:
			self.filename = ""
			self.xlBook = self.getApplication().ActiveWorkbook
		else:
			if filename:
				self.filename = filename
				self.xlBook = self.getApplication().Workbooks.Open(filename)
			else:
				self.filename = ""
				self.xlBook = self.getApplication().Workbooks.Add()

	def getApplication(self):
		return getExcelApplication()

	def save(self, newfilename=None, newpath=None):
		if newpath is not None:
			if newfilename is None:
				newfilename = self.filename
			newfilename = os.path.join(newpath, os.path.split(newfilename)[1])
		if newfilename:
			self.xlBook.SaveAs(newfilename)
			self.filename = newfilename
		else:
			self.xlBook.Save()

	def close(self):
		self.xlBook.Close(SaveChanges=0)

	def getSheet(self, sheet):
		return ExcelSheet(self, sheet)

class ExcelSheetRegion:
	def __init__(self,
				 sheet,		# : abris.excel.ExcelSheetRegion
				 row, col, rowSize, colSize):
		self.sheet = sheet
		self.data = list(sheet.getRange(row, col, rowSize, colSize))
		for i in xrange(len(self.data)):
			self.data[i] = list(self.data[i])
		self.row = row
		self.col = col
		self.lastRow = row + rowSize - 1
		self.lastCol = col + colSize - 1

	def hasCell(self, row, col):
		return row >= self.row and row <= self.lastRow and col >= self.col and col <= self.lastCol

	def hasRect(self, row, col, rowSize, colSize):
		return row >= self.row and col >= self.col and row + rowSize - 1 <= self.lastRow and col + colSize - 1 <= self.lastCol

	def setCell(self, row, col, val):
		if self.hasCell(row, col):
			self.data[row - self.row][col - self.col] = val
		else:
			debug.warning('%s does not have (%s,%s) ' % (self, row, col))
			self.sheet.setCell(row, col, val)

	def __str__(self):
		return "ExcelSheetRange (%s,%s)-(%s,%s)" % (self.row, self.col, self.lastRow, self.lastCol)

	def getCell(self, row, col):
		if self.hasCell(row, col):
			return self.data[row - self.row][col - self.col]
		else:
			debug.warning('%s does not have (%s,%s) ' % (self, row, col))
			return self.sheet.getCell(row, col)

	def getRange(self, row, col, rowSize, colSize):
		if self.hasRect(row, col, rowSize, colSize):
			row = row - self.row
			col = col - self.col
			res = range(rowSize)
			rowSlice = self.data[row : row+rowSize]
			for i in xrange(rowSize):
				res[i] = rowSlice[i][col : col + colSize]
			return res
		else:
			raise "Range (%s, %s), %s x %s does not fit SheetRegion" % (row, col, rowSize, colSize)

	def getRow(self, row, col, size):
		return self.getRange(row, col, 1, size)[0]

	def setRow(self, row, col, data):
		self.setRange(row, col, (data,))

	def setRange(self, row, col, data):
		rowSize = len(data)
		if rowSize == 0: return
		colSize = len(data[0])
		if self.hasRect(row, col, rowSize, colSize):
			row = row - self.row
			col = col - self.col
			lastCol = col+colSize
			for i in xrange(rowSize):
				self.data[row+i][col : lastCol] = data[i]
		else:
			raise "Range (%s, %s), %s x %s does not fit SheetRegion" % (row, col, rowSize, colSize)

	def commit(self, row=None, col=None, lastRow=None, lastCol=None):
		if row is None: row = self.row
		if col is None: col = self.col
		if lastRow is None: lastRow = self.lastRow
		if lastCol is None: lastCol = self.lastCol
		if row == self.row and col == self.col and lastRow == self.lastRow and lastCol == self.lastCol:
			##print "setRange %s, %s, %s" % (row, col, self.data)
			self.sheet.setRange(row, col, self.data)
		else:
			rowSize = lastRow - row + 1
			colSize = lastCol - col + 1
			row0 = row - self.row
			col0 = col - self.col
			if row0 >= 0 and col0 >= 0:
				data = amath.matrixSlice(self.data, row0, row0+rowSize, col0, col0+colSize)
				##print "setRange %s, %s, %s" % (row, col, data)
				self.sheet.setRange(row, col, data)
			else:
				raise "Range (%s, %s), %s x %s does not fit SheetRegion" % (row, col, rowSize, colSize)

class ExcelSheet:
	def __init__(self, book, sheetNo):
		self.book = book
		self.xlSheet = book.xlBook.Worksheets(sheetNo)

	def getBook(self):
		return self.book

	def getCell(self, row, col):
		""" returns cell value, cell index is 1 based"""
		return self.xlSheet.Cells(row, col).Value

	def setCell(self, row, col, value):
		""" sets cell value, cell index is 1 based"""
		self.xlSheet.Cells(row, col).Value = value

	def getRange(self, row, col, rowSize, colSize):
		""" returns two-dimension array, cell index is 1 based"""
		r = self.xlSheet.Range(self.xlSheet.Cells(row, col), self.xlSheet.Cells(row+rowSize-1, col+colSize-1)).Value
		# this returns not tuple in case of 1x1 range. Fixing it
		if type(r) is types.TupleType:
			if len(r) > 0:
				if type(r[0]) is types.TupleType:
					return r
				else:   # returned tuple of values, wrap it into tuple
					return (r,)
			else:   # returned empty tuple - it's ok
				return r
		else:   # returned single value, wrap it into 2 tuples
			return ((r,),)

	def getRegion(self, row, col, rowSize, colSize):
		""" returns range buffer """
		return ExcelSheetRegion(self, row, col, rowSize, colSize)

	def getCol(self, row, col, rowSize):
		data = self.getRange(row, col, rowSize, 1)
		n = len(data)
		res = range(n)
		for i in xrange(n):
			res[i] = data[i][0]
		return res

	def setRange(self, row, col, data):
		""" sets two-dimension array, cell index is 1 based"""
		rows = len(data)
		if rows > 0:
			cols = len(data[0])
			self.xlSheet.Range(self.xlSheet.Cells(row, col), self.xlSheet.Cells(row+rows-1, col+cols-1)).Value = data

	def loadDbObject(self, object, row, col, fieldNames=None, includePropNames=1, vertical=1):
		#print "Object: %s" % object
		if fieldNames is None:
			fieldNames = []
			for field in object:
				type = field.getTypeId()
				if type not in ['intid']:
					fieldNames.append(field.getName())

		print "FieldNames: %s" % fieldNames
		data = []
		if includePropNames:
			names = []
			for fieldName in fieldNames:
				names.append(object[fieldName].getUName())
			data.append(names)

		values = []
		for fieldName in fieldNames:
			prop = object[fieldName]
			values.append(prop.getUValue())
		data.append(values)

		if vertical:
			data = amath.matrixFlip(data)

		self.setRange(1, 1, data)
		sys.stdin.readline()


def formatDate(comdate):
	t = time.localtime(int(comdate))
	return time.strftime("%Y-%m-%d", t);

def formatDateTime(comdate):
	t = time.localtime(int(comdate))
	return time.strftime("%Y-%m-%d %H:%M:%S", t);

def formatTime(fday):
	h = fday * 24
	m = h * 60
	s = m * 60
	h = int(h)
	m = int(m % 60)
	s = int(s % 60)
	return "%s:%s:%s" % (h,m,s)

def index2alpha(n):
	"""
	Converts 0-based index into AA format
	"""
	if n is None:
		return ""
	assert isinstance(n, (int, long)), "Input argument type is not int: %s %s" % (n, type(n))
	if n > 255:
		raise ValueError, _('Excel supports only 256 columns')
	h, l = divmod(n, 26)
	if h > 0:  
		return chr(A + h - 1) + chr(A + l)
	else:
		return chr(A + l)

def alpha2index(name):
	if not name:
		return None
	name = name.upper()
	if len(name) > 2:		raise ValueError, _('Last column is IV')
	if not name.isalpha():	raise ValueError, name
	l = ord(name[-1]) - A
	if len(name) == 2:
		h = ord(name[0]) - A + 1
	else:
		h = 0
	n = h * 26 + l
	if n > 255:				raise ValueError, _('Last column is IV')
	return n

################ END OF MODULE ################

if __name__ == '__main__':
	def testGetHwnd():
		print getExcelHwnd()


	def test2():
		from dbengine.factory import EngineFactory
		obj = EngineFactory().getObjectManager().getObject('con_good05')
		obj.load(98)

		book = ExcelBook()
		getExcelApplication().Visible=1
		try:
			sheet = book.getSheet(1)
			sheet.loadDbObject(obj, 1, 1)

		finally:
			book.close()


	def test3():
		book = ExcelBook(r"z:\rata\time.xls")
		try:
			sheet = book.getSheet(1)
			data = sheet.getRange(1, 1, 1, 3)[0]
			print formatTime(data[0])
			print formatDate(data[1])
			print formatDateTime(data[2])

		finally:
			book.close()

	def test4():
		book = ExcelBook()
		__excelApp.Visible = 1
		try:
			sheet = book.getSheet(1)
			data = sheet.setRange(1, 1, (("2002-03-02 12:50:13","2002-03-02","12:50:13"),))
			sys.stdin.readline()

		finally:
			book.close()


	def test1():
		print "Generating..."
		data = []
		for i in xrange(256):
			print i, '\r',
			data.append(range(256))
			for j in xrange(256):
				data[i][j] = "%s, %s" % (i,j)
		print "Done"

		import time
		book = ExcelBook()
		try:
			sheet = book.getSheet(1)
			print "Setting range...",
			t = time.time()
			sheet.setRange(1,1, data)
			print "Range set in %s" % (time.time() - t)
			print "Getting range...",
			t = time.time()
			res = sheet.getRange(1, 1, 256, 256)
			print "Range got in %s" % (time.time() - t)
			sys.stdin.readline()

			print "Setting range...",
			t = time.time()
			book.getSheet(2).setRange(1,1, res)
			print "Range set in %s" % (time.time() - t)

		finally:
			book.close()

	def fillRegion():
		getExcelApplication().Visible = 1
		book = ExcelBook()
		sheet = book.getSheet(1)
		for i in xrange(32):
			for j in xrange(26):
				sheet.setCell(i+1, j+1, chr(65+j) + str(i+1))
		book.save("z:\\rata\\test.xls")
		book.close()

	def testRegion():
		getExcelApplication().Visible = 1
		book = ExcelBook("z:\\rata\\test.xls")
		sheet = book.getSheet(1).getRegion(5,5, 10, 10)
		printMatrix(sheet.data)
		print sheet.getRange(14, 14, 2, 2)
		sheet.commit()
		#book.close()

	def test5():
		print cellName(1,1)
		#for i in range(1, 100):
		#   print i, colName(i)

	ExcelBook('c:\\veve.xls')
	getExcelApplication().Visible = 1
	testGetHwnd()
	sys.stdin.readline()
	getExcelApplication().Visible = 0
	releaseExcelApplication()


