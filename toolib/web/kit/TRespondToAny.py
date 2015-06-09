###############################################################################
# Program:	wlib
"""

	Provides:
		respondToAny

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2008/06/10 13:24:58 $"
__version__ = "$Revision: 1.1 $"
# $Source: D:/HOME/cvs/toolib/web/kit/TRespondToAny.py,v $
###############################################################################

class TRespondToAny(object):

	def respondToGet(self, trans):
		self.respondToAny(trans)

	def respondToPost(self, trans):
		self.respondToAny(trans)

	def respondToPut(self, trans):
		self.respondToAny(trans)

	def respondToHead(self, trans):
		self.respondToAny(trans)
