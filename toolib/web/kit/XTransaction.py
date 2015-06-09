###############################################################################
# Program:	wlib
"""
Awake/sleep cycle base class

	Provides:
		transaction
		request
		responce
		session
		write

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2008/06/10 13:24:58 $"
__version__ = "$Revision: 1.1 $"
# $Source: D:/HOME/cvs/toolib/web/kit/XTransaction.py,v $
###############################################################################

class XTransaction(object):

	############## Awake-Sleep cycle #############################

	def awake(self, trans):
		super(XTransaction, self).awake(trans)
		self._transaction	= trans
		self._request		= trans.request()
		self._response		= trans.response()

	def sleep(self, trans):
		self._transaction	= None
		self._request		= None
		self._response		= None
		super(XTransaction, self).sleep(trans)

	############## state getters #############################

	def transaction(self):
		return self._transaction

	def request(self):
		return self._request

	def response(self):
		return self._response

	def session(self):
		return self._transaction.session()

	def write(self, text):
		self._response.write(text)

