###############################################################################
# Program:   toolib
"""
	Debuging module
	To customize Your tracing, just create a file in toolib/config

	===== debug.py >>>>>
	FORMAT = "$MARK$ $MODULENAME$($LINE$): $MSG$"
	TIME_FORMAT = "%d.%m.%y %H:%M:%S"

	MODULES = {
		"package.MyModule" : 1,
		"package" : 0,
		"__main__"  : 1,
	}
	<<<<< debug.py =====

	Format aliases:
		$MSG$			message text
		$MARK$			mark ("+" is message, "!" is error, "*" warning, etc.)
		$FILE$			file, in which trace have called
		$MODULE$		module, with package path
		$MODULENAME$	module name (no packages)
		$LINE$			line number
		$CODE$			code for that line
		$METHOD$		function (method), where trace occured

		$TIME$			time when trace occured, TIME_FORMAT is used to format
							time (see time.strftime())
		$AUTHOR$		author of module, (static __author__ variable from
							that module)
	Note: import * is DEPRECATED 
	      use "from toolib import debug"
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2012/03/05 11:24:46 $"
__version__ = "$Revision: 1.13 $"
# $Source: D:/HOME/cvs/toolib/debug.py,v $
###############################################################################

import os
import sys
import time
import types
import traceback

enabled = __debug__

VERBOSE    = False
USE_STDERR = False

# Defaults (overrided in trace2.py)
DEFAULT_FORMAT = "$MARK$ $MODULENAME$.$METHOD$: $MSG$ ($LINE$)"
DEFAULT_TIME_FORMAT = "%y-%m-%d %H:%M:%S"
DEFAULT_MODULES = { "__main__" : 1 }

try:
	import toolib.config.debug
	conf = toolib.config.debug.__dict__
except:
	conf = {}

MODULES		= conf.get('MODULES',	  DEFAULT_MODULES)
FORMAT		= conf.get('FORMAT',	  DEFAULT_FORMAT)
TIME_FORMAT = conf.get('TIME_FORMAT', DEFAULT_TIME_FORMAT)

ALIASES = [
	"$TIME$",
	"$MARK$",

	"$FILE$",
	"$LINE$",
	"$METHOD$",
	"$CODE$",

	"$MODULE$",
	"$MODULENAME$",
	"$AUTHOR$",
	"$MSG$",
]

__all__ = ["trace", "error", "warning", "deprecation", "strexc"]

def _checkModule(module, level):
	while module:
		try:
			return MODULES[module] >= level
		except KeyError:
			pass
		index = module.rfind('.')
		if index > 0:
			module = module[ : index]
		else:
			break


def deprecation(suggestion):
	_trace(suggestion, 0, '! DEPRECATION:', sys.stderr if USE_STDERR else sys.stdout, 1)
	return 1

def _trace(message, level, mark, out, stackIndex=0):
	#print traceback.print_stack(limit=2)
	stack = traceback.extract_stack(limit=3+stackIndex)
	#print stack
	if len(stack) > 0:
		file, line, method, code = stack[0]
	else:
		file, line, method, code = "?", "?", "?", "?"

	module = _getModule(file)

	moduleOk = 1
	if level > 0:
		moduleOk = _checkModule(module, level)

		if VERBOSE:
			if not moduleOk:
				print "  debug: module rejected: %s (message: %s)" % (module, message)

	if moduleOk:# and authorOk:

		# just synchronize it with ALIASES
		args = (
			(_getTime, (), {}),
			mark,

			file,
			line,
			method,
			code,

			module,
			(_getModuleName, (file,), {}),
			__author__,
			message,
		)

		string = FORMAT
		for i in xrange(len(args)):
			arg = args[i]
			alias = ALIASES[i]
			if alias and arg is not None:
				if type(arg) is types.TupleType:
					arg = apply(arg[0], arg[1], arg[2])
				else:
					arg = str(arg)

				string = string.replace(alias, arg)

		out.write(string)
		out.write("\n")

def trace(message, level=1, mark='+', out=None):
	if enabled:
		if out is None:
			_trace(message, level, mark, sys.stdout)
		else:
			_trace(message, level, mark, out)
	return 1

def error(message, level=0):
	_trace(message, level, '!', sys.stderr if USE_STDERR else sys.stdout)
	return 1

def warning(message, level=0):
	_trace(message, level, '*', sys.stderr if USE_STDERR else sys.stdout)
	return 1

def _getTime():
	return time.strftime(TIME_FORMAT, time.localtime(time.time()))

def _getModule(fileName):
	s = os.path.splitext(fileName)[0]

	# if path is absolute, cut absolute part
	supper = s.upper()
	for path in sys.path:
		n = len(path)
		if n>0:
			#print "compare %s VS %s" % (supper, path.upper())
			if supper.startswith(path.upper()):
				s = s[n+1:]
				break

	return s.replace(os.sep, '.')

def _getModuleName(fileName):
	s = os.path.splitext(fileName)[0]
	return s[s.rfind(os.sep) + 1: ]

def _resampleAliases():
	for i in xrange(len(ALIASES)):
		try:
			FORMAT.index(ALIASES[i])
		except ValueError:
			ALIASES[i]=None


location = ("%s@%s.%s" % (
	os.environ.get('USERNAME',     'unknown'),
	os.environ.get('COMPUTERNAME', 'unknown'),
	os.environ.get('USERDOMAIN',   'unknown'),
)).lower()

def isLocation(*contexts):
	"""
	location is user@host.domain
	returns True if debug.enabled
	and debug.location ends with contexts or one of contexts
	"""
	if enabled:

		for context in contexts:
			if location.endswith(context):
				return True

	return False	


def dump(value):
	from toolib.util import reprs
	return "%s, <%s>" % (reprs.repr(value), str(value.__class__).strip('<>'))


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

def stack(n=None):
	if n is not None: n += 1
	return ''.join(traceback.format_stack(None, n)[:-1])

## static init
_resampleAliases()


if __name__ == '__main__':
	try:
		a = 1/0
	except Exception, e:
		trace(strexc())
		error(strexc(e))
		warning(strexc())
