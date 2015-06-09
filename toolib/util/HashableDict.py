###############################################################################
# Program:   toolib
"""
Dictionary wrapper, allows to use it as key of dictionary
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2005/07/26 10:41:22 $"
__version__ = "$Revision: 1.2 $"
# $Source: D:/HOME/cvs/toolib/util/HashableDict.py,v $
###############################################################################
class HashableDict(object):
	"""
	Warning: dict can't mutate after wrapping
	"""
	def __init__(self, dict):
		self._dict = dict
		self._hash = hash(tuple(dict.items()))

	def __getattr__(self, name):
		return getattr(self._dict, name)

	def __hash__(self):
		return self._hash
