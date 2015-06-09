###############################################################################
"""
	Project: Database transfer utility
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2004/02/18 11:59:28 $"
__version__ = "$Revision: 1.1 $"
# $Source: D:/HOME/cvs/toolib/scripts/db/transfer/TransferContext.py,v $
###############################################################################

from DatabaseDescriptor import DatabaseDescriptor

class TransferContext:
	def __init__(self, host, inDb, outDb, user, password):
		self._inDb = DatabaseDescriptor(host, user, password, inDb)
		self._outDb = DatabaseDescriptor(host, user, password, outDb)

	def getInDb(self):
		return self._inDb

	def getOutDb(self):
		return self._outDb
