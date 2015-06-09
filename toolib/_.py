#################################################################
# Program:   toolib
"""
Defines _ function if language was not installed with startup.instalLanguage
For optimization it is suggested to import this module after language is installed

Usage:
	from toolib._ import *
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2005/01/14 15:41:47 $"
__version__ = "$Revision: 1.9 $"
# $Source: D:/HOME/cvs/toolib/_.py,v $
#																#
#################################################################
import __builtin__


if hasattr(__builtin__, '_'):
	__all__ = []
else:
	__all__ = ['_']

	def _(message):
		if hasattr(__builtin__, '_'):
			return __builtin__._(message)
		else:
			return message
