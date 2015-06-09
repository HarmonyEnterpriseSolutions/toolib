#################################################################
# Program:   toolib
"""
	Bean utils
"""
__author__  = "Oleg Noga"
__date__	= "$Date: 2004/12/30 15:28:05 $"
__version__ = "$Revision: 1.1 $"
# $Source: D:/HOME/cvs/toolib/util/beans.py,v $
#																#
#################################################################

class IntrospectionException(Exception):
	pass

def capitalize(s):
	return s[0].upper() + s[1:]

def getSetter(bean, propName):
	setter = getattr(bean, 'set' + capitalize(propName), None)
	if setter is None:
		raise IntrospectionException, "%s instance has no setter for property '%s'" % (bean.__class__.__name__, propName)
	return setter

def getGetter(bean, propName):
	cpn = capitalize(propName)
	getter = getattr(bean, 'get' + cpn, None)
	if getter is None:
		getter = getattr(bean, 'is' + cpn, None)
		if getter is None:
			raise IntrospectionException, "%s instance has no getter for property '%s'" % (bean.__class__.__name__, propName)
	return getter

def hasGetter(bean, propName):
	try:
		getGetter(bean, propName) 
		return 1
	except:
		return 0


def setProperty(bean, propName, propValue):
	apply(getSetter(bean, propName), (propValue,))

def getProperty(bean, propName):
	return apply(getGetter(bean, propName))


if __name__ == '__main__':
	class Test:
		def __init__(self):
			pass


		def setName(self, name):
			print "set name", name

		def getName(self):
			print "getName, returning: TestName"
			return "TestName"

		def isOk2(self):
			print "ok, returning 1"
			return 1

	obj = Test()

	setProperty(obj, "name", "New-Name")

	print getProperty(obj, "name")
	print getProperty(obj, "ok2")
