###############################################################################
"""
	Project: Database transfer utility
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2004/09/23 19:10:16 $"
__version__ = "$Revision: 1.5 $"
# $Source: D:/HOME/cvs/toolib/scripts/db/transfer/DatabaseDescriptor.py,v $
###############################################################################

from MySQLdb import Connection, DatabaseError
from toolib.util.Cache import Cache
from toolib.xtypes.iterators import OrderDictSequence

class FieldDescriptor:
	def __init__(self, data):
		self._id = data[0]
		self._type = data[1]
		self._required = data[2] != "YES"
		self._key = data[3]
		self._defaultValue = data[4]
		if len(data) > 5:
			self._extra = data[5]
		else:
			self._extra = None
		
	def getId(self):
		return self._id
	
	def __eq__(self, field):
		return self._id == field._id

	def __str__(self):
		return "| %19s | %16s | %5s | %3s | %19s | %s" % (
			self._id,
			self._type,
			self._required,
			self._key,
			self._defaultValue,
			self._extra,
		)

	def getType(self):
		return self._type


class TableDescriptor:
	def __init__(self, id, data):
		self._id = id
		self._order = map(lambda row: row[0], data)
		#self._order.sort()
		self._data = {}
		for row in data:
			self._data[row[0]] = FieldDescriptor(row)

	def getId(self):
		return self._id

	def getFieldIds(self):
		return self._order
	
	def getField(self, fieldId):
		return self._data[fieldId]

	def getFields(self):
		return OrderDictSequence(self._data, self._order)

	def getIntersection(self, table2):
		res = []
		for i in self.getFields():
			for j in table2.getFields():
				if i == j:
					res.append(i.getId())
					break
		return res
	
	def __eq__(self, table):
		return self._id == table._id

class DatabaseDescriptor:
	def __init__(self, host, user, password, db):
		self._host = host
		self._user = user
		self._password = password
		self._id = db
		self._connection = None
		self._tableIds = None
		self._tables = Cache(self._loadTableDescriptor)

	def getId(self):
		return self._id

	def connect(self):
		return Connection(self._host, self._user, self._password, self._id)

	def getConnection(self):
		if self._connection is None:
			self._connection = self.connect()
		return self._connection

	def query(self, query):
		cursor = self.getConnection().cursor()
		cursor.execute(query)
		return cursor.fetchall()

	def getTableIds(self):
		if self._tableIds == None:
			#print "##### table ids query for", self._id
			self._tableIds = map(lambda x: x[0], self.query("SHOW TABLES"))
			#self._tableIds.sort()
		return self._tableIds

	def _loadTableDescriptor(self, tableId):
		#print "##### describe table query for %s.%s" % (self._id, tableId)
		return TableDescriptor(tableId, self.query("DESCRIBE %s" % tableId))
		
	def getTable(self, tableId):
		return self._tables[tableId]
	
	def getTables(self):
		return OrderDictSequence(self._tables, self.getTableIds())

	def getIntersection(self, db2):
		res = []
		for i in self.getTables():
			for j in db2.getTables():
				if i == j:
					res.append(i.getId())
					break
		return res

if __name__ == '__main__':
	from toolib.utils import strdict

	def dumpTableNumbers():
		from DatabaseDescriptor import DatabaseDescriptor
		dd = DatabaseDescriptor("10.17.13.47", "root", "pipirka", "sula_agrosvista")

		m = {}
		for t in dd.getTables():
			try:
				n = int(t.getId()[-2:])
				m[n] = t
			except:
				print "W-t number: ", t.getId()

		for i in range(100):
			t = m.get(i)
			if t is not None:
				print "%02d %s" % (i, t.getId())
			else:
				print "%02d" % (i,)

		
	def dumpTables():
		from DatabaseDescriptor import DatabaseDescriptor
		dd = DatabaseDescriptor("10.17.13.47", "root", "pipirka", "sula_agrosvista")

		typesDict = {}

		for t in dd.getTables():
			print t.getId()
			for f in t.getFields():
				print "\t", f
				tp = f.getType()
				typesDict[tp] = typesDict.get(tp, 0) + 1

		print strdict(typesDict)

	#dumpTableNumbers()
	dumpTables()
