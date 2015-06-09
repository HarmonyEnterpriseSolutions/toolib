# -*- coding: Cp1251 -*-
#################################################################
# Program:   common
"""
	Very common utility functions and classes
	DEPRECATED: MODULE is mixed to mutch
"""
__author__  = "All"
__date__	= "$Date: 2009/11/02 17:01:52 $"
__version__ = "$Revision: 1.24 $"
# $Source: D:/HOME/cvs/toolib/utils.py,v $
#																#
#################################################################
import os
import sys
import types
import copy

from toolib.util import strings

def strexc(excinfo=None):
	"""
	Converts ecxeption or exception info or sys.exc_info() to string
	"""
	if excinfo is None:
		excinfo = sys.exc_info()
	if type(excinfo) is types.TupleType:
		if excinfo[1] is None:
			e = excinfo[0]
		else:
			e = excinfo[1]
	else:
		e = excinfo

	if str(e.__class__) == "pywintypes.com_error":
		code = e[0]
		if code < 0:
			code += 0x100000000L
		if e[2] is not None:
			descr = ' '.join((e[1], (e[2][2] or "").split('\n')[0]))
		else:
			descr = e[1]
		return "%s: 0x%8X, %s" % (e.__class__.__name__, code, descr)
	else:
		return "%s: %s" % (e.__class__.__name__, e)

def reprdict(d):
	"""
	Same as repr, but looks fine
	"""
	l = ['{']
	keys = d.keys()
	keys.sort()
	for k in keys:
		l.append("\t%-16s : %s," % (k.__repr__(), d[k].__repr__()))
	l.append('}')
	return '\n'.join(l)


def strdict(d):
	"""
	Converts dictionary to string
	"""
	l = []
	keys = d.keys()
	keys.sort()
	for k in keys:
		l.append("%20s : %s" % (k, d[k]))
	return '\n'.join(l)

def clone(object):
	return copy.copy(object)


FILE_SYSTEM_TT = '_' * 32 + strings.makeTranslationTable(
	*(r'"*/:<>?\|',
	  r"'#~-''?~;")
)[32:]

def strFileSystemEncode(s):
	return s.translate(FILE_SYSTEM_TT).lstrip(' ').rstrip('.')

def excepthook():
	sys.excepthook(*sys.exc_info())

def userProfilePath():
	"""
	returns place to store user dependent configs
	NOTE: not tested on unix
	"""
	if os.name == 'unix':
		return '~'			#@Oleg: test it under UNIX
	if os.name == 'nt':
		# try USERPROFILE
		return os.environ.get('USERPROFILE')

def ensureUserConfigSavePath(domain, confName):
	path = os.path.join(userProfilePath(), '.%s' % (domain,))
	if not os.path.exists(path):
		os.makedirs(path)
	return os.path.join(path, confName)

def userConfigsPath():
	return userProfilePath() or userHomePath()

def userHomePath():
	if os.name == 'unix':
		return '~'
	if os.name == 'nt':
		""" returns user home path """
		# try HOMEDRIVE and HOMEPATH
		drive = os.environ.get('HOMEDRIVE')
		path = os.environ.get('HOMEPATH')
		if drive and path and path != os.sep:
			return os.path.join(drive,path)


def existentPath(path):
	while 1:
		if not path or os.path.exists(path) and not os.path.isfile(path):
			return path
		path, splitted = os.path.split(path)
		if not splitted:
			return path

__uniqueNumber = 0
def getUniqueNumber():
	global __uniqueNumber
	__uniqueNumber+=1
	return __uniqueNumber

################ END OF MODULE ################

if __name__ == '__main__':
	pass
	import toolib.startup
	toolib.startup.hookStd()
	file = strFileSystemEncode("ПредприятІє <Рємстройпласт> №1")
	print file
	f = open(file, "wb")
	f.close()
	#print ('І',)

