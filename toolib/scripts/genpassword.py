#################################################################
# Program:   Scripts
"""
	Generates password of given lenght into stdout
"""
__author__  = "All"
__date__	= "$Date: 2003/11/18 13:02:01 $"
__version__ = "$Revision: 1.5 $"
# $Source: D:/HOME/cvs/toolib/scripts/genpassword.py,v $
#																#
#################################################################
if __name__ == '__main__':
	from toolib.utility.PasswordGenerator import PasswordGenerator
	import sys
	if len(sys.argv) > 1:
		print PasswordGenerator().genPassword(int(sys.argv[1]))
	else:
		print "Usage: python genpassword.py <char count> > file"
