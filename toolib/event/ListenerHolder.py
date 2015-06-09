###############################################################################
# Program:	toolib.event
'''
Used un dbgenie
'''
__author__  = "Oleg Noga"
__date__	= "$Date: 2009/04/10 16:36:58 $"
__version__ = "$Revision: 1.5 $"
# $Source: D:/HOME/cvs/toolib/event/ListenerHolder.py,v $
###############################################################################

class ListenerHolder(object):

	def __init__(self):
		self.__listeners = []

	def addListener(self, listener):
		self.__listeners.append(listener)

	def removeListener(self, listener):
		self.__listeners.remove(listener)

	def _fireEvent(self, event):
		"""
		Protected. event must have _send method
		"""
		event._send(self.__listeners)
		return event

