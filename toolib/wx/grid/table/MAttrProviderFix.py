
class MAttrProviderFix(object):
	"""
	attr provider fix
	All methods to attr provider overrided
	"""
	def __init__(self):
		self.__ap = None                          # attr provider
	
	def SetAttrProvider(self, ap):
		self.__ap = ap
		try:
			ap.setTable(self)
		except AttributeError:
			pass

	def GetAttrProvider(self):
		if self.__ap is None:
			return super(__class__, self).GetAttrProvider()
		return self.__ap

	def GetAttr(self, row, col, kind):
		if self.__ap:	
			return self.__ap.GetAttr(row, col, kind)
		else:			
			return super(__class__, self).GetAttr(row, col, kind)
	
	def SetAttr(self, attr, row, col):
		if self.__ap:	
			#rint "user SetAttr", row, col
			self.__ap.SetAttr(attr, row, col)
		else:			
			#rint "native SetAttr", row, col
			super(__class__, self).SetAttr(attr, row, col)

	def SetColAttr(self, attr, col):
		if self.__ap:	self.__ap.SetColAttr(attr, col)
		else:        	super(__class__, self).SetColAttr(attr, col)
	
	def SetRowAttr(self, attr, row):
		if self.__ap:	self.__ap.SetRowAttr(attr, row)
		else:        	super(__class__, self).SetRowAttr(attr, row)
	
	def UpdateAttrRows(self, pos, numrows):
		if self.__ap:	self.__ap.UpdateAttrRows(pos, numrows)
		else:        	super(__class__, self).UpdateAttrRows(pos, numrows)
	
	def UpdateAttrCols(self, pos, numcols):
		if self.__ap:	self.__ap.UpdateAttrCols(pos, numcols)
		else:        	super(__class__, self).UpdateAttrCols(pos, numcols)

__class__ = MAttrProviderFix
