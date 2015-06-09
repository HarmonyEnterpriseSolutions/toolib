# TODO: rewrite using _winreg

import weakref
import win32api
import win32con
import sys
import locale

__all__ = ['RegKey', 'RegValue', 'KEY_NOT_EXISTS', 'KEY_ACCESS_DENIED']

# to correct russian in str
win32api.error.__str__ = lambda self: '(%s)' % (', '.join(map(str, self)))
from toolib import debug

KEY_NOT_EXISTS = 2
KEY_ACCESS_DENIED = 5
ENCODING = locale.getdefaultlocale()[1]

def RegOpenKeyEx(hkey, name, n):
	"""
	Tries to create key with all access
	Then read-only
	Then fails
	"""
	try:
		return win32api.RegOpenKeyEx(hkey, name, n, win32con.KEY_ALL_ACCESS)
	except win32api.error, e:
		if e[0] == KEY_ACCESS_DENIED:	# access denied
			#try to lower access to read only
			return win32api.RegOpenKeyEx(hkey, name, n, win32con.KEY_READ)
		else:
			raise

class NoDefault(object):
	pass

class RegValue(object):
	def __init__(self, key, name, value=None, vtype=None):
		assert isinstance(key, RegKey), getattr(key, '__class__', type(key))
		assert isinstance(name, basestring), debug.dump(name)

		self.__key = key		# RegValue must hold RegKey object by reference
		self.__name  = name
		self.__value = value
		self.__type  = vtype

	def getName(self):
		return self.__name

	def getValue(self, defValue=NoDefault):
		if self.__value is None:
			self.load()
		if self.__value is None and defValue is not NoDefault:
			return defValue
		else:
			return self.__value

	def exists(self):
		self.flush()
		try:
			self.load()
		except:
			pass
		return self.__value is not None
		

	def flush(self):
		self.__value = None
		self.__type = None

	def getType(self):
		if self.__type is None:
			self.load()
		return self.__type

	def load(self):
		try:
			self.__value, self.__type = win32api.RegQueryValueEx(self.__key.getHKey(), self.__name)
			if isinstance(self.__value, str):
				self.__value = self.__value.decode(ENCODING)
		except win32api.error, e:
			# not to raise if value not exists
			if e[0] == KEY_NOT_EXISTS:
				self.flush()
			else:
				raise

	def __str__(self):
		return str(self.__name)

	def remove(self, mustExist=False):
		try:
			return win32api.RegDeleteValue(self.__key.getHKey(), self.__name)
		except win32api.error, e:
			if mustExist or not (e[0] == KEY_NOT_EXISTS or e[0] == KEY_ACCESS_DENIED and not self.exists()):
				raise

	def setValueIfChanged(self, value, vtype=None):
		assert debug.trace('name=%s, value=%s, vtype=%s' % (self.__name, repr(value), vtype))
		if self.getValue() != value:
			assert debug.trace('changed, old value was: %s' % (self.getValue(),))
			self.setValue(value, vtype)
		else:
			assert debug.trace('not changed')


	def setValue(self, value, vtype = None):
		if isinstance(value, unicode):
			value = value.encode(ENCODING)
		if vtype is not None:
			# no hacks, if we have type
			rc = win32api.RegSetValueEx(self.__key.getHKey(), self.__name, 0, vtype, value)
			self.__type  = vtype
		else:
			try:
				if self.__type is not None:
					# try to set value with old type
					rc = win32api.RegSetValueEx(self.__key.getHKey(), self.__name, 0, self.__type, value)
				else: # if conversionError
					raise ValueError
			except ValueError:
				# obtain type automatically
				if isinstance(value, basestring):
					vtype = win32con.REG_SZ
				elif isinstance(value, int):
					vtype = win32con.REG_DWORD

				if vtype is not None:
					#rint "type:", vtype, win32con.REG_SZ
					#rint "value:", value, type(value)
					rc = win32api.RegSetValueEx(self.__key.getHKey(), self.__name, 0, vtype, value)
					self.__type = vtype
				else:
					raise ValueError, "Can't resolve type for value"

		self.__value = value
		return rc


	## deprecated

	def name(self):
		debug.deprecation('RegValue.name -> getName')
		return self.getName()

	def value(self, *p, **pp):
		debug.deprecation('RegValue.value -> getValue')
		return self.getValue(*p, **pp)

	def type(self):
		debug.deprecation('RegValue.type -> getType')
		return self.getType()


class RegIterator(object):
	def __init__(self, key):
		assert isinstance(key, RegKey), debug.dump(key)
		
		self._key = key			# iterator must hold RegKey object by reference
		self._index = 0

	def __iter__(self):
		return self

	def next(self):
		try:
			res = self._next()
			self._index += 1
			return res
		except win32api.error:
			raise StopIteration

	def _next(self):
		raise win32api.error


class RegValueIterator(RegIterator):
	""" Iterates throught the key values, updates key value cache """
	def __init__(self, key):
		RegIterator.__init__(self, key)
		self._key._flushValues()

	def _next(self):
		name, value, vtype = win32api.RegEnumValue(self._key.getHKey(), self._index)
		if isinstance(name, str):
			name = name.decode(ENCODING)
		if isinstance(value, str):
			value = value.decode(ENCODING)
		value = RegValue(self._key, name, value, vtype)
		self._key._cacheValue(name, value)
		return value


class RegValueNameIterator(RegIterator):
	def _next(self):
		return win32api.RegEnumValue(self._key.getHKey(), self._index)[0]


class RegValueValueIterator(RegIterator):
	def _next(self):
		return win32api.RegEnumValue(self._key.getHKey(), self._index)[1]


class RegKeyIterator(RegIterator):
	def _next(self):
		return RegKey(self._key, win32api.RegEnumKey(self._key.getHKey(), self._index))

class RegKeyNameIterator(RegIterator):
	def _next(self):
		return win32api.RegEnumKey(self._key.getHKey(), self._index)

class RegKey(object):

	def __init__(self, parentKey=None, path=None, create=False):

		if not path:
			path = None

		if path is not None:
			path = path.split('\\')

		if parentKey is not None:
			hkey = parentKey._hkey
			p = list(parentKey._path)
		else:
			if path is not None:
				hkey = getattr(win32con, path[0])
				p = [path[0]]
				path = path[1:]
			else:
				raise AttributeError, "From what to create RegKey? No parentKey and no path"

		if path is not None:
			for keyname in path:
				#rint '>>', hkey
				oldhkey = hkey
				try:
					#rint '>>> open key:', keyname
					hkey = RegOpenKeyEx(oldhkey, keyname, 0)
				except win32api.error, e:
					code = e[0]
					if code == KEY_NOT_EXISTS:   # not exists
						if create:
							hkey = win32api.RegCreateKey(oldhkey, keyname)  # create key
							win32api.RegCloseKey(hkey)

							hkey = RegOpenKeyEx(oldhkey, keyname, 0)
						else:
							raise KeyError, keyname
					else:
						c, e, tb = sys.exc_info()
						e.args += ('\\'.join(p + [keyname]),)
						raise c, e, tb

				p.append(keyname)

				# close unused, not external
				if parentKey is None or parentKey._hkey != oldhkey:
					#rint "Close descriptor: ", oldhkey
					win32api.RegCloseKey(oldhkey)

		# clone hkey if it still the same as parent one
		if parentKey is not None and parentKey._hkey == hkey:
			#rint "Clone descriptor: ", hkey
			hkey = RegOpenKeyEx(hkey, None, 0)

		self._path = p
		self._hkey = hkey
		self._values = weakref.WeakValueDictionary()

	def _flushValues(self):
		self._values.clear()

	def _cacheValue(self, name, value):
		self._values[name] = value

	def remove(self):
		parentKey = self.getParentKey()
		self.__removeFromParent(parentKey)

	def removeAllValues(self):
		for i in self.getValues():
			i.remove()

	def __removeFromParent(self, parentKey):
		for subkey in tuple(self.iterKeys()):
			subkey.__removeFromParent(self)
		name = self.getName()
		self.close()
		#rint "DELETE:", parentKey, name
		win32api.RegDeleteKey(parentKey.getHKey(), name)

	def getParentKey(self):
		return RegKey(None, '\\'.join(self._path[:-1]))

	def value(self, name):
		value = self._values.get(name)
		if value is None:
			value = RegValue(self, name)
			self._values[name] = value
		return value

	def flushValues(self):
		del self._values

	def iterValues(self):
		"""returns iterator through value objects"""
		return RegValueIterator(self)

	def getValues(self):
		"""returns tuple of value objects"""
		return tuple(self.iterValues())

	def iterKeyNames(self):
		"""returns iterator through subkey names"""
		return RegKeyNameIterator(self)

	def getKeyNames(self):
		"""returns tuple of subkey names"""
		return tuple(self.iterKeyNames())

	def iterKeys(self):
		"""returns iterator through subkey RegKey objects"""
		return RegKeyIterator(self)

	def __iter__(self):
		return RegKeyIterator(self)

	def getKeys(self):
		"""returns tuple of subkey RegKey objects"""
		return tuple(self.iterKeys())


	def getName(self):
		"""returns Name of key"""
		return self._path[-1]

	def getDefaultValue(self, subKeyName=None):
		"""returns key's (or subkey's) default value"""
		return win32api.RegQueryValue(self._hkey, subKeyName)

	def __contains__(self, keyname):
		if self._hkey is not None:
			try:
				key = RegOpenKeyEx(self._hkey, keyname, 0)
				win32api.RegCloseKey(key)
				return True
			except:
				pass
		return False

	def getKey(self, name):
		return RegKey(self, name)

	def createKey(self, name):
		return RegKey(self, name, True)

	def __getitem__(self, name):
		try:
			return RegKey(self, name)
		except win32api.error, e:
			# TODO: own exception
			raise KeyError(name, "%s: %s, %s, %s" % (e.__class__.__name__, e[0], e[1], e[2]))

	def close(self):
		return win32api.RegCloseKey(self._hkey)

	def __str__(self):
		return "[%s]" % "\\".join(self._path)

	def __repr__(self):
		return "RegKey(path=%s)" % ("\\".join(self._path),)

	def __del__(self):
		try:
			win32api.RegCloseKey(self._hkey)
		except AttributeError:
			pass

	def getHKey(self):
		return self._hkey

	def dump(self, recursive=True, indent=0, out=None):
		from toolib.util import reprs

		if out is None:
			out = sys.stdout
		
		out.write('\t' * indent)
		out.write("[%s]" % self.getName())
		out.write('\n')

		for i in self.iterValues():
			out.write('\t' * indent)
			out.write("\t%s = %s" % (i.getName() or '@', reprs.repr(i.getValue())))
			out.write('\n')

		if recursive:
			for key in self:
				key.dump(True, indent + 1, out)
		

if __name__ == '__main__':
	from toolib.startup import hookStd
	hookStd()

	path = "HKEY_CURRENT_USER\\Software\\Oleg\\winregistry"
	try:
		#soft = RegKey(path)
		#last = soft["Shell Folders"]
		exp = RegKey(None, path, create = True)
		exp2 = RegKey(exp)

		print "Key:", exp2

		print " + default value: '%s'" % exp2.getDefaultValue()
		for value in exp2.iterValues():
			print " + value name:", value.getName()
			print " + value:", value

		for sk in exp2.iterKeys():
			print "   + subkey:", sk

		#print "test value: ", win32api.RegQueryValue(exp2.hkey(), 'test')
		print 'value is not set:', exp2.value("test").getValue()

		exp2.value("test").setValue(2314234) #, win32con.REG_DWORD
		print exp2.value("test").getValue()

		exp2.value("test").remove()
		exp2.value("test").remove()

		#exp2.value("test").setValue("rere")
		#print exp2.value("test").getValue()



		#win32api.RegSetValueEx(exp2.hkey(), "test", 0, 1, "FUCK!!!")

		#sf = exp["Shell Folders"]

		#print '>>', exp
		#print '>>', sf

		#print '"%s"' % exp.getDefaultValue()

	except win32api.error, e:
		a,b,c = e
		print "FINAL ERR", a,b,c
		raise

	exp.close()
	exp2.close()

	del exp
	del exp2
	print locals().keys()

	import gc
	gc.collect()

	print "GARBAGE"
	for i in gc.garbage:
		print "----------------------------------------"
		print type(i), i
		for j in gc.get_referrers(i):
			print '\t', type(j), j
			for jj in gc.get_referrers(j):
				print '\t\t', type(jj), jj
				#for jjj in gc.get_referrers(jj):
				#	print '\t\t\t', type(jjj), jjj
