#################################################################
# Program:   Toolib
"""
Dictionary, translates baseless pathes dictionary to base pathes
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2008/03/20 19:03:25 $"
__version__ = "$Revision: 1.4 $"
# $Source: D:/HOME/cvs/toolib/utility/PathDict.py,v $
#################################################################

import os, types

class PathDict:

	def __init__(self, basePath, pathes):
		"""
		basePath: string base path
		pathes: dictionary of baseless pathes or tuples of pathes
		"""
		self._basePath = basePath
		self._pathes = pathes

	def basePath(self):
		return self._basePath

	def get(self, key, default=None):
		path_or_pathes = self._pathes.get(key, default)
		if path_or_pathes is not None:
			if type(path_or_pathes) in (types.TupleType, types.ListType):
				ret = []
				for path in path_or_pathes:
					ret.append(os.path.join(self._basePath, path))
				return ret
			return os.path.join(self._basePath, path_or_pathes)

	def __getitem__(self, key):
		if self._pathes.has_key(key):
			return self.get(key)
		else:
			raise KeyError, key

	def __getattr__(self, name):
		return getattr(self._pathes, name)


if __name__ == '__main__':
	def test():
		d = {
			1 : 'hello',
			2 : 'hello2',
			3 : 'hello3',
			}

		p = PathDict("C:\\bebe", d)
		print p[2]

	test()
