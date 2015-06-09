import re
import os
from registry import RegKey

REC_ENV = re.compile(r'\%([^\%]+)\%')

def substenv(s):
	return REC_ENV.sub(lambda m: os.environ[m.groups()[0]], s)

class Variable(object):

	REG_KEY = r"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"

	def __init__(self, name):
		self.__regValue = RegKey(None, self.REG_KEY).value(name)

	def getValue(self):
		return self.__regValue.getValue()

	def setValue(self, value):
		return self.__regValue.setValue(value)


class ListedVariable(list, Variable):

	def __init__(self, name):
		Variable.__init__(self, name)
		self.extend(self.getValue().split(';'))
	
	def commit(self):
		self.setValue(';'.join(self))


class Path(ListedVariable):

	def __init__(self, ignored):
		ListedVariable.__init__(self, 'Path')

	def isValidAt(self, index):
		return os.path.exists(substenv(self[index]))

	def isValid(self):
		return reduce(lambda r, i: r and self.isValidAt(i), xrange(len(self)), True)

	def clean(self):
		for i in xrange(len(self)-1, -1, -1):
			self[i] = self[i].strip()
			if not self.isValidAt(i):
				del self[i]

	def getSubstPathAt(self, index):
		return substenv(self[index])

	def where(self, name):
		pathext = Environment.getVariable('PATHEXT')

		for ext in pathext:
			for i in xrange(len(self)):
				path = self.getSubstPathAt(i)
				p = os.path.join(path, name+ext)
				#print p
				if os.path.exists(p):
					return p



class Environment(object):
	
	CLASSES = {
		'path'    : Path,
		'pathext' : ListedVariable,
	}

	@classmethod
	def getVariable(cls, name):
		return cls.CLASSES.get(name.lower(), Variable)(name)


if __name__ == '__main__':
	path = Environment.getVariable('PATH')
	print path
	print path.isValid()
	print path.getSubstPathAt(0)
	path.clean()
	path.commit()
	print path.where('cmd')