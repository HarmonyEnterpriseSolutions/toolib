#################################################################
# Program:   Scripts
"""
	script to compile python recursive
"""
__author__  = "All"
__date__	= "$Date: 2003/11/18 13:02:01 $"
__version__ = "$Revision: 1.3 $"
# $Source: D:/HOME/cvs/toolib/scripts/compile.py,v $
#																#
#################################################################
if __name__ == '__main__':
	import compileall
	import sys
	dirs = sys.argv[1:]
	if dirs:
		for d in dirs:
			compileall.compile_dir(d)
	else:
		print "Usage: python [-O] compileall.py <dir1> <dir2> ..."
else:
	raise ImportError, "You can't import compileall.py"
