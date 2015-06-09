#################################################################
# Program:   toolib
"""
Python builtins extensions only
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2010/10/07 15:19:51 $"
__version__ = "$Revision: 1.17 $"
# $Source: D:/HOME/cvs/toolib/util/lang.py,v $
#																#
#################################################################

def isSequence(a):
	return isinstance(a, (tuple, list)) or hasattr(a, '__len__') and hasattr(a, '__getitem__')

def isIterable(a):
	try:
		iter(a)
		return True
	except TypeError:
		return False

def isInstance(object, interface):
	"""
	interface is class name or class
	"""
	return isCastable(object.__class__, interface)

def isCastable(clas, interface):
	"""
	interface is class name or class
	"""
	if isinstance(interface, basestring):
		if clas.__name__ == interface:
			return True
	else:
		if clas is interface:
			return True
	if hasattr(clas, '__bases__'):
		for base in clas.__bases__:
			if isCastable(base, interface):
				return True
	return False
	
def iif(cond, arg1, arg2=None):
	if cond:
		return arg1
	else:
		return arg2

def lif(cond, larg1, larg2=lambda: None):
	"""
	lazy evaluated lif
	should pass 'lambda: argument' instead 'agrument'
	"""
	if cond:
		return larg1()
	else:
		return larg2()

def leval(arg):
	import types
	if isinstance(arg, types.FunctionType):
		return arg()
	else:
		return arg

def sgn(a):
	"""
	sign of a, 
	returns a / abs(a) or 0 if a == 0
	"""
	if   a >  0: return  1
	elif a == 0: return  0
	else:        return -1

def alltrue(function, iterable):
	"""
	returns False if at list one of (function(i) for i in sequence) is False
	"""
	for i in iterable:
		if not function(i):
			return False
	return True

def onetrue(function, iterable):
	"""
	returns True if at list one of (function(i) for i in sequence) is True
	"""
	for i in iterable:
		if function(i):
			return True
	return False

def import_module(s):
	"""
	__import__('a.b.c') returns a 
	importModule('a.b.c') returns c
	"""
	m = __import__(s)
	for i in s.split(".")[1:]:
		m = getattr(m, i)
	return m

importModule = import_module

def import_module_relative(module, localModule='', package=None):
	"""
	relational import

	foo/bar/a.py
	foo/bar/impl/b.py
	
	import_module("foo.bar.a", 'b', 'impl') -> import foo.bar.impl.b
	import_module("__main__",  'b', 'impl') -> import impl.b
	import_module("a",  'b', 'impl') -> import impl.b


	imports module from package, call from 
	"""
	try:
		path = (localModule[:localModule.rindex('.')], package, module)
	except ValueError:
		path = (package, module)
	return import_module('.'.join(filter(None, path)))


#def normalize_args_with_function(f, origin, args, kwargs):
#
#	if hasattr(f, 'im_func'):
#		f = f.im_func
#
#	argCount = f.func_code.co_argcount - len(f.func_defaults)
#	kwOrder = f.func_code.co_varnames[argCount:f.func_code.co_argcount]
#	argCount -= origin
# 
#	return normalize_args(args, kwargs, kwOrder, argCount)

__docstring_signature = {}

def normalize_args_with_docstring(function, args, kwargs, skipCount=1):
	"""
	suitable for wxPython
	args are without self bu default
	"""
	sig = __docstring_signature.get(function, NotImplemented)

	if sig is NotImplemented:
		sig = None
		if function.__doc__:
			import pydocs
			sig = pydocs.FunctionSignature(function.__doc__)
		
		__docstring_signature[function] = sig = sig or None

	if sig is not None:
		return normalize_args(
			args,
			kwargs,
			[i.name for i in sig.namedAttrs],
			len(sig.positionalAttrs)-skipCount,
		)
	else:
		raise ValueError, "Can't extract signatures from %s doc: %s" % (function, function.__doc__)

def normalize_args(args, kwargs, kwOrder, argCount=0):
	"""
	argCount is count of positional
	"""
	unresolved = args[argCount:]
	args = args[:argCount]

	kwargs = kwargs.copy()
	for i in xrange(len(unresolved)):
		kwargs[kwOrder[i]] = unresolved[i]

	return args, kwargs

def ulong(x):
	"""
	converts int to long as unsigned int
	"""
	if isinstance(x, int) and x < 0:
		return 0x100000000L + x
	else:
		return long(x)

if __name__ == '__main__':
	print isIterable("sdsdf")
	print isSequence("sgdg")

	class A:
		pass

	class B(A):
		pass

	class C(B):
		pass

	class D:
		pass

	print isInstance(C(), "A")
	print isInstance(D(), "A")

	print importModule("toolib.debug")

	#dump_attr(normalize_args)
	print alltrue(lambda x: x >= 1, [1,1,2,4,5])
