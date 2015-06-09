#################################################################
# Program:   toolib
"""
	Common exceptions patterns
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2004/12/30 15:28:05 $"
__version__ = "$Revision: 1.2 $"
# $Source: D:/HOME/cvs/toolib/exceptions.py,v $
#																#
#################################################################

import sys

class WrapperException(Exception):
	def __init__(self, *args):
		apply(Exception.__init__, (self,)+ args)

	def __str__(self):
		nested = self.getNestedException()
		if nested is not None:
			return "Nested exception: %s: %s" % (nested.__class__.__name__, str(nested))
		else:
			return Exception.__str__(self)


	def getNestedException(self):
		if hasattr(self, "args") and len(self.args) > 0 and isinstance(self.args[0], Exception):
			return self.args[0]


if __name__ == '__main__':
	raise WrapperException, "fldkjdflkgjdflkgj"
	try:
		raise "sdiufeorituoeritu"
	except Exception, e:
		raise WrapperException, e, sys.exc_info()[2]
