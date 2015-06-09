# -*- coding: Cp1251 -*-
###############################################################################
# Program:   Sula 0.7
"""
XML-RPC type mapper
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2005/08/03 12:33:35 $"
__version__ = "$Revision: 1.5 $"
# $Source: D:/HOME/cvs/toolib/utility/XMLRPCTypeMapper.py,v $
###############################################################################

import toolib.debug as debug
from toolib.utils import strdict

__all__ = ["Mapper", "StringToUnicodeMapper", "UnicodeToStringMapper", "ReturnValueValidator"]

class Mapper:
	def map(self, v):
		return v

class GenericMapper(Mapper):

	def map(self, obj):
		if isinstance(obj, list):
			return self.mapList(obj)
		if isinstance(obj, tuple):
			return self.mapList(list(obj))
		elif isinstance(obj, dict): 
			return self.mapDict(obj)
		else: 
			return self.mapValue(obj)

	def mapList(self, v):
		for i in xrange(len(v)):
			v[i]=self.map(v[i])
		return v

	def mapDict(self, d):
		for k in d:
			d[k] = self.map(d[k])
		return d

	def mapValue(self, val):
		return val


class StringToUnicodeMapper(GenericMapper):

	def mapValue(self, val):
		if isinstance(val, str):
			return unicode(val, errors="replace")
		else:
			return val


class UnicodeToStringMapper(GenericMapper):
	
	def mapValue(self, val):
		if isinstance(val, unicode):
			return str(val)
		else:
			return val

class ReturnValueValidator(GenericMapper):
	
	def mapList(self, v):
		for e in v:
			if e is None:
				raise ValueError, "List item is None: %s" % v
			else:
				self.map(e)
		return v

	def mapDict(self, d):
		for k in d.keys():
			if k is None:
				raise ValueError, "Dict key is None: %s" % d
			else:
				self.map(k)	# validate key only

			v = d[k]
			if v is None:
				debug.warning("Dict value is None: {\n%s\n}\nRemoving key '%s'..." % (strdict(d), k))
				del d[k]
			else:
				self.map(v)
		return d

if __name__ == '__main__':

	import sys
	reload(sys)
	sys.setdefaultencoding("Cp1251")


	v = { 1 : [1,2,3], 2 : ["ЃҐЎҐ", 2, {"©жгЄҐ­" : "Ґ­Јий"}]}

	print v
	v2 = StringToUnicodeMapper().map(v)
	print v2
	v3 = UnicodeToStringMapper().map(v2)

	assert v == v3, "Mapper"

	print "---------------------------------------------"

	oo = [
		{'a':1, 'b':2, 'c': [1,2,3,], "234" : None},
		"2345",
		123
	]

	print str(oo)
	ReturnValueValidator().map(oo)
	print str(oo)

