#################################################################
# Program: Toolib
"""
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2007/09/17 13:19:14 $"
__version__ = "$Revision: 1.2 $"
# $Source: D:/HOME/cvs/toolib/wx/grid/table/wxGridTableBase.py,v $
#
#################################################################
from toolib import debug
from wx.grid import PyGridTableBase

FIX_SETTABLE = 1

if FIX_SETTABLE:

	class wxGridTableBase(object):
 
		def __init__(self):
			self.__wxTable = PyGridTableBase()

		def getWxTable(self):
			return self.__wxTable

		def _setWxTable(self, wxTable):
			self.__wxTable = wxTable

		#######################################################
		# redirect super calls to self.__wxTable PyGridTableBase class method
		# BEGIN_AUTO_GENERATED_CODE
		def AppendCols(self, *args, **kw):
			return PyGridTableBase.AppendCols(self.__wxTable, *args, **kw)
		
		def AppendRows(self, *args, **kw):
			return PyGridTableBase.AppendRows(self.__wxTable, *args, **kw)
		
		def AttrProvider(self, *args, **kw):
			return PyGridTableBase.AttrProvider(self.__wxTable, *args, **kw)
		
		def CanGetValueAs(self, *args, **kw):
			return PyGridTableBase.CanGetValueAs(self.__wxTable, *args, **kw)
		
		def CanHaveAttributes(self, *args, **kw):
			return PyGridTableBase.CanHaveAttributes(self.__wxTable, *args, **kw)
		
		def CanSetValueAs(self, *args, **kw):
			return PyGridTableBase.CanSetValueAs(self.__wxTable, *args, **kw)
		
		def ClassName(self, *args, **kw):
			return PyGridTableBase.ClassName(self.__wxTable, *args, **kw)
		
		def Clear(self, *args, **kw):
			return PyGridTableBase.Clear(self.__wxTable, *args, **kw)
		
		def DeleteCols(self, *args, **kw):
			return PyGridTableBase.DeleteCols(self.__wxTable, *args, **kw)
		
		def DeleteRows(self, *args, **kw):
			return PyGridTableBase.DeleteRows(self.__wxTable, *args, **kw)
		
		def Destroy(self, *args, **kw):
			return PyGridTableBase.Destroy(self.__wxTable, *args, **kw)
		
		def GetAttr(self, *args, **kw):
			return PyGridTableBase.GetAttr(self.__wxTable, *args, **kw)
		
		def GetAttrProvider(self, *args, **kw):
			return PyGridTableBase.GetAttrProvider(self.__wxTable, *args, **kw)
		
		def GetClassName(self, *args, **kw):
			return PyGridTableBase.GetClassName(self.__wxTable, *args, **kw)
		
		def GetColLabelValue(self, *args, **kw):
			return PyGridTableBase.GetColLabelValue(self.__wxTable, *args, **kw)
		
		def GetNumberCols(self, *args, **kw):
			return PyGridTableBase.GetNumberCols(self.__wxTable, *args, **kw)
		
		def GetNumberRows(self, *args, **kw):
			return PyGridTableBase.GetNumberRows(self.__wxTable, *args, **kw)
		
		def GetRowLabelValue(self, *args, **kw):
			return PyGridTableBase.GetRowLabelValue(self.__wxTable, *args, **kw)
		
		def GetTypeName(self, *args, **kw):
			return PyGridTableBase.GetTypeName(self.__wxTable, *args, **kw)
		
		def GetValue(self, *args, **kw):
			return PyGridTableBase.GetValue(self.__wxTable, *args, **kw)
		
		def GetValueAsBool(self, *args, **kw):
			return PyGridTableBase.GetValueAsBool(self.__wxTable, *args, **kw)
		
		def GetValueAsDouble(self, *args, **kw):
			return PyGridTableBase.GetValueAsDouble(self.__wxTable, *args, **kw)
		
		def GetValueAsLong(self, *args, **kw):
			return PyGridTableBase.GetValueAsLong(self.__wxTable, *args, **kw)
		
		def GetView(self, *args, **kw):
			return PyGridTableBase.GetView(self.__wxTable, *args, **kw)
		
		def InsertCols(self, *args, **kw):
			return PyGridTableBase.InsertCols(self.__wxTable, *args, **kw)
		
		def InsertRows(self, *args, **kw):
			return PyGridTableBase.InsertRows(self.__wxTable, *args, **kw)
		
		def IsEmptyCell(self, *args, **kw):
			return PyGridTableBase.IsEmptyCell(self.__wxTable, *args, **kw)
		
		def IsSameAs(self, *args, **kw):
			return PyGridTableBase.IsSameAs(self.__wxTable, *args, **kw)
		
		def NumberCols(self, *args, **kw):
			return PyGridTableBase.NumberCols(self.__wxTable, *args, **kw)
		
		def NumberRows(self, *args, **kw):
			return PyGridTableBase.NumberRows(self.__wxTable, *args, **kw)
		
		def SetAttr(self, *args, **kw):
			return PyGridTableBase.SetAttr(self.__wxTable, *args, **kw)
		
		def SetAttrProvider(self, *args, **kw):
			return PyGridTableBase.SetAttrProvider(self.__wxTable, *args, **kw)
		
		def SetColAttr(self, *args, **kw):
			return PyGridTableBase.SetColAttr(self.__wxTable, *args, **kw)
		
		def SetColLabelValue(self, *args, **kw):
			return PyGridTableBase.SetColLabelValue(self.__wxTable, *args, **kw)
		
		def SetRowAttr(self, *args, **kw):
			return PyGridTableBase.SetRowAttr(self.__wxTable, *args, **kw)
		
		def SetRowLabelValue(self, *args, **kw):
			return PyGridTableBase.SetRowLabelValue(self.__wxTable, *args, **kw)
		
		def SetValue(self, *args, **kw):
			return PyGridTableBase.SetValue(self.__wxTable, *args, **kw)
		
		def SetValueAsBool(self, *args, **kw):
			return PyGridTableBase.SetValueAsBool(self.__wxTable, *args, **kw)
		
		def SetValueAsDouble(self, *args, **kw):
			return PyGridTableBase.SetValueAsDouble(self.__wxTable, *args, **kw)
		
		def SetValueAsLong(self, *args, **kw):
			return PyGridTableBase.SetValueAsLong(self.__wxTable, *args, **kw)
		
		def SetView(self, *args, **kw):
			return PyGridTableBase.SetView(self.__wxTable, *args, **kw)
		
		def View(self, *args, **kw):
			return PyGridTableBase.View(self.__wxTable, *args, **kw)
		
		# END_AUTO_GENERATED_CODE
		#######################################################

else:

	wxGridTableBase = PyGridTableBase


if __name__ == '__main__':

	def inject(f):
		d = filter(lambda name: name[0].isupper(), dir(PyGridTableBase))
		d.sort()
	
		for i in d:
			print >> f, """\
		def %s(self, *args, **kw):
			return PyGridTableBase.%s(self.__wxTable, *args, **kw)
		""".replace("%s", i)

	f = open(__file__, 'rt')
	code = f.readlines()
	f.close()
		
	state = "begin"
	f = open(__file__, 'wt')
	for i in code:
		if state == 'begin':
			f.write(i)
			if i.find('BEGIN_AUTO_GENERATED_CODE') != -1:	
				inject(f)
				state = 'injected'
		elif state == 'injected':
			if i.find('END_AUTO_GENERATED_CODE') != -1:		
				f.write(i)
				state = 'end'
		elif state == 'end':
			f.write(i)
				
	f.close()
