###############################################################################
"""
	Project: Database transfer utility


<?xml version="1.0"?>
<dbtransfer dbin="db2" dbout="db1" usedb="in|out|none">
	<table into="taaaaaaa2" from="t2 LEFT JOIN t3 ON t2.id=t3.fk_t2">
		<field into='field0'>expression as is</field>
		<field into='field1'>field4</field>
		<field into='field2'>1</field>
		<field into='field3'>'string Constant'</field>
		<field into='field3'>field3 + field4</field>
		<field into='field4'/>
	</table>
	
	<table target='t3' from=''/>
	
</dbtransfer>

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2004/04/05 11:53:21 $"
__version__ = "$Revision: 1.2 $"
# $Source: D:/HOME/cvs/toolib/scripts/db/transfer/TransferDocument.py,v $
###############################################################################

from toolib.xtypes.iterators import OrderDictSequence
from DatabaseDescriptor import *


class FieldTransfer:
	
	TAG = "field"
	ATTR_TARGET="into"
	
	def __init__(self, target=None):
		self._target = target
		self._expression = None
		
	def getTarget(self):
		return self._target

	def setTarget(self, target):
		self._target = target

	def getExpression(self):
		return self._expression or "NULL"

	def setExpression(self, expression):
		self._expression = expression

	def __len__(self):
		return 2
	
	def __getitem__(self, i):
		if i==0:	return self._target
		elif i==1:	return self._expression
		else:		raise IndexError

	def updateFromElement(self, element):
		assert element.tagName == self.TAG
		
		# attributes
		self._target = element.getAttribute(self.ATTR_TARGET)
		#rint "\tFieldTrasfer.updateFromElement(%s)" % self._target
		expNode = element.firstChild
		if expNode is not None:
			self._expression = expNode.nodeValue.strip()
		else:
			self._expression = None

class TableTransfer:
	
	TAG="table"
	TAG_WHERE = "where"
	ATTR_TARGET="into"
	ATTR_FROM="from"
	
	def __init__(self, dbTransfer, target=None):
		self._dbTransfer = dbTransfer
		self._target = target	# table, passed as
		self._from = None	# join, passed as is
		self._where = None
		self._fieldTransfersOrder = []
		self._fieldTransfersDict = {}
		
	def getFieldTransfers(self):
		return OrderDictSequence(self._fieldTransfersDict, self._fieldTransfersOrder)
		
	def getDbTransfer(self):
		return self._dbTransfer
	
	def getId(self):
		return self._target

	def getTarget(self, context):
		if context is not None and self.getDbTransfer().getDefaultDb() != DbTransfer.DEFAULT_DB_OUT:
			return '.'.join((context.getOutDb().getId(), self._target))
		else:
			return self._target

	def getFrom(self):
		"""
		from == target by default
		"""
		#rint ">>>", self._from
		if self._from is None:
			return self._target
		else:
			return self._from 

	def getWhere(self):
		"""
		from == target by default
		"""
		#rint ">>>", self._from
		return self._where

	def setFrom(self, value):
		self._from = value

	def isEnabled(self):
		"""
		if transfer not enabled, no data copy for this table at all
		"""
		return self.getFrom() != ""

	def getTransferSql(self, context):
		if self.isEnabled():
			fields = []
			expressions = []
			for ft in self.getFieldTransfers():
				fields.append(ft.getTarget())
				expressions.append(ft.getExpression())
			#rint expressions
			if len(fields) > 0:
				sql = "INSERT INTO %s(\n\t%s\n)\nSELECT\n\t%s\nFROM %s" % (
					self.getTarget(context),
					',\n\t'.join(fields),
					',\n\t'.join(expressions),
					self.getFrom(),
				)
				if self.getWhere():
					sql = "%s\nWHERE %s" % (sql, self.getWhere())
				return sql+';'
			else:
				return "# No fields for %s" % self.getTarget(context)
		else:
			return "# Nothing to do with %s" % self.getTarget(context)

	def _addFieldTransfer(self, fieldId):
		"""
		Adds new field if was not in dict. returns it
		"""
		ft = self._fieldTransfersDict.get(fieldId)
		if ft is None:
			ft = FieldTransfer(fieldId)
			self._fieldTransfersDict[fieldId] = ft
			self._fieldTransfersOrder.append(fieldId)
		return ft

	def updateFromElement(self, tableElement):
		assert tableElement.tagName == self.TAG
		
		# attributes
		self._target = tableElement.getAttribute(self.ATTR_TARGET)
		if tableElement.hasAttribute(self.ATTR_FROM):
			self._from = tableElement.getAttribute(self.ATTR_FROM)
		else:
			self._from = None

		self._where = None
		try:
			whereTextNode = tableElement.getElementsByTagName(self.TAG_WHERE)[0].firstChild
			if whereTextNode:
				self._where = whereTextNode.nodeValue.strip()
		except IndexError:
			pass

		#rint ">> TableTransfer.updateFromElement(%s), from='%s'" % (self._target, self._from)
		
		# filling
		for fieldElement in tableElement.getElementsByTagName(FieldTransfer.TAG):
			id = fieldElement.getAttribute(FieldTransfer.ATTR_TARGET)
			self._addFieldTransfer(id).updateFromElement(fieldElement)
		
	def reset(self):
		self._ttdict = {}
		self._ttorder = []

	def initFromIntersection(self, tablein, tableout):
		self.reset()
		for fieldId in tablein.getIntersection(tableout):
			ft = self._addFieldTransfer(fieldId)
			ft.setExpression(fieldId)
		
class DbTransfer:
	
	# defaultDb variants
	DEFAULT_DB_IN="in"
	DEFAULT_DB_OUT="out"
	
	DEFAULT_DB_DEFAULT=DEFAULT_DB_IN
	
	TAG = "dbtransfer"
	ATTR_DEFAULT_DB = "usedb"

	def __init__(self):
		self._defaultDb=self.DEFAULT_DB_DEFAULT
		self._ttorder = []
		self._ttdict = {}

	def getDefaultDb(self):
		return self._defaultDb
	
	def getUseDb(self, context):
		if self._defaultDb == self.DEFAULT_DB_IN:
			return context.getInDb().getId()
		elif self._defaultDb == self.DEFAULT_DB_OUT:
			return context.getOutDb().getId()

	def getTableTransfers(self):
		return OrderDictSequence(self._ttdict, self._ttorder)

	def writeTransferSql(self, context, out):
		use = self.getUseDb(context)
		if use is not None:
			print >> out, "USE %s;\n" % use

		for tt in self.getTableTransfers():
			out.write(tt.getTransferSql(context))
			out.write("\n\n")

	def reset(self):
		self._ttdict = {}
		self._ttorder = []

	def _addTableTransfer(self, tableId):
		"""
		Adds new table if was not in dict. returns it
		"""
		tt = self._ttdict.get(tableId)
		if tt is None:
			tt = TableTransfer(self, tableId)
			self._ttdict[tableId] = tt
			self._ttorder.append(tableId)
		else:
			self._ttorder.remove(tableId)
			self._ttorder.append(tableId)
		return tt
		
		
	def initFromIntersection(self, dbin, dbout):
		self.reset()
		for tableId in dbin.getIntersection(dbout):
			tt = self._addTableTransfer(tableId)
			tt.setFrom(tableId)
			tt.initFromIntersection(dbin.getTable(tableId), dbout.getTable(tableId))
		
	def loadFromContext(self, context):
		"""
		opens databases and loads default transfer
		"""
		self.initFromIntersection(context.getInDb(), context.getOutDb())

	def updateFromElement(self, dbElement):
		assert dbElement.tagName == self.TAG
		
		# attributes
		if dbElement.hasAttribute(self.ATTR_DEFAULT_DB):
			self._defaultDb = dbElement.getAttribute(self.ATTR_DEFAULT_DB)
		else:
			self._defaultDb = self.DEFAULT_DB_DEFAULT
		
		# filling
		for tableElement in dbElement.getElementsByTagName(TableTransfer.TAG):
			id = tableElement.getAttribute(TableTransfer.ATTR_TARGET)
			self._addTableTransfer(id).updateFromElement(tableElement)
			
		
	def updateFromXmlFile(self, fileName):
		"""updates context from xml"""
		import xml.dom.minidom as parser
		dom = parser.parse(fileName)
		self.updateFromElement(dom.getElementsByTagName(self.TAG)[0])


