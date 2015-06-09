#################################################################
# Program: Toolib
"""

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2007/08/06 15:59:39 $"
__version__ = "$Revision: 1.1 $"
# $Source: D:/HOME/cvs/toolib/wx/mixin/TCoreHolderWindow.py,v $
#
#################################################################

from TWindowProperty		import TWindowProperty

class TCoreHolderWindow(TWindowProperty):
	"""
	Requires:
		GetParent
	Provides:
		getResources
		getParentWindowProperty
	"""
	def getCore(self):
		if not hasattr(self, '_TCoreHolderWindow__core'):
			self.__core = self.getParentWindowProperty('core')
		return self.__core
