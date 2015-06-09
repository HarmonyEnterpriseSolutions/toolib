#################################################################
# Program:   Scripts
"""
	Renames files in current dir to uppercase or to lovercase
"""
__author__  = "All"
__date__	= "$Date: 2003/11/18 13:02:01 $"
__version__ = "$Revision: 1.3 $"
# $Source: D:/HOME/cvs/toolib/scripts/frename.py,v $
#																#
#################################################################
import os, sys

def renameFiles(func, directory = '.'):
	print "Traget directory:", directory
	print "function:", func

	for file in os.listdir(directory):
		lfile = func(file)
		if file != lfile:
			try:
				print file, '->', lfile, "...",
				os.rename(file, lfile)
				print "Ok"
			except Exception, e:
				print "%s: %s" % (e.__class__.__name__, e)


if __name__ == '__main__':
	from types import StringType

	fn = None

	if len(sys.argv) == 2:
		if sys.argv[1] == 'u':
			fn = StringType.upper
		elif sys.argv[1] == 'l':
			fn = StringType.lower

	if fn:
		renameFiles(fn)
	else:
		print "Usage: frename u | l"
		print "\tu - make files uppercase"
		print "\tl - make files lowercase"
