#################################################################
# Program: Toolib
"""
Known issues:
	! GetTable call after Destroy leads to crush
	  Careful with delegating to table

	  Example (how to avoid crush):

		def __getattr__(self, name):
			if name != '__del__':
				return getattr(self.GetTable(), name)
			else:
				raise AttributeError, name

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2007/09/17 13:19:12 $"
__version__ = "$Revision: 1.3 $"
# $Source: D:/HOME/cvs/toolib/wx/grid/wxGrid.py,v $
#
#################################################################

import wx.grid

FIX_SETTABLE = 1

if FIX_SETTABLE:

	from table.MTableMessaging import MTableMessaging


	class NoneTable(wx.grid.PyGridTableBase):

		def GetNumberRows(self):
			return 0

		def GetNumberCols(self):
			return 0

		def __nonzero__(self):
			return False

	USE_SETWXTABLE = 0

	class DelegatingTable(wx.grid.PyGridTableBase, MTableMessaging):
		"""
		Since wxGrid SetTable is buggy
		using TableDelegator and pythonic tables
		"""

		def __init__(self, table=None):
			wx.grid.PyGridTableBase.__init__(self)
			MTableMessaging.__init__(self)

			self.__table = table or NoneTable()
			if USE_SETWXTABLE:
				self.__table._setWxTable(self)

		def _setTable(self, table):
			self.fireTableStructureChanging()

			if USE_SETWXTABLE:
				if self.__table is not None:
					self.__table._setWxTable(None)

			self.__table = table
		
			if USE_SETWXTABLE:
				self.__table._setWxTable(self)

			self.fireTableStructureChanged()

		def _getTable(self):
			return self.__table

		#######################################################
		# BEGIN_AUTO_GENERATED_CODE
		def AppendCols(self, *args):
			return self.__table.AppendCols(*args)
		
		def AppendRows(self, *args):
			return self.__table.AppendRows(*args)
		
		def AttrProvider(self, *args):
			return self.__table.AttrProvider(*args)
		
		def CanGetValueAs(self, *args):
			return self.__table.CanGetValueAs(*args)
		
		def CanHaveAttributes(self, *args):
			return self.__table.CanHaveAttributes(*args)
		
		def CanSetValueAs(self, *args):
			return self.__table.CanSetValueAs(*args)
		
		def ClassName(self, *args):
			return self.__table.ClassName(*args)
		
		def Clear(self, *args):
			return self.__table.Clear(*args)
		
		def DeleteCols(self, *args):
			return self.__table.DeleteCols(*args)
		
		def DeleteRows(self, *args):
			return self.__table.DeleteRows(*args)
		
		def Destroy(self, *args):
			return self.__table.Destroy(*args)
		
		def GetAttr(self, *args):
			return self.__table.GetAttr(*args)
		
		def GetAttrProvider(self, *args):
			return self.__table.GetAttrProvider(*args)
		
		def GetClassName(self, *args):
			return self.__table.GetClassName(*args)
		
		def GetColLabelValue(self, *args):
			return self.__table.GetColLabelValue(*args)
		
		def GetNumberCols(self, *args):
			return self.__table.GetNumberCols(*args)
		
		def GetNumberRows(self, *args):
			return self.__table.GetNumberRows(*args)
		
		def GetRowLabelValue(self, *args):
			return self.__table.GetRowLabelValue(*args)
		
		def GetTypeName(self, *args):
			return self.__table.GetTypeName(*args)
		
		def GetValue(self, *args):
			return self.__table.GetValue(*args)
		
		def GetValueAsBool(self, *args):
			return self.__table.GetValueAsBool(*args)
		
		def GetValueAsDouble(self, *args):
			return self.__table.GetValueAsDouble(*args)
		
		def GetValueAsLong(self, *args):
			return self.__table.GetValueAsLong(*args)
		
		def GetView(self, *args):
			return self.__table.GetView(*args)
		
		def InsertCols(self, *args):
			return self.__table.InsertCols(*args)
		
		def InsertRows(self, *args):
			return self.__table.InsertRows(*args)
		
		def IsEmptyCell(self, *args):
			return self.__table.IsEmptyCell(*args)
		
		def IsSameAs(self, *args):
			return self.__table.IsSameAs(*args)
		
		def NumberCols(self, *args):
			return self.__table.NumberCols(*args)
		
		def NumberRows(self, *args):
			return self.__table.NumberRows(*args)
		
		def SetAttr(self, *args):
			return self.__table.SetAttr(*args)
		
		def SetAttrProvider(self, *args):
			return self.__table.SetAttrProvider(*args)
		
		def SetColAttr(self, *args):
			return self.__table.SetColAttr(*args)
		
		def SetColLabelValue(self, *args):
			return self.__table.SetColLabelValue(*args)
		
		def SetRowAttr(self, *args):
			return self.__table.SetRowAttr(*args)
		
		def SetRowLabelValue(self, *args):
			return self.__table.SetRowLabelValue(*args)
		
		def SetValue(self, *args):
			return self.__table.SetValue(*args)
		
		def SetValueAsBool(self, *args):
			return self.__table.SetValueAsBool(*args)
		
		def SetValueAsDouble(self, *args):
			return self.__table.SetValueAsDouble(*args)
		
		def SetValueAsLong(self, *args):
			return self.__table.SetValueAsLong(*args)
		
		def SetView(self, *args):
			return self.__table.SetView(*args)
		
		def View(self, *args):
			return self.__table.View(*args)
		
		# END_AUTO_GENERATED_CODE
		#######################################################

	__super__ = wx.grid.Grid
	class wxGrid(__super__):

		def __init__(self, *args, **kwargs):
			__super__.__init__(self, *args, **kwargs)
			table = DelegatingTable()
			__super__.SetTable(self, table, True)
			table.addGridTableListener(self)

		def GetTable(self):
			return __super__.GetTable(self)._getTable()

		def SetTable(self, table, ignored_takeOwnership=False):
			__super__.GetTable(self)._setTable(table)

else:
	wxGrid = wx.grid.Grid


if __name__ == '__main__':

	def inject(f):
		d = filter(lambda name: name[0].isupper(), dir(wx.grid.PyGridTableBase))
		d.sort()
	
		for i in d:
		#if VERBOSE: print "%s", args
			print >>f, """\
		def %s(self, *args, **kwargs):
			return self.__table.%s(*args, **kwargs)
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
