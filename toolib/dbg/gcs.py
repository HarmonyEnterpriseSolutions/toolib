"""
provides user friendly get_referrers
"""

import gc
import types


def isFrame(o):
	return isinstance(o, types.FrameType)

def isModuleDict(o, referent):
	return isinstance(o, dict) and '__builtins__' in o and '__name__' in o and '__file__' in o and '__doc__' in o

def isInstanceMethod(o, referent):
	return isinstance(o, types.MethodType) and o.im_self == referent

def isListWithLastFrame(o, referent):
	return isinstance(o, list) and len(o) > 0 and isFrame(o[-1])


#def isListOfReferentAndFrame(o, referent):
#	return isinstance(o, list) and len(o)==2 and o[0] is referent and isFrame(o[1])
#def isTupleOfZeroAndReferent(o, referent):
#	return isinstance(o, tuple) and len(o)==2 and o[0] == 0 and o[1] is referent

def dump_dict(o, referent):
	keys = [k for k, v in o.iteritems() if v is referent]

	try:
		# check if it is a __dict__ of some referer
		instance = [i for i in gc.get_referrers(o) if getattr(i, '__dict__', None) == o][0]
	except IndexError:
		try:
			moduleDict = [i for i in gc.get_referrers(o) if isModuleDict(i, o)][0]
		except IndexError:
	    	# check maybe this is local variable of some other class

			for i in get_referrers(o):
				print '>>>', i

			# it is not instance dictionary, global?
			# at list remove values
			o = o.copy()
			for k, v in o.iteritems():
				if v is not referent:
					o[k] = '...'
			return o
		else:
			return "module %s" % moduleDict['__name__'], ', '.join(["var '%s'" % i for i in keys])
	else:
		# it is __dict__
		return instance, ', '.join(["var '%s'" % i for i in keys])


def dump_referer(o, referent):
	if isinstance(o, dict):
		return dump_dict(o, referent)
	else:
		return o
	

def get_referrers(obj):
	return [dump_referer(i, obj) for i in gc.get_referrers(obj)
		if  not isFrame(i) 
		and not isInstanceMethod(i, obj)
		and not isListWithLastFrame(i, obj)
	]



if __name__ == '__main__':
	import gcs
	
	class ClassC(object):
	
		def __init__(self):
			self.methods = { 'f' : self.m }

		def m(self):
			pass

	class ClassA(object):
	
		def __init__(self, c):
			self.class_A_var = c

			self.class_A_dict = { '' : c}


	a = ClassA(ClassC())

	d = {'popz' : a.class_A_var}
	
	for i in gcs.get_referrers(a.class_A_var):
		print i

