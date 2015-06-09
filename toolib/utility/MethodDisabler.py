#################################################################
# Program: Toolib
"""

"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2003/11/18 13:02:03 $"
__version__ = "$Revision: 1.2 $"
# $Source: D:/HOME/cvs/toolib/utility/MethodDisabler.py,v $
#
#################################################################

class MethodDisabler:

	def __init__(self):
		if hasattr(self.__class__, "__disabled_methods__"):
			for att in self.__disabled_methods__:
				setattr(self.__class__, att, self._disabledMethod)
			del self.__class__.__disabled_methods__

	def _disabledMethod(self, *p, **pp):
		raise AttributeError, "Method is disabled in " + self.__class__.__name__

