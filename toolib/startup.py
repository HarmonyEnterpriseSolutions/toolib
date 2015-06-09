# -*- coding: Cp1251 -*-
#################################################################
# Program:   common
"""
Utilities, used for static initialization of python application
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2011/05/05 19:39:56 $"
__version__ = "$Revision: 1.15 $"
# $Source: C:/HOME/cvs/toolib/startup.py,v $
#																#
#################################################################
import os
import sys
from toolib import debug

def setDefaultEncoding(encoding=None):
	"""
	Sets default encoding to sys.
	Does HACK with reloading sys module,
	to obtain removed sys.setdefaultencoding procedure
	"""
	if not hasattr(sys, "setdefaultencoding"):
		handles = sys.stdin, sys.stdout, sys.stderr
		reload(sys)
		sys.stdin, sys.stdout, sys.stderr = handles

	if encoding is None:	
		import locale
		encoding = locale.getdefaultlocale()[1]
		if encoding is None:
			print "! locale.getdefaultlocale()[1] gives None encoding:", locale.getdefaultlocale()

	sys.setdefaultencoding(encoding)

def hookStd(inputEnc=None, outputEnc=None):
	from toolib.util.streams import Rewriter
	sys.stdout = Rewriter(sys.stdout, inputEnc, outputEnc)
	sys.stderr = Rewriter(sys.stderr, inputEnc, outputEnc)

def startup():
	setDefaultEncoding()
	hookStd()

def unhookStd():
	from codecs import StreamWriter
	while isinstance(sys.stdout, StreamWriter):
		sys.stdout = sys.stdout.stream
	while isinstance(sys.stderr, StreamWriter):
		sys.stderr = sys.stderr.stream

def getProjectPath(nesting):
	path = os.path.abspath(sys.argv[0])
	for i in range(nesting+1):
		path = os.path.split(path)[0]
	return path

__installedLanguage = None
def installLanguage(domain=None, lang=None, locale_dir=None):
	"""
	Installs _ function into builtins
	@Param domain:  .mo files name, your application name
	@Param lang:	'ru', 'ua', etc...
	@Param locale_dir: dir, where
		\ru\LC_MESSAGES\<domain>.mo
		\ua\LC_MESSAGES\<domain>.mo
		are placed
	Use with no parameters to install see thrue _ function
	"""
	global __installedLanguage
	__installedLanguage = lang
	import gettext
	try:
		if domain is not None and lang is not None:
			gettext.Catalog(domain, locale_dir, (lang,)).install()
			return
	except Exception, e:
		debug.error(str(e))
	import __builtin__
	__builtin__.__dict__['_'] = gettext.gettext

def getInstalledLanguage():
	return __installedLanguage

###
## Python version and modules checking
##
def hexVersionToString(ver):
	d = range(4)
	for i in range(4):
		d[3-i] = ver & 0xFF
		ver = ver >> 8
	return "%d.%d.%d" % tuple(d[:3])

def checkPython(pythonVersion=0, modules=(), verbose=0):
	"""
	@Param pythonVersion: See sys.hexverion
	@Param modules: (("description", ("module1", "module2",)), ... )
	"""
	if sys.hexversion < pythonVersion:
		err = _("Incorrect Python version: %s. Version required: %s or later. Please, install new version of Python.") % (hexVersionToString(sys.hexversion), hexVersionToString(pythonVersion))
		return [err]

	errors = []
	for name, moduleList in modules:
		for module in moduleList:
			try:
				__import__(module)
			except ImportError:
				error = _("Package not found: '%s'. Please, install %s") % (module, name, )
				errors.append(error)
				break
	return errors

def winErrorMessage(msg, title=""):
	sys.stderr.write('[Error] %s\n' % msg)
	try:
		import win32gui, win32con
		win32gui.MessageBox(0, msg, title, win32con.MB_ICONHAND)
	except:
		os.system('msgbox "%s" "%s" 0 1' % (msg.replace('\n', '\\n'), title))

def winCheckPython(*p, **pp):
	errors = apply(checkPython, p, pp)
	if errors:
		winErrorMessage('\n'.join(errors), _('Required software not installed'))
		return 0
	else:
		return 1


if __name__ == '__main__':
	#test
	installLanguage()
	print "приветик"
	hookStd()
	print "приветик"
	unhookStd()
	print "приветик"
