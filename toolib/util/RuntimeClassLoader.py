from toolib.util.Cache import Cache
from toolib import debug

class RuntimeClassLoader(object):
	
	def __init__(self):
		self.__globals = {}
		self.__classes = Cache(self._loadClass)

	def execImport(self, code):
		exec(code, self.__globals)

	def importPackage(self, packageName, as=None):
		if as:
			self.execImport("import %s as %s" + packageName)
		else:
			self.execImport("import " + packageName)

	def importFrom(self, packageName, className='*', as=None):
		if as:
			self.execImport("from %s import %s as %s" % (packageName, className, as))
		else:
			self.execImport("from %s import %s" % (packageName, className))

	def registerClass(self, pyClass, as=None):
		"""
		registers imported class
		"""
		self.__globals[as or pyClass.__name__] = pyClass

	def _loadClass(self, features):
		assert len(features) > 0
		if len(features) == 1:
			c = eval(features[0], self.__globals)
		else:
			code = """\
class __RTCLASS__(%s):
	__super__=%s
	def __init__(self, *__args, **__kwargs):
%s
""" 		% (
				", ".join(features), 
				features[-1],		# assign last feature to SUPERCLASS
				"\n".join(map(lambda c: "\t\t%s.__init__(self, *__args, **__kwargs)" % c,  features[::-1])),
			)
			debug.trace(code)
			scope = self.__globals.copy()
			exec(code, scope)
			c = scope["__RTCLASS__"]

			c.__name__ = str('_'.join(features))	# have some unicode feature names here, check from where it comes
		return c

	def getClass(self, *features):
		return self.__classes[tuple(features)]
		
if __name__ == '__main__':

	#class Feature1:
	#	def __init__(self):
	#		print "init feature 1"

	#	def getFeature1(self):
	#		return "feature1"

	#class Feature2:
	#	def __init__(self):
	#		print "init feature 2"
			
	#	def getFeature2(self):
	#		return "feature2"

	#class Object:
	#	def __init__(self):
	#		print "init object"


	
	f = RuntimeClassLoader()

	f.importFrom('toolib.test.p.Feature1')
	f.importFrom('toolib.test.p.Feature2')
	f.importFrom('toolib.test.p.pp.Object')

	print f._RuntimeClassLoader__globals

	#del Object
	#del Feature1
	#del Feature2

	c1 = f.getClass("Object",)
	c2 = f.getClass("Object", "Feature1")
	c3 = f.getClass("Object", "Feature2")
	c4 = f.getClass("Object", "Feature1", "Feature2")
	c5 = f.getClass("Object", "Feature2")
	
	assert id(c3) == id(c5)

	print c1, "\t\t", id(c1)
	print c2, "\t\t", id(c2)
	print c3, "\t\t", id(c3)
	print c4, "\t\t", id(c4)
	print c5, "\t\t", id(c5)

	f.getClass("Object", "Feature1", "Feature2")()
